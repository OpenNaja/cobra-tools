import logging
import struct
from modules.formats.BaseFormat import BaseFile
import xml.etree.ElementTree as ET # prob move this to a custom modules.helpers or utils?

from modules.formats.shared import djb
from modules.helpers import zstr, as_bytes


def unpack_name(b):
	_hash, _name = b.split(b"::")
	hash_int = int(_hash)
	name_str = _unpack_name(_name).decode()[:-1]
	# logging.info(f"{hash_int} {djb('::'+name_str.lower())} {name_str}")
	return hash_int, name_str


def pack_name(h_int, name_str):
	return str(h_int).encode() + b"::" + _pack_name(name_str.encode()) + b"\x00"


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

	def assign_shader(self, xml):
		_hash, _shader = unpack_name(self.sized_str_entry.f0.pointers[1].data)
		xml.set('shader', _shader)
		xml.set('hash', str(_hash))

	def get_shader(self, xml):
		_shader = _pack_name(xml.attrib["shader"])
		return as_bytes(f"{xml.attrib['hash']}::{_shader}")

	def rename_content(self, name_tuples):
		_hash, _shader = unpack_name(self.sized_str_entry.f0.pointers[1].data)
		for old, new in name_tuples:
			_shader = _shader.replace(old, new)
		self.sized_str_entry.f0.pointers[1].update_data(pack_name(_hash, _shader))


class MatlayersLoader(MatAbstract):

	def collect(self):
		self.assign_ss_entry()
		logging.info(f"Matlayers: {self.sized_str_entry.name}")

		# Sized string initpos = position of first fragment for matcol
		self.sized_str_entry.fragments = self.ovs.frags_from_pointer(self.sized_str_entry.pointers[0], 2)
		self.sized_str_entry.f0, self.sized_str_entry.f1 = self.sized_str_entry.fragments

		# 2 ptrs, 2 counts, only one is used
		p0, p1, layer_count, _ = struct.unpack("<2Q 2Q", self.sized_str_entry.pointers[0].data)

		logging.debug(f"layer_count {layer_count}")
		entry_size = 24
		ptr11 = self.sized_str_entry.f1.pointers[1]
		out_frags, array_data = self.collect_array(ptr11, layer_count, entry_size)
		self.sized_str_entry.fragments.extend(out_frags)

		self.frag_data_pairs = []
		for i in range(layer_count):
			x = i * entry_size
			abs_offset = ptr11.data_offset+x
			# fgm name x + 8
			# layer name x + 16
			frags_entry = self.get_frags_between(out_frags, abs_offset, abs_offset+entry_size)
			self.frag_data_pairs.append((frags_entry, array_data[x:x+entry_size]))
			# rel_offsets = [f.pointers[0].data_offset-abs_offset for f in frags_entry]
			# we can have unused tiles, as in JWE2 trex (the last 2), which are all black and do not have an fgm
			# print(rel_offsets)

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
				self.ptr_relative(fgm_frag.pointers[0], f1.pointers[1], rel_offset=offset+8)
				self.write_to_pool(fgm_frag.pointers[1], 2, as_bytes(fgm_name))
			if "name" in layer.attrib:
				name = layer.attrib["name"]
				n_frag = self.create_fragments(self.sized_str_entry, 1)[0]
				self.ptr_relative(n_frag.pointers[0], f1.pointers[1], rel_offset=offset+16)
				self.write_to_pool(n_frag.pointers[1], 2, as_bytes(name))
			offset += 24
		# todo - might need padding after the names buffer


class MatvarsLoader(MatAbstract):

	def collect(self):
		self.assign_ss_entry()
		logging.info(f"Matlayers: {self.sized_str_entry.name}")
		# 48 bytes
		_, set_count, p0, p1, variant_count, _ = struct.unpack("<6Q", self.sized_str_entry.pointers[0].data)
		logging.debug(f"set_count: {set_count} variant_count: {variant_count}")

		# seen either 0 or 1, could possibly be more, would need refactor in that case
		self.sized_str_entry.fragments = self.ovs.frags_from_pointer(self.sized_str_entry.pointers[0], 2+set_count)
		if set_count:
			# rex 93 - has not materialpatterns, so that's probably why it's different
			self.sized_str_entry.f0, self.sized_str_entry.extra, self.sized_str_entry.f1 = self.sized_str_entry.fragments
			# self.sized_str_entry.extra is the set name
		else:
			# ichthyo
			self.sized_str_entry.f0, self.sized_str_entry.f1 = self.sized_str_entry.fragments

		# shader = unpack_name(self.sized_str_entry.f0.pointers[1].data)
		self.sized_str_entry.tex_frags = self.ovs.frags_from_pointer(self.sized_str_entry.f1.pointers[1], variant_count-1)
		for tex in self.sized_str_entry.tex_frags:
			tex.name = self.sized_str_entry.name

	def extract(self, out_dir, show_temp_files, progress_callback):
		name = self.sized_str_entry.name
		out_path = out_dir(name)
		xmldata = ET.Element('MaterialVariants')
		self.assign_shader(xmldata)

		if self.sized_str_entry.tex_frags:
			for frag in self.sized_str_entry.tex_frags:
				variant = ET.SubElement(xmldata, 'variant')
				variant.set('name', self.get_zstr(frag.pointers[1].data))
		else:
			variantset = ET.SubElement(xmldata, 'variantset')
			variantset.set('name', self.get_zstr(self.sized_str_entry.extra.pointers[1].data))

		self.write_xml(out_path, xmldata)
		return out_path,


class MateffsLoader(MatAbstract):

	def collect(self):
		self.assign_ss_entry()
		logging.info(f"Mateffs: {self.sized_str_entry.name}")

		# Sized string initpos = position of first fragment for matcol
		self.sized_str_entry.fragments = self.ovs.frags_from_pointer(self.sized_str_entry.pointers[0], 1)
		self.sized_str_entry.f0 = self.sized_str_entry.fragments[0]

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

		self.sized_str_entry.fragments = self.ovs.frags_from_pointer(self.sized_str_entry.pointers[0], 3)
		self.sized_str_entry.f0 = self.sized_str_entry.fragments[0]

		# shader = unpack_name(self.sized_str_entry.f0.pointers[1].data)
		# print(shader)
		# todo - support multiple sets, if set_count can be other than 1
		ptr0, set_count, ptr1, ptr2, pattern_count, _ = struct.unpack("<Q Q 2Q Q Q", self.sized_str_entry.pointers[0].data)
		assert set_count == 1
		# print(ptr0, set_count, ptr1, ptr2, pattern_count, _)

		self.sized_str_entry.f1 = self.sized_str_entry.fragments[1]
		self.sized_str_entry.f2 = self.sized_str_entry.fragments[2]

		logging.info(f"set {self.sized_str_entry.f1.pointers[1].data}")
		self.sized_str_entry.patterns = self.ovs.frags_from_pointer(self.sized_str_entry.f2.pointers[1], pattern_count-1)
		for tex in self.sized_str_entry.patterns:
			logging.info(f"pattern {tex.pointers[1].data}")
			tex.name = self.sized_str_entry.name
