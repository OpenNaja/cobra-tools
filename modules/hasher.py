from modules.formats.shared import djb
import io


def dat_hasher(ovl, name_tups, species_mode=False):
	print(f"Hashing and Renaming for {name_tups}")
	ovl_lists = [ovl.files, ovl.dependencies, ovl.dirs]
	ovs_lists = []
	for archive_entry in ovl.archives:
		content = archive_entry.content
		ovs_lists.extend((
			content.data_entries,
			content.set_header.sets,
			content.set_header.assets,
			content.header_entries,
			content.sized_str_entries
		))
	old_hash_to_new = {}
	old_hash_to_new_pz = {}
	# first go over the ovl lists to generate new hashes
	for i, entry_list in enumerate(ovl_lists):
		for entry_index, entry in enumerate(entry_list):
			try:
				if "bad hash" in entry.name:
					print("Skipping", entry.name, entry.file_hash)
					continue
				if species_mode:
					if entry.ext not in ".mdl2.ms2.motiongraph.materialcollection":
						print("Skipping", entry.name, entry.file_hash)
						continue
				new_name = entry.basename
				for old, new in name_tups:
					new_name = new_name.replace(old, new)
				if hasattr(entry, "file_hash"):
					new_hash = djb(new_name)
					old_hash_to_new[entry.file_hash] = (new_name, new_hash)
					old_hash_to_new_pz[entry_index] = (new_name, new_hash)
					print(f"List{i} {entry.basename} -> {new_name},  {entry.file_hash} ->  {new_hash}")
					entry.file_hash = new_hash
				else:
					print(f"List{i} {entry.basename} -> {new_name},  [NOT HASHED]")
				entry.basename = new_name
				entry.name = entry.basename+entry.ext
			except Exception as err:
				print(err)

	# we do this in a second step to resolve the links
	for i, entry_list in enumerate(ovs_lists):
		for entry in entry_list:
			if species_mode:
				if entry.ext not in ".mdl2.ms2.motiongraph.materialcollection":
					print("Skipping", entry.name, entry.file_hash)
					continue
			if ovl.user_version.is_jwe:
				new_name, new_hash = old_hash_to_new[entry.file_hash]
				entry.file_hash = new_hash
			else:
				new_name, new_hash = old_hash_to_new_pz[entry.file_hash]
			entry.basename = new_name
			entry.name = f"{new_name}{entry.ext}"

	ovl.update_names()
	# resort the file entries
	for i, file in enumerate(ovl.files):
		file.old_index = i

	# sort the different lists according to the criteria specified
	ovl.files.sort(key=lambda x: (x.ext, x.file_hash))
	ovl.dependencies.sort(key=lambda x: x.file_hash)

	# create a lookup table to map the old indices to the new ones
	lut = {}
	for i, file in enumerate(ovl.files):
		lut[file.old_index] = i

	# update the file indices
	for dependency in ovl.dependencies:
		dependency.file_index = lut[dependency.file_index]
	for aux in ovl.aux_entries:
		aux.file_index = lut[aux.file_index]
	if ovl.user_version.is_jwe:
		print("JWE")
	else:
		for i, entry_list in enumerate(ovs_lists):
			for entry in entry_list:
				entry.file_hash = lut[entry.file_hash]
	ovl.update_ss_dict()
	print("Done!")


def dat_hasher_species(ovl, name_tups):
	dat_hasher(ovl, name_tups, species_mode=True)


def dat_replacer(ovl, name_tups):
	print(f"Replacing Dat contents for {name_tups}")
	try:
		# hash the internal buffers
		for archive_entry in ovl.archives:
			ovs = archive_entry.content
			for header_entry in ovs.header_entries:
				b = header_entry.data.getvalue()
				header_entry.data = io.BytesIO(replace_bytes(b, name_tups))
			ovs.populate_pointers()
		# for buffer_entry in ovs.buffer_entries:
		# 	b = buffer_entry.data
		# 	buffer_entry.data = replace_bytes(b, name_tups)
	except Exception as err:
		print(err)
	print("Done!")


def species_dat_replacer(ovl, name_tups):
	print(f"Replacing Dat contents for {name_tups}")
	if ovl.user_version.is_jwe:
		for old, new in name_tups:
			old_a = old + "@"
			new_a = new + "@"
			old_b = old + "_Var"
			new_b = new + "_Var"
			old_c = old
			new_c = new
			old_ch = hex(djb(old_c.lower()))
			new_ch = hex(djb(new_c.lower()))
		name_tups_new = [(old_a, new_a), (old_b, new_b), (old_ch, new_ch)]
		name_tups_new2 = [(old_a, new_a), (old_b, new_b), (old_c, new_c), (old_ch, new_ch)]
	else:
		suffixes = []
		for gender in ("_Female", "_Male", "_Juvenile", ""):
			# various hardcoded suffixes
			for sym in ("@", "_Mat", "_Skin", "_Skin_NoDirt", "_Fur", "_Fur_Shell", "_Fur_Fin", "_Eyeball", "_Eyes",
						"_Eye", "_EyeMouthClaws", "_Whiskers", "_Hair", "_Feathers", "_Teeth", ""):
				suffixes.append(f"{gender}{sym}")
			# lods
			for i in range(7):
				suffixes.append(f"{gender}_l{i}")
		name_tups_new = []
		for old, new in name_tups:
			name_tups_temp = [(old+s, new+s) for s in suffixes]
			name_tups_new.extend(name_tups_temp)
			name_tups_new.extend([(hex(djb(o.lower())), hex(djb(n.lower()))) for o, n in name_tups_temp])
	try:
		# hash the internal buffers
		for archive_entry in ovl.archives:
			ovs = archive_entry.content
			for header_entry in ovs.header_entries:
				b = header_entry.data.getvalue()
				header_entry.data = io.BytesIO(replace_bytes(b, name_tups_new))
			ovs.populate_pointers()
			for buffer_entry in ovs.buffer_entries:
				if ovl.user_version.is_jwe:
					b = buffer_entry.data
					buffer_entry.data = replace_bytes(b, name_tups_new2)
				else:
					b = buffer_entry.data
					buffer_entry.data = replace_bytes(b, name_tups_new)
	except Exception as err:
		print(err)
	print("Done!")


def replace_bytes(b, name_tups):
	for old, new in name_tups:
		if old.startswith("0x"):
			print(f"HEX MODE for {old} -> {new}")
			if len(old[2:]) == 8:
				old = bytes.fromhex(old[2:])[::-1]
			elif len(old[2:]) == 7:
				old = bytes.fromhex("0" + old[2:])[::-1]
			elif len(old[2:]) == 6:
				old = bytes.fromhex("00" + old[2:])[::-1]
			if len(new[2:]) == 8:
				new = bytes.fromhex(new[2:])[::-1]
			elif len(new[2:]) == 7:
				new = bytes.fromhex("0" + new[2:])[::-1]
			elif len(new[2:]) == 6:
				new = bytes.fromhex("00" + new[2:])[::-1]
		else:
			old = old.encode(encoding="utf-8")
			new = new.encode(encoding="utf-8")
		print(old, new)
		if len(old) != len(new):
			print(f"WARNING: length of {old} and {new} don't match!")
		b = b.replace(old, new)
	return b
