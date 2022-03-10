import logging
import struct

from generated.formats.uimoviedefinition.compound.UiMovieHeader import UiMovieHeader
from modules.formats.BaseFormat import BaseFile
from modules.helpers import as_bytes
import xml.etree.ElementTree as ET  # prob move this to a custom modules.helpers or utils?


class UIMovieDefinitionLoader(BaseFile):

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
		self.header.num_list_1 = len(self.Count1List)
		self.header.num_list_2 = len(self.Count2List)
		self.header.num_ui_interfaces = len(self.ui_interfaces)
		ss_ptr = self.sized_str_entry.pointers[0]
		self.write_to_pool(ss_ptr, 2, as_bytes(self.header))

		# main names list
		data = (moviedef.attrib['MovieName'], moviedef.attrib['PkgName'], moviedef.attrib['CategoryName'], moviedef.attrib['TypeName'])
		self.link_list_at_rel_offset(data, ss_ptr, 0)

		# Up to here should be enough to build almost any movie without list
		# time now to attach all the lists
		self.write_list_at_rel_offset(self.ui_triggers, ss_ptr, 72)
		self.write_list_at_rel_offset(self.ui_names, ss_ptr, 88)
		self.write_list_at_rel_offset(self.assetpkgs, ss_ptr, 96)

		if len(self.Count1List):
			new_frag1 = self.create_fragments(self.sized_str_entry, 1)[0]
			self.ptr_relative(new_frag1.pointers[0], ss_ptr, 112)
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
			self.ptr_relative(new_frag1.pointers[0], ss_ptr, 120)
			itembytes = b''
			for item in self.Count2List:
				itembytes += struct.pack("<I", int(item))
			if len(self.Count2List) < 4:
				padding = 4*(4 - len(self.Count2List))
				itembytes += struct.pack(f"<{padding}s", b'')
			self.write_to_pool(new_frag1.pointers[1], 2, itembytes)

		self.write_list_at_rel_offset(self.ui_interfaces, ss_ptr, 128)

	def collect(self):
		self.assign_ss_entry()
		logging.info(f"Collecting {self.sized_str_entry.name}")

		self.header = self.sized_str_entry.pointers[0].load_as(UiMovieHeader)[0]

		# get name
		frags = self.ovs.frags_from_pointer(self.sized_str_entry.pointers[0], 4)
		self.MovieName = self.p1_ztsr(frags[0])
		self.PkgName = self.p1_ztsr(frags[1])
		self.CategoryName = self.p1_ztsr(frags[2])
		self.TypeName = self.p1_ztsr(frags[3])

		self.ui_triggers = self.get_string_list(self.header.num_ui_triggers)
		self.ui_names = self.get_string_list(self.header.num_ui_names)
		self.assetpkgs = self.get_string_list(self.header.num_assetpkgs)

		self.Count1List = []
		if self.header.num_list_1:
			tmpfragment = self.ovs.frags_from_pointer(self.sized_str_entry.pointers[0], 1)[0]
			self.Count1List = list(struct.unpack(f"<{self.header.num_list_1}I", tmpfragment.pointers[1].read_from_pool(0x4 * self.header.num_list_1)))
		
		self.Count2List = []
		if self.header.num_list_2:
			tmpfragment = self.ovs.frags_from_pointer(self.sized_str_entry.pointers[0], 1)[0]
			self.Count2List = list(struct.unpack(f"<{self.header.num_list_2}I", tmpfragment.pointers[1].read_from_pool(0x4 * self.header.num_list_2)))

		self.ui_interfaces = self.get_string_list(self.header.num_ui_interfaces)

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
