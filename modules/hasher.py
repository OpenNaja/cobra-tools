import os


def djbb(s):
	# calculates DJB hash for string s
	# from https://gist.github.com/mengzhuo/180cd6be8ba9e2743753#file-hash_djb2-py
	hash = 5381
	for x in s:
		hash = ((hash << 5) + hash) + ord(x)
	return hash & 0xFFFFFFFF


def dat_hasher(ovl, name_tups):
	lists = [ovl.files, ovl.textures, ]
	for ovs in ovl.ovs_files:
		lists.extend((ovs.data_entries,
					 ovs.set_header.sets,
					 ovs.set_header.assets,
					 ovs.header_entries,
					 ovs.sized_str_entries
					 ))
	# print("\nHashing from archive", archive.archive_index)
	for entry_list in lists:
		for entry in entry_list:
			if "bad hash" in entry.name:
				print("Skipping", entry.name, entry.file_hash)
				continue
			new_name, ext = os.path.splitext(entry.name)
			for old, new in name_tups:
				new_name = new_name.replace(old, new)
			new_hash = djbb(new_name)
			print(entry.name, entry.file_hash, hex(entry.file_hash), new_name, new_hash, hex(new_hash))
			entry.file_hash = new_hash

	print("Done!")
