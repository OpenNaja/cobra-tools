import os


def djbb(s):
	# calculates DJB hash for string s
	# from https://gist.github.com/mengzhuo/180cd6be8ba9e2743753#file-hash_djb2-py
	hash = 5381
	for x in s:
		hash = (( hash << 5) + hash) + ord(x)
	return hash & 0xFFFFFFFF


def dat_hasher(archive, name_tups, header_files, header_textures):
	print("\nHashing from archive", archive.archive_index)
	for entry_list in (archive.data_entries,
					   archive.set_header.sets,
					   archive.set_header.assets):
		for entry in entry_list:
			if "bad hash" in entry.name:
				print("Skipping",entry.name, entry.file_hash)
				continue
			new_name, ext = os.path.splitext(entry.name)
			for old, new in name_tups:
				new_name = new_name.replace(old, new)
			new_hash = djbb(new_name)
			print(entry.name, entry.file_hash, hex(entry.file_hash), new_name, new_hash, hex(new_hash))
			entry.file_hash = new_hash
            
            
            
	for entry_list in (archive.header_entries,
						archive.sized_str_entries):
		for entry in entry_list:
			if "bad hash" in entry.name:
				print("Skipping",entry.name, entry.file_hash)
				continue
			new_name = entry.basename
			for old, new in name_tups:
				new_name = new_name.replace(old, new)
			new_hash = djbb(new_name)
			print(entry.name, entry.file_hash, hex(entry.file_hash), new_name, new_hash, hex(new_hash))
			entry.file_hash = new_hash

	for entry_list in (header_files,
						header_textures):
		for entry in entry_list:
			if "bad hash" in entry.name:
				print("Skipping",entry.name, entry.file_hash)
				continue
			new_name = entry.name
			for old, new in name_tups:
				new_name = new_name.replace(old, new)
			new_hash = djbb(new_name)
			print(entry.name, entry.file_hash, hex(entry.file_hash), new_name, new_hash, hex(new_hash))
			entry.file_hash = new_hash					                
                       
	print("Done!")
