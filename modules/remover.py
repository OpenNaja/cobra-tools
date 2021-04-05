MAX_UINT32 = 4294967295
REVERSED_TYPES = (".tex", ".mdl2", ".ms2", ".lua", ".fdb", ".xmlconfig", ".fgm", ".assetpkg", ".materialcollection", ".txt")


def add_pointer(pointer, ss_entry, pointers_to_ss):
	if pointer.header_index != MAX_UINT32:
		pointers_to_ss[pointer.header_index][pointer.data_offset] = ss_entry


def header_hash_finder(ovs):
	# this algorithm depends on every fragment being assigned to the correct sized string entries
	print("Updating header entries")
	pointers_to_ss_ss = [{} for _ in ovs.header_entries]
	pointers_to_ss_frag = [{} for _ in ovs.header_entries]
	for sized_str_entry in ovs.sized_str_entries:
		add_pointer(sized_str_entry.pointers[0], sized_str_entry, pointers_to_ss_ss)
		for frag in sized_str_entry.fragments:
			for pointer in frag.pointers:
				add_pointer(pointer, sized_str_entry, pointers_to_ss_frag)
	for header_entry_index, header_entry in enumerate(ovs.header_entries):
		print(f"Header index {header_entry_index}")
		if header_entry.ext not in REVERSED_TYPES:
			print(f"Keeping header name {header_entry.name} as it has not been reverse engineered!")
			continue
		# print(header_entry)
		ss_map = pointers_to_ss_ss[header_entry_index]
		results = tuple(sorted(ss_map.items()))
		if not results:
			print("No ss pointer found, checking frag pointers!")
			ss_map = pointers_to_ss_frag[header_entry_index]
			results = tuple(sorted(ss_map.items()))
			if not results:
				print(f"No pointer found for header {header_entry_index}, error!")
				continue
		ss = results[0][1]
		print(f"Header[{header_entry_index}]: {header_entry.name} -> {ss.name}")
		header_entry.file_hash = ss.file_hash
		header_entry.ext_hash = ss.ext_hash
		header_entry.name = ss.name
		header_entry.basename = ss.basename
		header_entry.ext = ss.ext


def dir_remover(ovl, dirnames):
	for dirname in dirnames:
		# remove the directory entry
		for i, dir_entry in enumerate(ovl.dirs):
			if dirname == dir_entry.name:
				ovl.num_dirs -= 1
				ovl.dirs.pop(i)
			print("dir index", i)


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


def remove_from_ovs(ovl, filenames):
	ovs = ovl.archives[0]
	# remove sizedstring entry for file and remove its fragments if mapped
	for ss_index, ss_entry in sorted(enumerate(ovs.content.sized_str_entries), reverse=True):
		# delete the sized string and fragment data
		if ss_entry.name in filenames:
			ovs.content.sized_str_entries.pop(ss_index)
			ovs.num_files -= 1

			ss_entry.pointers[0].remove(ovs.content)
			for frag in ss_entry.fragments:
				frag.pointers[0].remove(ovs.content)
				frag.pointers[1].remove(ovs.content)
			for f_index in sorted([frg.o_ind for frg in ss_entry.fragments], reverse=True):
				ovs.content.fragments.pop(f_index)

	# remove data entry for file
	for data_index, data in sorted(enumerate(ovs.content.data_entries), reverse=True):
		if data.name in filenames:

			for b_index in sorted([b.o_ind for b in data.buffers], reverse=True):
				ovs.content.buffer_entries.pop(b_index)
			ovs.content.data_entries.pop(data_index)

			# ovl - sum of buffers for all archives?
			ovl.num_buffers -= len(data.buffers)
			ovl.num_datas -= 1
	ovs.num_fragments = len(ovs.content.fragments)
	ovs.num_datas = len(ovs.content.data_entries)
	ovs.num_buffers = len(ovs.content.buffer_entries)
	header_hash_finder(ovs.content)
	ovs.content.write_pointers_to_header_datas(ignore_unaccounted_bytes=True)
