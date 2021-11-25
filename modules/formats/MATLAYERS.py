import logging
import struct
from modules.formats.BaseFormat import BaseFile


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
		print("\nMatlayers:", self.sized_str_entry.name)

		# Sized string initpos = position of first fragment for matcol
		self.sized_str_entry.fragments = self.ovs.frags_from_pointer(self.sized_str_entry.pointers[0], 2)
		self.sized_str_entry.f0, self.sized_str_entry.f1 = self.sized_str_entry.fragments

		shader = unpack_name(self.sized_str_entry.f0.pointers[1].data)
		# print(self.sized_str_entry.f0)
		# 0,0,collection count,0, 0,0,
		# print(self.sized_str_entry.f1.pointers[0].data, len(self.sized_str_entry.f1.pointers[0].data))
		f0_d0 = struct.unpack("<6I", self.sized_str_entry.f1.pointers[0].data)
		layer_count = f0_d0[2]

		print(shader, layer_count)
		entry_size = 24
		ptr11 = self.sized_str_entry.f1.pointers[1]
		out_frags, array_data = self.collect_array(ptr11, layer_count, entry_size)
		for tex in out_frags:
			print(tex.pointers[1].data)
		# it's already sorted
		# out_frags.sort(key=lambda x:x.pointers[0].data_offset)
		# todo - the mapping is not quite right
		frag_i = 0
		# for x in range(0, len(array_data), entry_size):
		for i in range(layer_count):
			x = i * entry_size
			frags_entry = self.get_frags_between(out_frags, x, x+entry_size)
			# print(frags_entry)
			fd = struct.unpack("<6I", array_data[x:x+entry_size])
			has_fgm_name = fd[0]
			print(i, has_fgm_name)
			f_count = 2 if has_fgm_name else 0
			frags = out_frags[frag_i:frag_i+f_count]
			for tex in frags_entry:
				print(tex.pointers[1].data)
			frag_i += f_count

		# array_data = ptr11.read_from_pool(24 * layer_count)
		# print(array_data)
		byte_size = 16 + ((layer_count - 1) * entry_size)
		print(f0_d0, byte_size)
		self.sized_str_entry.tex_frags = self.ovs.frags_accumulate_from_pointer(
			ptr11, byte_size)
		print(len(self.sized_str_entry.tex_frags), len(out_frags))

		# layer_count = f0_d0[2]
		# print(f0_d0)
		# self.sized_str_entry.tex_frags = self.ovs.frags_from_pointer(self.sized_str_entry.f1.pointers[1],
		# 															 layer_count)

		print("self.sized_str_entry.pointers[0].data")
		print(self.sized_str_entry.pointers[0].data)
		print("self.sized_str_entry.f1.pointers[1]")
		print(self.sized_str_entry.f1.pointers[1].data)
		for tex in self.sized_str_entry.tex_frags:
			# p0 is just 1 or 0, but weird since 8 and 16 bytes alternate
			# first is fgm name, second layer identity name
			# b'Swatch_Thero_TRex_LumpySkin\x00'
			# b'Ichthyosaurus_Layer_01\x00'
			print(tex.pointers[0].data)
			print(tex.pointers[1].data)
			tex.name = self.sized_str_entry.name

	def extract(self):
		pass


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
