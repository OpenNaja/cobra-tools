import logging
import os
import shutil
import struct
import tempfile

from generated.formats.ms2 import Ms2File
from generated.formats.ovl.versions import *
from modules.formats.shared import djb
from ovl_util.interaction import showdialog

SPECIES_ONLY_FMTS = (".mdl2", ".ms2", ".motiongraph", ".materialcollection")


def djb_bytes(string):
	return struct.pack("<I", djb(string.lower()))


def name_bytes(string):
	return string.encode(encoding="utf-8")


def rename_entry(entry, name_tups, species_mode):
	if "bad hash" in entry.name:
		logging.warning(f"Skipping {entry.file_hash} because its hash could not be resolved to a name")
		return
	elif species_mode and entry.ext not in SPECIES_ONLY_FMTS:
		logging.debug(f"Skipping {entry.name} due to its file extension")
		return
	for old, new in name_tups:
		entry.name = entry.name.replace(old, new)
	entry.basename, entry.ext = os.path.splitext(entry.name)


def rename(ovl, name_tups, species_mode=False):
	logging.info(f"Renaming for {name_tups}")
	ovl_lists = [ovl.files, ovl.dependencies, ovl.dirs]
	ovs_lists = []
	for archive_entry in ovl.archives:
		content = archive_entry.content
		ovs_lists.extend((
			content.data_entries,
			content.buffer_entries,
			content.set_header.sets,
			content.set_header.assets,
			content.pools,
			content.sized_str_entries
		))
	# rename all entries
	for entry_list in ovl_lists + ovs_lists:
		for entry in entry_list:
			rename_entry(entry, name_tups, species_mode)
	ovl.update_hashes()
	ovl.update_ss_dict()
	logging.info("Finished renaming!")


def ms2_renamer(ovl, name_tups):
	logging.info(f"Replacing names in MS2 files for {name_tups}")

	temp_dir = tempfile.mkdtemp("-cobra")
	# print(tmp_dir)

	def out_dir_func(n):
		"""Helper function to generate temporary output file name"""
		return os.path.normpath(os.path.join(temp_dir, n))

	for ms2_entry in ovl.get_files((), (".ms2",), []):
		try:
			ms2_mdl2_files = ms2_entry.loader.extract(out_dir_func, False, None)
			# there is always just one ms2 in one entry's files
			ms2_path = [f for f in ms2_mdl2_files if f.endswith(".ms2")][0]

			# open the ms2 file
			ms2_file = Ms2File()
			ms2_file.load(ms2_path, read_bytes=True)
			# rename the materials
			ms2_file.rename(name_tups)
			# update the hashes & save
			ms2_file.save(ms2_path)
			# inject again
			ms2_entry.loader.inject((ms2_path,), False, False)
		except BaseException as err:
			print(err)
	# delete temp dir again
	shutil.rmtree(temp_dir)


def dat_replacer(ovl, name_tups):
	ms2_renamer(ovl, name_tups)
	logging.info(f"Replacing Dat contents for {name_tups}")
	if check_length(name_tups):
		return
	name_tups_new = [(name_bytes(o), name_bytes(n)) for o, n in name_tups]
	try:
		# hash the internal buffers
		for archive_entry in ovl.archives:
			ovs = archive_entry.content
			for fragment in ovs.fragments:
				for ptr in fragment.pointers:
					ptr.data = replace_bytes(ptr.data, name_tups_new)
	except Exception as err:
		showdialog(str(err))
	logging.info("Done!")


def check_length(name_tups):
	# Ask and return true if error is found and process should be stopped
	for old, new in name_tups:
		if len(old) != len(new):
			if showdialog(
					f"WARNING: length of '{old}' [{len(old)} chars] and '{new}' [{len(new)} chars] don't match!\n"
					f"Stop hashing?", ask=True):
				return True


def species_dat_replacer(ovl, name_tups):
	logging.info(f"Replacing Species Dat contents for {name_tups}")
	if check_length(name_tups):
		return
	name_tups_new = []
	name_tups_new2 = []
	if ovl.user_version.is_jwe:
		suffixes = ("@", "_Var")
		suffixes2 = ("", "@", "_Var")
		for old, new in name_tups:
			extend_name_tuples(name_tups_new, new, old, suffixes)
			extend_name_tuples(name_tups_new2, new, old, suffixes2)
	else:
		suffixes = []
		for gender in ("_Female", "_Male", "_Juvenile", ""):
			# various hardcoded suffixes
			for sym in (
					"@", "_Mat", "_Skin", "_Skin_NoDirt", "_Fur", "_Fur_Shell", "_Fur_Fin", "_Eyeball", "_Eyes",
					"_Eye", "_EyeMouthClaws", "_Whiskers", "_Hairs", "_Hair", "_Feathers", "_Teeth", ""):
				suffixes.append(f"{gender}{sym}")
			# lods
			for i in range(7):
				suffixes.append(f"{gender}_l{i}")
		for old, new in name_tups:
			extend_name_tuples(name_tups_new, new, old, suffixes)
	try:
		# hash the internal buffers
		for archive_entry in ovl.archives:
			ovs = archive_entry.content
			for fragment in ovs.fragments:
				for ptr in fragment.pointers:
					ptr.data = replace_bytes(ptr.data, name_tups_new)
			for buffer_entry in ovs.buffer_entries:
				if ovl.user_version.is_jwe:
					b = buffer_entry.data
					buffer_entry.data = replace_bytes(b, name_tups_new2)
				else:
					b = buffer_entry.data
					buffer_entry.data = replace_bytes(b, name_tups_new)
	except Exception as err:
		showdialog(str(err))
	logging.info("Finished DAT replacing")


def extend_name_tuples(name_tups_new, new, old, suffixes):
	name_tups_temp = [(old + s, new + s) for s in suffixes]
	name_tups_new.extend([(name_bytes(o), name_bytes(n)) for o, n in name_tups_temp])
	name_tups_new.extend([(djb_bytes(o), djb_bytes(n)) for o, n in name_tups_temp])


def replace_bytes(b, name_tups):
	for old, new in name_tups:
		b = b.replace(old, new)
	return b
