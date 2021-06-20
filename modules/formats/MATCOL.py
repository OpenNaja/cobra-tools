import struct

from modules.formats.BaseFormat import BaseFile
from modules.formats.shared import get_padding
from modules.helpers import as_bytes
from generated.formats.matcol import MatcolFile


def write_materialcollection(ovl, sized_str_entry, out_dir, show_temp_files, progress_callback):
	name = sized_str_entry.name.replace("materialcollection", "matcol")
	print("\nWriting", name)

	matcol_header = struct.pack("<4s 2I B", b"MATC ", int(ovl.version), int(ovl.user_version),
								sized_str_entry.has_texture_list_frag)

	out_path = out_dir(name)
	with open(out_path, 'wb') as outfile:
		# write custom matcol header
		outfile.write(matcol_header)

		outfile.write(sized_str_entry.f0.pointers[0].data)
		outfile.write(sized_str_entry.f0.pointers[1].data)
		if sized_str_entry.has_texture_list_frag:
			outfile.write(sized_str_entry.tex_pointer.pointers[0].data)
			for tex in sized_str_entry.tex_frags:
				outfile.write(tex.pointers[1].data)

		outfile.write(sized_str_entry.mat_pointer.pointers[0].data)
		for tup in sized_str_entry.mat_frags:
			# write root frag, always present
			m0 = tup[0]
			# the name of the material slot or variant
			outfile.write(m0.pointers[1].data)
			# material layers only: write info and attrib frags + children
			for f in tup[1:]:
				outfile.write(f.pointers[0].data)
				for child in f.children:
					for pointer in child.pointers:
						outfile.write(pointer.data)

	return out_path,


def update_matcol_pointers(pointers, new_names):
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


def load_materialcollection(ovl_data, matcol_file_path, sized_str_entry):
	matcol_data = MatcolFile()
	matcol_data.load(matcol_file_path)

	if sized_str_entry.has_texture_list_frag:
		pointers = [tex_frag.pointers[1] for tex_frag in sized_str_entry.tex_frags]
		new_names = [n for t in matcol_data.texture_wrapper.textures for n in
					 (t.fgm_name, t.texture_suffix, t.texture_type)]
	else:
		pointers = []
		new_names = []

	if sized_str_entry.is_variant:
		for (m0,), variant in zip(sized_str_entry.mat_frags, matcol_data.variant_wrapper.materials):
			# print(layer.name)
			pointers.append(m0.pointers[1])
			new_names.append(variant)
	elif sized_str_entry.is_layered:
		for (m0, info, attrib), layer in zip(sized_str_entry.mat_frags, matcol_data.layered_wrapper.layers):
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

	update_matcol_pointers(pointers, new_names)


