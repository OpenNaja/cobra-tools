import logging
import struct

from generated.formats.dinosaurmaterialvariants.compound.DinoVariantsHeader import DinoVariantsHeader
from modules.formats.BaseFormat import BaseFile
import xml.etree.ElementTree as ET  # prob move this to a custom modules.helpers or utils?

from modules.formats.shared import djb
from modules.helpers import zstr, as_bytes


def unpack_name(b):
	_hash, _name = b.split(b"::")
	hash_int = int(_hash)
	name_str = _unpack_name(_name).decode()[:-1]
	logging.info(f"unpack_name: {hash_int} {djb('::' + name_str.lower())} {name_str}")
	return hash_int, name_str


def pack_name(h_int, name_str):
	a = str(h_int).encode() + b"::" + _pack_name(name_str.encode()) + b"\x00"
	logging.info(f"pack_name: {a}")
	return a


def _unpack_name(b):
	b = bytearray(b)
	# decode the names
	for i in range(len(b)):
		b[i] = max(0, b[i] - 1)
	return bytes(b)


def _pack_name(b):
	b = bytearray(b)
	# decode the names
	for i in range(len(b)):
		b[i] = max(0, b[i] + 1)
	return bytes(b)


class MatAbstract(BaseFile):

	def assign_fgm(self, xml):
		_hash, _fgm = unpack_name(as_bytes(self.fgm))
		print("fgm string: " + _fgm)
		xml.set('fgm', _fgm)
		xml.set('hash', str(_hash))

	def assign_shader(self, xml):
		_hash, _shader = unpack_name(self.f0.pointers[1].data)
		xml.set('shader', _shader)
		xml.set('hash', str(_hash))

	def get_fgm(self, xml):
		_shader = _pack_name(xml.attrib["fgm"].encode()).decode('utf-8')
		b = as_bytes(xml.attrib['hash'] + "::" + _shader)
		return b

	def get_shader(self, xml):
		_shader = _pack_name(xml.attrib["shader"].encode()).decode('utf-8')
		b = as_bytes(xml.attrib['hash'] + "::" + _shader)
		return b

	def rename_content(self, name_tuples):
		_hash, _shader = unpack_name(self.f0.pointers[1].data)
		for old, new in name_tuples:
			_shader = _shader.replace(old, new)
		self.f0.pointers[1].update_data(pack_name(_hash, _shader))


