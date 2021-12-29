import logging
import struct
from modules.formats.BaseFormat import BaseFile
import xml.etree.ElementTree as ET # prob move this to a custom modules.helpers or utils?

from modules.helpers import zstr, as_bytes


def unpack_name(b):
	b = bytearray(b)
	# decode the names
	for i in range(len(b)):
		b[i] = max(0, b[i] - 1)
	return bytes(b)


def pack_name(b):
	b = bytearray(b.encode())
	# decode the names
	for i in range(len(b)):
		b[i] = max(0, b[i] + 1)
	return b.decode()


class MatlayersLoader(BaseFile):

	def collect(self):
		self.assign_ss_entry()
		logging.info(f"Matlayers: {self.sized_str_entry.name}")

		# Sized string initpos = position of first fragment for matcol
		self.sized_str_entry.fragments = self.ovs.frags_from_pointer(self.sized_str_entry.pointers[0], 2)
		self.sized_str_entry.f0, self.sized_str_entry.f1 = self.sized_str_entry.fragments

		# self.shader = unpack_name(self.sized_str_entry.f0.pointers[1].data)
		f0_d0 = struct.unpack("<6I", self.sized_str_entry.f1.pointers[0].data)
		layer_count = f0_d0[2]

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
			rel_offsets = [f.pointers[0].data_offset-abs_offset for f in frags_entry]
			# we can have unused tiles, as in JWE2 trex (the last 2), which are all black and do not have an fgm
			# print(rel_offsets)

	def extract(self, out_dir, show_temp_files, progress_callback):
		name = self.sized_str_entry.name
		out_path = out_dir(name)
		xmldata = ET.Element('Matlayers')
		shader = unpack_name(self.sized_str_entry.f0.pointers[1].data)
		xmldata.set('shader', self.get_zstr(shader))

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
		# pool2_index, pool2 = self.get_pool(2)
		# pool4_index, pool4 = self.get_pool(4)
		# offset = pool4.data.tell()
		self.sized_str_entry = self.create_ss_entry(self.file_entry)
		f0, f1 = self.create_fragments(self.sized_str_entry, 2)

		# first write the array
		data = b""
		for layer in xml:
			layer_data = struct.pack("<6I", int(layer.attrib["flag"]), 0, 0, 0, 0, 0)
			data += layer_data

		self.write_to_pool(f1.pointers[1], 4, data)  # ptr to array
		# empty ss, followed by 2 frags
		self.write_to_pool(self.sized_str_entry.pointers[0], 4, b"")
		self.write_to_pool(f0.pointers[0], 4, b"\x00" * 8)
		self.write_to_pool(f1.pointers[0], 4, struct.pack("<6I", 0, 0, len(xml), 0, 0, 0))

		shader = pack_name(xml.attrib["shader"])
		# first entry to name buffer
		self.write_to_pool(f0.pointers[1], 2, as_bytes(shader))

		# write the layers
		offset = f1.pointers[1].data_offset
		for layer in xml:
			# fgms go first if they exist
			if "fgm" in layer.attrib:
				fgm_frag = self.create_fragments(self.sized_str_entry, 1)[0]
				fgm_frag.pointers[0].data_offset = offset + 8
				fgm_name = layer.attrib["fgm"]
				self.write_to_pool(fgm_frag.pointers[1], 2, as_bytes(fgm_name))
			if "name" in layer.attrib:
				name = layer.attrib["name"]
				n_frag = self.create_fragments(self.sized_str_entry, 1)[0]
				n_frag.pointers[0].data_offset = offset + 16
				self.write_to_pool(n_frag.pointers[1], 2, as_bytes(name))
			offset += 24
		# todo - might need padding after the names buffer


