import os

def djbb(s):
	# calculates DJB hash for string s
	# from https://gist.github.com/mengzhuo/180cd6be8ba9e2743753#file-hash_djb2-py
	hash = 5381
	for x in s:
		hash = (( hash << 5) + hash) + ord(x)
	return hash & 0xFFFFFFFF

def dat_hasher(archive, name_tups, header_files, header_textures):
	print("\nHashing from archive",archive.archive_index)
	for entry_list in (archive.header_entries, archive.sized_str_entries, archive.data_entries, archive.set_header.sets, archive.set_header.assets):
		for entry in entry_list:
			# new_name = entry.basename
			new_name, ext = os.path.splitext(entry.name)
			for old, new in name_tups:
				new_name = new_name.replace(old, new)
			new_hash = djbb(new_name)
			print(entry.name, entry.file_hash, new_name, new_hash)
			entry.file_hash = new_hash
	print("\nFiles")
	for file_entry in header_files:  
		new_name = file_entry.name
		for old, new in name_tups:
			new_name = new_name.replace(old, new)
		new_hash = djbb(new_name)
		print(file_entry.name,file_entry.hash,new_name,new_hash)
		file_entry.hash = new_hash
	print("\nTextures")
	for texture_entry in header_textures: 
		if "bad hash" != texture_entry.name:
			new_name = texture_entry.name
			for old, new in name_tups:
				new_name = new_name.replace(old, new)
			new_hash = djbb(new_name)
			texture_entry.hash = new_hash
		else:
			new_hash = texture_entry.hash
			new_name = texture_entry.name
		print(texture_entry.name, texture_entry.hash, new_name,new_hash)
	print("Done!")