class MatlayersLoader(MatAbstract):

	def collect(self):
		self.assign_ss_entry()
		logging.info(f"Matlayers: {self.sized_str_entry.name}")

		# Sized string initpos = position of first fragment for matcol
		self.sized_str_entry.fragments = self.ovs.frags_from_pointer(self.sized_str_entry.pointers[0], 2)
		self.f0, self.f1 = self.sized_str_entry.fragments

		# 2 ptrs, 2 counts, only one is used
		p0, p1, layer_count, _ = struct.unpack("<2Q 2Q", self.sized_str_entry.pointers[0].data)

		logging.debug(f"layer_count {layer_count}")
		entry_size = 24
		ptr11 = self.f1.pointers[1]
		out_frags, array_data = self.collect_array(ptr11, layer_count, entry_size)
		self.sized_str_entry.fragments.extend(out_frags)
		print(array_data)
		self.frag_data_pairs = []
		for i in range(layer_count):
			x = i * entry_size
			abs_offset = ptr11.data_offset + x
			# fgm name x + 8
			# layer name x + 16
			frags_entry = self.get_frags_between(out_frags, abs_offset, abs_offset + entry_size)
			self.frag_data_pairs.append((frags_entry, array_data[x:x + entry_size]))
		print(self.frag_data_pairs)
		# rel_offsets = [f.pointers[0].data_offset-abs_offset for f in frags_entry]
		# we can have unused tiles, as in JWE2 trex (the last 2), which are all black and do not have an fgm
		# print(rel_offsets)

	def load(self, file_path):
		xml = self.load_xml(file_path)
		# fgm data
		shader_string = self.get_shader(xml)
		print(shader_string)

		# update fgm string
		print(shader_string, self.sized_str_entry.fragments[0].pointers[1].data)
		self.sized_str_entry.fragments[0].pointers[1].update_data(shader_string, update_copies=True)

		counter = 2
		size = 0
		for layer in xml:

			if "fgm" in layer.attrib:
				fgm_name = layer.attrib["fgm"]

				fgm_name_data = fgm_name.encode() + b"\x00"
				size += len(fgm_name_data)
				print(fgm_name_data, self.sized_str_entry.fragments[counter].pointers[1].data)
				self.sized_str_entry.fragments[counter].pointers[1].update_data(fgm_name_data, update_copies=True)
				counter += 1

			if "name" in layer.attrib:
				layer_name = layer.attrib["name"]

				layer_name_data = layer_name.encode() + b"\x00"
				size += len(layer_name_data)
				print(layer_name_data, self.sized_str_entry.fragments[counter].pointers[1].data)
				self.sized_str_entry.fragments[counter].pointers[1].update_data(layer_name_data, update_copies=True)
				counter += 1

		self.sized_str_entry.fragments[counter - 1].pointers[1].update_data(layer_name_data + b"\x00" * 7,
																			update_copies=True)

	def extract(self, out_dir, show_temp_files, progress_callback):
		name = self.sized_str_entry.name
		out_path = out_dir(name)
		xmldata = ET.Element('Matlayers')
		self.assign_shader(xmldata)

		for frags, entry_bytes in self.frag_data_pairs:
			layer = ET.SubElement(xmldata, 'layer')
			fd = struct.unpack("<6I", entry_bytes)
			flag = fd[0]
			layer.set('flag', str(flag))
			if len(frags) == 1:
				l = frags[0]
				fgm = None
			elif len(frags) == 2:
				fgm, l = frags
			elif len(frags) == 0:
				continue
			else:
				raise AttributeError(f"Not sure how to handle {len(frags)} on {self.file_entry.name}")
			layer_name = l.pointers[1].data
			layer.set('name', self.get_zstr(layer_name))
			if fgm:
				fgm_name = fgm.pointers[1].data
				layer.set('fgm', self.get_zstr(fgm_name))
		print(xmldata)
		self.write_xml(out_path, xmldata)
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


class MatvarsLoader(MatAbstract):

	def collect(self):
		self.assign_ss_entry()
		logging.info(f"Matvars: {self.sized_str_entry.name}")
		ss_ptr = self.sized_str_entry.pointers[0]
		self.header = ss_ptr.load_as(DinoVariantsHeader)[0]
		logging.debug(f"has_sets: {self.header.has_sets} variant_count: {self.header.variant_count}")
		self.header.read_ptrs(self.ovs, ss_ptr)
		print(self.header)

	def extract(self, out_dir, show_temp_files, progress_callback):
		name = self.sized_str_entry.name
		out_path = out_dir(name)
		xmldata = ET.Element('MaterialVariants')
		self.assign_fgm(xmldata)

		for var in self.variants:
			variant = ET.SubElement(xmldata, 'variant')
			variant.set('name', var)
		if self.variantset:
			variantset = ET.SubElement(xmldata, 'variantset')
			variantset.set('name', self.variantset)

		self.write_xml(out_path, xmldata)
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
		xml = self.load_xml(file_path)
		# fgm data
		fgm_string = self.get_fgm(xml)
		# variant set data
		variantset = xml.findall('.//variantset')
		if variantset:
			self.variantset = variantset[0].attrib.get("name")
			set_size = 4 - ((len(self.variantset) + 1) % 4)
			if set_size == 4:
				set_size = 0
			varsetdata = self.variantset.encode() + b"\x00" * (set_size + 1)
		else:
			self.variantset = None

		# variant string list data
		self.variants = [variant.attrib["name"] for variant in xml.findall('.//variant')]
		for i, var in enumerate(self.variants):
			pad_size = 4 - ((len(var) + 1) % 4)
			if pad_size == 4:
				pad_size = 0
			self.variants[i] = var.encode() + b"\x00" * (pad_size + 1)

		p0, has_sets, p1, p2, variant_count, _ = struct.unpack("<6Q", self.sized_str_entry.pointers[0].data)

		# update fgm string
		self.sized_str_entry.fragments[0].pointers[1].update_data(fgm_string, update_copies=True)

		# update set string if it has and set correct offset for variant list
		if has_sets == 1:
			thing = 3
			self.sized_str_entry.fragments[1].pointers[1].update_data(varsetdata, update_copies=True)
		else:
			thing = 2

		# update variant list strings
		for n, variants in enumerate(self.variants):
			self.sized_str_entry.fragments[thing + n].pointers[1].update_data(self.variants[n], update_copies=True)