class MatcolLoader(BaseFile):

	def collect(self, ovl, file_entry):
		self.ovl = ovl
		self.assign_ss_entry(file_entry)
		self.ovs = ovl.static_archive.content
		print("\nMATCOL:", self.sized_str_entry.name)

		# Sized string initpos = position of first fragment for matcol
		self.sized_str_entry.fragments = self.ovs.frags_from_pointer(self.sized_str_entry.pointers[0], 1)
		self.sized_str_entry.f0 = self.sized_str_entry.fragments[0]

		# print(self.sized_str_entry.f0)
		# 0,0,collection count,0
		f0_d0 = struct.unpack("<4I", self.sized_str_entry.f0.pointers[0].data)
		# flag (3=variant, 2=layered) , 0
		self.sized_str_entry.has_texture_list_frag = len(self.sized_str_entry.f0.pointers[1].data) == 8
		if self.sized_str_entry.has_texture_list_frag:
			f0_d1 = struct.unpack("<2I", self.sized_str_entry.f0.pointers[1].data)
		else:
			f0_d1 = struct.unpack("<6I", self.sized_str_entry.f0.pointers[1].data)
		# print("f0_d0", f0_d0)
		# print("f0_d1", f0_d1)
		self.sized_str_entry.is_variant = f0_d1[0] == 3
		self.sized_str_entry.is_layered = f0_d1[0] == 2
		# print("has_texture_list_frag",self.sized_str_entry.has_texture_list_frag)
		# print("is_variant",self.sized_str_entry.is_variant)
		# print("is_layered",self.sized_str_entry.is_layered)
		# print(self.sized_str_entry.tex_pointer)
		if self.sized_str_entry.has_texture_list_frag:
			self.sized_str_entry.tex_pointer = self.ovs.frags_from_pointer(self.sized_str_entry.f0.pointers[1], 1)[0]
			tex_pointer_d0 = struct.unpack("<4I", self.sized_str_entry.tex_pointer.pointers[0].data)
			# print("tex_pointer_d0", tex_pointer_d0)
			tex_count = tex_pointer_d0[2]
			# print("tex_count",tex_count)
			self.sized_str_entry.tex_frags = self.ovs.frags_from_pointer(self.sized_str_entry.tex_pointer.pointers[1], tex_count * 3)
		else:
			self.sized_str_entry.tex_pointer = None
		# material pointer frag
		self.sized_str_entry.mat_pointer = self.ovs.frags_from_pointer(self.sized_str_entry.f0.pointers[1], 1)[0]
		mat_pointer_d0 = struct.unpack("<6I", self.sized_str_entry.mat_pointer.pointers[0].data)
		# print("mat_pointer_d0",mat_pointer_d0)
		mat_count = mat_pointer_d0[2]
		# print("mat_count",mat_count)
		self.sized_str_entry.mat_frags = []
		for t in range(mat_count):
			if self.sized_str_entry.is_variant:
				m0 = self.ovs.frags_from_pointer(self.sized_str_entry.mat_pointer.pointers[1], 1)[0]
				# print(m0.pointers[1].data)
				m0.name = self.sized_str_entry.name
				self.sized_str_entry.mat_frags.append((m0,))
			elif self.sized_str_entry.is_layered:
				mat_frags = self.ovs.frags_from_pointer(self.sized_str_entry.mat_pointer.pointers[1], 3)
				m0, info, attrib = mat_frags
				m0.pointers[1].strip_zstring_padding()
				# print(m0.pointers[1].data)

				info_d0 = struct.unpack("<8I", info.pointers[0].data)
				info_count = info_d0[2]
				# print("info_count", info_count)
				info.children = self.ovs.frags_from_pointer(info.pointers[1], info_count)
				for info_child in info.children:
					# 0,0,byte flag,byte flag,byte flag,byte flag,float,float,float,float,0
					# info_child_d0 = struct.unpack("<2I4B4fI", info_child.pointers[0].data)
					info_child.pointers[1].strip_zstring_padding()
				# print(info_child.pointers[1].data, info_d0)

				attrib.children = []
				attrib.pointers[0].split_data_padding(16)
				attrib_d0 = struct.unpack("<4I", attrib.pointers[0].data)
				attrib_count = attrib_d0[2]
				# print("attrib_count",attrib_count)
				attrib.children = self.ovs.frags_from_pointer(attrib.pointers[1], attrib_count)
				for attr_child in attrib.children:
					# attr_child_d0 = struct.unpack("<2I4BI", attr_child.pointers[0].data)
					attr_child.pointers[1].strip_zstring_padding()
				# print(attr_child.pointers[1].data, attr_child_d0)

				# store names for frag log
				for frag in mat_frags + info.children + attrib.children:
					frag.name = self.sized_str_entry.name
				# store frags
				self.sized_str_entry.mat_frags.append(mat_frags)
		if self.sized_str_entry.has_texture_list_frag:
			for frag in self.sized_str_entry.tex_frags + [self.sized_str_entry.tex_pointer, ]:
				frag.name = self.sized_str_entry.name
		all_frags = [self.sized_str_entry.f0, self.sized_str_entry.mat_pointer]
		for frag in all_frags:
			frag.name = self.sized_str_entry.name
