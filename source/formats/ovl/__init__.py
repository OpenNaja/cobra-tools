import os
import itertools
import struct
import io
import time
import zlib

from generated.formats.ovl.compound.Header import Header
from generated.formats.ovl.compound.OvsHeader import OvsHeader
from generated.formats.ovl.compound.SetHeader import SetHeader
from generated.io import IoFile, ZipFile

from pyffi_ext.formats.ms2 import Ms2Format

MAX_UINT32 = 4294967295


def djb(s):
	# calculates DJB hash for string s
	# from https://gist.github.com/mengzhuo/180cd6be8ba9e2743753#file-hash_djb2-py
	hash = 5381
	for x in s:
		hash = ((hash << 5) + hash) + ord(x)
	return hash & 0xFFFFFFFF


class OvsFile(OvsHeader, ZipFile):

	def __init__(self, ovl, archive_entry, archive_index):
		super().__init__()
		self.ovl = ovl
		self.arg = archive_entry
		self.archive_index = archive_index

		# for temporary pyffi compat
		self.version = self.ovl.version
		self.user_version = self.ovl.user_version
		self._byte_order = "<"

	def unzip(self, filepath, start, skip, compressed_size=0):
		save_temp_dat = f"{filepath}_{self.arg.name}.dat" if "write_dat" in self.ovl.commands else ""
		with self.unzipper(filepath, start, skip, compressed_size, save_temp_dat=save_temp_dat) as stream:
			print("reading from unzipped ovs")
			stream.version = self.ovl.version
			stream.user_version = self.ovl.user_version
			# print("stream.version", stream.version)
			# print("stream.user_version", stream.user_version)
			super().read(stream)

			# print(self.header_entries)
			header_entry_index = 0
			for header_type in self.header_types:
				for i in range(header_type.num_headers):
					header_entry = self.header_entries[header_entry_index]
					header_entry.header_type = header_type
					header_entry.type = header_type.type
					# print(header_entry)
					header_entry.name = self.get_name(header_entry)
					header_entry.basename, header_entry.ext = os.path.splitext(header_entry.name)
					header_entry.ext = header_entry.ext[1:]
					# store fragments per header for faster lookup
					header_entry.fragments = []
					header_entry_index += 1

			for data_entry in self.data_entries:
				data_entry.name = self.get_name(data_entry)
			for sized_str_entry in self.sized_str_entries:
				sized_str_entry.name = self.get_name(sized_str_entry)
				sized_str_entry.lower_name = sized_str_entry.name.lower()
				sized_str_entry.basename, ext = os.path.splitext(sized_str_entry.name)
				sized_str_entry.ext = ext[1:]
				sized_str_entry.children = []
				sized_str_entry.parent = None
				sized_str_entry.fragments = []
				sized_str_entry.model_data_frags = []
				sized_str_entry.model_count = 0
				# print(sized_str_entry.name)
				# get data entry for link to buffers, or none
				try:
					sized_str_entry.data_entry = self.find_entry(self.data_entries, sized_str_entry)
				except:
					print("ERROR: Could not find a data entry!")

			for fragment in self.fragments:
				# we assign these later
				fragment.done = False
				fragment.lod = False
				fragment.name = None
			# print(self.ovl)
			# print(self)
			set_data_offset = stream.tell()
			print("Set header address", set_data_offset)
			self.set_header = stream.read_type(SetHeader)
			# print(self.set_header)
			if not (self.set_header.sig_a == 1065336831 and self.set_header.sig_b == 16909320):
				raise AttributeError("Set header signature check failed!")

			for set_entry in self.set_header.sets:
				set_entry.name = self.get_name(set_entry)
				set_entry.entry = self.find_entry(self.sized_str_entries, set_entry)

			for asset_entry in self.set_header.assets:
				asset_entry.name = self.get_name(asset_entry)
				try:
					asset_entry.entry = self.sized_str_entries[asset_entry.file_index]
				except:
					raise IndexError(f"Could not find a sizedstr entry for asset {asset_entry} in {len(self.sized_str_entries)}")

			self.map_assets()

			# size check again
			self.header_size = stream.tell()
			set_data_size = self.header_size - set_data_offset
			if set_data_size != self.arg.set_data_size:
				raise AttributeError(f"Set data size incorrect (got {set_data_size}, expected {self.arg.set_data_size})!")

			# another integrity check
			if not self.is_pc() and self.calc_uncompressed_size() != self.arg.uncompressed_size:
				raise AttributeError(f"Archive.uncompressed_size ({self.arg.uncompressed_size}) "
									 f"does not match calculated size ({self.calc_uncompressed_size})")

			# go back to header offset
			stream.seek(self.header_size)
			# add IO object to every header_entry
			for header_entry in self.header_entries:
				header_entry.data = io.BytesIO(stream.read(header_entry.size))

			self.check_header_data_size = self.calc_header_data_size()
			self.map_pointers()
			self.calc_pointer_addresses()
			self.calc_pointer_sizes()
			self.populate_pointers()

			self.map_frags()
			self.map_buffers(stream)

			if "write_frag_log" in self.ovl.commands:
				self.write_frag_log()
			
	def calc_pointer_addresses(self):
		print("Calculating pointer addresses")
		# store absolute read addresses from the start of file
		for entry in itertools.chain(self.fragments, self.sized_str_entries):
			# for access from start of file
			for pointer in entry.pointers:
				# some have max_uint as a header value, what do they refer to
				if pointer.header_index == MAX_UINT32:
					# print("Warning: {} has no header index (-1)".format(entry.name))
					pointer.header = 9999999
					pointer.type = 9999999
					pointer.address = 9999999
				# sized_str_entry.parent
				else:
					pointer.header = self.header_entries[pointer.header_index]
					# store type number of each header entry
					pointer.type = pointer.header.type
					pointer.address = self.header_size + pointer.header.offset + pointer.data_offset

	def calc_pointer_sizes(self):
		"""Assign an estimated size to every pointer"""
		print("calculating pointer sizes")
		# calculate pointer data sizes
		for entry in self.header_entries:
			# make them unique and sort them
			sorted_items = sorted(entry.pointer_map.items())
			# add the end of the header data block
			sorted_items.append((entry.size, None))
			# get the size of each fragment: find the next entry's address and substract it from address
			for i, (offset, pointers) in enumerate(sorted_items[:-1]):
				# get the offset of the next entry that points into this buffer, substract this offset
				data_size = sorted_items[i + 1][0] - offset
				for pointer in pointers:
					pointer.data_size = data_size

	def map_pointers(self):
		"""Assign list of copies to every pointer so they can be updated with the same data easily"""
		print("\nMapping pointers")
		# reset pointer map for each header entry
		for header_entry in self.header_entries:
			header_entry.pointer_map = {}
		print("\nLinking pointers to header")
		# append all valid pointers to their respective dicts
		for entry in itertools.chain(self.fragments, self.sized_str_entries):
			for pointer in entry.pointers:
				pointer.link_to_header(self)
		print("\nFinding duplicate pointers")
		for header_entry in self.header_entries:
			# for every pointer, store any other pointer that points to the same address
			for offset, pointers in header_entry.pointer_map.items():
				for p in pointers:
					# p.copies = [po for po in pointers if po != p]
					p.copies = pointers

	def populate_pointers(self):
		"""Load data for every pointer"""
		print("Reading data into pointers")
		for entry in itertools.chain(self.fragments, self.sized_str_entries):
			for pointer in entry.pointers:
				pointer.read_data(self)

	def map_assets(self):
		"""Store start and stop indices to asset entries, translate hierarchy to sizedstr entries"""
		# store start and stop asset indices
		for i, set_entry in enumerate(self.set_header.sets):
			# for the last entry
			if i == self.set_header.set_count - 1:
				set_entry.end = self.set_header.asset_count
			# store start of the next one as this one's end
			else:
				set_entry.end = self.set_header.sets[i + 1].start
			# map assets to entry
			set_entry.assets = self.set_header.assets[set_entry.start: set_entry.end]
			# print("SET:", set_entry.name)
			# print("ASSETS:", [a.name for a in set_entry.assets])
			# store the references on the corresponding sized str entry
			set_entry.entry.children = [self.sized_str_entries[a.file_index] for a in set_entry.assets]
			for child in set_entry.entry.children:
				child.parent = set_entry.entry

	def frags_from_pointer(self, p, count):
		frags = self.frags_for_pointer(p)
		return self.get_frags_after_count(frags, p.address, count)
	
	def frags_from_pointer_discon(self, p):
		frags = self.frags_for_pointer(p)
		return self.get_frags_til_discon(frags, p.address, len(p.data))
            
	def frags_from_pointer_equals(self, p):
		frags = self.frags_for_pointer(p)
		return self.get_frag_equal(frags, p.address, len(p.data))
            
	def frags_from_pointer_equals_counts(self, p, count):
		frags = self.frags_for_pointer(p)
		return self.get_frag_equal_counts(frags, p.address, count)
            
	def frags_from_pointer_equalsb(self, p):
		frags = self.frags_for_pointer(p)
		return self.get_frag_equalb(frags, p.address, len(p.data))
            
	def frags_from_pointer_equalsb_counts(self, p, count):
		frags = self.frags_for_pointer(p)
		return self.get_frag_equalb_counts(frags, p.address, len(p.data), count)

	def frags_for_pointer(self, p):
		return self.header_entries[p.header_index].fragments
	
	def prefab_unpack_temp(self,len,data):
		if len%4 != 0:
			ret = data
		elif len >=50:
			num = int(len/4)
			strr = "<"+str(num)+"I"
			ret = struct.unpack(strr, data)
		else:
			num = int(len/4)
			strr = "<"+str(num)+"I"
			ret = struct.unpack(strr, data)
		return ret
            
	def prefab_unpack_ss(self,len,data):
		num = int(len)
		strr = "<"+str(num)+"B"
		ret = struct.unpack(strr, data)
		return ret
	
	def collect_prefab(self, ss_entry, ad0_fragments):
		ssdata = self.prefab_unpack_ss(len(ss_entry.pointers[0].data),ss_entry.pointers[0].data)
		#if ss_entry.name in ("dingo_game.prefab"+"cassowary_game.prefab"+"red_kangaroo_game.prefab"+"koala_game.prefab"):
		print("\nPREFAB:",ss_entry.name)
		print(ssdata)
		if (ssdata[4] == 0) and (ssdata[6] ==0):
			ss_entry.fragments = self.frags_from_pointer(ss_entry.pointers[0], 1)
		elif (ssdata[4] != 0) and (ssdata[6] ==0):
			ss_entry.fragments = self.frags_from_pointer(ss_entry.pointers[0], 4)
			f3_d0 = self.prefab_unpack_temp(len(ss_entry.fragments[3].pointers[0].data),ss_entry.fragments[3].pointers[0].data)
			f2_d0 = self.prefab_unpack_temp(len(ss_entry.fragments[2].pointers[0].data),ss_entry.fragments[2].pointers[0].data)
		elif (ssdata[4] == 0) and (ssdata[6] !=0):
			ss_entry.fragments = self.frags_from_pointer(ss_entry.pointers[0], 3)
			f3_d0 = self.prefab_unpack_temp(len(ss_entry.fragments[2].pointers[0].data),ss_entry.fragments[2].pointers[0].data)
			f2_d0 = self.prefab_unpack_temp(len(ss_entry.fragments[2].pointers[0].data),ss_entry.fragments[2].pointers[0].data)
		elif (ssdata[4] != 0) and (ssdata[6] !=0):
			ss_entry.fragments = self.frags_from_pointer(ss_entry.pointers[0], 6) 
			f5_d0 = self.prefab_unpack_temp(len(ss_entry.fragments[5].pointers[0].data),ss_entry.fragments[5].pointers[0].data)
			f2_d0 = self.prefab_unpack_temp(len(ss_entry.fragments[2].pointers[0].data),ss_entry.fragments[2].pointers[0].data)
		else:
			ss_entry.fragments = self.frags_from_pointer(ss_entry.pointers[0], 1)
		gub = []
		fug = []
		
			
		if (ssdata[4] != 0) and (ssdata[6] ==0):
			if len(f3_d0) == 8:
				gub = self.frags_from_pointer(ss_entry.pointers[0], 1)
				ss_entry.fragments += gub
			ss_entry.fragments += self.frags_from_pointer(ss_entry.fragments[0].pointers[1], ssdata[4])
			if f2_d0[2] ==536870911: #in ("dingo_game.prefab"+"cassowary_game.prefab"+"red_kangaroo_game.prefab"+"koala_game.prefab"):
				ss_entry.fragments += self.frags_from_pointer(ss_entry.fragments[2].pointers[1], 18)
				for x in range(34,52):
					if x ==34:
						ss_entry.fragments += self.frags_from_pointer_equalsb_counts(ss_entry.fragments[x].pointers[1], 2)
					elif x ==35:
						ss_entry.fragments += self.frags_from_pointer_equalsb_counts(ss_entry.fragments[x].pointers[1],5)
					elif x ==38:
						ss_entry.fragments += self.frags_from_pointer_equalsb_counts(ss_entry.fragments[x].pointers[1],3)
					elif x ==41:
						ss_entry.fragments += self.frags_from_pointer_equalsb(ss_entry.fragments[x].pointers[1])
					elif x ==43:
						ss_entry.fragments += self.frags_from_pointer_equalsb_counts(ss_entry.fragments[x].pointers[1], 2)
					elif x ==45:
						ss_entry.fragments += self.frags_from_pointer_equalsb(ss_entry.fragments[x].pointers[1])
					elif x ==47:
						ss_entry.fragments += self.frags_from_pointer_equalsb(ss_entry.fragments[x].pointers[1])
					elif x ==48:
						ss_entry.fragments += self.frags_from_pointer_equalsb(ss_entry.fragments[x].pointers[1])
					elif x ==50:
						ss_entry.fragments += self.frags_from_pointer_equalsb_counts(ss_entry.fragments[x].pointers[1], 2)
					elif x ==51:
						ss_entry.fragments += self.frags_from_pointer_equalsb_counts(ss_entry.fragments[x].pointers[1], 2)
				#elif  f2_d0[2] ==127:
				#	ss_entry.fragments += self.frags_from_pointer(ss_entry.fragments[2].pointers[1], 6)
				#elif  f2_d0[2] ==3:
				#	ss_entry.fragments += self.frags_from_pointer(ss_entry.fragments[2].pointers[1], 1)
				#elif  f2_d0[2] ==63:
				#	ss_entry.fragments += self.frags_from_pointer(ss_entry.fragments[2].pointers[1], 5)
				#elif  f2_d0[2] ==1:
				#	ss_entry.fragments += self.frags_from_pointer(ss_entry.fragments[2].pointers[1], 1)
				#elif  f2_d0[2] ==7:
				#	ss_entry.fragments += self.frags_from_pointer(ss_entry.fragments[2].pointers[1], 4)
				#elif  f2_d0[2] ==15:
				#	ss_entry.fragments += self.frags_from_pointer(ss_entry.fragments[2].pointers[1], 3)  
			if len(f3_d0) == 8:
				fug += self.frags_from_pointer_equalsb_counts(ss_entry.fragments[4].pointers[1], 5)
				ss_entry.fragments+= fug
				gub_d1 = self.prefab_unpack_temp(len(gub[0].pointers[1].data),gub[0].pointers[1].data )
				fug0_d1 = self.prefab_unpack_temp(len(fug[0].pointers[1].data),fug[0].pointers[1].data )
				fug1_d1 = self.prefab_unpack_temp(len(fug[1].pointers[1].data),fug[1].pointers[1].data )
				fug2_d1 = self.prefab_unpack_temp(len(fug[2].pointers[1].data),fug[2].pointers[1].data )
				fug3_d1 = self.prefab_unpack_temp(len(fug[3].pointers[1].data),fug[3].pointers[1].data )
				fug4_d1 = self.prefab_unpack_temp(len(fug[4].pointers[1].data),fug[4].pointers[1].data )
				print("gub",gub_d1)
				print("fug0",fug0_d1)
				print("fug1",fug1_d1)
				print("fug2",fug2_d1)
				print("fug3",fug3_d1)
				print("fug4",fug4_d1)
				if fug0_d1[len(fug0_d1)-1] == 0:
					ss_entry.fragments+=  self.frags_from_pointer_equalsb_counts(fug[1].pointers[1], len(fug0_d1)-1) #count equal to len(fug[0].pointers[1].data)/4 -1
					ss_entry.fragments+=  self.frags_from_pointer_equalsb_counts(fug[2].pointers[1], len(fug0_d1)-1) #count equal to len(fug[0].pointers[1].data)/4 -1	
				else:
					ss_entry.fragments+=  self.frags_from_pointer_equalsb_counts(fug[1].pointers[1], len(fug0_d1) )#count equal to len(fug[0].pointers[1].data)/4 -1
					ss_entry.fragments+=  self.frags_from_pointer_equalsb_counts(fug[2].pointers[1], len(fug0_d1)) #count equal to len(fug[0].pointers[1].data)/4 -1
				if gub_d1[0] == 1638405:
					ss_entry.fragments+=  self.frags_from_pointer_equalsb_counts(fug[4].pointers[1], 8)
				elif gub_d1[0] == 1966113:
					ss_entry.fragments+=  self.frags_from_pointer_equalsb_counts(fug[4].pointers[1], 13)
				elif gub_d1[0] == 1966113:
					ss_entry.fragments+=  self.frags_from_pointer_equalsb_counts(fug[4].pointers[1], 13)

		elif (ssdata[4] == 0) and (ssdata[6] !=0):
			if len(f2_d0) == 4:
				gub = self.frags_from_pointer(ss_entry.pointers[0], 1)
				ss_entry.fragments += gub
			ss_entry.fragments += self.frags_from_pointer(ss_entry.fragments[1].pointers[1], ssdata[6])

                
		elif (ssdata[4] != 0) and (ssdata[6] !=0):
			if len(f5_d0) == 4:
				gub = self.frags_from_pointer(ss_entry.pointers[0], 1)
				ss_entry.fragments += gub
			ss_entry.fragments += self.frags_from_pointer(ss_entry.fragments[0].pointers[1], ssdata[4])
			if f2_d0[2] ==536870911: #in ("dingo_game.prefab"+"cassowary_game.prefab"+"red_kangaroo_game.prefab"+"koala_game.prefab"):
				ss_entry.fragments += self.frags_from_pointer(ss_entry.fragments[2].pointers[1], 18)
				for x in range(34,52):
					if x ==34:
						ss_entry.fragments += self.frags_from_pointer_equalsb_counts(ss_entry.fragments[x].pointers[1], 2)
					elif x ==35:
						ss_entry.fragments += self.frags_from_pointer_equalsb_counts(ss_entry.fragments[x].pointers[1],5)
					elif x ==38:
						ss_entry.fragments += self.frags_from_pointer_equalsb_counts(ss_entry.fragments[x].pointers[1],3)
					elif x ==41:
						ss_entry.fragments += self.frags_from_pointer_equalsb(ss_entry.fragments[x].pointers[1])
					elif x ==43:
						ss_entry.fragments += self.frags_from_pointer_equalsb_counts(ss_entry.fragments[x].pointers[1], 2)
					elif x ==45:
						ss_entry.fragments += self.frags_from_pointer_equalsb(ss_entry.fragments[x].pointers[1])
					elif x ==47:
						ss_entry.fragments += self.frags_from_pointer_equalsb(ss_entry.fragments[x].pointers[1])
					elif x ==48:
						ss_entry.fragments += self.frags_from_pointer_equalsb(ss_entry.fragments[x].pointers[1])
					elif x ==50:
						ss_entry.fragments += self.frags_from_pointer_equalsb_counts(ss_entry.fragments[x].pointers[1], 2)
					elif x ==51:
						ss_entry.fragments += self.frags_from_pointer_equalsb_counts(ss_entry.fragments[x].pointers[1], 2)
				#elif  f2_d0[2] ==127:
				#	ss_entry.fragments += self.frags_from_pointer(ss_entry.fragments[2].pointers[1], 6)
				#elif  f2_d0[2] ==3:
				#	ss_entry.fragments += self.frags_from_pointer(ss_entry.fragments[2].pointers[1], 1)
				#elif  f2_d0[2] ==63:
				#	ss_entry.fragments += self.frags_from_pointer(ss_entry.fragments[2].pointers[1], 5)
				#elif  f2_d0[2] ==1:
				#	ss_entry.fragments += self.frags_from_pointer(ss_entry.fragments[2].pointers[1], 1)
				#elif  f2_d0[2] ==7:
				#	ss_entry.fragments += self.frags_from_pointer(ss_entry.fragments[2].pointers[1], 4)
				#elif  f2_d0[2] ==15:
				#	ss_entry.fragments += self.frags_from_pointer(ss_entry.fragments[2].pointers[1], 3)   
			if len(f5_d0) == 4:
				fug += self.frags_from_pointer_equalsb_counts(ss_entry.fragments[6].pointers[1], 5)
				ss_entry.fragments+= fug
				gub_d1 = self.prefab_unpack_temp(len(gub[0].pointers[1].data),gub[0].pointers[1].data )
				fug0_d1 = self.prefab_unpack_temp(len(fug[0].pointers[1].data),fug[0].pointers[1].data )
				fug1_d1 = self.prefab_unpack_temp(len(fug[1].pointers[1].data),fug[1].pointers[1].data )
				fug2_d1 = self.prefab_unpack_temp(len(fug[2].pointers[1].data),fug[2].pointers[1].data )
				fug3_d1 = self.prefab_unpack_temp(len(fug[3].pointers[1].data),fug[3].pointers[1].data )
				fug4_d1 = self.prefab_unpack_temp(len(fug[4].pointers[1].data),fug[4].pointers[1].data )
				print("gub",gub_d1)
				print("fug0",fug0_d1)
				print("fug1",fug1_d1)
				print("fug2",fug2_d1)
				print("fug3",fug3_d1)
				print("fug4",fug4_d1)
				if fug0_d1[len(fug0_d1)-1] == 0:
					ss_entry.fragments+=  self.frags_from_pointer_equalsb_counts(fug[1].pointers[1], len(fug0_d1)-1) #count equal to len(fug[0].pointers[1].data)/4 -1
					ss_entry.fragments+=  self.frags_from_pointer_equalsb_counts(fug[2].pointers[1], len(fug0_d1)-1) #count equal to len(fug[0].pointers[1].data)/4 -1	
				else:
					ss_entry.fragments+=  self.frags_from_pointer_equalsb_counts(fug[1].pointers[1], len(fug0_d1) )#count equal to len(fug[0].pointers[1].data)/4 -1
					ss_entry.fragments+=  self.frags_from_pointer_equalsb_counts(fug[2].pointers[1], len(fug0_d1)) #count equal to len(fug[0].pointers[1].data)/4 -1
				#if gub_d1[0] == 393217:
					#ss_entry.fragments+=  self.frags_from_pointer_equalsb_counts(fug[4].pointers[1], 0) #count equal to len(fug[0].pointers[1].data)/4 -1
				if gub_d1[0] == 1638405:
					ss_entry.fragments+=  self.frags_from_pointer_equalsb_counts(fug[4].pointers[1], 8)
				elif gub_d1[0] == 1966113:
					ss_entry.fragments+=  self.frags_from_pointer_equalsb_counts(fug[4].pointers[1], 13)
				elif gub_d1[0] == 1966113:
					ss_entry.fragments+=  self.frags_from_pointer_equalsb_counts(fug[4].pointers[1], 13)


                        
			ss_entry.fragments += self.frags_from_pointer(ss_entry.fragments[4].pointers[1], ssdata[6])

		zzz=0
		#if ss_entry.name in "dingo_game.prefab":
		for fragg in ss_entry.fragments:
			if zzz<6:
				print("frag"+str(zzz))
				print(self.prefab_unpack_temp(len(fragg.pointers[0].data),fragg.pointers[0].data))
				print(self.prefab_unpack_temp(len(fragg.pointers[1].data),fragg.pointers[1].data))
				zzz+=1

	def collect_matcol(self, ss_entry):
		print("\nMATCOL:", ss_entry.name)

		# Sized string initpos = position of first fragment for matcol
		# input_frags = self.frags_for_pointer(ss_entry.pointers[0])
		# ss_entry.fragments = self.get_frag_after(input_frags, ((4,4),), ss_entry.pointers[0].address)
		ss_entry.fragments = self.frags_from_pointer(ss_entry.pointers[0], 1)
		ss_entry.f0 = ss_entry.fragments[0]

		# print(ss_entry.f0)
		# 0,0,collection count,0
		f0_d0 = struct.unpack("<4I", ss_entry.f0.pointers[0].data)
		# flag (3=variant, 2=layered) , 0
		ss_entry.has_texture_list_frag = len(ss_entry.f0.pointers[1].data) == 8
		if ss_entry.has_texture_list_frag:
			f0_d1 = struct.unpack("<2I", ss_entry.f0.pointers[1].data)
		else:
			f0_d1 = struct.unpack("<6I", ss_entry.f0.pointers[1].data)
		# print("f0_d0", f0_d0)
		# print("f0_d1", f0_d1)
		ss_entry.is_variant = f0_d1[0] == 3
		ss_entry.is_layered = f0_d1[0] == 2
		# print("has_texture_list_frag",ss_entry.has_texture_list_frag)
		# print("is_variant",ss_entry.is_variant)
		# print("is_layered",ss_entry.is_layered)
		# print(ss_entry.tex_pointer)
		if ss_entry.has_texture_list_frag:
			# input_frags = self.frags_for_pointer(ss_entry.f0.pointers[1])
			# ss_entry.tex_pointer = self.get_frag_after(input_frags, ((4,4),), ss_entry.f0.pointers[1].address)[0]
			ss_entry.tex_pointer = self.frags_from_pointer(ss_entry.f0.pointers[1], 1)[0]
			tex_pointer_d0 = struct.unpack("<4I", ss_entry.tex_pointer.pointers[0].data)
			# print("tex_pointer_d0", tex_pointer_d0)
			tex_count = tex_pointer_d0[2]
			# print("tex_count",tex_count)
			ss_entry.tex_frags = self.frags_from_pointer(ss_entry.tex_pointer.pointers[1], tex_count * 3)
		# ss_entry.tex_frags = []
		# input_frags = self.frags_for_pointer(ss_entry.tex_pointer.pointers[1])
		# for t in range(tex_count):
		#	 ss_entry.tex_frags += self.get_frag_after(input_frags, ((4,6),(4,6),(4,6)), ss_entry.tex_pointer.pointers[1].address)
		# for tex in ss_entry.tex_frags:
		#	 print(tex.pointers[1].data)
		else:
			ss_entry.tex_pointer = None
		# material pointer frag
		ss_entry.mat_pointer = self.frags_from_pointer(ss_entry.f0.pointers[1], 1)[0]
		# ss_entry.mat_pointer_frag = self.get_frag_after(address_0_fragments, ((4,4),), ss_entry.f0.pointers[1].address)
		# ss_entry.mat_pointer = ss_entry.mat_pointer_frag[0]
		mat_pointer_d0 = struct.unpack("<6I", ss_entry.mat_pointer.pointers[0].data)
		# print("mat_pointer_d0",mat_pointer_d0)
		mat_count = mat_pointer_d0[2]
		# print("mat_count",mat_count)
		ss_entry.mat_frags = []
		for t in range(mat_count):
			if ss_entry.is_variant:
				m0 = self.frags_from_pointer(ss_entry.mat_pointer.pointers[1], 1)[0]
				# m0 = self.get_frag_after(address_0_fragments, ((4,6),), ss_entry.mat_pointer.pointers[1].address)[0]
				# print(m0.pointers[1].data)
				m0.name = ss_entry.name
				ss_entry.mat_frags.append((m0,))
			elif ss_entry.is_layered:
				mat_frags = self.frags_from_pointer(ss_entry.mat_pointer.pointers[1], 3)
				# mat_frags = self.get_frag_after(address_0_fragments, ((4,6),(4,4),(4,4)), ss_entry.mat_pointer.pointers[1].address)

				m0, info, attrib = mat_frags
				m0.pointers[1].strip_zstring_padding()
				# print(m0.pointers[1].data)

				info_d0 = struct.unpack("<8I", info.pointers[0].data)
				info_count = info_d0[2]
				# print("info_count", info_count)
				info.children = self.frags_from_pointer(info.pointers[1], info_count)
				for info_child in info.children:
					# info_child = self.get_frag_after(address_0_fragments, ((4,6),), info.pointers[1].address)[0]
					# 0,0,byte flag,byte flag,byte flag,byte flag,float,float,float,float,0
					# info_child_d0 = struct.unpack("<2I4B4fI", info_child.pointers[0].data)
					info_child.pointers[1].strip_zstring_padding()
				# print(info_child.pointers[1].data, info_d0)

				attrib.children = []
				attrib.pointers[0].split_data_padding(16)
				attrib_d0 = struct.unpack("<4I", attrib.pointers[0].data)
				attrib_count = attrib_d0[2]
				# print("attrib_count",attrib_count)
				attrib.children = self.frags_from_pointer(attrib.pointers[1], attrib_count)
				for attr_child in attrib.children:
					# attr_child = self.get_frag_after(address_0_fragments, ((4,6),), attrib.pointers[1].address)[0]
					# attrib.children.append(attr_child)
					# attr_child_d0 = struct.unpack("<2I4BI", attr_child.pointers[0].data)
					attr_child.pointers[1].strip_zstring_padding()
				# print(attr_child.pointers[1].data, attr_child_d0)

				# store names for frag log
				for frag in mat_frags + info.children + attrib.children:
					frag.name = ss_entry.name
				# store frags
				ss_entry.mat_frags.append(mat_frags)
		if ss_entry.has_texture_list_frag:
			for frag in ss_entry.tex_frags + [ss_entry.tex_pointer, ]:
				frag.name = ss_entry.name
		all_frags = [ss_entry.f0, ss_entry.mat_pointer]
		for frag in all_frags:
			frag.name = ss_entry.name

	def collect_mdl2(self, mdl2_sized_str_entry, model_info, mdl2_pointer):
		# print("Collecting model fragments for", mdl2_sized_str_entry.name)
		mdl2_sized_str_entry.fragments = self.frags_from_pointer(mdl2_pointer, 5)
		mdl2_sized_str_entry.model_info = model_info
		mdl2_sized_str_entry.model_count = model_info.model_count
		lod_pointer = mdl2_sized_str_entry.fragments[3].pointers[1]
		# remove padding from materials1 fragment
		mdl2_sized_str_entry.fragments[2].pointers[1].split_data_padding(4 * model_info.mat_1_count)

		# get and set fragments
		# print("Num model data frags",mdl2_sized_str_entry.model_count)
		mdl2_sized_str_entry.model_data_frags = self.frags_from_pointer(lod_pointer, mdl2_sized_str_entry.model_count)

	def map_frags(self):
		print("\nMapping SizedStrs to Fragments")

		# we go from the start
		address_0_fragments = list(sorted(self.fragments, key=lambda f: f.pointers[0].address))

		# just reverse is good enough, no longer need to sort them
		sorted_sized_str_entries = list(reversed(self.sized_str_entries))
		for frag in address_0_fragments:
			# header_index = frag.pointers[0].header_index
			# print(header_index, header_index != MAX_UINT32)
			# fragments always have a validheader index
			self.header_entries[frag.pointers[0].header_index].fragments.append(frag)

		# todo: document more of these type requirements
		dic = {"ms2": 3,
			   "bani": 1,
			   "tex": 2,
			   "xmlconfig": 1,
			   # "enumnamer": ( (4,4), ),
			   # "motiongraphvars": ( (4,4), (4,6), (4,6), (4,6), (4,6), (4,6), (4,6), (4,6), ),
			   # "hier": ( (4,6) for x in range(19) ),
			   "spl": 1,
			   "lua": 2,
			   "assetpkg": 1,
			   "userinterfaceicondata": 2,
			   "renderparameters": 1, #temp
			   "renderparametercurves": 1, #temp
			   "animalresearchunlocksettings": 1, #temp
			   "mechanicresearchsettings": 1, #temp
			   "pathextrusion": 1,#temp
			   "pathmaterial": 1, #temp
			   "pathresource": 1 #temp
			   # "world": will be a variable length one with a 4,4; 4,6; then another variable length 4,6 set : set world before assetpkg in order
			   }
		ss_max = len(sorted_sized_str_entries)
		for ss_index, sized_str_entry in enumerate(sorted_sized_str_entries):
			self.ovl.print_and_callback("Collecting fragments", value=ss_index, max_value=ss_max)
			# get fixed fragments
			print("Collecting fragments for", sized_str_entry.name, sized_str_entry.pointers[0].address)
			hi = sized_str_entry.pointers[0].header_index
			if hi != MAX_UINT32:
				frags = self.header_entries[hi].fragments
			else:
				frags = address_0_fragments
			if sized_str_entry.ext == "ms2" and self.is_pc():
				sized_str_entry.fragments = self.get_frags_after_count(frags, sized_str_entry.pointers[0].address, 1)
			elif sized_str_entry.ext == "tex" and self.is_pc():
				sized_str_entry.fragments = self.get_frags_after_count(frags, sized_str_entry.pointers[0].address, 1)
			elif sized_str_entry.ext in dic:

				t = dic[sized_str_entry.ext]
				# get and set fragments
				sized_str_entry.fragments = self.get_frags_after_count(frags, sized_str_entry.pointers[0].address, t)

			elif sized_str_entry.ext == "fgm":
				sized_str_entry.fragments = self.get_frag_after_terminator(frags, sized_str_entry.pointers[0].address)
				
			elif sized_str_entry.ext == "materialcollection":
				self.collect_matcol(sized_str_entry)
			elif sized_str_entry.ext == "prefab":
				self.collect_prefab(sized_str_entry, address_0_fragments)
		# print("sizedstr",sized_str_entry.pointers[0].header_index)
		# print("frags",tuple((f.pointers[0].header_index, f.pointers[1].header_index) for f in sized_str_entry.fragments))
		# for f in sized_str_entry.fragments:
		#	 assert(f.pointers[0].header_index == sized_str_entry.pointers[0].header_index)
		# second pass: collect model fragments
		# assign the mdl2 frags to their sized str entry
		for set_entry in self.set_header.sets:
			set_sized_str_entry = set_entry.entry
			if set_sized_str_entry.ext == "ms2"  and not self.is_pc():
				f_1 = set_sized_str_entry.fragments[1]
				print("F-1:", f_1)
				self.write_frag_log()
				next_model_info = f_1.pointers[1].read_as(Ms2Format.CoreModelInfo, self.ovl)[0]
				print("next model info:", next_model_info)
				for asset_entry in set_entry.assets:
					assert (asset_entry.name == asset_entry.entry.name)
					sized_str_entry = asset_entry.entry
					if sized_str_entry.ext == "mdl2":
						self.collect_mdl2(sized_str_entry, next_model_info, f_1.pointers[1])
						pink = sized_str_entry.fragments[4]
						if (self.ovl.flag_2 == 24724 and pink.pointers[0].data_size == 144) \
								or (self.ovl.flag_2 == 8340 and pink.pointers[0].data_size == 160):
							next_model_info = pink.pointers[0].read_as(Ms2Format.Mdl2ModelInfo, self.ovl)[0].info

		# # for debugging only:
		for sized_str_entry in sorted_sized_str_entries:
			for frag in sized_str_entry.model_data_frags + sized_str_entry.fragments:
				frag.name = sized_str_entry.name

	# for header_i, header_entry in enumerate(self.header_entries):
	# print("Header {} with unknown count {}".format(header_i, header_entry.num_files))

	def map_buffers(self, stream):
		"""Map buffers to data entries, sort buffers into load order, populate buffers with data"""
		print("\nMapping buffers")

		# this holds the buffers in the order they are read from the file
		self.buffers_io_order = []

		# sequentially attach buffers to data entries by each entry's buffer count
		buff_ind = 0
		for i, data in enumerate(self.data_entries):
			data.buffers = []
			for j in range(data.buffer_count):
				# print("data",i,"buffer",j, "buff_ind",buff_ind)
				buffer = self.buffer_entries[buff_ind]
				# also give each buffer a reference to data so we can access it later
				buffer.data_entry = data
				data.buffers.append(buffer)
				buff_ind += 1

		# only do this if there are any data entries so that max() doesn't choke
		if self.data_entries:
			# check how many buffers occur at max in one data block
			max_buffers_per_data = max([data.buffer_count for data in self.data_entries])
			# first read the first buffer for every file
			# then the second if it has any
			# and so on, until there is no data entry left with unprocessed buffers
			for i in range(max_buffers_per_data):
				for data in self.data_entries:
					if i < data.buffer_count:
						self.buffers_io_order.append(data.buffers[i])

		# finally, we have the buffers in the correct sorting so we can read their contents
		print("\nReading from buffers")
		stream.seek(self.header_size + self.check_header_data_size)
		for buffer in self.buffers_io_order:
			# read buffer data and store it in buffer object
			buffer.read_data(stream)

	def write_frag_log(self, ):
		# # this is just for developing to see which unique attributes occur across a list of entries
		# ext_hashes = sorted(set([f.offset for f in self.ovl.files]))
		# print(ext_hashes)
		# # this is just for developing to see which unique attributes occur across a list of entries
		# ext_hashes = sorted(set([f.size for f in self.fragments]))
		# print(ext_hashes)
		self.dir = os.getcwd()
		# # for development; collect info about fragment types
		frag_log = "self.fragments > sizedstr\nfragments in file order"
		for i, frag in enumerate(sorted(self.fragments, key=lambda f: f.pointers[0].address)):
			# #frag_log+="\n\nFragment nr "+str(i)
			# #frag_log+="\nHeader types "+str(f.type_0)+" "+str(f.type_1)
			# #frag_log+="\nEntry "+str(f.header_index_0)+" "+str(f.data_offset_0)+" "+str(f.header_index_1)+" "+str(f.data_offset_1)
			# #frag_log+="\nSized str "+str(f.sized_str_entry_index)+" "+str(f.name)
			frag_log += "\n" + str(i) + " " + str(frag.pointers[0].address) + " " + str(
				frag.pointers[0].data_size) + " " + str(frag.pointers[1].address) + " " + str(
				frag.pointers[1].data_size) + " " + str(frag.name) + " " + str(frag.pointers[0].type) + " " + str(
				frag.pointers[1].type)
		frag_log_path = self.indir("frag" + str(self.archive_index) + ".log")
		print(f"Writing Fragment log to {frag_log_path}")
		with open(frag_log_path, "w") as f:
			f.write(frag_log)

	@staticmethod
	def get_frag_after_terminator(l, initpos, terminator=24):
		"""Returns entries of l matching h_types that have not been processed until it reaches a frag of terminator size."""
		out = []
		# print("looking for",h_types)
		for f in l:
			# can't add self.fragments that have already been added elsewhere
			if f.done:
				continue
			if f.pointers[0].address >= initpos:
				# print(f.data_offset_0,"  ",initpos)
				f.done = True
				out.append(f)
				if f.pointers[0].data_size == terminator:
					break
		else:
			raise AttributeError(
				f"Could not find a terminator fragment matching initpos {initpos} and pointer[0].size {terminator}")
		return out

	@staticmethod
	def get_frags_after_count(frags, initpos, count):
		"""Returns count entries of frags that have not been processed and occur after initpos."""
		out = []
		for f in frags:
			# check length of fragment, grab good ones
			if len(out) == count:
				break
			# can't add fragments that have already been added elsewhere
			if f.done:
				continue
			if f.pointers[0].address >= initpos:
				f.done = True
				out.append(f)
		else:
			if len(out) != count:
				raise AttributeError(
					f"Could not find {count} fragments after initpos {initpos}, only found {len(out)}!")
		return out
	
	@staticmethod
	def get_frag_equal(frags, initpos, datalength):
		"""Returns count entries of frags that have not been processed and occur after initpos."""
		out = []
		for f in frags:
			# can't add fragments that have already been added elsewhere
			if f.done:
				continue
			if f.pointers[0].address == initpos:
				f.done = True
				out.append(f)
				break
		return out
	
	@staticmethod
	def get_frag_equal_counts(frags, initpos, count):
		"""Returns count entries of frags that have not been processed and occur after initpos."""
		out = []
		first = 1
		for f in frags:
			if first == 1:
				if f.done:
					continue
				if (f.pointers[0].address == initpos):
					f.done = True
					out.append(f)
					first = 0
			else:
				# check length of fragment, grab good ones
				if len(out) == count:
					break
				# can't add fragments that have already been added elsewhere
				if f.done:
					continue
				if f.pointers[0].address >= initpos:
					f.done = True
					out.append(f)
		return out
	
	@staticmethod
	def get_frags_til_discon(frags, initpos, datalength):
		"""Returns entries of frags that have not been processed and until discontinuity."""
		out = []
		lastpos = initpos
		length = 0
		firstgrab = 1
		for f in frags:
			if firstgrab == 1:
				if f.done:
					continue
				if (f.pointers[0].address == initpos) or (f.pointers[0].address == initpos+datalength):
					f.done = True
					out.append(f)
					firstgrab = 0
					length= len(f.pointers[0].data)
					lastpos = f.pointers[0].address
					print("first ",initpos,length,lastpos)
			else:
				if f.pointers[0].address-length == lastpos:
					if f.done:
						continue
					if f.pointers[0].address >= initpos:
						f.done = True
						out.append(f)
						length= len(f.pointers[0].data)
						lastpos = f.pointers[0].address
				else: 
					break
		return out
            
	@staticmethod
	def get_frags_til_disconb(frags, initpos, datalength):
		"""Returns entries of frags that have not been processed and until discontinuity."""
		out = []
		lastpos = initpos
		length = 0
		firstgrab = 1
		for f in frags:
			if firstgrab == 1:
				if f.done:
					continue
				if f.pointers[0].address == initpos:
					f.done = True
					out.append(f)
					firstgrab = 0
					length= len(f.pointers[0].data)
					lastpos = f.pointers[0].address
					print("first ",initpos,length,lastpos)
			else:
				if f.pointers[0].address-length == lastpos:
					if f.done:
						continue
					if f.pointers[0].address >= initpos:
						f.done = True
						out.append(f)
						length= len(f.pointers[0].data)
						lastpos = f.pointers[0].address
				else: 
					break
		return out

	def find_entry(self, l, src_entry):
		""" returns entry from list l whose file hash matches hash, or none"""
		if self.is_pc():
			# try to find it
			for entry in l:
				if entry.file_hash == src_entry.file_hash:
					return entry
		else:
			# try to find it
			for entry in l:
				if entry.file_hash == src_entry.file_hash and entry.ext_hash == src_entry.ext_hash:
					return entry

	def is_pc(self):
		return self.version == 18

	def is_pz(self):
		return self.ovl.flag_2 == 8340 and not self.is_pc()

	def is_jwe(self):
		return self.ovl.flag_2 == 24724 and not self.is_pc()

	def get_name(self, entry):
		"""Fetch a filename from hash dict"""
		# JWE style
		if self.is_jwe():
			# print("JWE ids",entry.file_hash, entry.ext_hash)
			try:
				n = self.ovl.name_hashdict[entry.file_hash]
			except:
				n = "NONAME"
			try:
				e = self.ovl.name_hashdict[entry.ext_hash]
			except:
				e = "UNKNOWN"
		# PZ Style
		elif self.is_pz():
			# print("PZ ids",entry.file_hash, entry.ext_hash)
			try:
				n = self.ovl.name_list[entry.file_hash]
			except:
				n = "NONAME"
			try:
				e = self.ovl.name_hashdict[entry.ext_hash]
			except:
				e = "UNKNOWN"
		# PC Style
		elif self.is_pc():
		# print("PC ids",entry.file_hash, entry.ext_hash)
			try:
				n = self.ovl.files[entry.file_hash].name#self.header.name_list[entry.file_hash]
			except:
				n = "NONAME"
			try:
				e = self.ovl.mimes[self.ovl.files[entry.file_hash].extension].ext
			except:
				e = "UNKNOWN"
		return n + "." + e

	def calc_uncompressed_size(self, ):
		"""Calculate the size of the whole decompressed stream for this archive"""

		# TODO: this is apparently wrong during write_archive, as if something wasn't properly updated

		check_data_size_1 = 0
		check_data_size_2 = 0
		for data_entry in self.data_entries:
			check_data_size_1 += data_entry.size_1
			if hasattr(data_entry, "size_2"):
				check_data_size_2 += data_entry.size_2
		return self.header_size + self.calc_header_data_size() + check_data_size_1 + check_data_size_2

	def calc_header_data_size(self, ):
		"""Calculate the size of the whole data entry region that sizedstr and fragment entries point into"""
		return sum(header_entry.size for header_entry in self.header_entries)

	def indir(self, name):
		return os.path.join(self.dir, name)

	def write_archive(self, stream):

		for i, header_entry in enumerate(self.header_entries):
			# maintain sorting order
			# grab the first pointer for each address
			# it is assumed that subsequent pointers to that address share the same data
			sorted_first_pointers = [pointers[0] for offset, pointers in sorted(header_entry.pointer_map.items())]
			if sorted_first_pointers:
				# only known from indominus
				first_offset = sorted_first_pointers[0].data_offset
				if first_offset != 0:
					print(f"Found {first_offset} unaccounted bytes at start of header data {i}")
					unaccounted_bytes = header_entry.data.getvalue()[:first_offset]
				else:
					unaccounted_bytes = b""

				# clear io objects
				header_entry.data = io.BytesIO()
				header_entry.data.write(unaccounted_bytes)
				# write updated strings
				for pointer in sorted_first_pointers:
					pointer.write_data(self, update_copies=True)
			else:
				print(f"No pointers into header entry {i} - keeping its stock data!")

		# do this first so header entries can be updated
		header_data_writer = io.BytesIO()
		# the ugly stuff with all fragments and sizedstr entries
		for header_entry in self.header_entries:
			header_data_bytes = header_entry.data.getvalue()
			# JWE style
			if self.ovl.flag_2 == 24724:
				header_entry.offset = header_data_writer.tell()
			# PZ Style
			elif self.ovl.flag_2 == 8340:
				header_entry.offset = self.arg.ovs_header_offset + header_data_writer.tell()
			header_entry.size = len(header_data_bytes)
			header_data_writer.write(header_data_bytes)

		# write out all entries
		super().write(stream)
		# write set & asset stuff
		self.set_header.write(stream)
		# write the header data containing all the pointers' datas
		stream.write(header_data_writer.getvalue())

		# write buffer data
		for b in self.buffers_io_order:
			stream.write(b.data)


