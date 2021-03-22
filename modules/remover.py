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
		new_bb = Array()
		new_f = Array()
		basename, fileext = os.path.splitext(filename)
		# remove file entry
		for i, file_entry in enumerate(ovl.files):
			if basename == file_entry.name and file_entry.ext == fileext:
				old_index = i

				del_hash = file_entry.file_hash
				next_hash = ovl.files[i - 1].file_hash

				ovl.files.pop(i)

				# update mime entries
				for mime_index, mime in enumerate(ovl.mimes):
					# found mime matching removed file
					if mime_index == file_entry.extension:
						mime.file_count -= 1
						if mime.file_count < 1:
							ovl.mimes.pop(mime_index)
					# mime type comes after the affected mime
					elif mime_index > file_entry.extension:
						mime.file_index_offset -= 1
				# remove dependencies for removed file
				for dep_i, dep in enumerate(ovl.dependencies):
					if dep.file_index == i:
						ovl.dependencies.pop(dep_i)
					elif dep.file_index > i:
						dep.file_index -= 1

				remove_from_ovs(del_hash, file_entry, fileext, new_bb, new_f, next_hash, old_index, ovl)

			print("file index", i)
			new_bb = Array()
			new_f = Array()
	# adjust the counts
	ovl.num_files = ovl.num_files_2 = ovl.num_files_3 = len(ovl.files)
	ovl.num_dependencies = len(ovl.dependencies)
	ovl.num_mimes = len(ovl.mimes)


def remove_from_ovs(del_hash, file_entry, fileext, new_bb, new_f, next_hash, old_index, ovl):
	# remove sizedstring entry for file and remove its fragments if mapped
	for ss, string in enumerate(ovl.archives[0].content.sized_str_entries):
		# delete the sized string and fragment data
		if string.lower_name == file_entry.name + fileext:
			ovl.archives[0].content.sized_str_entries.pop(ss)
			ovl.archives[0].num_files -= 1
			ovl.archives[0].uncompressed_size -= 16

			string.pointers[0].update_data(b"", update_copies=True)
			for frag in string.fragments:
				frag.pointers[0].update_data(b"", update_copies=True)
				frag.pointers[1].update_data(b"", update_copies=True)

			fgg = []
			for frg in string.fragments:
				fgg.append(frg.o_ind)

			rem_ff = len(fgg)

			for fff in ovl.archives[0].content.fragments:
				if fff.o_ind not in fgg:
					new_f.append(fff)

			ovl.archives[0].content.fragments = new_f
			ovl.archives[0].num_fragments -= rem_ff

		# update name indices for PZ (JWE hashes remain untouched!)
		if not ovl.user_version.is_jwe:
			if string.lower_name == file_entry.name + fileext:
				print("deleting", string.lower_name, string.file_hash, old_index)
				try:
					print(ovl.archives[0].content.sized_str_entries[ss + 1].file_hash, old_index)
					ovl.archives[0].content.sized_str_entries[ss + 1].file_hash -= 1
					print("changed to:  ", ovl.archives[0].content.sized_str_entries[ss + 1].file_hash)
				except:
					print("last file index")
			else:
				print(string.file_hash, old_index)
				if string.file_hash >= old_index:
					string.file_hash -= 1
					print("changed to: ", string.file_hash)

	# TODO UPDATE THE HEADER ENTRIES WITH THE FIRST FILE HASH AND NEW COUNTS
	for he, header_entry in enumerate(ovl.archives[0].content.header_entries):
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
	for de, data in enumerate(ovl.archives[0].content.data_entries):
		if data.basename == file_entry.name and data.ext == fileext:

			ovl.archives[0].num_datas -= 1
			ovl.num_datas -= 1
			ovl.archives[0].uncompressed_size -= 32

			zero_buff_array = [b"" for buffer in data.buffer_datas]
			data.update_data(zero_buff_array)
			thing = []
			for buff in data.buffers:
				thing.append(buff.o_ind)
			thing.sort()
			rem_buf = len(thing)

			for bbf in ovl.archives[0].content.buffer_entries:
				if bbf.o_ind not in thing:
					new_bb.append(bbf)

			ovl.archives[0].content.buffer_entries = new_bb
			ovl.archives[0].num_buffers -= rem_buf
			ovl.num_buffers -= rem_buf

			ovl.archives[0].uncompressed_size -= 8 * rem_buf
			ovl.archives[0].content.data_entries.pop(de)
		if not ovl.user_version.is_jwe:
			if data.basename == file_entry.name and data.ext == fileext:
				print("deleting", data.basename, old_index)
				try:
					print(ovl.archives[0].content.data_entries[de + 1].file_hash, old_index)
					ovl.archives[0].content.data_entries[de + 1].file_hash -= 1
					print("changed to:  ", ovl.archives[0].content.data_entries[de + 1].file_hash)
				except:
					print("last file index")
			else:
				print(data.file_hash, old_index)
				if data.file_hash > old_index:
					data.file_hash -= 1
					print("changed to: ", data.file_hash)
