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


class MatlayersLoader(BaseFile):

	def collect(self, ovl, file_entry):
		self.ovl = ovl
		self.assign_ss_entry(file_entry)
		self.ovs = ovl.static_archive.content
		print("\nMatlayers:", self.sized_str_entry.name)

		# Sized string initpos = position of first fragment for matcol
		self.sized_str_entry.fragments = self.ovs.frags_from_pointer(self.sized_str_entry.pointers[0], 2)
		self.sized_str_entry.f0, self.sized_str_entry.f1 = self.sized_str_entry.fragments

		print(self.sized_str_entry.f0.pointers[1].data)
		# print(self.sized_str_entry.f0)
		# 0,0,collection count,0, 0,0,
		# print(self.sized_str_entry.f1.pointers[0].data, len(self.sized_str_entry.f1.pointers[0].data))
		f0_d0 = struct.unpack("<6I", self.sized_str_entry.f1.pointers[0].data)
		layer_count = f0_d0[2]
		print(f0_d0)
		self.sized_str_entry.tex_frags = self.ovs.frags_from_pointer(self.sized_str_entry.f1.pointers[1],
																	 layer_count*2)
		for tex in self.sized_str_entry.tex_frags:
			# p0 is just 1 or 0, but weird since 8 and 16 bytes alternate
			# first is fgm name, second layer identity name
			# b'Swatch_Thero_TRex_LumpySkin\x00'
			# b'Ichthyosaurus_Layer_01\x00'
			print(tex.pointers[1].data)
			tex.name = self.sized_str_entry.name
            
class MatvarsLoader(BaseFile):

	def collect(self, ovl, file_entry):
		self.ovl = ovl
		self.assign_ss_entry(file_entry)
		self.ovs = ovl.static_archive.content
		print("\nMatlayers:", self.sized_str_entry.name)

		# Sized string initpos = position of first fragment for matcol
		self.sized_str_entry.fragments = self.ovs.frags_from_pointer(self.sized_str_entry.pointers[0], 2)
		self.sized_str_entry.f0, self.sized_str_entry.f1 = self.sized_str_entry.fragments

		print(self.sized_str_entry.f0.pointers[1].data)
		# print(self.sized_str_entry.f0)
		# 0,0,collection count,0, 0,0,
		# print(self.sized_str_entry.f1.pointers[0].data, len(self.sized_str_entry.f1.pointers[0].data))
		f0_d0 = struct.unpack("<6I", self.sized_str_entry.f1.pointers[0].data)
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

	def collect(self, ovl, file_entry):
		self.ovl = ovl
		self.assign_ss_entry(file_entry)
		self.ovs = ovl.static_archive.content
		print("\nMatlayers:", self.sized_str_entry.name)

		# Sized string initpos = position of first fragment for matcol
		self.sized_str_entry.fragments = self.ovs.frags_from_pointer(self.sized_str_entry.pointers[0], 1)
		self.sized_str_entry.f0 = self.sized_str_entry.fragments[0]

		print(self.sized_str_entry.f0.pointers[1].data)
		print(self.sized_str_entry.f0.pointers[0].data)
		# print(self.sized_str_entry.f0)
		# 0,0,collection count,0, 0,0,
		# print(self.sized_str_entry.f1.pointers[0].data, len(self.sized_str_entry.f1.pointers[0].data))
		#f0_d0 = struct.unpack("<6I", self.sized_str_entry.f1.pointers[0].data)
		#layer_count = f0_d0[2] - 1
		#print(f0_d0)
		#self.sized_str_entry.tex_frags = self.ovs.frags_from_pointer(self.sized_str_entry.f1.pointers[1],
		#															 layer_count)
		#for tex in self.sized_str_entry.tex_frags:
			# p0 is just 1 or 0, but weird since 8 and 16 bytes alternate
			# first is fgm name, second layer identity name
			# b'Swatch_Thero_TRex_LumpySkin\x00'
			# b'Ichthyosaurus_Layer_01\x00'
			#print(tex.pointers[1].data)
			#tex.name = self.sized_str_entry.name
            
class MatpatsLoader(BaseFile):

	def collect(self, ovl, file_entry):
		self.ovl = ovl
		self.assign_ss_entry(file_entry)
		self.ovs = ovl.static_archive.content
		print("\nMatlayers:", self.sized_str_entry.name)

		# Sized string initpos = position of first fragment for matcol
		self.sized_str_entry.fragments = self.ovs.frags_from_pointer(self.sized_str_entry.pointers[0], 1)
		self.sized_str_entry.f0 = self.sized_str_entry.fragments[0]

		print(self.sized_str_entry.f0.pointers[1].data)
		# print(self.sized_str_entry.f0)
		# 0,0,collection count,0, 0,0,
		# print(self.sized_str_entry.f1.pointers[0].data, len(self.sized_str_entry.f1.pointers[0].data))
		f0_d0 = struct.unpack("<4I", self.sized_str_entry.f0.pointers[0].data)
		layer_count = f0_d0[2]
		print(f0_d0)
		self.sized_str_entry.fragments.extend(self.ovs.frags_from_pointer(self.sized_str_entry.pointers[0], layer_count*2))
        
		self.sized_str_entry.f1 = self.sized_str_entry.fragments[1]
		self.sized_str_entry.f2 = self.sized_str_entry.fragments[2]
		print(self.sized_str_entry.f1.pointers[1].data)
		f2_d0 = struct.unpack("<6I", self.sized_str_entry.f2.pointers[0].data)
		layer_count2 = f2_d0[2] - 1
		print(f2_d0)
        
		self.sized_str_entry.tex_frags = self.ovs.frags_from_pointer(self.sized_str_entry.f2.pointers[1], layer_count2)
        
		#print(self.sized_str_entry.fragments)
		for tex in self.sized_str_entry.tex_frags:
			# p0 is just 1 or 0, but weird since 8 and 16 bytes alternate
			# first is fgm name, second layer identity name
			# b'Swatch_Thero_TRex_LumpySkin\x00'
			# b'Ichthyosaurus_Layer_01\x00'
			print(tex.pointers[1].data)
			tex.name = self.sized_str_entry.name
