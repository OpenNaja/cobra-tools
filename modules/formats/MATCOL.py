import logging
import struct

from modules.formats.BaseFormat import BaseFile
from modules.formats.shared import get_padding
from modules.helpers import as_bytes
from generated.formats.matcol import MatcolFile


class MatcolLoader(BaseFile):

	def collect(self):
		self.assign_ss_entry()
		logging.info(f"MATCOL: {self.sized_str_entry.name}")

		# Sized string initpos = position of first fragment for matcol
		self.sized_str_entry.fragments = self.ovs.frags_from_pointer(self.sized_str_entry.pointers[0], 1)
		self.sized_str_entry.f0 = self.sized_str_entry.fragments[0]
		# ptr, one = struct.unpack("<2Q", self.sized_str_entry.pointers[0].data)
		mat_type, ptr0, tex_count, ptr1, mat_count, ptr2 = struct.unpack("<6Q", self.sized_str_entry.f0.pointers[1].data)
		# print(ptr, one)
		# print(mat_type, ptr0, tex_count, ptr1, mat_count, ptr2)
		# mat_type (3=variant, 2=layered)
		self.sized_str_entry.is_variant = mat_type == 3
		self.sized_str_entry.is_layered = mat_type == 2
		if tex_count:
			self.sized_str_entry.tex_pointer = self.ovs.frags_from_pointer(self.sized_str_entry.f0.pointers[1], 1)[0]
			self.sized_str_entry.tex_frags = self.ovs.frags_from_pointer(self.sized_str_entry.tex_pointer.pointers[1], tex_count * 3)
			self.sized_str_entry.fragments.extend(self.sized_str_entry.tex_frags)
			self.sized_str_entry.fragments.append(self.sized_str_entry.tex_pointer)
		else:
			self.sized_str_entry.tex_frags = []
		# material pointer frag
		self.sized_str_entry.mat_pointer = self.ovs.frags_from_pointer(self.sized_str_entry.f0.pointers[1], 1)[0]
		self.sized_str_entry.mat_frags = self.collect_array_elements(self.sized_str_entry.mat_pointer.pointers[1], mat_count, 72)
		# todo - this is broken, as mat_frags is not a list of fragments atm, maybe rethink the nesting
		# self.sized_str_entry.fragments.extend(self.sized_str_entry.mat_frags)
		self.sized_str_entry.fragments.append(self.sized_str_entry.mat_pointer)
		# print(self.sized_str_entry.mat_pointer.pointers[1])
		for frags, data in self.sized_str_entry.mat_frags:
			# print(rel_offsets, data)
			# rel [0, 24, 56] or [0]
			name_ptr, u0, u1, info_ptr, info_count, u2, u3, attrib_ptr, attrib_count = struct.unpack("<9Q", data)
			if self.sized_str_entry.is_layered:
				m0, info, attrib = frags
				info.children, info.data = self.collect_array(info.pointers[1], info_count, 32)
				attrib.children, attrib.data = self.collect_array(attrib.pointers[1], attrib_count, 16)
				self.sized_str_entry.fragments.extend(info.children)
				self.sized_str_entry.fragments.extend(attrib.children)
			# self.sized_str_entry.mat_frags.append((frags[0],))
				# m0.pointers[1].strip_zstring_padding()
				# print("info_count", info_count)
				# print("info_count", info)
				# for fr, info_data in self.collect_array_elements(info.pointers[1], info_count, 32):
				# 	# print(fr, info_data, rel_offsets)
				# 	fr[0].pointers[1].strip_zstring_padding()
				# 	info_child_d0 = struct.unpack("<Q 4B 4f I", info_data)
				# 	# print(info_child_d0)
				# attrib.pointers[0].split_data_padding(16)
				# attrib_d0 = struct.unpack("<4I", attrib.pointers[0].data)
				# print("attrib_count",attrib_count)
				# for fr, attr_data in self.collect_array_elements(attrib.pointers[1], attrib_count, 16):
				# 	# print(fr, info_data, rel_offsets)
				# 	fr[0].pointers[1].strip_zstring_padding()
				# 	attr_child_d0 = struct.unpack("<2I4BI", attr_data)
				# 	# print(attr_child_d0)

	def extract(self, out_dir, show_temp_files, progress_callback):
		name = self.sized_str_entry.name.replace("materialcollection", "matcol")
		print(f"Writing {name}")
		out_path = out_dir(name)
		with open(out_path, 'wb') as outfile:
			# write custom matcol header
			outfile.write(self.pack_header(b"MATC"))

			outfile.write(self.sized_str_entry.pointers[0].data)
			outfile.write(self.sized_str_entry.f0.pointers[1].data)
			# these are just 8 * 00 for each ptr
			# outfile.write(self.sized_str_entry.tex_pointer.pointers[1].data)
			for tex in self.sized_str_entry.tex_frags:
				outfile.write(tex.pointers[1].data)

			for frags, data in self.sized_str_entry.mat_frags:
				# write root frag, always present
				m0 = frags[0]
				# the name of the material slot or variant
				outfile.write(m0.pointers[1].data)
				# material layers only: write info and attrib frags + children
				for f in frags[1:]:
					outfile.write(f.pointers[1].data)
					# for children, data in f.children:
					# 	outfile.write(data)
		return out_path,

	def update_matcol_pointers(self, pointers, new_names):
		# it looks like fragments are not reused here, and not even pointers are
		# but as they point to the same address the writer treats them as same
		# so the pointer map has to be updated for the involved pools
		# also the copies list has to be adjusted

		# so this is a hack that only considers one entry for each union of pointers
		# map doffset to tuple of pointer and new data
		dic = {}
		for p, n in zip(pointers, new_names):
			dic[p.data_offset] = (p, n.encode() + b"\x00")
		sorted_keys = list(sorted(dic))
		# print(sorted_keys)
		print("Names in ovl order:", list(dic[k][1] for k in sorted_keys))
		sum_l = 0
		for k in sorted_keys:
			p, d = dic[k]
			sum_l += len(d)
			for pc in p.copies:
				pc.data = d
				pc.padding = b""
		# apply padding to the last element
		padding = get_padding(sum_l, alignment=64)
		for pc in p.copies:
			pc.padding = padding

	def load(self, file_path):
		matcol_data = MatcolFile()
		matcol_data.load(file_path)

		if self.sized_str_entry.has_texture_list_frag:
			pointers = [tex_frag.pointers[1] for tex_frag in self.sized_str_entry.tex_frags]
			new_names = [n for t in matcol_data.texture_wrapper.textures for n in
						 (t.fgm_name, t.texture_suffix, t.texture_type)]
		else:
			pointers = []
			new_names = []

		if self.sized_str_entry.is_variant:
			for (m0,), variant in zip(self.sized_str_entry.mat_frags, matcol_data.variant_wrapper.materials):
				# print(layer.name)
				pointers.append(m0.pointers[1])
				new_names.append(variant)
		elif self.sized_str_entry.is_layered:
			for (m0, info, attrib), layer in zip(self.sized_str_entry.mat_frags, matcol_data.layered_wrapper.layers):
				# print(layer.name)
				pointers.append(m0.pointers[1])
				new_names.append(layer.name)
				for frag, wrapper in zip(info.children, layer.infos):
					frag.pointers[0].update_data(as_bytes(wrapper.info), update_copies=True)
					frag.pointers[1].update_data(as_bytes(wrapper.name), update_copies=True)
					pointers.append(frag.pointers[1])
					new_names.append(wrapper.name)
				for frag, wrapper in zip(attrib.children, layer.attribs):
					frag.pointers[0].update_data(as_bytes(wrapper.attrib), update_copies=True)
					frag.pointers[1].update_data(as_bytes(wrapper.name), update_copies=True)
					pointers.append(frag.pointers[1])
					new_names.append(wrapper.name)

		self.update_matcol_pointers(pointers, new_names)