# do some calculations
# self.archive_entry.uncompressed_size = stream.tell()
# self.archive_entry.uncompressed_size = self.calc_uncompressed_size()


class OvlFile(Header, IoFile):

	def __init__(self, progress_callback=None):
		super().__init__()

		self.last_print = None
		if progress_callback:
			self.progress_callback = progress_callback
		else:
			self.progress_callback = self.dummy_callback

	def get_sized_str_entry(self, name):
		lower_name = name.lower()
		for archive in self.ovs_files:
			for sized_str_entry in archive.sized_str_entries:
				if lower_name == sized_str_entry.lower_name:
					return sized_str_entry
		# still here - error!
		raise KeyError(f"Can't find a sizedstr entry for {name}, not from this archive?")

	# dummy (black hole) callback for if we decide we don't want one
	def dummy_callback(self, *args, **kwargs):
		return

	def print_and_callback(self, message, value=None, max_value=None):
		# don't print the message if it is identical to the last one - it
		# will slow down massively repetitive tasks
		if self.last_print != message:
			print(message)
			self.last_print = message

		# call the callback
		if not self.mute:
			self.progress_callback(message, value, max_value)

	def load(self, filepath, verbose=0, commands=(), mute=False):
		start_time = time.time()
		eof = super().load(filepath)

		# for temporary pyffi compat
		self.user_version = self.flag_2
		self._byte_order = "<"

		# store commands
		self.commands = commands
		self.mute = mute
		# store file name for later
		self.filepath = filepath
		self.dir, self.basename = os.path.split(filepath)
		self.file_no_ext = os.path.splitext(self.filepath)[0]

		# maps OVL hash to final filename + extension
		self.name_hashdict = {}
		# for PZ names
		self.name_list = []

		# add extensions to hash dict
		hm_max = len(self.mimes)
		for hm_index, mime_entry in enumerate(self.mimes):
			self.print_and_callback("Adding extensions to hash dict", value=hm_index, max_value=hm_max)
			# get the whole mime type string
			mime_type = self.names.get_str_at(mime_entry.offset)
			# only get the extension
			mime_entry.ext = mime_type.split(":")[-1]
			# the stored mime hash is not used anywhere
			self.name_hashdict[mime_entry.mime_hash] = mime_type
			# instead we must calculate the DJB hash of the extension and store that
			# because this is how we find the extension from inside the archive
			self.name_hashdict[djb(mime_entry.ext)] = mime_entry.ext

		# add file name to hash dict; ignoring the extension pointer
		hf_max = len(self.files)
		for hf_index, file_entry in enumerate(self.files):
			self.print_and_callback("Adding file names to hash dict", value=hf_index, max_value=hf_max)
			# get file name from name table
			file_name = self.names.get_str_at(file_entry.offset)
			self.name_hashdict[file_entry.file_hash] = file_name
			# there seems to be no need for now to link the two
			file_entry.ext = self.mimes[file_entry.extension].ext
			file_entry.name = file_name
			self.name_list.append(file_name)
		# print(file_name+"."+file_entry.ext , file_entry.unkn_0, file_entry.unkn_1)
		# return
		# print(self.name_hashdict)

		# create directories
		hd_max = len(self.dirs)
		for hd_index, dir_entry in enumerate(self.dirs):
			self.print_and_callback("Creating directories", value=hd_index, max_value=hd_max)
			# get dir name from name table
			dir_name = self.names.get_str_at(dir_entry.offset)
		# fix up the name
		# dir = os.path.normpath(os.path.join(os.getcwd(), dir_name.lstrip("..\\")))
		# create dir, do nothing if it already exists
		# os.makedirs(dir, exist_ok=True)
		# print(dir)

		# get names of all texture assets
		ht_max = len(self.textures)
		for ht_index, texture_entry in enumerate(self.textures):
			self.print_and_callback("Getting texture asset names", value=ht_index, max_value=ht_max)
			# nb. 4 unknowns per texture
			try:
				texture_entry.name = self.name_hashdict[texture_entry.file_hash]
			except:
				# this seems to happen for main.ovl - external textures?
				texture_entry.name = "bad hash"
		# print(name, texture_entry.unknown_1, texture_entry.unknown_2, texture_entry.unknown_3, texture_entry.unknown_4, texture_entry.unknown_5, texture_entry.unknown_6)#, texture_entry.unknown_7)

		# print(sorted(set([t.unknown_6 for t in self.ovl.textures])))
		# print(textures)
		self.ovs_files = []
		ha_max = len(self.archives)
		for archive_index, archive_entry in enumerate(self.archives):
			self.print_and_callback("Extracting archives", value=archive_index, max_value=ha_max)
			archive_entry.name = self.archive_names.get_str_at(archive_entry.offset)
			self.print_and_callback(f"Reading archive {archive_entry.name}")
			# skip archives that are empty
			if archive_entry.compressed_size == 0 and self.flag_2 == 8212:
				print("archive is not compressed")
			elif archive_entry.compressed_size == 0:
				print("archive is empty")
				continue
			# those point to external ovs archives
			if archive_index > 0:
				# JWE style
				if self.flag_2 == 24724:
					archive_entry.ovs_path = self.file_no_ext + ".ovs." + archive_entry.name.lower()
				# PZ Style
				elif self.flag_2 == 8340:
					archive_entry.ovs_path = self.file_no_ext + ".ovs"
				else:
					print("unsupported flag_2", self.flag_2)
					return
				# make sure that the ovs exists
				if not os.path.exists(archive_entry.ovs_path):
					raise FileNotFoundError("OVS file not found. Make sure is is here: \n" + archive_entry.ovs_path)
				read_start = archive_entry.read_start
			else:
				print("Internal OVS data")
				read_start = eof
				archive_entry.ovs_path = self.filepath
			archive = OvsFile(self, archive_entry, archive_index)

			archive.unzip(archive_entry.ovs_path, read_start, self.flag_2, archive_entry.compressed_size)

			self.ovs_files.append(archive)

		# find texstream buffers
		tb_max = len(self.ovs_files[0].sized_str_entries)
		for tb_index, sized_str_entry in enumerate(self.ovs_files[0].sized_str_entries):
			# self.print_and_callback("Finding texstream buffers", value=tb_index, max_value=tb_max)
			if sized_str_entry.ext == "tex":
				for lod_i in range(3):
					for archive in self.ovs_files[1:]:
						for other_sizedstr in archive.sized_str_entries:
							if sized_str_entry.basename in other_sizedstr.name and "_lod" + str(
									lod_i) in other_sizedstr.name:
								sized_str_entry.data_entry.buffers.extend(other_sizedstr.data_entry.buffers)

		# postprocessing of data buffers
		for archive in self.ovs_files:
			for data_entry in archive.data_entries:
				# just sort buffers by their index value
				data_entry.update_buffers()

		print(time.time() - start_time)

	def save(self, filepath, ):
		"""Write a dds file."""

		print("Writing OVL")

		exp_dir = os.path.dirname(filepath)
		ovs_dict = {}
		# compress data stream
		for i, (archive_entry, archive) in enumerate(zip(self.archives, self.ovs_files)):
			# write archive into bytes IO stream
			archive_entry.uncompressed_size, archive_entry.compressed_size, compressed = archive.zipper()
			if i == 0:
				ovl_compressed = compressed
				archive_entry.read_start = 0
			else:
				exp_path = os.path.join(exp_dir, os.path.basename(archive_entry.ovs_path))
				# gotta keep them open because more than one archive can live in one ovs file eg PZ inspector
				if exp_path not in ovs_dict:
					ovs_dict[exp_path] = open(exp_path, 'wb')

				# todo: account for OVS offsets specified in archive_entry
				# todo: footer bytes in OVS?
				ovs_stream = ovs_dict[exp_path]

				archive_entry.read_start = ovs_stream.tell()
				ovs_stream.write(compressed)

		# we don't use context manager so gotta close them
		for ovs_file in ovs_dict.values():
			ovs_file.close()

		print("Updating AUX sizes in OVL")
		for aux in self.aux_entries:
			name = self.files[aux.file_index].name
			if aux.extension_index != 0:
				bnkpath = f"{self.file_no_ext}_{name}_bnk_s.aux"
			else:
				bnkpath = f"{self.file_no_ext}_{name}_bnk_b.aux"

			# grab and update size
			if os.path.isfile(bnkpath):
				aux.size = os.path.getsize(bnkpath)
		# print(aux.size)

		eof = super().save(filepath)
		with self.writer(filepath) as stream:
			# first header
			self.write(stream)
			# write zlib block
			stream.write(ovl_compressed)


if __name__ == "__main__":
	bnk = OvlFile()
	bnk.load("C:/Users/arnfi/Desktop/Coding/ovl/OVLs/Parrot.ovl")
	# bnk.load("C:/Users/arnfi/Desktop/Coding/ovl/OVLs/Gharial_Male.ovl")
	# bnk.load("C:/Users/arnfi/Desktop/Coding/ovl/PC_Primitives_01.ovl")
# print(bnk)
