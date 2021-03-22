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
	ovl.update_counts()


def remove_from_ovs(del_hash, file_entry, fileext, new_bb, new_f, next_hash, old_index, ovl):
	ovs = ovl.archives[0]
	# remove sizedstring entry for file and remove its fragments if mapped
	for ss_index, ss_entry in enumerate(ovs.content.sized_str_entries):
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

		# update name indices for PZ (JWE hashes remain untouched!)
		if not ovl.user_version.is_jwe:
			if ss_entry.lower_name == file_entry.name + fileext:
				print("deleting", ss_entry.lower_name, ss_entry.file_hash, old_index)
				try:
					print(ovs.content.sized_str_entries[ss_index + 1].file_hash, old_index)
					ovs.content.sized_str_entries[ss_index + 1].file_hash -= 1
					print("changed to:  ", ovs.content.sized_str_entries[ss_index + 1].file_hash)
				except:
					print("last file index")
			else:
				print(ss_entry.file_hash, old_index)
				if ss_entry.file_hash >= old_index:
					ss_entry.file_hash -= 1
					print("changed to: ", ss_entry.file_hash)

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
	for de, data in enumerate(ovs.content.data_entries):
		if data.basename == file_entry.name and data.ext == fileext:

			ovs.num_datas -= 1
			ovl.num_datas -= 1

			zero_buff_array = [b"" for buffer in data.buffer_datas]
			data.update_data(zero_buff_array)
			thing = []
			for buff in data.buffers:
				thing.append(buff.o_ind)
			thing.sort()
			rem_buf = len(thing)

			for bbf in ovs.content.buffer_entries:
				if bbf.o_ind not in thing:
					new_bb.append(bbf)

			ovs.content.buffer_entries = new_bb
			ovs.num_buffers -= rem_buf
			ovl.num_buffers -= rem_buf
			ovs.content.data_entries.pop(de)
		if not ovl.user_version.is_jwe:
			if data.basename == file_entry.name and data.ext == fileext:
				print("deleting", data.basename, old_index)
				try:
					print(ovs.content.data_entries[de + 1].file_hash, old_index)
					ovs.content.data_entries[de + 1].file_hash -= 1
					print("changed to:  ", ovs.content.data_entries[de + 1].file_hash)
				except:
					print("last file index")
			else:
				print(data.file_hash, old_index)
				if data.file_hash > old_index:
					data.file_hash -= 1
					print("changed to: ", data.file_hash)
