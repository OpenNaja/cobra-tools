from modules.formats.shared import djb
import struct
import io

from ovl_util.interaction import showdialog

SPECIES_ONLY_FMTS = (".mdl2", ".ms2", ".motiongraph", ".materialcollection")


def djb_bytes(string):
	return struct.pack("<I", djb(string.lower()))


def name_bytes(string):
	return string.encode(encoding="utf-8")


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
			content.pools,
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
					if entry.ext not in SPECIES_ONLY_FMTS:
						print("Skipping", entry.name, entry.file_hash)
						continue
				new_name = entry.basename
				for old, new in name_tups:
					new_name = new_name.replace(old, new)
				if hasattr(entry, "file_hash"):
					new_hash = djb(new_name)
					if i == 0:  # only want a list of file names, dont want dirs and dependencies overriding this next loop
						old_hash_to_new[entry.file_hash] = (new_name, new_hash)
						old_hash_to_new_pz[entry_index] = (new_name, new_hash)
					print(f"List{i} {entry.basename} -> {new_name},  {entry.file_hash} ->  {new_hash}")
					entry.file_hash = new_hash
				else:
					print(f"List{i} {entry.basename} -> {new_name},  [NOT HASHED]")
				entry.basename = new_name
				entry.name = entry.basename + entry.ext
			except Exception as err:
				print(err)

	# we do this in a second step to resolve the links
	for i, entry_list in enumerate(ovs_lists):
		for entry in entry_list:
			if species_mode:
				if entry.ext not in SPECIES_ONLY_FMTS:
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
	if check_length(name_tups):
		return
	name_tups_new = [(name_bytes(o), name_bytes(n)) for o, n in name_tups]
	try:
		# hash the internal buffers
		for archive_entry in ovl.archives:
			ovs = archive_entry.content
			for pool in ovs.pools:
				b = pool.data.getvalue()
				pool.data = io.BytesIO(replace_bytes(b, name_tups_new))
			ovs.populate_pointers()
	# for buffer_entry in ovs.buffer_entries:
	# 	b = buffer_entry.data
	# 	buffer_entry.data = replace_bytes(b, name_tups)
	except Exception as err:
		print(err)
	print("Done!")


def check_length(name_tups):
	# Ask and return true if error is found and process should be stopped
	for old, new in name_tups:
		if len(old) != len(new):
			if showdialog(f"WARNING: length of '{old}' [{len(old)} chars] and '{new}' [{len(new)} chars] don't match!\n"
							 f"Stop hashing?", ask=True):
				return True


def species_dat_replacer(ovl, name_tups):
	print(f"Replacing Species Dat contents for {name_tups}")
	if check_length(name_tups):
		return
	name_tups_new = []
	name_tups_new2 = []
	if ovl.user_version.is_jwe:
		suffixes = ("@", "_Var")
		suffixes2 = ("", "@", "_Var")
		for old, new in name_tups:
			extend_name_tuples(name_tups_new, new, old, suffixes)
			extend_name_tuples(name_tups_new2, new, old, suffixes2)
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
		for old, new in name_tups:
			extend_name_tuples(name_tups_new, new, old, suffixes)
	try:
		# hash the internal buffers
		for archive_entry in ovl.archives:
			ovs = archive_entry.content
			for pool in ovs.pools:
				b = pool.data.getvalue()
				pool.data = io.BytesIO(replace_bytes(b, name_tups_new))
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


def extend_name_tuples(name_tups_new, new, old, suffixes):
	name_tups_temp = [(old + s, new + s) for s in suffixes]
	name_tups_new.extend([(name_bytes(o), name_bytes(n)) for o, n in name_tups_temp])
	name_tups_new.extend([(djb_bytes(o), djb_bytes(n)) for o, n in name_tups_temp])


def replace_bytes(b, name_tups):
	for old, new in name_tups:
		b = b.replace(old, new)
	return b
