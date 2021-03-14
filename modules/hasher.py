import os
from modules.formats.shared import djb
import io
import struct


def dat_hasher(ovl, name_tups):
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
		for e,entry in enumerate(entry_list):
			try:
				if "bad hash" in entry.name:
					print("Skipping", entry.name, entry.file_hash)
					continue
				new_name = entry.name
				for old, new in name_tups:
					new_name = new_name.replace(old, new)
				if hasattr(entry, "file_hash"):
					new_hash = djb(new_name)
					old_hash_to_new[entry.file_hash] = (new_name, new_hash)
					old_hash_to_new_pz[e] = (new_name, new_hash)
					print(f"List{i} {entry.name} -> {new_name},  {entry.file_hash} ->  {new_hash}")
					entry.file_hash = new_hash
				else:
					print(f"List{i} {entry.name} -> {new_name},  [NOT HASHED]")
				entry.name = new_name
			except Exception as err:
				print(err)

	# we do this in a second step to resolve the links
	for i, entry_list in enumerate(ovs_lists):
		for entry in entry_list:
			if ovl.user_version.is_jwe:
				new_name, new_hash = old_hash_to_new[entry.file_hash]
				entry.file_hash = new_hash
				entry.name = f"{new_name}{entry.ext}"
				print(entry.ext)
			else:
				new_name, new_hash = old_hash_to_new_pz[entry.file_hash]
				#entry.file_hash = new_hash
				entry.name = f"{new_name}{entry.ext}"
				
	# update the name buffer and offsets
	ovl.names.update_with((
		(ovl.dependencies, "ext"),
		(ovl.dirs, "name"),
		(ovl.mimes, "name"),
		(ovl.files, "name")
	))
	ovl.len_names = len(ovl.names.data)
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
				
	#print("Hashing dat contents...")
	#try:
	#	# hash the internal buffers
	#	for archive_entry in ovl.archives:
	#		ovs = archive_entry.content
	#		for header_entry in ovs.header_entries:
	#			b = header_entry.data.getvalue()
	#			header_entry.data = io.BytesIO(replace_bytes(b, name_tups))
	#		ovs.populate_pointers()
	#		for buffer_entry in ovs.buffer_entries:
	#			b = buffer_entry.data
	#			buffer_entry.data = replace_bytes(b, name_tups)
	#except Exception as err:
	#	print(err)
	print("Done!")
    
def dat_hasher_species(ovl, name_tups):
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
		for e,entry in enumerate(entry_list):
			try:
				if "bad hash" in entry.name:
					print("Skipping", entry.name, entry.file_hash)
					continue
				if entry.ext not in ".mdl2.ms2.motiongraph.materialcollection":
					print("Skipping", entry.name, entry.file_hash)
					continue
				new_name = entry.name
				for old, new in name_tups:
					new_name = new_name.replace(old, new)
				if hasattr(entry, "file_hash"):
					new_hash = djb(new_name)
					old_hash_to_new[entry.file_hash] = (new_name, new_hash)
					old_hash_to_new_pz[e] = (new_name, new_hash)
					print(f"List{i} {entry.name} -> {new_name},  {entry.file_hash} ->  {new_hash}")
					entry.file_hash = new_hash
				else:
					print(f"List{i} {entry.name} -> {new_name},  [NOT HASHED]")
				entry.name = new_name
			except Exception as err:
				print(err)

	# we do this in a second step to resolve the links
	for i, entry_list in enumerate(ovs_lists):
		for entry in entry_list:
			if entry.ext not in ".mdl2.ms2.motiongraph.materialcollection":
				print("Skipping", entry.name, entry.file_hash)
				continue
			if ovl.user_version.is_jwe:
				new_name, new_hash = old_hash_to_new[entry.file_hash]
				entry.file_hash = new_hash
				entry.name = f"{new_name}{entry.ext}"
			else:
				new_name, new_hash = old_hash_to_new_pz[entry.file_hash]
				#entry.file_hash = new_hash
				entry.name = f"{new_name}{entry.ext}"
				
	# update the name buffer and offsets
	ovl.names.update_with((
		(ovl.dependencies, "ext"),
		(ovl.dirs, "name"),
		(ovl.mimes, "name"),
		(ovl.files, "name")
	))
	ovl.len_names = len(ovl.names.data)
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
                
