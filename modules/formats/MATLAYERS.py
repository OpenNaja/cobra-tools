import logging
import struct
from modules.formats.BaseFormat import BaseFile
import xml.etree.ElementTree as ET # prob move this to a custom modules.helpers or utils?

from modules.helpers import zstr


def unpack_name(b):
	b = bytearray(b)
	# print(shader)
	# decode the names
	for i in range(len(b)):
		b[i] = max(0, b[i] - 1)
	return bytes(b)


class MatlayersLoader(BaseFile):

	def collect(self):
		self.assign_ss_entry()
		logging.info(f"Matlayers: {self.sized_str_entry.name}")

		# Sized string initpos = position of first fragment for matcol
		self.sized_str_entry.fragments = self.ovs.frags_from_pointer(self.sized_str_entry.pointers[0], 2)
		self.sized_str_entry.f0, self.sized_str_entry.f1 = self.sized_str_entry.fragments

		self.shader = unpack_name(self.sized_str_entry.f0.pointers[1].data)
		f0_d0 = struct.unpack("<6I", self.sized_str_entry.f1.pointers[0].data)
		layer_count = f0_d0[2]

		logging.debug(f"{self.shader} {layer_count}")
		entry_size = 24
		ptr11 = self.sized_str_entry.f1.pointers[1]
		out_frags, array_data = self.collect_array(ptr11, layer_count, entry_size)
		self.sized_str_entry.fragments.extend(out_frags)

		self.frag_data_pairs = []
		for i in range(layer_count):
			x = i * entry_size
			# fgm name x + 8
			# layer name x + 16
			frags_entry = self.get_frags_between(out_frags, x, x+entry_size)
			self.frag_data_pairs.append((frags_entry, array_data[x:x+entry_size]))
			rel_offsets = [f.pointers[0].data_offset-x for f in frags_entry]
			print(rel_offsets)

	def extract(self, out_dir, show_temp_files, progress_callback):
		name = self.sized_str_entry.name
		out_path = out_dir(name)
		xmldata = ET.Element('Matlayers')
		xmldata.set('shader', self.get_zstr(self.shader))

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
		self.write_to_pool(self.sized_str_entry.pointers[0], 4, b"")
		f0, f1 = self.create_fragments(self.sized_str_entry, 2)

		# first write the array
		data = b""
		for layer in xml:
			data += struct.pack("<6I", int(layer["flag"]), 0, 0, 0, 0, 0)

		self.write_to_pool(f1.pointers[1], 2, data)  # ptr to array

		self.write_to_pool(f0.pointers[0], 4, b"\x00" * 8)
		self.write_to_pool(f1.pointers[0], 4, struct.pack("<6I", 0, 0, len(xml), 0, 0, 0))

		self.write_to_pool(f0.pointers[1], 2, zstr(xml["shader"]))

		offset = f1.pointers[1].data_offset
		for layer in xml:
			name = layer["name"]
			n_frag = self.create_fragments(self.sized_str_entry, 1)[0]
			n_frag.pointers[0].data_offset = offset + 16
			self.write_to_pool(n_frag.pointers[1], 2, zstr(name))
			if layer["fgm"]:
				fgm_frag = self.create_fragments(self.sized_str_entry, 1)[0]
				fgm_frag.pointers[0].data_offset = offset + 8
			offset += 24


class MatvarsLoader(BaseFile):

	def collect(self):
		self.assign_ss_entry()
		print("\nMatvars:", self.sized_str_entry.name)
		print(self.sized_str_entry.pointers[0].data)
		# Sized string initpos = position of first fragment for matcol

		ss_d = struct.unpack("<4I", self.sized_str_entry.pointers[0].data[:16])
		cnt = ss_d[2]
		self.sized_str_entry.fragments = self.ovs.frags_from_pointer(self.sized_str_entry.pointers[0], 2+cnt)
		if cnt:
			# rex 93
			self.sized_str_entry.f0, self.sized_str_entry.extra, self.sized_str_entry.f1 = self.sized_str_entry.fragments
		else:
			# ichthyo
			self.sized_str_entry.f0, self.sized_str_entry.f1 = self.sized_str_entry.fragments

		shader = unpack_name(self.sized_str_entry.f0.pointers[1].data)
		print(shader)
		f1_ptr = self.sized_str_entry.f1.pointers[0].data
		# print(self.sized_str_entry.f0)
		# 0,0,collection count,0, 0,0,
		# print(self.sized_str_entry.f1.pointers[0].data, len(self.sized_str_entry.f1.pointers[0].data))

		f0_d0 = struct.unpack("<4I", f1_ptr[:16])
		layer_count = f0_d0[2] - 1
		print(f0_d0)
		self.sized_str_entry.tex_frags = self.ovs.frags_from_pointer(self.sized_str_entry.f1.pointers[1],
																	 layer_count)
		for tex in self.sized_str_entry.tex_frags:
			# p0 is just 1 or 0, but weird since 8 and 16 bytes alternate
			# first is fgm name, second layer identity name
			# b'Swatch_Thero_TRex_LumpySkin\x00'
			# b'Ichthyosaurus_Layer_01\x00'
			print(tex.pointers[1].data)
			tex.name = self.sized_str_entry.name


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
