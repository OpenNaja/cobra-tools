import logging
import xml.etree.ElementTree as ET  # prob move this to a custom modules.helpers or utils?

from generated.formats.specdef.compound.SpecdefRoot import SpecdefRoot
from modules.formats.BaseFormat import MemStructLoader
from modules.helpers import as_bytes
import struct


class SpecdefLoader(MemStructLoader):
	target_class = SpecdefRoot
	extension = ".specdef"

	# def create(self):
	# 	# Note: this version of create ignores specdef attributes
	# 	self.sized_str_entry = self.create_ss_entry(self.file_entry)
	# 	specdef = self.load_xml(self.file_entry.path)
	#
	# 	namelistdata = specdef.findall('.//Name')
	# 	names = []
	# 	for name in namelistdata:
	# 		names.append(name.text)
	#
	# 	attrib_count = 0
	# 	name_count = len(names)
	# 	childspec_count = 0
	# 	manager_count = 0
	# 	script_count = 0
	# 	ss = struct.pack("<2H4B 7Q", attrib_count, int(specdef.attrib['Flags']), name_count, childspec_count, manager_count, script_count, 0, 0, 0, 0, 0, 0, 0)
	# 	self.write_to_pool(self.sized_str_entry.pointers[0], 2, ss)
	#
	# 	# need to write 3 frags always
	# 	frags = self.create_fragments(self.sized_str_entry, 3)
	# 	self.write_to_pool(frags[0].pointers[0], 2, b"\x00" * 8)
	# 	self.ptr_relative(frags[0].pointers[0], self.sized_str_entry.pointers[0], 8)
	# 	self.ptr_relative(frags[1].pointers[0], self.sized_str_entry.pointers[0], 16)
	# 	self.ptr_relative(frags[2].pointers[0], self.sized_str_entry.pointers[0], 24)
	# 	self.ptr_relative(frags[0].pointers[1], self.sized_str_entry.pointers[0], 64)
	# 	self.ptr_relative(frags[1].pointers[1], self.sized_str_entry.pointers[0], 64)
	# 	self.ptr_relative(frags[2].pointers[1], self.sized_str_entry.pointers[0], 64)
	#
	# 	if len(names) > 0:
	# 		# write features, name count
	# 		root_f = self.create_fragments(self.sized_str_entry, 1)[0]
	# 		self.sized_str_entry.vars = self.create_fragments(self.sized_str_entry, len(names))
	#
	# 		# write the options
	# 		for option, frag in zip(names, self.sized_str_entry.vars):
	# 			self.write_to_pool(frag.pointers[1], 2, as_bytes(option))
	# 		# apparently no padding
	# 		# self.sized_str_entry.vars[-1].pointers[1].pool.pad(alignment=4)
	# 		for frag in self.sized_str_entry.vars:
	# 			self.write_to_pool(frag.pointers[0], 4, b"\x00" * 8)
	# 		self.ptr_relative(root_f.pointers[0], self.sized_str_entry.pointers[0], 32)
	# 		# point to start of options array
	# 		self.ptr_relative(root_f.pointers[1], self.sized_str_entry.vars[0].pointers[0])

	# def collect(self):
	# 	self.assign_ss_entry()
	# 	ss_ptr = self.sized_str_entry.pointers[0]
	# 	logging.info(f"Collecting specdef: {self.sized_str_entry.name}")
	#
	# 	# p0, p1, p2 for attribs
	# 	# p3, p4, p5, p6 only used for each of the 4 counts
	# 	attrib_count, flags, name_count, childspec_count, manager_count, script_count, \
	# 		p0, p1, p2, p3, p4, p5, p6 = struct.unpack("<2H4B 7Q", ss_ptr.data)
	# 	lists = (name_count, childspec_count, manager_count, script_count)
	# 	# logging.info(f"{ss_data}")
	# 	# if ss_data[0] == 0:
	# 	# 	logging.info(f"specdef has no attributes")
	# 	# we always have 3 fragments for attributes, even if there are none
	# 	self.sized_str_entry.fragments = self.ovs.frags_from_pointer(ss_ptr, 3)
	#
	# 	logging.debug(f"SPECDEF lists: {lists}")
	# 	for dep in self.file_entry.dependencies:
	# 		logging.debug(f"SPECDEF dependency: {dep.name}")
	# 	self.lists_frags = []
	# 	for listItems in lists:
	# 		if listItems > 0:
	# 			frag = self.ovs.frags_from_pointer(ss_ptr, 1)[0]
	# 			self.sized_str_entry.fragments.append(frag)
	# 			self.lists_frags.append(frag)
	# 		else:
	# 			self.lists_frags.append(None)
	#
	# 	self.attributes = []
	# 	# this frag has padding
	# 	self.dtypes = struct.unpack(f"<{attrib_count}I",
	# 								self.sized_str_entry.fragments[0].pointers[1].data[:4 * attrib_count])
	# 	self.attrib_names = self.ovs.frags_from_pointer(self.sized_str_entry.fragments[1].pointers[1], attrib_count)
	# 	self.attrib_datas = self.ovs.frags_from_pointer(self.sized_str_entry.fragments[2].pointers[1], attrib_count)
	# 	# get any default data linked to in data pointers
	# 	for attrib_name, attrib_data, dtype in zip(self.attrib_names, self.attrib_datas, self.dtypes):
	# 		attrib_default = None
	# 		# iname = self.get_zstr(attrib_name.pointers[1].data)
	# 		# if dtype == 5:
	# 		# 	tflags = attrib_data.pointers[1].data
	# 		# 	imin, imax, ivalue, ioptional = struct.unpack("<4B", tflags[0:4])
	# 		# 	# logging.debug(f"TEST {iname} {len(attrib_data.pointers[1].data)} {ioptional}")
	# 		dep = None
	# 		if dtype < 9:  # only int types may use enums
	# 			# see if this file has a dependency that starts where the attrib data ends
	# 			ptr = attrib_data.pointers[1]
	# 			for dep in self.file_entry.dependencies:
	# 				# there may be more possible offsets
	# 				if dep.pointers[0].data_offset == ptr.data_offset + ptr.data_size:
	# 					break
	# 			else:
	# 				dep = None
	#
	# 		# TODO: Other types might also have default values, specially 13 and 14
	# 		if dtype == 10 or dtype == 15:
	# 			attrib_default = self.ovs.frag_at_pointer(attrib_data.pointers[1], offset=0)
	#
	# 		if dtype == 13:
	# 			# has a linking frag that points to the dependency ptr
	# 			attrib_link = self.ovs.frag_at_pointer(attrib_data.pointers[1], offset=0)
	# 			ptr = attrib_link.pointers[1]
	# 			for dep in self.file_entry.dependencies:
	# 				if dep.pointers[0].data_offset == ptr.data_offset:
	# 					break
	# 			else:
	# 				dep = None
	#
	# 		if dtype == 14:
	# 			# data frag points to the dependency ptr
	# 			ptr = attrib_data.pointers[1]
	# 			for dep in self.file_entry.dependencies:
	# 				if dep.pointers[0].data_offset == ptr.data_offset:
	# 					break
	# 			else:
	# 				dep = None
	#
	# 		self.attributes.append((dtype, attrib_name, attrib_data, attrib_default, dep))
	#
	# 	self.sized_str_entry.fragments.extend(self.attrib_names + self.attrib_datas)
	#
	# 	for list_frag, list_count in zip(self.lists_frags, lists):
	# 		if list_frag:
	# 			list_frag.child_frags = self.ovs.frags_from_pointer(list_frag.pointers[1], list_count)
	# 			self.sized_str_entry.fragments.extend(list_frag.child_frags)

	# def extract(self, out_dir, show_temp_files, progress_callback):
	# 	name = self.sized_str_entry.name
	# 	logging.info(f"Writing {name}")
	#
	# 	ovl_header = self.pack_header(b"SPEC")
	# 	out_path = out_dir(name)
	#
	# 	ss_ptr = self.sized_str_entry.pointers[0]
	# 	# save .raw data
	# 	with open(out_path, 'wb') as outfile:
	# 		logging.debug("Exporting binary specdef file")
	# 		# logging.debug(f"SPECDEF: {self.sized_str_entry.pointers}")
	# 		# logging.debug(f"SPECDEF: {self.sized_str_entry.fragments}")
	# 		# logging.debug(f"SPECDEF: {self.sized_str_entry.pointers[0].data}")
	# 		outfile.write(ovl_header)
	# 		outfile.write(ss_ptr.data)
	# 		for f in self.sized_str_entry.fragments:
	# 			# logging.debug(f"SPECDEF: dumping pool type {f}")
	# 			outfile.write(f.pointers[1].data)
	# 		outfile.close()
	#
	# 	# save .xml file
	# 	logging.debug("Exporting xml specdef file")
	# 	attrib_count, flags, name_count, childspec_count, manager_count, script_count, \
	# 		p0, p1, p2, p3, p4, p5, p6 = struct.unpack("<2H4B 7Q", ss_ptr.data)
	#
	# 	xml_data = ET.Element('Specdef')
	# 	xml_data.set('Name', name[:-8])
	# 	xml_data.set('Flags', str(flags))
	#
	# 	if self.attrib_names:
	# 		xml_attribs = ET.SubElement(xml_data, 'Attributes')
	# 		for dtype, attrib_name, attrib_data, attrib_default, dep in self.attributes:
	# 			iname = self.get_zstr(attrib_name.pointers[1].data)
	# 			# the tflags structure depends on the dtype value
	# 			tflags = attrib_data.pointers[1].data
	# 			xml_attrib = ET.SubElement(xml_attribs, 'Attribute')
	# 			xml_attrib.set('Name', iname)
	# 			try:  # all flags data seems to be padded to 8 bytes
	# 				if dep:
	# 					xml_attrib.set('Enum', dep.name)
	# 				if dtype == 0:  # Boolean type
	# 					# 8 bytes of data, only 2 bytes used
	# 					xml_attrib.set('Type', "bool")
	# 					xml_attrib.set('Value', str(bool(tflags[0])))
	# 					xml_attrib.set('Optional', str(bool(tflags[1])))
	# 				elif dtype == 1:  # Unused, int8
	# 					imin, imax, ivalue, ioptional = struct.unpack("<4b", tflags[0:4])
	# 					xml_attrib.set('Type', "int8")
	# 					xml_attrib.set('Min', str(imin))
	# 					xml_attrib.set('Max', str(imax))
	# 					xml_attrib.set('Value', str(ivalue))
	# 					xml_attrib.set('Optional', str(bool(ioptional)))
	# 				elif dtype == 2:  # Unused, int16
	# 					imin, imax, ivalue, ioptional = struct.unpack("<4h", tflags[0:8])
	# 					xml_attrib.set('Type', "int16")
	# 					xml_attrib.set('Min', str(imin))
	# 					xml_attrib.set('Max', str(imax))
	# 					xml_attrib.set('Value', str(ivalue))
	# 					xml_attrib.set('Optional', str(bool(ioptional)))
	# 				elif dtype == 3:  # int32 type
	# 					# 8 ints of data, only five used?
	# 					imin, imax, ivalue, ioptional = struct.unpack("<4i", tflags[0:16])
	# 					xml_attrib.set('Type', "int32")
	# 					xml_attrib.set('Min', str(imin))
	# 					xml_attrib.set('Max', str(imax))
	# 					xml_attrib.set('Value', str(ivalue))
	# 					xml_attrib.set('Optional', str(bool(ioptional)))
	# 				elif dtype == 4:  # Unused, int64
	# 					imin, imax, ivalue, ioptional = struct.unpack("<4q", tflags[0:32])
	# 					xml_attrib.set('Type', "int64")
	# 					xml_attrib.set('Min', str(imin))
	# 					xml_attrib.set('Max', str(imax))
	# 					xml_attrib.set('Value', str(ivalue))
	# 					xml_attrib.set('Optional', str(bool(ioptional)))
	# 				elif dtype == 5:  # UInt8
	# 					# 8 bytes, only 4 used
	# 					imin, imax, ivalue, ioptional = struct.unpack("<4B", tflags[0:4])
	# 					xml_attrib.set('Type', "uint8")
	# 					xml_attrib.set('Min', str(imin))
	# 					xml_attrib.set('Max', str(imax))
	# 					xml_attrib.set('Value', str(ivalue))
	# 					xml_attrib.set('Optional', str(bool(ioptional)))
	# 				elif dtype == 6:  # UInt16
	# 					# 8 short, only 4 used
	# 					imin, imax, ivalue, ioptional = struct.unpack("<4H", tflags[0:8])
	# 					xml_attrib.set('Type', "uint16")
	# 					xml_attrib.set('Min', str(imin))
	# 					xml_attrib.set('Max', str(imax))
	# 					xml_attrib.set('Value', str(ivalue))
	# 					xml_attrib.set('Optional', str(bool(ioptional)))
	# 				elif dtype == 7:  # UInt32 type
	# 					# 8 ints of data, only 4 used?
	# 					imin, imax, ivalue, ioptional = struct.unpack("<4I", tflags[0:16])
	# 					xml_attrib.set('Type', "uint32")
	# 					xml_attrib.set('Min', str(imin))
	# 					xml_attrib.set('Max', str(imax))
	# 					xml_attrib.set('Value', str(ivalue))
	# 					xml_attrib.set('Optional', str(bool(ioptional)))
	# 				elif dtype == 8:  # UInt64 type
	# 					# 8 longs of data, only 4 used?, last one here could just be an int
	# 					imin, imax, ivalue, ioptional = struct.unpack("<4Q", tflags[0:32])
	# 					xml_attrib.set('Type', "uint64")
	# 					xml_attrib.set('Min', str(imin))
	# 					xml_attrib.set('Max', str(imax))
	# 					xml_attrib.set('Value', str(ivalue))
	# 					xml_attrib.set('Optional', str(bool(ioptional)))
	# 				elif dtype == 9:  # Float type
	# 					# 3 floats of data, and 1 int
	# 					imin, imax, ivalue, ioptional = struct.unpack("<3fI", tflags[0:16])
	# 					xml_attrib.set('Type', "float")
	# 					xml_attrib.set('Min', str(imin))
	# 					xml_attrib.set('Max', str(imax))
	# 					xml_attrib.set('Value', str(ivalue))
	# 					xml_attrib.set('Optional', str(bool(ioptional)))
	# 				elif dtype == 10:  # String
	# 					# 1ptr, and 1 int
	# 					iptr, ioptional = struct.unpack("<QI", tflags[0:12])
	#
	# 					# find the default value through the pointed frag, but only if it belongs to this data
	# 					strname = self.get_zstr(attrib_default.pointers[1].data) if attrib_default else ""
	#
	# 					xml_attrib.set('Type', "string")
	# 					xml_attrib.set('Value', strname)
	# 					xml_attrib.set('Optional', str(bool(ioptional)))
	# 				elif dtype == 11:  # Vector2
	# 					# vector2 float, 1, 0 (padding?)
	# 					ix, iy, ioptional = struct.unpack("<2fI", tflags[0:12])
	# 					xml_attrib.set('Type', "vector2")
	# 					xml_attrib.set('Value', f"({ix},{iy})")
	# 					xml_attrib.set('Optional', str(bool(ioptional)))
	# 				elif dtype == 12:  # Vector3
	# 					# vector3 float, 1
	# 					ix, iy, iz, ioptional = struct.unpack("<3fI", tflags[0:16])
	# 					xml_attrib.set('Type', "vector3")
	# 					xml_attrib.set('Value', f"({ix},{iy},{iz})")
	# 					xml_attrib.set('Optional', str(bool(ioptional)))
	# 				elif dtype == 13:  # array of items
	# 					iptr, iCType = struct.unpack("<QI", tflags[0:12])
	# 					xml_attrib.set('Type', "array")
	# 					xml_attrib.set('ChildrenType', str(iCType))
	# 				elif dtype == 14:  # Child item
	# 					xml_attrib.set('Type', "struct")
	# 				elif dtype == 15:  # Reference to an object
	# 					# 1ptr, and 1 int
	# 					iptr, ioptional = struct.unpack("<QI", tflags[0:12])
	#
	# 					# find the default value through the pointed frag, but only if it belongs to this data
	# 					strname = self.get_zstr(attrib_default.pointers[1].data) if attrib_default else ""
	#
	# 					xml_attrib.set('Type', "reference")
	# 					xml_attrib.set('Value', strname)
	# 					xml_attrib.set('Optional', str(bool(ioptional)))
	# 				else:
	# 					xml_attrib.set('dType', str(dtype))  # remove once finished
	# 					xml_attrib.set('Flags', str(tflags))  # remove once finished
	# 			except:
	# 				logging.warning(f"Unexpected data {tflags} (size: {len(tflags)}) for type {dtype}")
	#
	# 	list_names = ("Name", "Requirement", "Manager", "Script")
	# 	for list_frag, list_name in zip(self.lists_frags, list_names):
	# 		if list_frag:
	# 			list_xml = ET.SubElement(xml_data, f"{list_name}s")
	# 			for child_frag in list_frag.child_frags:
	# 				iname = child_frag.pointers[1].data.decode().rstrip('\x00')
	# 				item_xml = ET.SubElement(list_xml, list_name)
	# 				item_xml.text = iname
	#
	# 	self.write_xml(out_path + ".xml", xml_data)
	#
	# 	return out_path + ".xml", out_path,
