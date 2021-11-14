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
        
	def prefab_unpack_gub(self, len, data):
		if len % 4 != 0:
			ret = data
		else:
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
            
		return out_path + ".bin", #out_path,
        
	def collect(self,):
		self.assign_ss_entry()
		ss_entry = self.sized_str_entry
        
        
		att_type_dict = [0,0,0,0,0,0,0,0,0,0,1,0,0,1,0,1,0,0,0]
		att_type_dict2 = [0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0]
        
        
		ssdata = self.prefab_unpack_ss(len(ss_entry.pointers[0].data), ss_entry.pointers[0].data)
		print("\nPREFAB:", ss_entry.name)
		print(ssdata)
		gub = []
		fug = []

		if (ssdata[4] == 0) and (ssdata[6] == 0):
			ss_entry.fragments = self.ovs.frags_from_pointer(ss_entry.pointers[0], 1)
		elif (ssdata[4] != 0) and (ssdata[6] == 0):
			ss_entry.fragments = self.ovs.frags_from_pointer(ss_entry.pointers[0], 4)
			f3_d0 = self.prefab_unpack_temp(len(ss_entry.fragments[3].pointers[0].data),
											ss_entry.fragments[3].pointers[0].data)
			f2_d0 = self.prefab_unpack_temp(len(ss_entry.fragments[2].pointers[0].data),
											ss_entry.fragments[2].pointers[0].data)
		elif (ssdata[4] == 0) and (ssdata[6] != 0):
			ss_entry.fragments = self.ovs.frags_from_pointer(ss_entry.pointers[0], 3)
			f3_d0 = self.prefab_unpack_temp(len(ss_entry.fragments[2].pointers[0].data),
											ss_entry.fragments[2].pointers[0].data)
			f2_d0 = self.prefab_unpack_temp(len(ss_entry.fragments[2].pointers[0].data),
										ss_entry.fragments[2].pointers[0].data)
		elif (ssdata[4] != 0) and (ssdata[6] != 0):
			ss_entry.fragments = self.ovs.frags_from_pointer(ss_entry.pointers[0], 6)
			f5_d0 = self.prefab_unpack_temp(len(ss_entry.fragments[5].pointers[0].data),
											ss_entry.fragments[5].pointers[0].data)
			f2_d0 = self.prefab_unpack_temp(len(ss_entry.fragments[2].pointers[0].data),
											ss_entry.fragments[2].pointers[0].data)
		else:
			ss_entry.fragments = self.ovs.frags_from_pointer(ss_entry.pointers[0], 1)

        
                
		if (ssdata[4] != 0) and (ssdata[6] == 0):
			if len(ss_entry.fragments[3].pointers[0].data) != 40:
				gub = self.ovs.frags_from_pointer(ss_entry.pointers[0], 1)
				ss_entry.fragments += gub

			ss_entry.specdef_name_fragments += self.ovs.frags_from_pointer(ss_entry.fragments[0].pointers[1], ssdata[4])
			for i, entry in enumerate(ss_entry.specdef_name_fragments):
				entry.data_frags = []
			ss_entry.fragments += ss_entry.specdef_name_fragments
            
			for name_frag in ss_entry.specdef_name_fragments:
            
				if name_frag.pointers[1].data.rstrip(b'\x00') in specdefs_jwe.jwe_specdefs:
                
					print(name_frag.pointers[1].data.rstrip(b'\x00'))
					specdef_frag_counts = specdefs_jwe.jwe_specdefs[name_frag.pointers[1].data.rstrip(b'\x00')]
					print(specdef_frag_counts)
					if specdef_frag_counts[0] != 0:
						name_frag.data_frags.extend(self.ovs.frags_from_pointer(ss_entry.fragments[2].pointers[1], specdef_frag_counts[0]))
						if len(name_frag.data_frags[0].pointers[1].data) >= 16:
							countt = self.prefab_unpack_temp(len(name_frag.data_frags[0].pointers[1].data),
											name_frag.data_frags[0].pointers[1].data)[2]
					if b'AssetPackageLoader' == name_frag.pointers[1].data.rstrip(b'\x00'):
						check = self.prefab_unpack_temp(len(name_frag.data_frags[0].pointers[1].data),
										name_frag.data_frags[0].pointers[1].data)[2] 
						print("AssetPackageLoader has : "+str(check))
						name_frag.data_frags.extend(self.ovs.frags_from_pointer(name_frag.data_frags[0].pointers[1], check+1))
						for i in range(check+1):
							name_frag.data_frags.extend(self.ovs.frags_from_pointer(name_frag.data_frags[i+1].pointers[1], 1))
					elif b'AudioDinosaurCore' == name_frag.pointers[1].data.rstrip(b'\x00'):
						check = self.prefab_unpack_temp(len(name_frag.data_frags[0].pointers[1].data),
										name_frag.data_frags[0].pointers[1].data)[2] 
						print("AudioDinosaurCore has : "+str(check))
						name_frag.data_frags.extend(self.ovs.frags_from_pointer(name_frag.data_frags[0].pointers[1], 2))
						if len(name_frag.data_frags[2].pointers[0].data) != 32:
							print("len len ",len(name_frag.data_frags[2].pointers[0].data))
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
                    
			if len(ss_entry.fragments[3].pointers[0].data) != 40:
				fug += self.ovs.frags_from_pointer_equalsb_counts(gub[0].pointers[1], 5)
				ss_entry.fragments += fug
				gub_d1 = self.prefab_unpack_gub(len(gub[0].pointers[1].data), gub[0].pointers[1].data)
				fug0_d1 = self.prefab_unpack_temp(len(fug[0].pointers[1].data), fug[0].pointers[1].data)
				fug1_d1 = self.prefab_unpack_temp(len(fug[1].pointers[1].data), fug[1].pointers[1].data)
				fug2_d1 = self.prefab_unpack_temp(len(fug[2].pointers[1].data), fug[2].pointers[1].data)
				fug3_d1 = self.prefab_unpack_temp(len(fug[3].pointers[1].data), fug[3].pointers[1].data)
				fug4_d1 = self.prefab_unpack_temp(len(fug[4].pointers[1].data), fug[4].pointers[1].data)

				
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

		elif (ssdata[4] == 0) and (ssdata[6] != 0):
			if len(ss_entry.fragments[2].pointers[0].data) != 24:
				gub = self.ovs.frags_from_pointer(ss_entry.pointers[0], 1)
				ss_entry.fragments += gub
			ss_entry.fragments += self.ovs.frags_from_pointer(ss_entry.fragments[1].pointers[1], ssdata[6])
            
			if len(ss_entry.fragments[2].pointers[0].data) != 24:
				fug += self.ovs.frags_from_pointer_equalsb_counts(gub[0].pointers[1], 5)
				ss_entry.fragments += fug
				gub_d1 = self.prefab_unpack_gub(len(gub[0].pointers[1].data), gub[0].pointers[1].data)
				fug0_d1 = self.prefab_unpack_temp(len(fug[0].pointers[1].data), fug[0].pointers[1].data)
				fug1_d1 = self.prefab_unpack_temp(len(fug[1].pointers[1].data), fug[1].pointers[1].data)
				fug2_d1 = self.prefab_unpack_temp(len(fug[2].pointers[1].data), fug[2].pointers[1].data)
				fug3_d1 = self.prefab_unpack_temp(len(fug[3].pointers[1].data), fug[3].pointers[1].data)
				fug4_d1 = self.prefab_unpack_temp(len(fug[4].pointers[1].data), fug[4].pointers[1].data)

				
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


		elif (ssdata[4] != 0) and (ssdata[6] != 0):
			if (len(ss_entry.fragments[5].pointers[0].data) != 24) and (len(ss_entry.fragments[5].pointers[0].data) != 8):
				gub = self.ovs.frags_from_pointer(ss_entry.pointers[0], 1)
				ss_entry.fragments += gub
			ss_entry.specdef_name_fragments += self.ovs.frags_from_pointer(ss_entry.fragments[0].pointers[1], ssdata[4])
			for i, entry in enumerate(ss_entry.specdef_name_fragments):
				entry.data_frags = []
			ss_entry.fragments += ss_entry.specdef_name_fragments
            
			for name_frag in ss_entry.specdef_name_fragments:
            
				if name_frag.pointers[1].data.rstrip(b'\x00') in specdefs_jwe.jwe_specdefs:
                
					print(name_frag.pointers[1].data.rstrip(b'\x00'))
					specdef_frag_counts = specdefs_jwe.jwe_specdefs[name_frag.pointers[1].data.rstrip(b'\x00')]
					print(specdef_frag_counts)
					if specdef_frag_counts[0] != 0:
						name_frag.data_frags.extend(self.ovs.frags_from_pointer(ss_entry.fragments[2].pointers[1], specdef_frag_counts[0]))
						if len(name_frag.data_frags[0].pointers[1].data) >= 16:
							countt = self.prefab_unpack_temp(len(name_frag.data_frags[0].pointers[1].data),
											name_frag.data_frags[0].pointers[1].data)[2]     
					if b'AssetPackageLoader' == name_frag.pointers[1].data.rstrip(b'\x00'):
						check = self.prefab_unpack_temp(len(name_frag.data_frags[0].pointers[1].data),
										name_frag.data_frags[0].pointers[1].data)[2] 
						print("AssetPackageLoader has : "+str(check))
						name_frag.data_frags.extend(self.ovs.frags_from_pointer(name_frag.data_frags[0].pointers[1], check+1))
						for i in range(check+1):
							ccc = self.prefab_unpack_temp(len(name_frag.data_frags[i+1].pointers[0].data),name_frag.data_frags[i+1].pointers[0].data)[2]
							name_frag.data_frags.extend(self.ovs.frags_from_pointer(name_frag.data_frags[i+1].pointers[1], ccc))
					elif b'AudioDinosaurCore' == name_frag.pointers[1].data.rstrip(b'\x00'):
						check = self.prefab_unpack_temp(len(name_frag.data_frags[0].pointers[1].data),
										name_frag.data_frags[0].pointers[1].data)[2] 
						print("AudioDinosaurCore has : "+str(check))
						name_frag.data_frags.extend(self.ovs.frags_from_pointer(name_frag.data_frags[0].pointers[1], 2))
						if len(name_frag.data_frags[2].pointers[0].data) != 32:
							print("len len ",len(name_frag.data_frags[2].pointers[0].data))
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
						county = self.prefab_unpack_temp(len(name_frag.data_frags[2].pointers[1].data),name_frag.data_frags[2].pointers[1].data)[2]
						name_frag.data_frags.extend(self.ovs.frags_from_pointer(name_frag.data_frags[1].pointers[1], specdef_frag_counts[2]))
						name_frag.data_frags.extend(self.ovs.frags_from_pointer(name_frag.data_frags[2].pointers[1], self.specdef_thing(county,specdef_frag_counts[3])))
						name_frag.data_frags.extend(self.ovs.frags_from_pointer(name_frag.data_frags[3].pointers[1], specdef_frag_counts[4]))
                                           
					ss_entry.fragments += name_frag.data_frags

			if (len(ss_entry.fragments[5].pointers[0].data) != 24) and (len(ss_entry.fragments[5].pointers[0].data) != 8):
				fug += self.ovs.frags_from_pointer_equalsb_counts(gub[0].pointers[1], 5) #attr types, attr names, attr datas, list of some ints, list of short-like things
				print(gub)
				ss_entry.fragments += fug
				gub_d1 = self.prefab_unpack_gub(len(gub[0].pointers[1].data), gub[0].pointers[1].data)
				fug0_d1 = self.prefab_unpack_temp(len(fug[0].pointers[1].data), fug[0].pointers[1].data)
				fug1_d1 = self.prefab_unpack_temp(len(fug[1].pointers[1].data), fug[1].pointers[1].data)
				fug2_d1 = self.prefab_unpack_temp(len(fug[2].pointers[1].data), fug[2].pointers[1].data)
				fug3_d1 = self.prefab_unpack_temp(len(fug[3].pointers[1].data), fug[3].pointers[1].data)
				fug4_d1 = self.prefab_unpack_temp(len(fug[4].pointers[1].data), fug[4].pointers[1].data)

				
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
      
			#child Prefabs in the archive
			ss_entry.fragments += self.ovs.frags_from_pointer(ss_entry.fragments[4].pointers[1], ssdata[6])
	
		try:
			print("gub", gub_d1)
			print("fug0", fug0_d1)
			print("fug1", fug1_d1)
			print("fug2", fug2_d1)
			print("fug3", fug3_d1)
			print("fug4", fug4_d1)
		except:
			print("no gub")

                    
