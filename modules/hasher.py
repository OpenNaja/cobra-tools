
def djbb(s):
	# calculates DJB hash for string s
	# from https://gist.github.com/mengzhuo/180cd6be8ba9e2743753#file-hash_djb2-py
	hash = 5381
	for x in s:
		hash = (( hash << 5) + hash) + ord(x)
	return hash & 0xFFFFFFFF

def dat_hasher(archive,old1,old2,old3,new1,new2,new3,header_files,header_textures):
	print("\nHashing from archive",archive.archive_index)
	print("\nHeaders")
	for header_entry in archive.header_entries:
		new_name = header_entry.basename
		new_name2 = new_name.replace(old1,new1)
		new_name3 = new_name2.replace(old2,new2)
		new_name4 = new_name3.replace(old3,new3)
		new_hash = djbb(new_name4)
		print(header_entry.basename,header_entry.file_hash,new_name4,new_hash)
		header_entry.file_hash = new_hash
	print("\nStrings")
	for sized_str_entry in archive.sized_str_entries:
		new_name = sized_str_entry.basename
		new_name2 = new_name.replace(old1,new1)
		new_name3 = new_name2.replace(old2,new2)
		new_name4 = new_name3.replace(old3,new3)
		new_hash = djbb(new_name4)
		print(sized_str_entry.basename,sized_str_entry.file_hash,new_name4,new_hash)
		sized_str_entry.file_hash = new_hash
	print("\nDatas")
	for data_entry in archive.data_entries:
		new_name,ext = os.path.splitext(data_entry.name)
		new_name2 = new_name.replace(old1,new1)
		new_name3 = new_name2.replace(old2,new2)
		new_name4 = new_name3.replace(old3,new3)
		new_hash = djbb(new_name4)
		print(data_entry.name,data_entry.file_hash,new_name4,new_hash)
		data_entry.file_hash = new_hash
	print("\nSets")
	for set_entry in archive.set_header.sets:
		new_name,ext = os.path.splitext(set_entry.name)
		new_name2 = new_name.replace(old1,new1)
		new_name3 = new_name2.replace(old2,new2)
		new_name4 = new_name3.replace(old3,new3)
		new_hash = djbb(new_name4)
		print(set_entry.name,set_entry.file_hash,new_name4,new_hash)
		set_entry.file_hash = new_hash
	print("\nAssets")
	for asset_entry in archive.set_header.assets:
		new_name,ext = os.path.splitext(asset_entry.name)
		new_name2 = new_name.replace(old1,new1)
		new_name3 = new_name2.replace(old2,new2)
		new_name4 = new_name3.replace(old3,new3)
		new_hash = djbb(new_name4)
		print(asset_entry.name,asset_entry.file_hash,new_name4,new_hash)
		asset_entry.file_hash = new_hash
	print("\nFiles")
	for file_entry in header_files:  
		new_name = file_entry.name
		new_name2 = new_name.replace(old1,new1)
		new_name3 = new_name2.replace(old2,new2)
		new_name4 = new_name3.replace(old3,new3)
		new_hash = djbb(new_name4)
		print(file_entry.name,file_entry.hash,new_name4,new_hash)
		file_entry.hash = new_hash
	print("\nTextures")
	for texture_entry in header_textures: 
		if "bad hash" not in [texture_entry.name]:
			new_name = texture_entry.name
			new_name2 = new_name.replace(old1,new1)
			new_name3 = new_name2.replace(old2,new2)
			new_name4 = new_name3.replace(old3,new3)
			new_hash = djbb(new_name4)
		else:
			new_hash = texture_entry.hash
			new_name4 = texture_entry.name
		print(texture_entry.name,texture_entry.hash,new_name4,new_hash)
		texture_entry.hash = new_hash
	print("Done!")
