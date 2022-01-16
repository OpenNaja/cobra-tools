import logging
import struct

from generated.formats.matcol.compound.LayerFrag import LayerFrag
from generated.formats.matcol.compound.RootFrag import RootFrag
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
		header = self.sized_str_entry.f0.pointers[1].load_as(RootFrag)[0]
		# print(ptr, one)
		print(header)
		# mat_type (3=variant, 2=layered)
		self.sized_str_entry.is_variant = header.mat_type == 3
		self.sized_str_entry.is_layered = header.mat_type == 2
		if header.tex_count:
			self.sized_str_entry.tex_pointer = self.ovs.frags_from_pointer(self.sized_str_entry.f0.pointers[1], 1)[0]
			self.sized_str_entry.tex_frags = self.ovs.frags_from_pointer(self.sized_str_entry.tex_pointer.pointers[1], header.tex_count * 3)
			self.sized_str_entry.fragments.extend(self.sized_str_entry.tex_frags)
			self.sized_str_entry.fragments.append(self.sized_str_entry.tex_pointer)
		else:
			self.sized_str_entry.tex_frags = []
		# material pointer frag
		self.sized_str_entry.mat_pointer = self.ovs.frags_from_pointer(self.sized_str_entry.f0.pointers[1], 1)[0]
		self.sized_str_entry.fragments.append(self.sized_str_entry.mat_pointer)
		self.sized_str_entry.mat_structs = self.collect_array_structs(self.sized_str_entry.mat_pointer.pointers[1], header.mat_count, LayerFrag)
		for frags, data in self.sized_str_entry.mat_structs:
			self.sized_str_entry.fragments.extend(frags)
			# rel [0, 24, 56] or [0]
			if self.sized_str_entry.is_layered:
				m0, info, attrib = frags
				info.children, info.data = self.collect_array(info.pointers[1], data.info_count, 32)
				attrib.children, attrib.data = self.collect_array(attrib.pointers[1], data.attrib_count, 16)
				self.sized_str_entry.fragments.extend(info.children)
				self.sized_str_entry.fragments.extend(attrib.children)

	def extract(self, out_dir, show_temp_files, progress_callback):
		name = self.sized_str_entry.name.replace("materialcollection", "matcol")
		logging.info(f"Writing {name}")
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

			# outfile.write(self.sized_str_entry.mat_pointer.pointers[1].data)
			for frags, data in self.sized_str_entry.mat_structs:
				# write root frag, always present
				m0 = frags[0]
				# counts
				outfile.write(as_bytes(data))
				# the name of the material slot or variant
				outfile.write(m0.pointers[1].data)
				# material layers only: write info and attrib frags + children
				for f in frags[1:]:
					outfile.write(f.pointers[1].data)
					for c in f.children:
						outfile.write(as_bytes(self.p1_ztsr(c)))
		m = MatcolFile()
		m.load(out_path)
		print(m)
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
			for (m0,), variant in zip(self.sized_str_entry.mat_structs, matcol_data.variant_wrapper.materials):
				# print(layer.name)
				pointers.append(m0.pointers[1])
				new_names.append(variant)
		elif self.sized_str_entry.is_layered:
			for (m0, info, attrib), layer in zip(self.sized_str_entry.mat_structs, matcol_data.layered_wrapper.layers):
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
