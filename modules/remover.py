import logging


def file_remover(ovl, filenames):
	"""
	Removes files from an ovl file
	:param ovl: an ovl instance
	:param filenames: list of file names (eg. "example.ext") that should be removed from ovl
	:return:
	"""
	logging.info(f"Removing files for {filenames}")
	_remove_files(ovl, filenames)
	for i, pool in sorted(enumerate(ovl.pools), reverse=True):
		pool.flush_pointers()
		logging.info(f"pool {i} {pool.offset_2_struct_entries}")
		if not pool.offset_2_struct_entries:
			logging.info(f"Deleting pool {pool.name} as it has no pointers")
			for archive in ovl.archives:
				if pool in archive.content.pools:
					archive.content.pools.remove(pool)
			ovl.pools.remove(pool)


def _remove_files(ovl, filenames):
	children_names = []
	# remove file entry
	for i, file_entry in sorted(enumerate(ovl.files), reverse=True):
		if file_entry.name in filenames:
			children_names.extend(ovl.get_children(file_entry))
			logging.info(f"Removing {file_entry.name}")
			ovl.files.pop(i)
			if file_entry.loader:
				file_entry.loader.remove()
	if children_names:
		logging.info(f"Removing children")
		_remove_files(ovl, children_names)


def bulk_delete(input_list, entries_to_delete):
	entries_to_delete = set(entries_to_delete)
	lut_dict = {e: e_index for e_index, e in enumerate(input_list)}
	indices_to_delete = [lut_dict[e] for e in entries_to_delete]
	for e_index in sorted(indices_to_delete, reverse=True):
		input_list.pop(e_index)