#	if ovl.user_version.is_jwe:
	#	for old, new in name_tups:
	#		old_c = old
	#		new_c = new
	#		old_ch = hex(djb(old_c.lower()))
	#		new_ch = hex(djb(new_c.lower()))
	#	name_tups_new = [(old_ch,new_ch),]
 #       
#	try:
#		# hash the internal buffers
#		for archive_entry in ovl.archives:
#			ovs = archive_entry.content
#			for header_entry in ovs.header_entries:
#				b = header_entry.data.getvalue()
#				header_entry.data = io.BytesIO(replace_bytes(b, name_tups_new))
#			ovs.populate_pointers()
#			for buffer_entry in ovs.buffer_entries:
#				b = buffer_entry.data
#				buffer_entry.data = replace_bytes(b, name_tups_new)
#	except Exception as err:
#		print(err)
	print("Done!")
    
    
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
			#for buffer_entry in ovs.buffer_entries:
				#b = buffer_entry.data
				#buffer_entry.data = replace_bytes(b, name_tups)
	except Exception as err:
		print(err)
	print("Done!")
    
    
def species_dat_replacer(ovl, name_tups):
	print(f"Replacing Dat contents for {name_tups}")
	if ovl.user_version.is_jwe:
		for old, new in name_tups:
			old_a = old+"@"
			new_a = new+"@"
			old_b = old+"_Var"
			new_b = new+"_Var"
			old_c = old
			new_c = new
			old_ch = hex(djb(old_c.lower()))
			new_ch = hex(djb(new_c.lower()))
		name_tups_new = [(old_a,new_a),(old_b,new_b),(old_ch,new_ch)]
		name_tups_new2 = [(old_a,new_a),(old_b,new_b),(old_c,new_c),(old_ch,new_ch)]
	else:
		for old, new in name_tups:
			old_a = old+"@"
			new_a = new+"@"
			old_af = old+"_Female@"
			new_af = new+"_Female@"
			old_aj = old+"_Male@"
			new_aj = new+"_Male@"
			old_am = old+"_Juvenile@"
			new_am = new+"_Juvenile@"
            
			old_l0 = old+"_l0"
			new_l0 = new+"_l0"
			old_l0f = old+"_Female_l0"
			new_l0f = new+"_Female_l0"
			old_l0j = old+"_Male_l0"
			new_l0j = new+"_Male_l0"
			old_l0m = old+"_Juvenile_l0"
			new_l0m = new+"_Juvenile_l0"
			old_l0h = hex(djb(old_l0.lower()))
			new_l0h = hex(djb(new_l0.lower()))
			old_l0fh = hex(djb(old_l0f.lower()))
			new_l0fh = hex(djb(new_l0f.lower()))
			old_l0jh = hex(djb(old_l0j.lower()))
			new_l0jh = hex(djb(new_l0j.lower()))
			old_l0mh = hex(djb(old_l0m.lower()))
			new_l0mh = hex(djb(new_l0m.lower()))
            
			old_l1 = old+"_l1"
			new_l1 = new+"_l1"
			old_l1f = old+"_Female_l1"
			new_l1f = new+"_Female_l1"
			old_l1j = old+"_Male_l1"
			new_l1j = new+"_Male_l1"
			old_l1m = old+"_Juvenile_l1"
			new_l1m = new+"_Juvenile_l1"
			old_l1h = hex(djb(old_l1.lower()))
			new_l1h = hex(djb(new_l1.lower()))
			old_l1fh = hex(djb(old_l1f.lower()))
			new_l1fh = hex(djb(new_l1f.lower()))
			old_l1jh = hex(djb(old_l1j.lower()))
			new_l1jh = hex(djb(new_l1j.lower()))
			old_l1mh = hex(djb(old_l1m.lower()))
			new_l1mh = hex(djb(new_l1m.lower()))
            
			old_l2 = old+"_l2"
			new_l2 = new+"_l2"
			old_l2f = old+"_Female_l2"
			new_l2f = new+"_Female_l2"
			old_l2j = old+"_Male_l2"
			new_l2j = new+"_Male_l2"
			old_l2m = old+"_Juvenile_l2"
			new_l2m = new+"_Juvenile_l2"
			old_l2h = hex(djb(old_l2.lower()))
			new_l2h = hex(djb(new_l2.lower()))
			old_l2fh = hex(djb(old_l2f.lower()))
			new_l2fh = hex(djb(new_l2f.lower()))
			old_l2jh = hex(djb(old_l2j.lower()))
			new_l2jh = hex(djb(new_l2j.lower()))
			old_l2mh = hex(djb(old_l2m.lower()))
			new_l2mh = hex(djb(new_l2m.lower()))
            
			old_l3 = old+"_l3"
			new_l3 = new+"_l3"
			old_l3f = old+"_Female_l3"
			new_l3f = new+"_Female_l3"
			old_l3j = old+"_Male_l3"
			new_l3j = new+"_Male_l3"
			old_l3m = old+"_Juvenile_l3"
			new_l3m = new+"_Juvenile_l3"
			old_l3h = hex(djb(old_l3.lower()))
			new_l3h = hex(djb(new_l3.lower()))
			old_l3fh = hex(djb(old_l3f.lower()))
			new_l3fh = hex(djb(new_l3f.lower()))
			old_l3jh = hex(djb(old_l3j.lower()))
			new_l3jh = hex(djb(new_l3j.lower()))
			old_l3mh = hex(djb(old_l3m.lower()))
			new_l3mh = hex(djb(new_l3m.lower()))
            
			old_l4 = old+"_l4"
			new_l4 = new+"_l4"
			old_l4f = old+"_Female_l4"
			new_l4f = new+"_Female_l4"
			old_l4j = old+"_Male_l4"
			new_l4j = new+"_Male_l4"
			old_l4m = old+"_Juvenile_l4"
			new_l4m = new+"_Juvenile_l4"
			old_l4h = hex(djb(old_l4.lower()))
			new_l4h = hex(djb(new_l4.lower()))
			old_l4fh = hex(djb(old_l4f.lower()))
			new_l4fh = hex(djb(new_l4f.lower()))
			old_l4jh = hex(djb(old_l4j.lower()))
			new_l4jh = hex(djb(new_l4j.lower()))
			old_l4mh = hex(djb(old_l4m.lower()))
			new_l4mh = hex(djb(new_l4m.lower()))
            
			old_l5 = old+"_l5"
			new_l5 = new+"_l5"
			old_l5f = old+"_Female_l5"
			new_l5f = new+"_Female_l5"
			old_l5j = old+"_Male_l5"
			new_l5j = new+"_Male_l5"
			old_l5m = old+"_Juvenile_l5"
			new_l5m = new+"_Juvenile_l5"
			old_l5h = hex(djb(old_l5.lower()))
			new_l5h = hex(djb(new_l5.lower()))
			old_l5fh = hex(djb(old_l5f.lower()))
			new_l5fh = hex(djb(new_l5f.lower()))
			old_l5jh = hex(djb(old_l5j.lower()))
			new_l5jh = hex(djb(new_l5j.lower()))
			old_l5mh = hex(djb(old_l5m.lower()))
			new_l5mh = hex(djb(new_l5m.lower()))
            
			old_l6 = old+"_l6"
			new_l6 = new+"_l6"
			old_l6f = old+"_Female_l6"
			new_l6f = new+"_Female_l6"
			old_l6j = old+"_Male_l6"
			new_l6j = new+"_Male_l6"
			old_l6m = old+"_Juvenile_l6"
			new_l6m = new+"_Juvenile_l6"
			old_l6h = hex(djb(old_l6.lower()))
			new_l6h = hex(djb(new_l6.lower()))
			old_l6fh = hex(djb(old_l6f.lower()))
			new_l6fh = hex(djb(new_l6f.lower()))
			old_l6jh = hex(djb(old_l6j.lower()))
			new_l6jh = hex(djb(new_l6j.lower()))
			old_l6mh = hex(djb(old_l6m.lower()))
			new_l6mh = hex(djb(new_l6m.lower()))
            
			old_b = old+"_Mat"
			new_b = new+"_Mat"
			old_bf = old+"_Female_Mat"
			new_bf = new+"_Female_Mat"
			old_bj = old+"_Male_Mat"
			new_bj = new+"_Male_Mat"
			old_bm = old+"_Juvenile_Mat"
			new_bm = new+"_Juvenile_Mat"
			old_bh = hex(djb(old_b.lower()))
			new_bh = hex(djb(new_b.lower()))
			old_bfh = hex(djb(old_bf.lower()))
			new_bfh = hex(djb(new_bf.lower()))
			old_bjh = hex(djb(old_bj.lower()))
			new_bjh = hex(djb(new_bj.lower()))
			old_bmh = hex(djb(old_bm.lower()))
			new_bmh = hex(djb(new_bm.lower()))
            
			old_c = old+"_Skin"
			new_c = new+"_Skin"
			old_cf = old+"_Female_Skin"
			new_cf = new+"_Female_Skin"
			old_cj = old+"_Male_Skin"
			new_cj = new+"_Male_Skin"
			old_cm = old+"_Juvenile_Skin"
			new_cm = new+"_Juvenile_Skin"
			old_ch = hex(djb(old_c.lower()))
			new_ch = hex(djb(new_c.lower()))
			old_cfh = hex(djb(old_cf.lower()))
			new_cfh = hex(djb(new_cf.lower()))
			old_cjh = hex(djb(old_cj.lower()))
			new_cjh = hex(djb(new_cj.lower()))
			old_cmh = hex(djb(old_cm.lower()))
			new_cmh = hex(djb(new_cm.lower()))
            
			old_d = old+"_Skin_NoDirt"
			new_d = new+"_Skin_NoDirt"
			old_df = old+"_Female_Skin_NoDirt"
			new_df = new+"_Female_Skin_NoDirt"
			old_dj = old+"_Male_Skin_NoDirt"
			new_dj = new+"_Male_Skin_NoDirt"
			old_dm = old+"_Juvenile_Skin_NoDirt"
			new_dm = new+"_Juvenile_Skin_NoDirt"
			old_dh = hex(djb(old_d.lower()))
			new_dh = hex(djb(new_d.lower()))
			old_dfh = hex(djb(old_df.lower()))
			new_dfh = hex(djb(new_df.lower()))
			old_djh = hex(djb(old_dj.lower()))
			new_djh = hex(djb(new_dj.lower()))
			old_dmh = hex(djb(old_dm.lower()))
			new_dmh = hex(djb(new_dm.lower()))
            
			old_e = old+"_Fur"
			new_e = new+"_Fur"
			old_ef = old+"_Female_Fur"
			new_ef = new+"_Female_Fur"
			old_ej = old+"_Male_Fur"
			new_ej = new+"_Male_Fur"
			old_em = old+"_Juvenile_Fur"
			new_em = new+"_Juvenile_Fur"
			old_eh = hex(djb(old_e.lower()))
			new_eh = hex(djb(new_e.lower()))
			old_efh = hex(djb(old_ef.lower()))
			new_efh = hex(djb(new_ef.lower()))
			old_ejh = hex(djb(old_ej.lower()))
			new_ejh = hex(djb(new_ej.lower()))
			old_emh = hex(djb(old_em.lower()))
			new_emh = hex(djb(new_em.lower()))
            
			old_f = old+"_Fur_Shell"
			new_f = new+"_Fur_Shell"
			old_ff = old+"_Female_Fur_Shell"
			new_ff = new+"_Female_Fur_Shell"
			old_fj = old+"_Male_Fur_Shell"
			new_fj = new+"_Male_Fur_Shell"
			old_fm = old+"_Juvenile_Fur_Shell"
			new_fm = new+"_Juvenile_Fur_Shell"
			old_fh = hex(djb(old_f.lower()))
			new_fh = hex(djb(new_f.lower()))
			old_ffh = hex(djb(old_ff.lower()))
			new_ffh = hex(djb(new_ff.lower()))
			old_fjh = hex(djb(old_fj.lower()))
			new_fjh = hex(djb(new_fj.lower()))
			old_fmh = hex(djb(old_fm.lower()))
			new_fmh = hex(djb(new_fm.lower()))
            
			old_g = old+"_Fur_Fin"
			new_g = new+"_Fur_Fin"
			old_gf = old+"_Female_Fur_Fin"
			new_gf = new+"_Female_Fur_Fin"
			old_gj = old+"_Male_Fur_Fin"
			new_gj = new+"_Male_Fur_Fin"
			old_gm = old+"_Juvenile_Fur_Fin"
			new_gm = new+"_Juvenile_Fur_Fin"
			old_gh = hex(djb(old_g.lower()))
			new_gh = hex(djb(new_g.lower()))
			old_gfh = hex(djb(old_gf.lower()))
			new_gfh = hex(djb(new_gf.lower()))
			old_gjh = hex(djb(old_gj.lower()))
			new_gjh = hex(djb(new_gj.lower()))
			old_gmh = hex(djb(old_gm.lower()))
			new_gmh = hex(djb(new_gm.lower()))
            
			old_h = old+"_Eye"
			new_h = new+"_Eye"
			old_hf = old+"_Female_Eye"
			new_hf = new+"_Female_Eye"
			old_hj = old+"_Male_Eye"
			new_hj = new+"_Male_Eye"
			old_hm = old+"_Juvenile_Eye"
			new_hm = new+"_Juvenile_Eye"
			old_hh = hex(djb(old_h.lower()))
			new_hh = hex(djb(new_h.lower()))
			old_hfh = hex(djb(old_hf.lower()))
			new_hfh = hex(djb(new_hf.lower()))
			old_hjh = hex(djb(old_hj.lower()))
			new_hjh = hex(djb(new_hj.lower()))
			old_hmh = hex(djb(old_hm.lower()))
			new_hmh = hex(djb(new_hm.lower()))
            
			old_j = old+"_Eyes"
			new_j = new+"_Eyes"
			old_jf = old+"_Female_Eyes"
			new_jf = new+"_Female_Eyes"
			old_jj = old+"_Male_Eyes"
			new_jj = new+"_Male_Eyes"
			old_jm = old+"_Juvenile_Eyes"
			new_jm = new+"_Juvenile_Eyes"
			old_jh = hex(djb(old_j.lower()))
			new_jh = hex(djb(new_j.lower()))
			old_jfh = hex(djb(old_jf.lower()))
			new_jfh = hex(djb(new_jf.lower()))
			old_jjh = hex(djb(old_jj.lower()))
			new_jjh = hex(djb(new_jj.lower()))
			old_jmh = hex(djb(old_jm.lower()))
			new_jmh = hex(djb(new_jm.lower()))
            
			old_i = old+"_Eyeball"
			new_i = new+"_Eyeball"
			old_if = old+"_Female_Eyeball"
			new_if = new+"_Female_Eyeball"
			old_ij = old+"_Male_Eyeball"
			new_ij = new+"_Male_Eyeball"
			old_im = old+"_Juvenile_Eyeball"
			new_im = new+"_Juvenile_Eyeball"
			old_ih = hex(djb(old_i.lower()))
			new_ih = hex(djb(new_i.lower()))
			old_ifh = hex(djb(old_if.lower()))
			new_ifh = hex(djb(new_if.lower()))
			old_ijh = hex(djb(old_ij.lower()))
			new_ijh = hex(djb(new_ij.lower()))
			old_imh = hex(djb(old_im.lower()))
			new_imh = hex(djb(new_im.lower()))

			old_k = old+"_EyeMouthClaws"
			new_k = new+"_EyeMouthClaws"
			old_kf = old+"_Female_EyeMouthClaws"
			new_kf = new+"_Female_EyeMouthClaws"
			old_kj = old+"_Male_EyeMouthClaws"
			new_kj = new+"_Male_EyeMouthClaws"
			old_km = old+"_Juvenile_EyeMouthClaws"
			new_km = new+"_Juvenile_EyeMouthClaws"
			old_kh = hex(djb(old_k.lower()))
			new_kh = hex(djb(new_k.lower()))
			old_kfh = hex(djb(old_kf.lower()))
			new_kfh = hex(djb(new_kf.lower()))
			old_kjh = hex(djb(old_kj.lower()))
			new_kjh = hex(djb(new_kj.lower()))
			old_kmh = hex(djb(old_km.lower()))
			new_kmh = hex(djb(new_km.lower()))
            
			old_l = old+"_Whiskers"
			new_l = new+"_Whiskers"
			old_lf = old+"_Female_Whiskers"
			new_lf = new+"_Female_Whiskers"
			old_lj = old+"_Male_Whiskers"
			new_lj = new+"_Male_Whiskers"
			old_lm = old+"_Juvenile_Whiskers"
			new_lm = new+"_Juvenile_Whiskers"
			old_lh = hex(djb(old_l.lower()))
			new_lh = hex(djb(new_l.lower()))
			old_lfh = hex(djb(old_lf.lower()))
			new_lfh = hex(djb(new_lf.lower()))
			old_ljh = hex(djb(old_lj.lower()))
			new_ljh = hex(djb(new_lj.lower()))
			old_lmh = hex(djb(old_lm.lower()))
			new_lmh = hex(djb(new_lm.lower()))
            
			old_m = old+"_Hair"
			new_m = new+"_Hair"
			old_mf = old+"_Female_Hair"
			new_mf = new+"_Female_Hair"
			old_mj = old+"_Male_Hair"
			new_mj = new+"_Male_Hair"
			old_mm = old+"_Juvenile_Hair"
			new_mm = new+"_Juvenile_Hair"
			old_mh = hex(djb(old_m.lower()))
			new_mh = hex(djb(new_m.lower()))
			old_mfh = hex(djb(old_mf.lower()))
			new_mfh = hex(djb(new_mf.lower()))
			old_mjh = hex(djb(old_mj.lower()))
			new_mjh = hex(djb(new_mj.lower()))
			old_mmh = hex(djb(old_mm.lower()))
			new_mmh = hex(djb(new_mm.lower()))
            
            
			old_n = old+"_Feathers"
			new_n = new+"_Feathers"
			old_nf = old+"_Female_Feathers"
			new_nf = new+"_Female_Feathers"
			old_nj = old+"_Male_Feathers"
			new_nj = new+"_Male_Feathers"
			old_nm = old+"_Juvenile_Feathers"
			new_nm = new+"_Juvenile_Feathers" 
			old_nh = hex(djb(old_n.lower()))
			new_nh = hex(djb(new_n.lower()))
			old_nfh = hex(djb(old_nf.lower()))
			new_nfh = hex(djb(new_nf.lower()))
			old_njh = hex(djb(old_nj.lower()))
			new_njh = hex(djb(new_nj.lower()))
			old_nmh = hex(djb(old_nm.lower()))
			new_nmh = hex(djb(new_nm.lower()))
            
            
            
		name_tups_new = [(old_a,new_a),(old_af,new_af),(old_aj,new_aj),(old_am,new_am),
            (old_l0,new_l0),(old_l0f,new_l0f),(old_l0j,new_l0j),(old_l0m,new_l0m),(old_l0h,new_l0h),(old_l0fh,new_l0fh),(old_l0jh,new_l0jh),(old_l0mh,new_l0mh),
            (old_l1,new_l1),(old_l1f,new_l1f),(old_l1j,new_l1j),(old_l1m,new_l1m),(old_l1h,new_l1h),(old_l1fh,new_l1fh),(old_l1jh,new_l1jh),(old_l1mh,new_l1mh),
            (old_l2,new_l2),(old_l2f,new_l2f),(old_l2j,new_l2j),(old_l2m,new_l2m),(old_l2h,new_l2h),(old_l2fh,new_l2fh),(old_l2jh,new_l2jh),(old_l2mh,new_l2mh),
            (old_l3,new_l3),(old_l3f,new_l3f),(old_l3j,new_l3j),(old_l3m,new_l3m),(old_l3h,new_l3h),(old_l3fh,new_l3fh),(old_l3jh,new_l3jh),(old_l3mh,new_l3mh),
            (old_l4,new_l4),(old_l4f,new_l4f),(old_l4j,new_l4j),(old_l4m,new_l4m),(old_l4h,new_l4h),(old_l4fh,new_l4fh),(old_l4jh,new_l4jh),(old_l4mh,new_l4mh),
            (old_l5,new_l5),(old_l5f,new_l5f),(old_l5j,new_l5j),(old_l5m,new_l5m),(old_l5h,new_l5h),(old_l5fh,new_l5fh),(old_l5jh,new_l5jh),(old_l5mh,new_l5mh),
            (old_l6,new_l6),(old_l6f,new_l6f),(old_l6j,new_l6j),(old_l6m,new_l6m),(old_l6h,new_l6h),(old_l6fh,new_l6fh),(old_l6jh,new_l6jh),(old_l6mh,new_l6mh),
            (old_b,new_b),(old_bf,new_bf),(old_bj,new_bj),(old_bm,new_bm),(old_bh,new_bh),(old_bfh,new_bfh),(old_bjh,new_bjh),(old_bmh,new_bmh),
            (old_c,new_c),(old_cf,new_cf),(old_cj,new_cj),(old_cm,new_cm),(old_ch,new_ch),(old_cfh,new_cfh),(old_cjh,new_cjh),(old_cmh,new_cmh),
            (old_d,new_d),(old_df,new_df),(old_dj,new_dj),(old_dm,new_dm),(old_dh,new_dh),(old_dfh,new_dfh),(old_djh,new_djh),(old_dmh,new_dmh),
            (old_e,new_e),(old_ef,new_ef),(old_ej,new_ej),(old_em,new_em),(old_eh,new_eh),(old_efh,new_efh),(old_ejh,new_ejh),(old_emh,new_emh),
            (old_f,new_f),(old_ff,new_ff),(old_fj,new_fj),(old_fm,new_fm),(old_fh,new_fh),(old_ffh,new_ffh),(old_fjh,new_fjh),(old_fmh,new_fmh),
            (old_g,new_g),(old_gf,new_gf),(old_gj,new_gj),(old_gm,new_gm),(old_gh,new_gh),(old_gfh,new_gfh),(old_gjh,new_gjh),(old_gmh,new_gmh),
            (old_h,new_h),(old_hf,new_hf),(old_hj,new_hj),(old_hm,new_hm),(old_hh,new_hh),(old_hfh,new_hfh),(old_hjh,new_hjh),(old_hmh,new_hmh),
            (old_i,new_i),(old_if,new_if),(old_ij,new_ij),(old_im,new_im),(old_ih,new_ih),(old_ifh,new_ifh),(old_ijh,new_ijh),(old_imh,new_imh),
            (old_j,new_j),(old_jf,new_jf),(old_jj,new_jj),(old_jm,new_jm),(old_jh,new_jh),(old_jfh,new_jfh),(old_jjh,new_jjh),(old_jmh,new_jmh),
            (old_k,new_k),(old_kf,new_kf),(old_kj,new_kj),(old_km,new_km),(old_kh,new_kh),(old_kfh,new_kfh),(old_kjh,new_kjh),(old_kmh,new_kmh),
            (old_l,new_l),(old_lf,new_lf),(old_lj,new_lj),(old_lm,new_lm),(old_lh,new_lh),(old_lfh,new_lfh),(old_ljh,new_ljh),(old_lmh,new_lmh),
            (old_m,new_m),(old_mf,new_mf),(old_mj,new_mj),(old_mm,new_mm),(old_mh,new_mh),(old_mfh,new_mfh),(old_mjh,new_mjh),(old_mmh,new_mmh),
            (old_n,new_n),(old_nf,new_nf),(old_nj,new_nj),(old_nm,new_nm),(old_nh,new_nh),(old_nfh,new_nfh),(old_njh,new_njh),(old_nmh,new_nmh)]
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
				old = bytes.fromhex("0"+old[2:])[::-1]
			elif len(old[2:]) == 6:
				old = bytes.fromhex("00"+old[2:])[::-1]
			if len(new[2:]) == 8:
				new = bytes.fromhex(new[2:])[::-1]
			elif len(new[2:]) == 7:
				new = bytes.fromhex("0"+new[2:])[::-1]
			elif len(new[2:]) == 6:
				new = bytes.fromhex("00"+new[2:])[::-1]
		else:
			old = old.encode(encoding="utf-8")
			new = new.encode(encoding="utf-8")
		print(old, new)
		if len(old) != len(new):
			print(f"WARNING: length of {old} and {new} don't match!")
		b = b.replace(old, new)
	return b
