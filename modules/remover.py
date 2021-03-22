import os
from modules.formats.shared import djb
from generated.array import Array
import io


def dir_remover(ovl, dirnames):
	for dirname in dirnames:
		# remove the directory entry
		for i, dir_entry in enumerate(ovl.dirs):
			if dirname == dir_entry.name:
				ovl.num_dirs -= 1
				ovl.dirs.pop(i)
			print("dir index", i)


def file_remover(ovl, filenames):
	for filename in filenames:
		basename, fileext = os.path.splitext(filename)
		# remove file entry
		for i, file_entry in sorted(enumerate(ovl.files), reverse=True):
			if basename == file_entry.name and file_entry.ext == fileext:
				old_index = i

				del_hash = file_entry.file_hash
				next_hash = ovl.files[i - 1].file_hash

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

				remove_from_ovs(del_hash, file_entry, fileext, next_hash, old_index, ovl)

			# print("file index", i)
	# update name indices for PZ (JWE hashes remain untouched!)
	if not ovl.user_version.is_jwe:
		print("Updating name indices for ovs archives")
		name_lut = {file.name+file.ext: file_index for file_index, file in enumerate(ovl.files)}
		# print(name_lut)
		for archive in ovl.archives:
			# remove sizedstring entry for file and remove its fragments if mapped
			for ss_entry in archive.content.sized_str_entries:
				ss_entry.file_hash = name_lut[ss_entry.name]
			for da_entry in archive.content.data_entries:
				da_entry.file_hash = name_lut[da_entry.name]
	ovl.update_counts()


def remove_from_ovs(del_hash, file_entry, fileext, next_hash, old_index, ovl):
	ovs = ovl.archives[0]
	# remove sizedstring entry for file and remove its fragments if mapped
	for ss_index, ss_entry in sorted(enumerate(ovs.content.sized_str_entries), reverse=True):
		# delete the sized string and fragment data
		if ss_entry.lower_name == file_entry.name + fileext:
			ovs.content.sized_str_entries.pop(ss_index)
			ovs.num_files -= 1

			ss_entry.pointers[0].remove(ovs.content)
			for frag in ss_entry.fragments:
				frag.pointers[0].remove(ovs.content)
				frag.pointers[1].remove(ovs.content)
			for f_index in sorted([frg.o_ind for frg in ss_entry.fragments], reverse=True):
				ovs.content.fragments.pop(f_index)
			ovs.num_fragments = len(ovs.content.fragments)

	# TODO UPDATE THE HEADER ENTRIES WITH THE FIRST FILE HASH AND NEW COUNTS
	for he, header_entry in enumerate(ovs.content.header_entries):
		if ovl.user_version.is_jwe:
			if header_entry.file_hash == del_hash:
				if header_entry.ext_hash == djb(fileext[1:]):
					print("updated header entry")
					header_entry.file_hash = next_hash
		else:
			print(header_entry.file_hash, old_index)
			if header_entry.file_hash >= old_index:
				print("updated header entry", header_entry.file_hash - 1)
				header_entry.file_hash -= 1
	# remove data entry for file
	for data_index, data in sorted(enumerate(ovs.content.data_entries), reverse=True):
		if data.basename == file_entry.name and data.ext == fileext:

			for b_index in sorted([b.o_ind for b in data.buffers], reverse=True):
				ovs.content.buffer_entries.pop(b_index)
			ovs.content.data_entries.pop(data_index)
			ovs.num_datas = len(ovs.content.data_entries)
			ovs.num_buffers = len(ovs.content.buffer_entries)

			# ovl - sum of buffers for all archives?
			ovl.num_buffers -= len(data.buffers)
			ovl.num_datas -= 1
