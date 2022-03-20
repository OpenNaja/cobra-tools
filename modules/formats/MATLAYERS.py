import logging
import struct

from generated.formats.dinosaurmaterialvariants.compound.DinoLayersHeader import DinoLayersHeader
from generated.formats.dinosaurmaterialvariants.compound.DinoPatternsHeader import DinoPatternsHeader
from generated.formats.dinosaurmaterialvariants.compound.DinoVariantsHeader import DinoVariantsHeader
from modules.formats.BaseFormat import BaseFile
import xml.etree.ElementTree as ET  # prob move this to a custom modules.helpers or utils?

from modules.helpers import as_bytes


class MatlayersLoader(BaseFile):

	def collect(self):
		self.assign_ss_entry()
		ss_ptr = self.sized_str_entry.pointers[0]
		self.header = DinoLayersHeader.from_stream(ss_ptr.stream, self.ovl.context)
		self.header.read_ptrs(self.ovs, ss_ptr)
		print(self.header)

	def load(self, file_path):
		self.header = DinoLayersHeader.from_xml_file(file_path, self.ovl.context)
		print(self.header)
	# 	xml = self.load_xml(file_path)
	# 	# fgm data
	# 	shader_string = self.get_shader(xml)
	# 	print(shader_string)
	#
	# 	# update fgm string
	# 	print(shader_string, self.sized_str_entry.fragments[0].pointers[1].data)
	# 	self.sized_str_entry.fragments[0].pointers[1].update_data(shader_string, update_copies=True)
	#
	# 	counter = 2
	# 	size = 0
	# 	for layer in xml:
	#
	# 		if "fgm" in layer.attrib:
	# 			fgm_name = layer.attrib["fgm"]
	#
	# 			fgm_name_data = fgm_name.encode() + b"\x00"
	# 			size += len(fgm_name_data)
	# 			print(fgm_name_data, self.sized_str_entry.fragments[counter].pointers[1].data)
	# 			self.sized_str_entry.fragments[counter].pointers[1].update_data(fgm_name_data, update_copies=True)
	# 			counter += 1
	#
	# 		if "name" in layer.attrib:
	# 			layer_name = layer.attrib["name"]
	#
	# 			layer_name_data = layer_name.encode() + b"\x00"
	# 			size += len(layer_name_data)
	# 			print(layer_name_data, self.sized_str_entry.fragments[counter].pointers[1].data)
	# 			self.sized_str_entry.fragments[counter].pointers[1].update_data(layer_name_data, update_copies=True)
	# 			counter += 1
	#
	# 	self.sized_str_entry.fragments[counter - 1].pointers[1].update_data(layer_name_data + b"\x00" * 7,
	# 																		update_copies=True)

	def extract(self, out_dir, show_temp_files, progress_callback):
		name = self.sized_str_entry.name
		out_path = out_dir(name)
		self.header.to_xml_file(out_path)
		return out_path,

	def create(self):
		xml = self.load_xml(self.file_entry.path)
		self.sized_str_entry = self.create_ss_entry(self.file_entry)
		f0, f1 = self.create_fragments(self.sized_str_entry, 2)

		# first write the array
		data = b""
		for layer in xml:
			layer_data = struct.pack("<6I", int(layer.attrib["flag"]), 0, 0, 0, 0, 0)
			data += layer_data

		self.write_to_pool(f1.pointers[1], 4, data)  # ptr to array
		# 2 ptrs at start of struct
		self.write_to_pool(self.sized_str_entry.pointers[0], 4, struct.pack("<2Q 2Q", 0, 0, len(xml), 0))
		self.ptr_relative(f0.pointers[0], self.sized_str_entry.pointers[0])
		self.ptr_relative(f1.pointers[0], self.sized_str_entry.pointers[0], rel_offset=8)

		# first entry to name buffer
		self.write_to_pool(f0.pointers[1], 2, self.get_shader(xml))

		# write the layers
		offset = 0
		for layer in xml:
			# fgms go first if they exist
			if "fgm" in layer.attrib:
				fgm_frag = self.create_fragments(self.sized_str_entry, 1)[0]
				fgm_name = layer.attrib["fgm"]
				self.ptr_relative(fgm_frag.pointers[0], f1.pointers[1], rel_offset=offset + 8)
				self.write_to_pool(fgm_frag.pointers[1], 2, as_bytes(fgm_name))
			if "name" in layer.attrib:
				name = layer.attrib["name"]
				n_frag = self.create_fragments(self.sized_str_entry, 1)[0]
				self.ptr_relative(n_frag.pointers[0], f1.pointers[1], rel_offset=offset + 16)
				self.write_to_pool(n_frag.pointers[1], 2, as_bytes(name))
			offset += 24
		# todo - might need padding after the names buffer


