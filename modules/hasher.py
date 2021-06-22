import logging

from modules.formats.shared import djb
import struct
import io
import os
from generated.formats.ovl.versions import *
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
	if is_pz16(ovl):
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
	else:   
		for archive_entry in ovl.archives:
			content = archive_entry.content
			ovs_lists.extend((
				content.data_entries,
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


def dat_replacer(ovl, name_tups):
	logging.info(f"Replacing Dat contents for {name_tups}")
	if check_length(name_tups):
		return
	name_tups_new = [(name_bytes(o), name_bytes(n)) for o, n in name_tups]
	try:
		# hash the internal buffers
		for archive_entry in ovl.archives:
			ovs = archive_entry.content
			for pool in ovs.pools:
				b = pool.data.getvalue()
				pool.data = io.BytesIO(replace_bytes(b, name_tups_new))
		# do a total reload of all ptrs, data reload would be enough
		ovl.load_pointers()
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
					"_Eye", "_EyeMouthClaws", "_Whiskers", "_Hair", "_Feathers", "_Teeth", ""):
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
			for pool in ovs.pools:
				b = pool.data.getvalue()
				pool.data = io.BytesIO(replace_bytes(b, name_tups_new))
			for buffer_entry in ovs.buffer_entries:
				if ovl.user_version.is_jwe:
					b = buffer_entry.data
					buffer_entry.data = replace_bytes(b, name_tups_new2)
				else:
					b = buffer_entry.data
					buffer_entry.data = replace_bytes(b, name_tups_new)
		# do a total reload of all ptrs, data reload would be enough
		ovl.load_pointers()
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