class MatvarsLoader(BaseFile):

	def collect(self):
		self.assign_ss_entry()
		logging.info(f"Matlayers: {self.sized_str_entry.name}")
		# total data seems to be 48 bytes: 0, set_count, 0, 0, variant_count, 0
		all_bytes = self.sized_str_entry.pointers[0].read_from_pool(48)
		_, set_count, _, _, variant_count, _ = struct.unpack("<6Q", all_bytes)
		logging.debug(f"set_count: {set_count} variant_count: {variant_count}")

		# seen either 0 or 1, could possibly be more, would need refactor in that case
		self.sized_str_entry.fragments = self.ovs.frags_from_pointer(self.sized_str_entry.pointers[0], 2+set_count)
		if set_count:
			# rex 93
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
		shader = unpack_name(self.sized_str_entry.f0.pointers[1].data)
		xmldata.set('shader', self.get_zstr(shader))

		if self.sized_str_entry.tex_frags:
			for frag in self.sized_str_entry.tex_frags:
				variant = ET.SubElement(xmldata, 'variant')
				variant.set('name', self.get_zstr(frag.pointers[1].data))
		else:
			variantset = ET.SubElement(xmldata, 'variantset')
			variantset.set('name', self.get_zstr(self.sized_str_entry.extra.pointers[1].data))

		self.write_xml(out_path, xmldata)
		return out_path,


class MateffsLoader(BaseFile):

	def collect(self):
		self.assign_ss_entry()
		print("\nMateffs:", self.sized_str_entry.name)

		# Sized string initpos = position of first fragment for matcol
		self.sized_str_entry.fragments = self.ovs.frags_from_pointer(self.sized_str_entry.pointers[0], 1)
		self.sized_str_entry.f0 = self.sized_str_entry.fragments[0]

		shader = unpack_name(self.sized_str_entry.f0.pointers[1].data)
		print(shader)
		print(self.sized_str_entry.f0.pointers[0].data)
	# print(self.sized_str_entry.f0)
	# 0,0,collection count,0, 0,0,
	# print(self.sized_str_entry.f1.pointers[0].data, len(self.sized_str_entry.f1.pointers[0].data))
	# f0_d0 = struct.unpack("<6I", self.sized_str_entry.f1.pointers[0].data)
	# layer_count = f0_d0[2] - 1
	# print(f0_d0)
	# self.sized_str_entry.tex_frags = self.ovs.frags_from_pointer(self.sized_str_entry.f1.pointers[1],
	#															 layer_count)
	# for tex in self.sized_str_entry.tex_frags:
	# p0 is just 1 or 0, but weird since 8 and 16 bytes alternate
	# first is fgm name, second layer identity name
	# b'Swatch_Thero_TRex_LumpySkin\x00'
	# b'Ichthyosaurus_Layer_01\x00'
	# print(tex.pointers[1].data)
	# tex.name = self.sized_str_entry.name


class MatpatsLoader(BaseFile):

	def collect(self):
		self.assign_ss_entry()
		print("\nMatpats:", self.sized_str_entry.name)

		# Sized string initpos = position of first fragment for matcol
		self.sized_str_entry.fragments = self.ovs.frags_from_pointer(self.sized_str_entry.pointers[0], 1)
		self.sized_str_entry.f0 = self.sized_str_entry.fragments[0]

		shader = unpack_name(self.sized_str_entry.f0.pointers[1].data)
		print(shader)
		# print(self.sized_str_entry.f0)
		# 0,0,collection count,0, 0,0,
		# print(self.sized_str_entry.f1.pointers[0].data, len(self.sized_str_entry.f1.pointers[0].data))
		f0_d0 = struct.unpack("<4I", self.sized_str_entry.f0.pointers[0].data)
		layer_count = f0_d0[2]
		print(f0_d0)
		self.sized_str_entry.fragments.extend(
			self.ovs.frags_from_pointer(self.sized_str_entry.pointers[0], layer_count * 2))

		self.sized_str_entry.f1 = self.sized_str_entry.fragments[1]
		self.sized_str_entry.f2 = self.sized_str_entry.fragments[2]
		print(self.sized_str_entry.f1.pointers[1].data)
		f2_d0 = struct.unpack("<6I", self.sized_str_entry.f2.pointers[0].data)
		layer_count2 = f2_d0[2] - 1
		print(f2_d0)

		self.sized_str_entry.tex_frags = self.ovs.frags_from_pointer(self.sized_str_entry.f2.pointers[1], layer_count2)

		# print(self.sized_str_entry.fragments)
		for tex in self.sized_str_entry.tex_frags:
			# p0 is just 1 or 0, but weird since 8 and 16 bytes alternate
			# first is fgm name, second layer identity name
			# b'Swatch_Thero_TRex_LumpySkin\x00'
			# b'Ichthyosaurus_Layer_01\x00'
			print(tex.pointers[1].data)
			tex.name = self.sized_str_entry.name