class MatvarsLoader(BaseFile):

	def collect(self):
		self.assign_ss_entry()
		ss_ptr = self.sized_str_entry.pointers[0]
		self.header = DinoVariantsHeader.from_stream(ss_ptr.stream, self.ovl.context)
		self.header.read_ptrs(self.ovs, ss_ptr)
		print(self.header)

	def extract(self, out_dir, show_temp_files, progress_callback):
		name = self.sized_str_entry.name
		out_path = out_dir(name)
		self.header.to_xml_file(out_path)
		return out_path,

	def create(self):
		self.sized_str_entry = self.create_ss_entry(self.file_entry)
		ss_ptr = self.sized_str_entry.pointers[0]

		xml = self.load_xml(self.file_entry.path)
		# there's just 0 or 1 variantset for now
		variantset = xml.findall('.//variantset')
		if variantset:
			self.variantset = variantset[0].attrib.get("name")
		else:
			self.variantset = None
		self.variants = [variant.attrib["name"] for variant in xml.findall('.//variant')]
		ptr = 0
		has_sets = 1 if self.variantset else 0
		self.write_to_pool(ss_ptr, 4, struct.pack("<Q Q Q Q Q Q", ptr, has_sets, ptr, ptr, len(self.variants) + 1, 0))
		# todo - may use wrong pools !
		fgm_string = self.get_fgm(xml)
		self.write_str_at_rel_offset(ss_ptr, 0, fgm_string)
		self.write_str_at_rel_offset(ss_ptr, 16, self.variantset)
		self.write_str_list_at_rel_offset(ss_ptr, 24, self.variants)
		# todo - may need padding here

	def load(self, file_path):
		self.header = DinoVariantsHeader.from_xml_file(file_path, self.ovl.context)
		print(self.header)
	# 	xml = self.load_xml(file_path)
	# 	# fgm data
	# 	fgm_string = self.get_fgm(xml)
	# 	# variant set data
	# 	variantset = xml.findall('.//variantset')
	# 	if variantset:
	# 		self.variantset = variantset[0].attrib.get("name")
	# 		set_size = 4 - ((len(self.variantset) + 1) % 4)
	# 		if set_size == 4:
	# 			set_size = 0
	# 		varsetdata = self.variantset.encode() + b"\x00" * (set_size + 1)
	# 	else:
	# 		self.variantset = None
	#
	# 	# variant string list data
	# 	self.variants = [variant.attrib["name"] for variant in xml.findall('.//variant')]
	# 	for i, var in enumerate(self.variants):
	# 		pad_size = 4 - ((len(var) + 1) % 4)
	# 		if pad_size == 4:
	# 			pad_size = 0
	# 		self.variants[i] = var.encode() + b"\x00" * (pad_size + 1)
	#
	# 	p0, has_sets, p1, p2, variant_count, _ = struct.unpack("<6Q", self.sized_str_entry.pointers[0].data)
	#
	# 	# update fgm string
	# 	self.sized_str_entry.fragments[0].pointers[1].update_data(fgm_string, update_copies=True)
	#
	# 	# update set string if it has and set correct offset for variant list
	# 	if has_sets == 1:
	# 		thing = 3
	# 		self.sized_str_entry.fragments[1].pointers[1].update_data(varsetdata, update_copies=True)
	# 	else:
	# 		thing = 2
	#
	# 	# update variant list strings
	# 	for n, variants in enumerate(self.variants):
	# 		self.sized_str_entry.fragments[thing + n].pointers[1].update_data(self.variants[n], update_copies=True)


