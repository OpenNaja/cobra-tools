import logging

from modules.formats.BaseFormat import BaseFile
import struct


class SpecdefLoader(BaseFile):

	def _get_data(self, file_path):
		"""Loads and returns the data for a specdef"""
		buffer_0 = self.get_content(file_path)
		ss = struct.pack("IIII", len(buffer_0), 16000, 0x00, 0x00)
		return ss, buffer_0

	def create(self):
		# ignore content, just write an empty specdef 
		ss, buffer_0 = self._get_data(self.file_entry.path)
		file_name_bytes = self.file_entry.basename.encode(encoding='utf8')

		pool_index, pool = self.get_pool(2)
		offset = pool.data.tell()

		# add empty specdef, 64b size struct
		#empty_buffer  = struct.pack("<64s", b'') # empty buffer
		empty_buffer  = struct.pack("<2sH60s",b'',101, b'') # Set flags to 1

		#empty_buffer  = struct.pack("<6sB57s", b'',1,b'') #managers
		#empty_buffer  = struct.pack("<7sB56s", b'',1,b'')  # scripts
		pool.data.write(empty_buffer) 

		dpool_index, dpool = self.get_pool(2)
		doffset = dpool.data.tell()

		# add empty data buffer for now
		empty_data    = struct.pack("<I4s", 0x87126e, b'') 
		dpool.data.write(empty_data)  
		luaoffset = dpool.data.tell()
		dpool.data.write(b"building")  
		dpool.data.write(b'')
		pluaoffset = dpool.data.tell()
		dpool.data.write(struct.pack("<8s", b''))
		# add space for the lua ptr


		# add three required fragments for the specdef
		# ignoring the current specdef struct, point all
		# fragments to the beginning of the buffer
		new_frag0 = self.create_fragment()
		new_frag0.pointers[0].pool_index = pool_index
		new_frag0.pointers[0].data_offset = offset + 0x08
		new_frag0.pointers[1].pool_index = dpool_index
		new_frag0.pointers[1].data_offset = doffset + 0x00
		new_frag1 = self.create_fragment()
		new_frag1.pointers[0].pool_index = pool_index
		new_frag1.pointers[0].data_offset = offset + 0x10
		new_frag1.pointers[1].pool_index = dpool_index
		new_frag1.pointers[1].data_offset = doffset + 0x00
		new_frag2 = self.create_fragment()
		new_frag2.pointers[0].pool_index = pool_index
		new_frag2.pointers[0].data_offset = offset + 0x18
		new_frag2.pointers[1].pool_index = dpool_index
		new_frag2.pointers[1].data_offset = doffset + 0x00

		if False: #commented out, used to test adding Feature or Dependencies
			## this is the pointer to the lua string
			new_frag3 = self.create_fragment()
			new_frag3.pointers[0].pool_index = dpool_index
			new_frag3.pointers[0].data_offset = pluaoffset
			new_frag3.pointers[1].pool_index = dpool_index
			new_frag3.pointers[1].data_offset = luaoffset


			## this is the pointer to the lua list
			new_frag4 = self.create_fragment()
			new_frag4.pointers[0].pool_index = pool_index
			new_frag4.pointers[0].data_offset = offset + 0x38
			new_frag4.pointers[1].pool_index = dpool_index
			new_frag4.pointers[1].data_offset = pluaoffset

		self.sized_str_entry = self.create_ss_entry(self.file_entry)
		self.sized_str_entry.pointers[0].pool_index = pool_index
		self.sized_str_entry.pointers[0].data_offset = offset

	def collect(self):
		self.assign_ss_entry()
		ss_pointer = self.sized_str_entry.pointers[0]
		logging.info(f"SPECDEF: {self.sized_str_entry.name}")
		ss_data = struct.unpack("<2H4B", ss_pointer.data)
		logging.info(f"{ss_data}")
		if ss_data[0] == 0:
			logging.info(f"spec is zero ")
		self.sized_str_entry.fragments = self.ovs.frags_from_pointer(ss_pointer, 3, reuse=False)
		logging.info(f"SPECDEF fragments: {self.sized_str_entry.fragments}")
		attrib_count = ss_data[0]
		conditions = ss_data[2:]
		self.condition_frags = []
		for condition in conditions:
			if condition > 0:
				frag = self.ovs.frags_from_pointer(ss_pointer, 1, reuse=False)[0]
				self.sized_str_entry.fragments.append(frag)
				# logging.debug(frag.pointers[0].data)
				self.condition_frags.append(frag)
			else:
				self.condition_frags.append(None)

		self.attrib_names = self.ovs.frags_from_pointer(self.sized_str_entry.fragments[1].pointers[1], attrib_count, reuse=False)
		self.attrib_datas = self.ovs.frags_from_pointer(self.sized_str_entry.fragments[2].pointers[1], attrib_count, reuse=False)
		self.sized_str_entry.fragments.extend(self.attrib_names + self.attrib_datas)

		for cond_frag, cond_count in zip(self.condition_frags, conditions):
			if cond_frag:
				cond_frag.child_frags = self.ovs.frags_from_pointer(cond_frag.pointers[1], cond_count, reuse=False)
				self.sized_str_entry.fragments.extend(cond_frag.child_frags)

	def extract(self, out_dir, show_temp_files, progress_callback):
		name = self.sized_str_entry.name
		logging.info(f"Writing {name}")

		ovl_header = self.pack_header(b"SPEC")
		out_path = out_dir(name)

		# save .bin data
		with open(out_path + ".bin", 'wb') as outfile:
			logging.warning("Exporting binary specdef file")
			logging.warning(f"SPECDEF: {self.sized_str_entry.pointers}")
			logging.warning(f"SPECDEF: {self.sized_str_entry.fragments}")
			logging.warning(f"SPECDEF: {self.sized_str_entry.pointers[0].data}")
			outfile.write(ovl_header)
			outfile.write(self.sized_str_entry.pointers[0].data)
			for f in self.sized_str_entry.fragments:
				logging.warning(f"SPECDEF: dumping pool type {f}")

				outfile.write(f.pointers[1].data)
			outfile.close()

		# save .text file
		with open(out_path, 'w') as outfile:
			logging.debug("Exporting text specdef file")
			attrib_count, flags, name_count, childspec_count, manager_count, script_count = struct.unpack(
				"<2H4B", self.sized_str_entry.pointers[0].data)
			outfile.write(f"Name : {name}\nFlags: {flags:x}\n")

			if self.attrib_names:
				outfile.write(f"Attributes:\n")
				# this frag has padding
				dtypes = struct.unpack(f"<{attrib_count}I", self.sized_str_entry.fragments[0].pointers[1].data[:4 * attrib_count])

				for attrib_name, attrib_data, dtype in zip(self.attrib_names, self.attrib_datas, dtypes):
					iname = attrib_name.pointers[1].data.decode().rstrip('\x00')
					# the tflags structure depends on the dtype value
					tflags = attrib_data.pointers[1].data
					# 00 boolean(true or false)
					# 01 Unused
					# 02 Unused
					# 03 UInt8(I think)
					# 04 Unused
					#                                                                DeTy
					# 05 Enum type({Default =, Enum = filename, Type = "uint8"} 00ff02010000000000000000000000000000000000000000
					# 06 Uint64 with dependencies({Type = "uint64", Default = 0})
					# 07 table ( or String List) (list of ptr)  00000000ffffffff0000000001 << this to 1 seen when it can be just a string (no list)
					# 08 uint64 (used for entities as well)
					# 09 float
					# 10 string (expected ptr)
					# 11 Vector2
					# 12 Vector3
					# 13 String list (0000000000000000 0a < could be max)
					# 14 table
					# 15 String or table
					# 16 also string

					try:
						if dtype == 0:
							# boot on the second byte, todo maybe more
							tflags = bool(tflags[1])
						elif dtype == 3:
							# int16
							tflags = struct.unpack("8h", tflags[:16])
						# elif dtype == 5:
						# 	# boot on the second byte,
						# 	logging.info(f"type 5 {tflags}")
						elif dtype == 9:
							# lower_bound, upper_bound, float, 1
							tflags = struct.unpack("3fI", tflags[:16])
						elif dtype == 11:
							# vector2 float, 1, 0 (padding?)
							tflags = struct.unpack("2fII", tflags[:16])
						elif dtype == 12:
							# vector3 float, 1
							tflags = struct.unpack("3fI", tflags[:16])
					except:
						logging.warning(f"Unexpected data {tflags} (size: {len(tflags)}) for type {dtype}")
					outstr = f" - Type: {dtype:02} Name: {iname}  Flags: {tflags}"
					logging.debug(outstr)
					outfile.write(outstr + "\n")

			condition_names = ("Name", "Child Specdef", "Manager", "Script")
			for cond_frag, cond_name in zip(self.condition_frags, condition_names):
				if cond_frag:
					outfile.write(f"{cond_name}s:\n")
					for child_frag in cond_frag.child_frags:
						iname = child_frag.pointers[1].data.decode().rstrip('\x00')
						outstr = f" - {cond_name}: {iname}"
						outfile.write(outstr + "\n")

		return out_path + ".bin", out_path,

