import logging
from generated.formats.ovl.versions import *
REVERSED_TYPES = (
	".tex", ".mdl2", ".ms2", ".lua", ".fdb", ".xmlconfig", ".fgm", ".assetpkg", ".materialcollection", ".txt")


def add_pointer(pointer, ss_entry, pointers_to_ss):
	if pointer.pool_index != -1:
		pointers_to_ss[pointer.pool_index][pointer.data_offset] = ss_entry


def header_hash_finder(ovs):
	# this algorithm depends on every fragment being assigned to the correct sized string entries
	print("Updating pools")
	pointers_to_ss = [{} for _ in ovs.pools]
	pointers_to_ss_frag = [{} for _ in ovs.pools]
	for sized_str_entry in ovs.sized_str_entries:
		add_pointer(sized_str_entry.pointers[0], sized_str_entry, pointers_to_ss)
		for frag in sized_str_entry.fragments:
			for pointer in frag.pointers:
				add_pointer(pointer, sized_str_entry, pointers_to_ss_frag)
	for pool_index, pool in enumerate(ovs.pools):
		print(f"pool_index {pool_index}")
		if pool.ext not in REVERSED_TYPES:
			print(f"Keeping header name {pool.name} as it has not been reverse engineered!")
			continue
		# print(pool)
		ss_map = pointers_to_ss[pool_index]
		results = tuple(sorted(ss_map.items()))
		if not results:
			print("No ss pointer found, checking frag pointers!")
			ss_map = pointers_to_ss_frag[pool_index]
			results = tuple(sorted(ss_map.items()))
			if not results:
				print(f"No pointer found for header {pool_index}, error!")
				continue
		ss = results[0][1]
		print(f"Header[{pool_index}]: {pool.name} -> {ss.name}")
		ovs.transfer_identity(pool, ss)


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
			ss_entry =  ovl.get_sized_str_entry(file_entry.name)
			children_names.extend([ss.name for ss in ss_entry.children])
			logging.info(f"Removing {file_entry.name}")
			ovl.files.pop(i)

			# update mime entries
			for mime_index, mime in sorted(enumerate(ovl.mimes), reverse=True):
				# found mime matching removed file
				if mime_index == file_entry.extension:
					mime.file_count -= 1
					if mime.file_count < 1:
						ovl.mimes.pop(mime_index)
				# mime type comes after the affected mime
				elif mime_index > file_entry.extension:
					mime.file_index_offset -= 1
			# remove dependencies for removed file
			for dep_i, dep in sorted(enumerate(ovl.dependencies), reverse=True):
				if dep.file_index == i:
					ovl.dependencies.pop(dep_i)
				elif dep.file_index > i:
					dep.file_index -= 1

	remove_from_ovs(ovl, filenames)

	# update file entry's index into mime list
	ext_lut = {mime.ext: mime_index for mime_index, mime in enumerate(ovl.mimes)}
	for file in ovl.files:
		file.extension = ext_lut[file.ext]

	for ovs in ovl.archives:
		header_hash_finder(ovs.content)
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
			ss_entry.pointers[0].update_data(b"", update_copies=True)

			for frag in ss_entry.fragments:
				frag.pointers[0].update_data(b"", update_copies=True)
				frag.pointers[1].update_data(b"", update_copies=True)
				frag.pointers[0].remove(ovs.content)
				frag.pointers[1].remove(ovs.content)
				# remove frag and then ss entry
				ovs.content.fragments.remove(frag)
			ss_entry.pointers[0].remove(ovs.content)
			ovs.content.sized_str_entries.remove(ss_entry)

	# remove data entry for file
	for data_index, data in sorted(enumerate(ovs.content.data_entries), reverse=True):
		if data.name in filenames:
			if is_pz16(ovl):
				for b_group in ovs.content.new_entries:
					print(b_group)
			# buffers_to_delete.extend(data.buffers)
			for buffer in data.buffers:
				if is_pz16(ovl):
					buff_size = buffer.size
					buffer.buffer_group.size -= buffer.size
					buffer.buffer_group.buffer_count -= 1
					buffer.buffer_group.data_count -= 1
				buffer.update_data(b"")
				ovs.content.buffer_entries.remove(buffer)
			if is_pz16(ovl):
				counta = 0
				countb = 0
				for b_group in ovs.content.new_entries:
					b_group.buffer_offset = counta
					counta += b_group.buffer_count
					if b_group.buffer_index == 0:
						b_group.data_offset = countb
						countb += b_group.data_count
				#for b_group in ovs.content.new_entries:
					#print(b_group)
			ovs.content.data_entries.remove(data)
	ovs.content.write_pointers_to_pools(ignore_unaccounted_bytes=True)
