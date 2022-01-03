import logging
import xml.etree.ElementTree as ET  # prob move this to a custom modules.helpers or utils?

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
		# empty_buffer  = struct.pack("<64s", b'') # empty buffer
		empty_buffer = struct.pack("<2sH60s", b'', 101, b'')  # Set flags to 1

		# empty_buffer  = struct.pack("<6sB57s", b'',1,b'') #managers
		# empty_buffer  = struct.pack("<7sB56s", b'',1,b'')  # scripts
		pool.data.write(empty_buffer)

		dpool_index, dpool = self.get_pool(2)
		doffset = dpool.data.tell()

		# add empty data buffer for now
		empty_data = struct.pack("<I4s", 0x87126e, b'')
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

		if False:  # commented out, used to test adding Feature or Dependencies
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
		logging.info(f"Collecting specdef: {self.sized_str_entry.name}")

		ss_data = struct.unpack("<2H4B", ss_pointer.data)
		logging.info(f"{ss_data}")
		# if ss_data[0] == 0:
		# 	logging.info(f"specdef has no attributes")
		# we always have 3 fragments for attributes, even if there are none
		self.sized_str_entry.fragments = self.ovs.frags_from_pointer(ss_pointer, 3)

		attrib_count = ss_data[0]
		lists = ss_data[2:]
		logging.debug(f"SPECDEF lists: {lists}")
		self.lists_frags = []
		for listItems in lists:
			if listItems > 0:
				frag = self.ovs.frags_from_pointer(ss_pointer, 1)[0]
				self.sized_str_entry.fragments.append(frag)
				self.lists_frags.append(frag)
			else:
				self.lists_frags.append(None)

		self.attributes = []
		# this frag has padding
		self.dtypes = struct.unpack(f"<{attrib_count}I",
									self.sized_str_entry.fragments[0].pointers[1].data[:4 * attrib_count])
		self.attrib_names = self.ovs.frags_from_pointer(self.sized_str_entry.fragments[1].pointers[1], attrib_count)
		self.attrib_datas = self.ovs.frags_from_pointer(self.sized_str_entry.fragments[2].pointers[1], attrib_count)
		# get any default data linked to in data pointers
		for attrib_name, attrib_data, dtype in zip(self.attrib_names, self.attrib_datas, self.dtypes):
			attrib_default = None
			dep = None
			if dtype == 5:
				for dep in self.file_entry.dependencies:
					# there may be more possible offsets
					if dep.pointers[0].data_offset == attrib_data.pointers[1].data_offset + 8:
						# attrib_default = dep
						break
				# iname = self.get_zstr(attrib_name.pointers[1].data)
				# d = None
				# if attrib_default:
				# 	d = attrib_default.name
				# logging.debug(f"TEST {iname} {attrib_data.pointers[1].data} {d}")
			if dtype == 10:
				attrib_default = self.ovs.frag_at_pointer(attrib_data.pointers[1], offset=0)

			self.attributes.append((dtype, attrib_name, attrib_data, attrib_default, dep))

		self.sized_str_entry.fragments.extend(self.attrib_names + self.attrib_datas)

		for list_frag, list_count in zip(self.lists_frags, lists):
			if list_frag:
				list_frag.child_frags = self.ovs.frags_from_pointer(list_frag.pointers[1], list_count)
				self.sized_str_entry.fragments.extend(list_frag.child_frags)

	def extract(self, out_dir, show_temp_files, progress_callback):
		name = self.sized_str_entry.name
		logging.info(f"Writing {name}")

		ovl_header = self.pack_header(b"SPEC")
		out_path = out_dir(name)

		# save .raw data
		with open(out_path, 'wb') as outfile:
			logging.debug("Exporting binary specdef file")
			# logging.debug(f"SPECDEF: {self.sized_str_entry.pointers}")
			# logging.debug(f"SPECDEF: {self.sized_str_entry.fragments}")
			# logging.debug(f"SPECDEF: {self.sized_str_entry.pointers[0].data}")
			outfile.write(ovl_header)
			outfile.write(self.sized_str_entry.pointers[0].data)
			for f in self.sized_str_entry.fragments:
				# logging.debug(f"SPECDEF: dumping pool type {f}")
				outfile.write(f.pointers[1].data)
			outfile.close()

		# save .xml file
		logging.debug("Exporting xml specdef file")
		attrib_count, flags, name_count, childspec_count, manager_count, script_count = struct.unpack(
			"<2H4B", self.sized_str_entry.pointers[0].data)

		xml_data = ET.Element('Specdef')
		xml_data.set('Name', name[:-8])
		xml_data.set('Flags', str(flags))

		if self.attrib_names:
			xml_attribs = ET.SubElement(xml_data, 'Attributes')
			for dtype, attrib_name, attrib_data, attrib_default, dep in self.attributes:
				iname = self.get_zstr(attrib_name.pointers[1].data)
				# the tflags structure depends on the dtype value
				tflags = attrib_data.pointers[1].data
				xml_attrib = ET.SubElement(xml_attribs, 'Attribute')
				xml_attrib.set('Name', iname)
				try:  # all flags data seems to be padded to 8 bytes
					if dep:
						xml_attrib.set('Enum', dep.name)
					if dtype == 0:  # Boolean type
						# 8 bytes of data, only 2 bytes used
						xml_attrib.set('Type', "bool")
						xml_attrib.set('Value', str(bool(tflags[0])))
						xml_attrib.set('Optional', str(bool(tflags[1])))
					elif dtype == 1:  # Unused, int8
						imin, imax, ivalue, ioptional = struct.unpack("<4b", tflags[0:4])
						xml_attrib.set('Type', "int8")
						xml_attrib.set('Min', str(imin))
						xml_attrib.set('Max', str(imax))
						xml_attrib.set('Value', str(ivalue))
						xml_attrib.set('Optional', str(bool(ioptional)))
					elif dtype == 2:  # Unused, int16
						imin, imax, ivalue, ioptional = struct.unpack("<4h", tflags[0:8])
						xml_attrib.set('Type', "int16")
						xml_attrib.set('Min', str(imin))
						xml_attrib.set('Max', str(imax))
						xml_attrib.set('Value', str(ivalue))
						xml_attrib.set('Optional', str(bool(ioptional)))
					elif dtype == 3:  # int32 type
						# 8 ints of data, only five used?
						imin, imax, ivalue, ioptional = struct.unpack("<4i", tflags[0:16])
						xml_attrib.set('Type', "int32")
						xml_attrib.set('Min', str(imin))
						xml_attrib.set('Max', str(imax))
						xml_attrib.set('Value', str(ivalue))
						xml_attrib.set('Optional', str(bool(ioptional)))
					elif dtype == 4:  # Unused, int64
						imin, imax, ivalue, ioptional = struct.unpack("<4q", tflags[0:32])
						xml_attrib.set('Type', "int64")
						xml_attrib.set('Min', str(imin))
						xml_attrib.set('Max', str(imax))
						xml_attrib.set('Value', str(ivalue))
						xml_attrib.set('Optional', str(bool(ioptional)))
					elif dtype == 5:  # UInt8
						# 8 bytes, only 4 used
						imin, imax, ivalue, ioptional = struct.unpack("<4B", tflags[0:4])
						xml_attrib.set('Type', "uint8")
						xml_attrib.set('Min', str(imin))
						xml_attrib.set('Max', str(imax))
						xml_attrib.set('Value', str(ivalue))
						xml_attrib.set('Optional', str(bool(ioptional)))
					elif dtype == 6:  # UInt16
						# 8 short, only 4 used
						imin, imax, ivalue, ioptional = struct.unpack("<4H", tflags[0:8])
						xml_attrib.set('Type', "uint16")
						xml_attrib.set('Min', str(imin))
						xml_attrib.set('Max', str(imax))
						xml_attrib.set('Value', str(ivalue))
						xml_attrib.set('Optional', str(bool(ioptional)))
					elif dtype == 7:  # UInt32 type
						# 8 ints of data, only 4 used?
						imin, imax, ivalue, ioptional = struct.unpack("<4I", tflags[0:16])
						xml_attrib.set('Type', "uint32")
						xml_attrib.set('Min', str(imin))
						xml_attrib.set('Max', str(imax))
						xml_attrib.set('Value', str(ivalue))
						xml_attrib.set('Optional', str(bool(ioptional)))
					elif dtype == 8:  # UInt64 type
						# 8 longs of data, only 4 used?, last one here could just be an int
						imin, imax, ivalue, ioptional = struct.unpack("<4Q", tflags[0:32])
						xml_attrib.set('Type', "uint64")
						xml_attrib.set('Min', str(imin))
						xml_attrib.set('Max', str(imax))
						xml_attrib.set('Value', str(ivalue))
						xml_attrib.set('Optional', str(bool(ioptional)))
					elif dtype == 9:  # Float type
						# 3 floats of data, and 1 int
						imin, imax, ivalue, ioptional = struct.unpack("<3fI", tflags[0:16])
						xml_attrib.set('Type', "float")
						xml_attrib.set('Min', str(imin))
						xml_attrib.set('Max', str(imax))
						xml_attrib.set('Value', str(ivalue))
						xml_attrib.set('Optional', str(bool(ioptional)))
					elif dtype == 10:  # String
						# 1ptr, and 1 int
						iptr, ioptional = struct.unpack("<QI", tflags[0:12])

						# find the default value through the pointed frag, but only if it belongs to this data
						strname = self.get_zstr(attrib_default.pointers[1].data) if attrib_default else ""

						xml_attrib.set('Type', "string")
						xml_attrib.set('Value', strname)
						xml_attrib.set('Optional', str(bool(ioptional)))
					elif dtype == 11:  # Vector2
						# vector2 float, 1, 0 (padding?)
						ix, iy, ioptional = struct.unpack("<2fI", tflags[0:12])
						xml_attrib.set('Type', "Vector2")
						xml_attrib.set('Value', f"({ix},{iy})")
						xml_attrib.set('Optional', str(bool(ioptional)))
					elif dtype == 12:  # Vector3
						# vector3 float, 1
						ix, iy, iz, ioptional = struct.unpack("<3fI", tflags[0:16])
						xml_attrib.set('Type', "Vector3")
						xml_attrib.set('Value', f"({ix},{iy},{iz})")
						xml_attrib.set('Optional', str(bool(ioptional)))
					else:
						xml_attrib.set('dType', str(dtype))  # remove once finished
						xml_attrib.set('Flags', str(tflags))  # remove once finished
				except:
					logging.warning(f"Unexpected data {tflags} (size: {len(tflags)}) for type {dtype}")

		list_names = ("Name", "Requirement", "Manager", "Script")
		for list_frag, list_name in zip(self.lists_frags, list_names):
			if list_frag:
				list_xml = ET.SubElement(xml_data, f"{list_name}s")
				for child_frag in list_frag.child_frags:
					iname = child_frag.pointers[1].data.decode().rstrip('\x00')
					item_xml = ET.SubElement(list_xml, list_name)
					item_xml.text = iname

		self.write_xml(out_path + ".xml", xml_data)

		return out_path + ".xml", out_path,
