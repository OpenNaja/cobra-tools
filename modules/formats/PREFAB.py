import struct

from modules.formats.shared import get_padding
from modules.formats.BaseFormat import BaseFile
from modules.helpers import zstr
from hashes import specdefs_jwe

class PrefabLoader(BaseFile):
	def prefab_unpack_temp(self, len, data):
		if len % 4 != 0:
			ret = data
		elif len >= 50:
			num = int(len / 4)
			strr = "<" + str(num) + "I"
			ret = struct.unpack(strr, data)
		else:
			num = int(len / 4)
			strr = "<" + str(num) + "I"
			ret = struct.unpack(strr, data)
		return ret	
	def prefab_unpack_temp2(self, len, data):
		if len % 8 != 0:
			ret = data
		else:
			num = int(len / 8)
			strr = "<" + str(num) + "Q"
			ret = struct.unpack(strr, data)
		return ret
        
        
	def prefab_unpack_gub(self, len, data):
		num = int(len / 1)
		strr = "<" + str(num) + "B"
		ret = struct.unpack(strr, data)
		return ret
        
	def specdef_thing(self, countt, data):
		if isinstance(data, int):
        
			return data
		else:
			return countt
            
	def prefab_unpack_ss(self, len, data):
		num = int(len)
		strr = "<" + str(num) + "B"
		ret = struct.unpack(strr, data)
		return ret
        
	def prefab_unpack_dtype(self, dtype, tflags):
		try:
			if dtype == 0:
				# boot on the second byte, todo maybe more
				tflag = struct.unpack("4BI", tflags[:16])
				bool0 = bool(tflag[0])
				bool1 = bool(tflag[1])
				tflags = [bool0,bool1]
			elif dtype == 3:
				# int16
				tflags = struct.unpack("4i", tflags[:16])
				#tflags = struct.unpack("8h", tflags[:16])
			elif dtype == 5:
				# lower_bound, upper_bound, int, 1
				tflags = struct.unpack("4bI", tflags[:8])
			elif dtype == 6:
				# lower_bound, upper_bound, int, 1
				tflags = struct.unpack("4BI", tflags[:8])
			elif dtype == 7:
				# 0, 0, count, 0 (padding?)
				tflags = struct.unpack("4I", tflags[:16])
			elif dtype == 9:
				# lower_bound, upper_bound, float, 1
				tflags = struct.unpack("3fI", tflags[:16])
			elif dtype == 10:
				# 0, 0, 1, 0 (padding?)
				tflags = struct.unpack("4I", tflags[:16])
			elif dtype == 11:
				# vector2 float, 1, 0 (padding?)
				tflags = struct.unpack("2fII", tflags[:16])
			elif dtype == 12:
				# vector3 float, 1
				tflags = struct.unpack("3fI", tflags[:16])
			elif dtype == 13:
				# 0, 0, count, 0 (padding?)
				tflags = struct.unpack("4I", tflags[:16])
			elif dtype == 15:
				# 0, 0, count, 0 (padding?)
				tflags = struct.unpack("4I", tflags[:16])
		except:
			logging.warning(f"Unexpected data {tflags} (size: {len(tflags)}) for type {dtype}")
		return tflags
        
	def extract(self, out_dir, show_temp_files, progress_callback):
		name = self.sized_str_entry.name
		n = name.replace("/"," ")
		print(f"\nWriting {n}")
        
		ovl_header = self.pack_header(b"PREFAB")
		out_path = out_dir(n)
        
		with open(out_path + ".bin", 'wb') as outfile:
			print("Exporting binary prefab file")
			outfile.write(ovl_header)
			outfile.write(self.sized_str_entry.pointers[0].data)
			for f in self.sized_str_entry.fragments:
				outfile.write(f.pointers[0].data)
				outfile.write(f.pointers[1].data)
			outfile.close()
            
		with open(out_path, 'w') as outfile:
			print("Exporting prefab file")
			outfile.write(self.sized_str_entry.name+"\n")
			ss_entry = self.sized_str_entry
			ssdata = self.prefab_unpack_ss(len(ss_entry.pointers[0].data), ss_entry.pointers[0].data)
			outfile.write(f"Number of Components: {ssdata[4]}\nNumber of Children: {ssdata[6]}\nNumber of Properties: {len(ss_entry.specdef_attr_names)}\n{{\n")

			outfile.write(f"        Components = {{\n")
			if ssdata[4] > 0:
				for frag in ss_entry.specdef_name_fragments:
					name = frag.pointers[1].data.rstrip(b'\x00').decode("utf-8") 
					#print(name)
					outfile.write(f"                {name} {{\n")
					for i, data_frag in enumerate(frag.data_frags):
						outfile.write(f"                    data_frag_{i} p0: {data_frag.pointers[0].data},\n")
						outfile.write(f"                    data_frag_{i} p1: {data_frag.pointers[1].data},\n")
					outfile.write(f"                }},\n")
			outfile.write(f"        }},\n")
            
            
			outfile.write(f"        Children = {{\n")
			if ssdata[6] > 0:
				for frag in ss_entry.prefab_children:
					name = frag.pointers[1].data.rstrip(b'\x00').decode("utf-8") 
					#print(name)
					outfile.write(f"                {name},\n")
			outfile.write(f"        }},\n")
            
			outfile.write(f"        Properties = {{\n")
			if len(ss_entry.specdef_attr_names) > 0:
				property_types = self.prefab_unpack_temp(len(ss_entry.specdef_attr_types[0].pointers[1].data),ss_entry.specdef_attr_types[0].pointers[1].data)
				for i, frag in enumerate(ss_entry.specdef_attr_names):
					name = frag.pointers[1].data.rstrip(b'\x00').decode("utf-8") 
					#print(name)
					outfile.write(f"                {name} {{\n")
					outfile.write(f"                        Type = {property_types[i]},\n")
					data = self.prefab_unpack_dtype(property_types[i], ss_entry.specdef_attr_datas[i].pointers[1].data)
					outfile.write(f"                        Data = {data},\n")
					for entry in ss_entry.specdef_attr_datas[i].child_datas:
						if property_types[i] == 10:
							outfile.write(f"                            Child Data = '"+entry.pointers[1].data.rstrip(b'\x00').decode('utf-8')+"',\n")
						elif property_types[i] == 13:
							outfile.write(f"                            Child Data = {self.prefab_unpack_dtype(data[2], entry.pointers[1].data)},\n")
						elif property_types[i] == 15:
							outfile.write(f"                            Child Data = '"+entry.pointers[1].data.rstrip(b'\x00').decode('utf-8')+"',\n")
						else:
							outfile.write(f"                            Child Data = {entry.pointers[1].data},\n")
                    

                
					outfile.write(f"                }},\n")
			outfile.write(f"        }},\n") 
            
			outfile.write(f"        {self.prefab_unpack_temp2(len(ss_entry.specdef_attr_types[3].pointers[1].data),ss_entry.specdef_attr_types[3].pointers[1].data)}{{\n")
			outfile.write(f"        Other = {{\n")
			for frag in ss_entry.specdef_other_list:
				outfile.write(f"                {self.prefab_unpack_temp(len(frag.pointers[0].data),frag.pointers[0].data)},\n")
				outfile.write(f"                {self.prefab_unpack_gub(len(frag.pointers[1].data),frag.pointers[1].data)},\n")
				outfile.write(f"                ---------\n")
				for f in frag.other_datas:
					outfile.write(f"                {self.prefab_unpack_gub(len(f.pointers[0].data),f.pointers[0].data)},\n")
					outfile.write(f"                {self.prefab_unpack_gub(len(f.pointers[1].data),f.pointers[1].data)},\n")
				outfile.write(f"                ---------\n\n")
			outfile.write(f"        }},\n")
           
			outfile.write(f"}}")
			#for f in self.sized_str_entry.fragments:
				#outfile.write(f.pointers[0].data)
				#outfile.write(f.pointers[1].data)
			outfile.close()
            
		return out_path + ".bin", out_path,
        
	def collect(self,):
		self.assign_ss_entry()
		#return
		ss_entry = self.sized_str_entry
		att_type_dict = [0,0,0,0,0,0,0,0,0,0,1,0,0,1,0,1,0,0,0]
		att_type_dict2 = [0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0]
		ssdata = self.prefab_unpack_ss(len(ss_entry.pointers[0].data), ss_entry.pointers[0].data)
		print("\nPREFAB:", ss_entry.name)
		print(ssdata)
		ss_entry.fragments = self.ovs.frags_accumulate_from_pointer_till_count(ss_entry.pointers[0], 88-len(ss_entry.pointers[0].data), 7)
		init_frag_count = len(ss_entry.fragments)
		has_properties = False
		has_components = False
		has_children = False
		fug = []
		if (ssdata[4] != 0) and (ssdata[6] == 0):
			print("has components but no children")
			component_name_frag = 0
			component_data_frag = 2
			has_components = True
            
			if init_frag_count == 5:
				has_properties = True
				print("has properties")
            
		elif (ssdata[4] != 0) and (ssdata[6] != 0):
			print("has components and children")
			component_name_frag = 0
			component_data_frag = 2
			child_frag = 4
			has_components = True
			has_children = True
            
			if init_frag_count == 7:
				has_properties = True
				print("has properties")
            
		elif (ssdata[4] == 0) and (ssdata[6] != 0):
			print("has children but no components")
			has_children = True
			child_frag = 1
            
			if init_frag_count == 4:
				has_properties = True
				print("has properties")
            
		else:
			print("has no components and no children")
            
            
		if has_components == True:
			ss_entry.specdef_name_fragments += self.ovs.frags_from_pointer(ss_entry.fragments[component_name_frag].pointers[1], ssdata[4])
			for i, entry in enumerate(ss_entry.specdef_name_fragments):
				entry.data_frags = []
			ss_entry.fragments += ss_entry.specdef_name_fragments
			for name_frag in ss_entry.specdef_name_fragments:
				if name_frag.pointers[1].data.rstrip(b'\x00') in specdefs_jwe.jwe_specdefs:
					print(name_frag.pointers[1].data.rstrip(b'\x00'))
					specdef_frag_counts = specdefs_jwe.jwe_specdefs[name_frag.pointers[1].data.rstrip(b'\x00')]
					print(specdef_frag_counts)
					if specdef_frag_counts[0] != 0:
						name_frag.data_frags.extend(self.ovs.frags_from_pointer(ss_entry.fragments[component_data_frag].pointers[1], specdef_frag_counts[0]))
						if len(name_frag.data_frags[0].pointers[1].data) >= 16:
							countt = self.prefab_unpack_temp(len(name_frag.data_frags[0].pointers[1].data), name_frag.data_frags[0].pointers[1].data)[2]   




                            
					if b'AssetPackageLoader' == name_frag.pointers[1].data.rstrip(b'\x00'):
						check = self.prefab_unpack_temp(len(name_frag.data_frags[0].pointers[1].data),
										name_frag.data_frags[0].pointers[1].data)[2] 
						lenn = len(name_frag.data_frags[0].pointers[1].data)
						print("AssetPackageLoader has : "+str(check))
                        
						if check > 0:
                        
							if lenn == 16:
								name_frag.data_frags.extend(self.ovs.frags_from_pointer(name_frag.data_frags[0].pointers[1], 2))
								for i in range(2):
									ccc = self.prefab_unpack_temp(len(name_frag.data_frags[i+1].pointers[0].data),name_frag.data_frags[i+1].pointers[0].data)[2]
									name_frag.data_frags.extend(self.ovs.frags_from_pointer(name_frag.data_frags[i+1].pointers[1], ccc))
							elif lenn == 32:
								name_frag.data_frags.extend(self.ovs.frags_from_pointer(name_frag.data_frags[0].pointers[1], 1))
								ccc = self.prefab_unpack_temp(len(name_frag.data_frags[1].pointers[0].data),name_frag.data_frags[1].pointers[0].data)[2]
								name_frag.data_frags.extend(self.ovs.frags_from_pointer(name_frag.data_frags[1].pointers[1], ccc))
                                
                                
					elif b'AudioDinosaurCore' == name_frag.pointers[1].data.rstrip(b'\x00'):
						check = self.prefab_unpack_temp(len(name_frag.data_frags[0].pointers[1].data),
										name_frag.data_frags[0].pointers[1].data)[2] 
						print("AudioDinosaurCore has : "+str(check))
						name_frag.data_frags.extend(self.ovs.frags_from_pointer(name_frag.data_frags[0].pointers[1], 2))
						if len(name_frag.data_frags[2].pointers[0].data) != 32:
							#print("len len ",len(name_frag.data_frags[2].pointers[0].data))
							name_frag.data_frags.extend(self.ovs.frags_from_pointer(name_frag.data_frags[0].pointers[1], 2))
					elif b'IKFootPlant' == name_frag.pointers[1].data.rstrip(b'\x00'):  
						if len(name_frag.data_frags[0].pointers[1].data) == 16:
							name_frag.data_frags.extend(self.ovs.frags_from_pointer(name_frag.data_frags[0].pointers[1], 3))
							name_frag.data_frags.extend(self.ovs.frags_from_pointer(name_frag.data_frags[1].pointers[1], self.specdef_thing(countt,specdef_frag_counts[2])))
							name_frag.data_frags.extend(self.ovs.frags_from_pointer(name_frag.data_frags[2].pointers[1], 1))
							name_frag.data_frags.extend(self.ovs.frags_from_pointer(name_frag.data_frags[3].pointers[1], specdef_frag_counts[3]))
                            
						else:
							name_frag.data_frags.extend(self.ovs.frags_from_pointer(name_frag.data_frags[0].pointers[1], 2))
							name_frag.data_frags.extend(self.ovs.frags_from_pointer(name_frag.data_frags[1].pointers[1], self.specdef_thing(countt,specdef_frag_counts[2])))
							name_frag.data_frags.extend(self.ovs.frags_from_pointer(name_frag.data_frags[2].pointers[1], specdef_frag_counts[3]))
                            
					elif len(specdef_frag_counts) == 2:
						name_frag.data_frags.extend(self.ovs.frags_from_pointer(name_frag.data_frags[0].pointers[1], specdef_frag_counts[1]))
					elif len(specdef_frag_counts) == 3:
						name_frag.data_frags.extend(self.ovs.frags_from_pointer(name_frag.data_frags[0].pointers[1], specdef_frag_counts[1]))
						name_frag.data_frags.extend(self.ovs.frags_from_pointer(name_frag.data_frags[1].pointers[1], self.specdef_thing(countt,specdef_frag_counts[2])))
					elif len(specdef_frag_counts) == 4:

						name_frag.data_frags.extend(self.ovs.frags_from_pointer(name_frag.data_frags[0].pointers[1], specdef_frag_counts[1]))
						name_frag.data_frags.extend(self.ovs.frags_from_pointer(name_frag.data_frags[1].pointers[1], self.specdef_thing(countt,specdef_frag_counts[2])))
						name_frag.data_frags.extend(self.ovs.frags_from_pointer(name_frag.data_frags[2].pointers[1], specdef_frag_counts[3]))
                        
					elif len(specdef_frag_counts) == 5:
						name_frag.data_frags.extend(self.ovs.frags_from_pointer(name_frag.data_frags[0].pointers[1], specdef_frag_counts[1]))
						county = self.prefab_unpack_temp(len(name_frag.data_frags[2].pointers[0].data),name_frag.data_frags[2].pointers[0].data)[2]
						name_frag.data_frags.extend(self.ovs.frags_from_pointer(name_frag.data_frags[1].pointers[1], specdef_frag_counts[2]))
						name_frag.data_frags.extend(self.ovs.frags_from_pointer(name_frag.data_frags[2].pointers[1], self.specdef_thing(county,specdef_frag_counts[3])))
						name_frag.data_frags.extend(self.ovs.frags_from_pointer(name_frag.data_frags[3].pointers[1], specdef_frag_counts[4]))
                        
					ss_entry.fragments += name_frag.data_frags
                    
		if has_children == True:
			ss_entry.prefab_children = []
			ss_entry.prefab_children.extend(self.ovs.frags_from_pointer(ss_entry.fragments[child_frag].pointers[1], ssdata[6]))
			ss_entry.fragments += ss_entry.prefab_children
            
		if has_properties == True:
			gub = ss_entry.fragments[init_frag_count-1]
			fug += self.ovs.frags_from_pointer_equalsb_counts(gub.pointers[1], 5) #attr types, attr names, attr datas, list of some ints, list of short-like things
			#print(gub)
			ss_entry.fragments += fug
			gub_d1 = self.prefab_unpack_gub(len(gub.pointers[1].data), gub.pointers[1].data)
			fug0_d1 = self.prefab_unpack_temp(len(fug[0].pointers[1].data), fug[0].pointers[1].data)
			fug1_d1 = self.prefab_unpack_temp(len(fug[1].pointers[1].data), fug[1].pointers[1].data)
			fug2_d1 = self.prefab_unpack_temp(len(fug[2].pointers[1].data), fug[2].pointers[1].data)
			fug3_d1 = self.prefab_unpack_temp2(len(fug[3].pointers[1].data), fug[3].pointers[1].data)
			fug4_d1 = self.prefab_unpack_temp(len(fug[4].pointers[1].data), fug[4].pointers[1].data)

			ss_entry.specdef_attr_types = [fug[0],fug[1],fug[2],fug[3],fug[4]]
			ss_entry.specdef_attr_names += self.ovs.frags_from_pointer_equalsb_counts(fug[1].pointers[1], gub_d1[0])
			ss_entry.specdef_attr_datas += self.ovs.frags_from_pointer_equalsb_counts(fug[2].pointers[1], gub_d1[0])
			for entry in ss_entry.specdef_attr_datas:
				entry.child_datas = []
			ss_entry.fragments += ss_entry.specdef_attr_names
			ss_entry.fragments += ss_entry.specdef_attr_datas
			cc = 0
			for i, entry in enumerate(ss_entry.specdef_attr_datas):
				count = att_type_dict[fug0_d1[i]]
				count2 = att_type_dict2[fug0_d1[i]]
				cc+=count2
				entry.child_datas.extend(self.ovs.frags_from_pointer(entry.pointers[1],count))
				ss_entry.fragments += entry.child_datas
				ss_entry.specdef_other_list.extend(self.ovs.frags_from_pointer(fug[4].pointers[1], count2))
			if cc == 0:
				ss_entry.specdef_other_list.extend(self.ovs.frags_from_pointer(fug[4].pointers[1], 1))

                
                
				
			for i, entry in enumerate(ss_entry.specdef_other_list):
				entry.other_datas = []
			ss_entry.fragments += ss_entry.specdef_other_list
                
			for frag in ss_entry.specdef_other_list:
				count = self.prefab_unpack_temp(len(frag.pointers[0].data), frag.pointers[0].data)
				frag.other_datas.extend(self.ovs.frags_from_pointer_equalsb_counts(frag.pointers[1], count[2]))
				ss_entry.fragments += frag.other_datas
            
        

	
		try:
			print("gub", gub_d1)
			print("fug0", fug0_d1)
			print("fug1", fug1_d1)
			print("fug2", fug2_d1)
			print("fug3", fug3_d1)
			print("fug4", fug4_d1)
		except:
			print("no gub")

                    
