import logging
import xml.etree.ElementTree as ET

from generated.formats.uimoviedefinition.compound.UiMovieHeader import UiMovieHeader
from modules.formats.BaseFormat import BaseFile
from modules.helpers import as_bytes


class UIMovieDefinitionLoader(BaseFile):

	def extract(self, out_dir, show_temp_files, progress_callback):
		name = self.sized_str_entry.name
		out_path = out_dir(name)
		self.header.to_xml_file(out_path)
		return out_path,

	# def create(self):
	# 	self.sized_str_entry = self.create_ss_entry(self.file_entry)
	#
	# 	xml = self.load_xml(self.file_entry.path)
	# 	self.ui_names = [data.text for data in xml.findall('.//Control')]
	# 	self.assetpkgs = [data.text for data in xml.findall('.//AssetPackage')]
	# 	self.ui_triggers = [data.text for data in xml.findall('.//UITrigger')]
	# 	self.ui_interfaces = [data.text for data in xml.findall('.//Interface')]
	# 	self.Count1List = [int(data.text) for data in xml.findall('.//List1')]
	# 	self.Count2List = [int(data.text) for data in xml.findall('.//List2')]
	#
	# 	self.header = UiMovieHeader(self.ovl.context)
	# 	self.header.flag_1 = int(xml.attrib['flags1'])
	# 	self.header.flag_2 = int(xml.attrib['flags2'])
	# 	self.header.flag_3 = int(xml.attrib['flags3'])
	# 	self.header.floats[0] = float(xml.attrib['float1'])
	# 	self.header.floats[1] = float(xml.attrib['float2'])
	# 	self.header.floats[2] = float(xml.attrib['float3'])
	# 	self.header.num_ui_triggers = len(self.ui_triggers)
	# 	self.header.num_ui_names = len(self.ui_names)
	# 	self.header.num_assetpkgs = len(self.assetpkgs)
	# 	self.header.num_ui_names = len(self.ui_names)
	# 	self.header.num_list_1 = len(self.Count1List)
	# 	self.header.num_list_2 = len(self.Count2List)
	# 	self.header.num_ui_interfaces = len(self.ui_interfaces)
	# 	ss_ptr = self.sized_str_entry.pointers[0]
	# 	self.write_to_pool(ss_ptr, 2, as_bytes(self.header))
	#
	# 	# attach all the data
	# 	self.write_str_at_rel_offset(ss_ptr, 0, xml.attrib['MovieName'])
	# 	self.write_str_at_rel_offset(ss_ptr, 8, xml.attrib['PkgName'])
	# 	self.write_str_at_rel_offset(ss_ptr, 16, xml.attrib['CategoryName'])
	# 	self.write_str_at_rel_offset(ss_ptr, 24, xml.attrib['TypeName'])
	# 	self.write_str_list_at_rel_offset(ss_ptr, 72, self.ui_triggers)
	# 	self.write_str_list_at_rel_offset(ss_ptr, 88, self.ui_names)
	# 	self.write_str_list_at_rel_offset(ss_ptr, 96, self.assetpkgs)
	# 	self.write_int_list_at_rel_offset(ss_ptr, 112, self.Count1List)
	# 	self.write_int_list_at_rel_offset(ss_ptr, 120, self.Count2List)
	# 	self.write_str_list_at_rel_offset(ss_ptr, 128, self.ui_interfaces)
	#

	def collect(self):
		self.assign_ss_entry()
		ss_ptr = self.sized_str_entry.pointers[0]
		self.header = UiMovieHeader.from_stream(ss_ptr.stream, self.ovl.context)
		self.header.read_ptrs(self.ovs, ss_ptr, self.sized_str_entry)
		print(self.header)
		# self.header = self.sized_str_entry.pointers[0].load_as(UiMovieHeader)[0]
		#
		# self.MovieName = self.get_str_at_offset(0)
		# self.PkgName = self.get_str_at_offset(8)
		# self.CategoryName = self.get_str_at_offset(16)
		# self.TypeName = self.get_str_at_offset(24)
		# self.ui_triggers = self.get_str_list_at_offset(self.header.num_ui_triggers, 72)
		# self.ui_names = self.get_str_list_at_offset(self.header.num_ui_names, 88)
		# self.assetpkgs = self.get_str_list_at_offset(self.header.num_assetpkgs, 96)
		# self.Count1List = self.get_int_list_at_offset(self.header.num_list_1, 112)
		# self.Count2List = self.get_int_list_at_offset(self.header.num_list_2, 120)
		# self.ui_interfaces = self.get_str_list_at_offset(self.header.num_ui_interfaces, 128)
	#
	# def extract(self, out_dir, show_temp_files, progress_callback):
	# 	name = self.sized_str_entry.name
	# 	logging.info(f"Writing {name}")
	#
	# 	xml = ET.Element('UIMovieDefinition')
	# 	xml.set('MovieName', str(self.MovieName))
	# 	xml.set('PkgName', str(self.PkgName))
	# 	xml.set('CategoryName', str(self.CategoryName))
	# 	xml.set('TypeName', str(self.TypeName))
	# 	xml.set('flags1', str(self.header.flag_1))
	# 	xml.set('flags2', str(self.header.flag_2))
	# 	xml.set('flags3', str(self.header.flag_3))
	# 	xml.set('float1', str(self.header.floats[0]))
	# 	xml.set('float2', str(self.header.floats[1]))
		# xml.set('float3', str(self.header.floats[2]))
		#
		# for cl in self.ui_triggers:
		# 	clitem = ET.SubElement(xml, 'UITrigger')
		# 	clitem.text = cl
		#
		# for cl in self.ui_names:
		# 	clitem = ET.SubElement(xml, 'Control')
		# 	clitem.text = cl
		#
		# for cl in self.assetpkgs:
		# 	clitem = ET.SubElement(xml, 'AssetPackage')
		# 	clitem.text = cl
		#
		# for cl in self.ui_interfaces:
		# 	clitem = ET.SubElement(xml, 'Interface')
		# 	clitem.text = cl
		#
		# for cl in self.Count1List:
		# 	clitem = ET.SubElement(xml, 'List1')
		# 	clitem.text = str(cl)
		#
		# for cl in self.Count2List:
		# 	clitem = ET.SubElement(xml, 'List2')
		# 	clitem.text = str(cl)
		#
		# out_path = out_dir(name)
		# self.write_xml(out_path, xml)
		# return out_path,
