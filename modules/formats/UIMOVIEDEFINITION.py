import logging
import struct

from generated.formats.uimoviedefinition.compound.UiMovieHeader import UiMovieHeader
from modules.formats.BaseFormat import BaseFile
from modules.helpers import as_bytes
import xml.etree.ElementTree as ET  # prob move this to a custom modules.helpers or utils?


class UIMovieDefinitionLoader(BaseFile):

	# the final format will be after the 3 float values there are 12 count (bytes) values, and 
	# then 10 ptr values (one for each count in order), however all uimoviedefinition in jwe1/2
	# have most of these counters to 0 so their ptr type is unknown.

	def create(self):
		self.sized_str_entry = self.create_ss_entry(self.file_entry)

		moviedef = self.load_xml(self.file_entry.path)

		namelistdata = moviedef.findall('.//Name')
		names = []
		for name in namelistdata:
			names.append(name.text)

		self.ui_names = [data.text for data in moviedef.findall('.//Control')]
		self.assetpkgs = [data.text for data in moviedef.findall('.//AssetPackage')]
		self.ui_triggers = [data.text for data in moviedef.findall('.//UITrigger')]
		self.ui_interfaces = [data.text for data in moviedef.findall('.//Interface')]
		self.Count1List = [int(data.text) for data in moviedef.findall('.//List1')]
		self.Count2List = [int(data.text) for data in moviedef.findall('.//List2')]

		self.header = UiMovieHeader(self.ovl.context)
		self.header.flag_1 = int(moviedef.attrib['flags1'])
		self.header.flag_2 = int(moviedef.attrib['flags2'])
		self.header.flag_3 = int(moviedef.attrib['flags3'])
		self.header.floats[0] = float(moviedef.attrib['float1'])
		self.header.floats[1] = float(moviedef.attrib['float2'])
		self.header.floats[2] = float(moviedef.attrib['float3'])
		self.header.num_ui_triggers = len(self.ui_triggers)
		self.header.num_ui_names = len(self.ui_names)
		self.header.num_assetpkgs = len(self.assetpkgs)
		self.header.num_ui_names = len(self.ui_names)
		self.header.num_list1 = len(self.Count1List)
		self.header.num_list2 = len(self.Count2List)
		self.header.num_ui_interfaces = len(self.ui_interfaces)
		self.write_to_pool(self.sized_str_entry.pointers[0], 2, as_bytes(self.header))

		# main names list
		data = (moviedef.attrib['MovieName'], moviedef.attrib['PkgName'], moviedef.attrib['CategoryName'], moviedef.attrib['TypeName'])
		self.link_list_at_rel_offset(data, self.sized_str_entry.pointers[0], 0)

		# Up to here should be enough to build almost any movie without list
		# time now to attach all the lists
		self.write_list_at_rel_offset(self.ui_triggers, self.sized_str_entry.pointers[0], 72)
		self.write_list_at_rel_offset(self.ui_names, self.sized_str_entry.pointers[0], 88)
		self.write_list_at_rel_offset(self.assetpkgs, self.sized_str_entry.pointers[0], 96)

		if len(self.Count1List):
			new_frag1 = self.create_fragments(self.sized_str_entry, 1)[0]
			self.ptr_relative(new_frag1.pointers[0], self.sized_str_entry.pointers[0], 112)
			itembytes = b''
			for item in self.Count1List:
				itembytes += struct.pack("<I", int(item))
			if len(self.Count1List) < 4:
				padding = 4*(4 - len(self.Count1List))
				itembytes += struct.pack(f"<{padding}s", b'')
			self.write_to_pool(new_frag1.pointers[1], 2, itembytes)

		if len(self.Count2List):
			# point the list frag to the end of the data now.
			new_frag1 = self.create_fragments(self.sized_str_entry, 1)[0]
			self.ptr_relative(new_frag1.pointers[0], self.sized_str_entry.pointers[0], 120)
			itembytes = b''
			for item in self.Count2List:
				itembytes += struct.pack("<I", int(item))
			if len(self.Count2List) < 4:
				padding = 4*(4 - len(self.Count2List))
				itembytes += struct.pack(f"<{padding}s", b'')
			self.write_to_pool(new_frag1.pointers[1], 2, itembytes)

		self.write_list_at_rel_offset(self.ui_interfaces, self.sized_str_entry.pointers[0], 128)

	def link_list_at_rel_offset(self, items_list, ref_ptr, rel_offset):
		"""Links a list of pointers relative to rel_offset to the items"""
		frags = self.create_fragments(self.sized_str_entry, len(items_list))
		for item, frag in zip(items_list, frags):
			self.ptr_relative(frag.pointers[0], ref_ptr, rel_offset=rel_offset)
			rel_offset += 8
			self.write_to_pool(frag.pointers[1], 2, as_bytes(item))

	def write_list_at_rel_offset(self, items_list, ref_ptr, rel_offset):
		"""Writes a list of pointers and items, and reference it from a ptr at rel_offset from the ref_ptr"""
		if items_list:
			# for each line, add the frag ptr space and create the frag ptr
			item_frags = self.create_fragments(self.sized_str_entry, len(items_list))
			for frag in item_frags:
				self.write_to_pool(frag.pointers[0], 2, b"\x00" * 8)
			for item, frag in zip(items_list, item_frags):
				self.write_to_pool(frag.pointers[1], 2, as_bytes(item))
			# point the list frag to the end of the data now.
			new_frag1 = self.create_fragments(self.sized_str_entry, 1)[0]
			self.ptr_relative(new_frag1.pointers[0], ref_ptr, rel_offset)
			self.ptr_relative(new_frag1.pointers[1], item_frags[0].pointers[0])

	def collect(self):
		self.assign_ss_entry()
		logging.info(f"Collecting {self.sized_str_entry.name}")

		self.header = self.sized_str_entry.pointers[0].load_as(UiMovieHeader)

		# get name
		frags = self.ovs.frags_from_pointer(self.sized_str_entry.pointers[0], 4)[0]
		self.MovieName = self.p1_ztsr(frags[0])
		self.PkgName = self.p1_ztsr(frags[1])
		self.CategoryName = self.p1_ztsr(frags[2])
		self.TypeName = self.p1_ztsr(frags[3])

		self.ui_triggers = self.get_string_list(self.header.num_ui_triggers)
		self.ui_names = self.get_string_list(self.header.num_ui_names)
		self.assetpkgs = self.get_string_list(self.header.num_assetpkgs)

		self.Count1List = []
		if self.header.num_list1:
			tmpfragment = self.ovs.frags_from_pointer(self.sized_str_entry.pointers[0], 1)[0]
			self.Count1List = list(struct.unpack(f"<{self.header.num_list1}I", tmpfragment.pointers[1].read_from_pool(0x4 * self.header.num_list1)))
		
		self.Count2List = []
		if self.header.num_list2:
			tmpfragment = self.ovs.frags_from_pointer(self.sized_str_entry.pointers[0], 1)[0]
			self.Count2List = list(struct.unpack(f"<{self.header.num_list2}I", tmpfragment.pointers[1].read_from_pool(0x4 * self.header.num_list2)))

		self.ui_interfaces = self.get_string_list(self.header.num_ui_interfaces)

	def get_string_list(self, count):
		# todo - this assumes the pointer exists if the count exists, and relies on the correct call order
		# change to get frag at offset?
		output = []
		if count:
			link_frag = self.ovs.frags_from_pointer(self.sized_str_entry.pointers[0], 1)[0]
			tmp_fragments = self.ovs.frags_from_pointer(link_frag.pointers[1], self.header.num_ui_interfaces)
			for frag in tmp_fragments:
				output.append(self.p1_ztsr(frag))
		return output

	def extract(self, out_dir, show_temp_files, progress_callback):
		name = self.sized_str_entry.name
		logging.info(f"Writing {name}")

		xmldata = ET.Element('UIMovieDefinition')
		xmldata.set('MovieName', str(self.MovieName))
		xmldata.set('PkgName', str(self.PkgName))
		xmldata.set('CategoryName', str(self.CategoryName))
		xmldata.set('TypeName', str(self.TypeName))
		xmldata.set('flags1', str(self.header.flag_1))
		xmldata.set('flags2', str(self.header.flag_2))
		xmldata.set('flags3', str(self.header.flag_3))
		xmldata.set('float1', str(self.header.floats[0]))
		xmldata.set('float2', str(self.header.floats[1]))
		xmldata.set('float3', str(self.header.floats[2]))

		for cl in self.ui_triggers:
			clitem = ET.SubElement(xmldata, 'UITrigger')
			clitem.text = cl

		for cl in self.ui_names:
			clitem = ET.SubElement(xmldata, 'Control')
			clitem.text = cl

		for cl in self.assetpkgs:
			clitem = ET.SubElement(xmldata, 'AssetPackage')
			clitem.text = cl

		for cl in self.ui_interfaces:
			clitem = ET.SubElement(xmldata, 'Interface')
			clitem.text = cl

		for cl in self.Count1List:
			clitem = ET.SubElement(xmldata, 'List1')
			clitem.text = str(cl)

		for cl in self.Count2List:
			clitem = ET.SubElement(xmldata, 'List2')
			clitem.text = str(cl)

		out_path = out_dir(name)
		self.write_xml(out_path, xmldata)
		return out_path,
