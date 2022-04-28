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
			for dep in file_entry.dependencies:
				dep.link_ptr.remove()
	remove_from_ovs(ovl, filenames)
	if children_names:
		logging.info(f"Removing children")
		_remove_files(ovl, children_names)


def bulk_delete(input_list, entries_to_delete):
	entries_to_delete = set(entries_to_delete)
	lut_dict = {e: e_index for e_index, e in enumerate(input_list)}
	indices_to_delete = [lut_dict[e] for e in entries_to_delete]
	for e_index in sorted(indices_to_delete, reverse=True):
		input_list.pop(e_index)


def remove_from_ovs(ovl, filenames):
	for archive in ovl.archives:
		ovs = archive.content
		# remove sizedstring entry for file and remove its fragments if mapped
		for ss_index, ss_entry in sorted(enumerate(ovs.sized_str_entries), reverse=True):
			# delete the sized string and fragment data
			if ss_entry.name in filenames:
				# wipe out ss and frag data
				for frag in ss_entry.fragments:
					frag.struct_ptr.remove()
					frag.link_ptr.remove()
					# ovs.fragments.remove(frag)
				ss_entry.struct_ptr.remove()
				# remove frag and then ss entry
				ovs.sized_str_entries.remove(ss_entry)

		# remove data entry for file
		for data_index, data in sorted(enumerate(ovs.data_entries), reverse=True):
			if data.name in filenames:
				# buffers_to_delete.extend(data.buffers)
				for buffer in data.buffers:
					buffer.update_data(b"")
					ovs.buffer_entries.remove(buffer)
				ovs.data_entries.remove(data)