class MateffsLoader(MatAbstract):

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


class MatpatsLoader(MatAbstract):

	def collect(self):
		self.assign_ss_entry()
		logging.info(f"Matpats: {self.sized_str_entry.name}")
		ss_ptr = self.sized_str_entry.pointers[0]

		# todo - support multiple sets, if set_count can be other than 1
		ptr0, set_count, ptr1, ptr2, pattern_count, _ = struct.unpack("<Q Q 2Q Q Q", ss_ptr.data)
		assert set_count == 1
		# print(ptr0, set_count, ptr1, ptr2, pattern_count, _)
		self.fgm = str(self.get_str_at_offset(0))
		# fgm looks like 3545960137::Bmcfsuptbvsvt`QbuufsoTfu`12

		self.patternset = self.get_str_at_offset(16)
		self.patterns = self.get_str_list_at_offset(pattern_count - 1, 24)

	def extract(self, out_dir, show_temp_files, progress_callback):
		name = self.sized_str_entry.name
		out_path = out_dir(name)
		xmldata = ET.Element('MaterialPatterns')

		# It is not a shader, it is the main pattern material name (an fgm).
		self.assign_fgm(xmldata)

		# there is no proper support for more than 1 patternset
		if self.patterns:
			patternset = ET.SubElement(xmldata, 'patternset')
			patternset.set('name', self.patternset)
			for name in self.patterns:
				variant = ET.SubElement(patternset, 'pattern')
				variant.set('name', name)

		self.write_xml(out_path, xmldata)
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
		xml = self.load_xml(file_path)
		# fgm data
		fgm_string = self.get_fgm(xml)
		# pattern set data
		patternset = xml.findall('.//patternset')
		if patternset:
			self.patternset = patternset[0].attrib.get("name")
			set_size = 4 - ((len(self.patternset) + 1) % 4)
			if set_size == 4:
				set_size = 0
			varsetdata = self.patternset.encode() + b"\x00" * (set_size + 1)
		else:
			self.patternset = None

		# pattern string list data
		self.patterns = [pattern.attrib["name"] for pattern in xml.findall('.//pattern')]
		for i, var in enumerate(self.patterns):
			pad_size = 4 - ((len(var) + 1) % 4)
			if pad_size == 4:
				pad_size = 0
			self.patterns[i] = var.encode() + b"\x00" * (pad_size + 1)

		p0, set_count, p1, p2, pattern_count, _ = struct.unpack("<6Q", self.sized_str_entry.pointers[0].data)

		# update fgm string
		print(fgm_string, self.sized_str_entry.fragments[0].pointers[1].data)
		self.sized_str_entry.fragments[0].pointers[1].update_data(fgm_string, update_copies=True)

		# update set string if it has and set correct offset for pattern list
		if set_count == 1:
			thing = 3
			print(varsetdata, self.sized_str_entry.fragments[1].pointers[1].data)
			self.sized_str_entry.fragments[1].pointers[1].update_data(varsetdata, update_copies=True)

		else:
			thing = 2

		# update pattern list strings
		for n, patterns in enumerate(self.patterns):
			print(self.patterns[n], self.sized_str_entry.fragments[thing + n].pointers[1].data)
			self.sized_str_entry.fragments[thing + n].pointers[1].update_data(self.patterns[n], update_copies=True)

