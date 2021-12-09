import logging
import os
import shutil
import tempfile

from generated.formats.ms2 import Ms2File
from ovl_util.interaction import showdialog


def name_bytes(string):
	return string.encode(encoding="utf-8")


def rename_entry(entry, name_tups):
	if "bad hash" in entry.name:
		logging.warning(f"Skipping {entry.file_hash} because its hash could not be resolved to a name")
		return
	for old, new in name_tups:
		entry.name = entry.name.replace(old, new)
	entry.basename, entry.ext = os.path.splitext(entry.name)


def rename(ovl, name_tups):
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
			rename_entry(entry, name_tups)
	ovl.update_hashes()
	ovl.update_ss_dict()
	logging.info("Finished renaming!")


def ms2_renamer(ovl, name_tups):
	logging.info(f"Replacing names in MS2 files for {name_tups}")

	temp_dir = tempfile.mkdtemp("-cobra")

	def out_dir_func(n):
		"""Helper function to generate temporary output file name"""
		return os.path.normpath(os.path.join(temp_dir, n))

	for ms2_entry in ovl.get_extract_files((), (".ms2",), []):
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
			ms2_entry.loader.load(ms2_path)
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


def replace_bytes(b, name_tups):
	for old, new in name_tups:
		b = b.replace(old, new)
	return b
