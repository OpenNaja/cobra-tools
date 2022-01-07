import logging


def file_remover(ovl, filenames):
	"""
	Removes files from an ovl file
	:param ovl: an ovl instance
	:param filenames: list of file names (eg. "example.ext") that should be removed from ovl
	:return:
	"""
	logging.info(f"Removing files for {filenames}")
	children_names = []
	# remove file entry
	for i, file_entry in sorted(enumerate(ovl.files), reverse=True):
		if file_entry.name in filenames:
			ss_entry = ovl.get_sized_str_entry(file_entry.name)
			children_names.extend([ss.name for ss in ss_entry.children])
			children_names.extend([stream.name for stream in file_entry.streams])
			logging.info(f"Removing {file_entry.name}")
			ovl.files.pop(i)
			for dep in file_entry.dependencies:
				dep.pointers[0].remove()

	remove_from_ovs(ovl, filenames)

	if children_names:
		logging.info(f"Removing children")
		file_remover(ovl, children_names)


def bulk_delete(input_list, entries_to_delete):
	entries_to_delete = set(entries_to_delete)
	lut_dict = {e: e_index for e_index, e in enumerate(input_list)}
	indices_to_delete = [lut_dict[e] for e in entries_to_delete]
	for e_index in sorted(indices_to_delete, reverse=True):
		input_list.pop(e_index)


def remove_from_ovs(ovl, filenames):
	ovs = ovl.archives[0]

	# remove sizedstring entry for file and remove its fragments if mapped
	for ss_index, ss_entry in sorted(enumerate(ovs.content.sized_str_entries), reverse=True):
		# delete the sized string and fragment data
		if ss_entry.name in filenames:
			# wipe out ss and frag data
			for frag in ss_entry.fragments:
				frag.pointers[1].remove()
				ovs.content.fragments.remove(frag)
			ss_entry.pointers[0].remove()
			# remove frag and then ss entry
			ovs.content.sized_str_entries.remove(ss_entry)

	# remove data entry for file
	for data_index, data in sorted(enumerate(ovs.content.data_entries), reverse=True):
		if data.name in filenames:
			# buffers_to_delete.extend(data.buffers)
			for buffer in data.buffers:
				buffer.update_data(b"")
				ovs.content.buffer_entries.remove(buffer)
			ovs.content.data_entries.remove(data)
	for pool in ovl.pools:
		# if the pool has editable pointers, flush them to the pool writer first
		pool.flush_pointers()