class MateffsLoader(BaseFile):

	def collect(self):
		self.assign_ss_entry()
		logging.info(f"Mateffs: {self.sized_str_entry.name}")

		# Sized string initpos = position of first fragment for matcol
		self.sized_str_entry.fragments = self.ovs.frags_from_pointer(self.sized_str_entry.pointers[0], 1)
		self.f0 = self.sized_str_entry.fragments[0]

	def extract(self, out_dir, show_temp_files, progress_callback):
		name = self.sized_str_entry.name
		out_path = out_dir(name)
		xmldata = ET.Element('MaterialEffects')
		self.assign_shader(xmldata)
		# 1 ptr at the start, not 100% sold on these just yet
		data = struct.unpack("<Q 6f 2I 12f 2I 2f I 39f I f", self.sized_str_entry.pointers[0].data)
		xmldata.set('data', data)
		self.write_xml(out_path, xmldata)
		return out_path,


class MatpatsLoader(BaseFile):

	def collect(self):
		self.assign_ss_entry()
		ss_ptr = self.sized_str_entry.pointers[0]
		self.header = DinoPatternsHeader.from_stream(ss_ptr.stream, self.ovl.context)
		self.header.read_ptrs(self.ovs, ss_ptr)
		print(self.header)

	def extract(self, out_dir, show_temp_files, progress_callback):
		name = self.sized_str_entry.name
		out_path = out_dir(name)
		self.header.to_xml_file(out_path)
		return out_path,

	def create(self):
		self.sized_str_entry = self.create_ss_entry(self.file_entry)
		ss_ptr = self.sized_str_entry.pointers[0]

		xml = self.load_xml(self.file_entry.path)
		# there's just 1 patternset for now
		patternset = xml[0]
		self.patternset = patternset.attrib["name"]
		self.patterns = [pattern.attrib["name"] for pattern in patternset]
		ptr = 0
		self.write_to_pool(ss_ptr, 4, struct.pack("<Q Q 2Q Q Q", ptr, len(xml), ptr, ptr, len(self.patterns) + 1, 0))
		# todo - may use wrong pools !
		fgm_string = self.get_fgm(xml)
		self.write_str_at_rel_offset(ss_ptr, 0, fgm_string)
		self.write_str_at_rel_offset(ss_ptr, 16, self.patternset)
		self.write_str_list_at_rel_offset(ss_ptr, 24, self.patterns)
		# todo - may need padding here

	def load(self, file_path):
		self.header = DinoPatternsHeader.from_xml_file(file_path, self.ovl.context)
		print(self.header)
		# xml = self.load_xml(file_path)
		# # fgm data
		# fgm_string = self.get_fgm(xml)
		# # pattern set data
		# patternset = xml.findall('.//patternset')
		# if patternset:
		# 	self.patternset = patternset[0].attrib.get("name")
		# 	set_size = 4 - ((len(self.patternset) + 1) % 4)
		# 	if set_size == 4:
		# 		set_size = 0
		# 	varsetdata = self.patternset.encode() + b"\x00" * (set_size + 1)
		# else:
		# 	self.patternset = None
		#
		# # pattern string list data
		# self.patterns = [pattern.attrib["name"] for pattern in xml.findall('.//pattern')]
		# for i, var in enumerate(self.patterns):
		# 	pad_size = 4 - ((len(var) + 1) % 4)
		# 	if pad_size == 4:
		# 		pad_size = 0
		# 	self.patterns[i] = var.encode() + b"\x00" * (pad_size + 1)
		#
		# p0, set_count, p1, p2, pattern_count, _ = struct.unpack("<6Q", self.sized_str_entry.pointers[0].data)
		#
		# # update fgm string
		# print(fgm_string, self.sized_str_entry.fragments[0].pointers[1].data)
		# self.sized_str_entry.fragments[0].pointers[1].update_data(fgm_string, update_copies=True)
		#
		# # update set string if it has and set correct offset for pattern list
		# if set_count == 1:
		# 	thing = 3
		# 	print(varsetdata, self.sized_str_entry.fragments[1].pointers[1].data)
		# 	self.sized_str_entry.fragments[1].pointers[1].update_data(varsetdata, update_copies=True)
		#
		# else:
		# 	thing = 2
		#
		# # update pattern list strings
		# for n, patterns in enumerate(self.patterns):
		# 	print(self.patterns[n], self.sized_str_entry.fragments[thing + n].pointers[1].data)
		# 	self.sized_str_entry.fragments[thing + n].pointers[1].update_data(self.patterns[n], update_copies=True)

