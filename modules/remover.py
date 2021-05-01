REVERSED_TYPES = (".tex", ".mdl2", ".ms2", ".lua", ".fdb", ".xmlconfig", ".fgm", ".assetpkg", ".materialcollection", ".txt")


def add_pointer(pointer, ss_entry, pointers_to_ss):
	if pointer.pool_index != -1:
		pointers_to_ss[pointer.pool_index][pointer.data_offset] = ss_entry


def header_hash_finder(ovs):
	# this algorithm depends on every fragment being assigned to the correct sized string entries
	print("Updating pools")
	pointers_to_ss_ss = [{} for _ in ovs.pools]
	pointers_to_ss_frag = [{} for _ in ovs.pools]
	for sized_str_entry in ovs.sized_str_entries:
		add_pointer(sized_str_entry.pointers[0], sized_str_entry, pointers_to_ss_ss)
		for frag in sized_str_entry.fragments:
			for pointer in frag.pointers:
				add_pointer(pointer, sized_str_entry, pointers_to_ss_frag)
	for pool_index, pool in enumerate(ovs.pools):
		print(f"pool_index {pool_index}")
		if pool.ext not in REVERSED_TYPES:
			print(f"Keeping header name {pool.name} as it has not been reverse engineered!")
			continue
		# print(pool)
		ss_map = pointers_to_ss_ss[pool_index]
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
		pool.file_hash = ss.file_hash
		pool.ext_hash = ss.ext_hash
		pool.name = ss.name
		pool.basename = ss.basename
		pool.ext = ss.ext


def file_remover(ovl, filenames):
	"""
	Removes files from an ovl file
	:param ovl: an ovl instance
	:param filenames: list of file names (eg. "example.ext") that should be removed from ovl
	:return:
	"""
	# remove file entry
	for i, file_entry in sorted(enumerate(ovl.files), reverse=True):
		if file_entry.name in filenames:
			print("Removing", file_entry.name)
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

	ovl.update_names()
	# update name indices for PZ (JWE hashes remain untouched!)
	if not ovl.user_version.is_jwe:
		print("Updating name indices for ovs archives")
		name_lut = {file.name: file_index for file_index, file in enumerate(ovl.files)}
		# print(name_lut)
		for archive in ovl.archives:
			# remove sizedstring entry for file and remove its fragments if mapped
			for ss_entry in archive.content.sized_str_entries:
				ss_entry.file_hash = name_lut[ss_entry.name]
			for da_entry in archive.content.data_entries:
				da_entry.file_hash = name_lut[da_entry.name]
	ovl.update_counts()
	for ovs in ovl.archives:
		header_hash_finder(ovs.content)


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

			ovs.num_files -= 1
            #wipe out ss and frag data
			ss_entry.pointers[0].update_data(b"", update_copies=True)

			for frag in ss_entry.fragments:
				frag.pointers[0].update_data(b"", update_copies=True)
				frag.pointers[1].update_data(b"", update_copies=True)
				frag.pointers[0].remove(ovs.content)
				frag.pointers[1].remove(ovs.content)
                #remove frag and then ss entry
				ovs.content.fragments.remove(frag)
			ss_entry.pointers[0].remove(ovs.content)
			ovs.content.sized_str_entries.remove(ss_entry)


	# remove data entry for file
	for data_index, data in sorted(enumerate(ovs.content.data_entries), reverse=True):
		if data.name in filenames:
			ovl.num_buffers -= len(data.buffers)
			ovl.num_datas -= 1

			#buffers_to_delete.extend(data.buffers)
			for buffer in data.buffers:
				buffer.update_data(b"")
				ovs.content.buffer_entries.remove(buffer)
			ovs.content.data_entries.remove(data)

			# ovl - sum of buffers for all archives?
			#ovl.num_buffers -= len(data.buffers)
			#ovl.num_datas -= 1

	ovs.num_fragments = len(ovs.content.fragments)
	ovs.num_datas = len(ovs.content.data_entries)
	ovs.num_buffers = len(ovs.content.buffer_entries)
	ovs.content.write_pointers_to_pools(ignore_unaccounted_bytes=True)
