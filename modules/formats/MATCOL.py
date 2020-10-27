import struct

from modules.util import as_bytes
from generated.formats.matcol import MatcolFile


def write_materialcollection(archive, sized_str_entry, out_dir):
	name = sized_str_entry.name.replace("materialcollection", "matcol")
	print("\nWriting",name)

	matcol_header = struct.pack("<4s 2I B", b"MATC ", archive.ovl.version, archive.ovl.flag_2, sized_str_entry.has_texture_list_frag )

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
	# so the pointer map has to be updated for the involved header entries
	# also the copies list has to be adjusted

	# so this is a hack that only considers one entry for each union of pointers
	# map doffset to tuple of pointer and new data
	dic = {}
	for p, n in zip(pointers, new_names):
		dic[p.data_offset] = (p, n.encode() + b"\x00")
	sorted_keys = list(sorted(dic))
	# print(sorted_keys)
	print("Names in ovl order:", list(dic[k][1] for k in sorted_keys))
	sum = 0
	for k in sorted_keys:
		p, d = dic[k]
		sum += len(d)
		for pc in p.copies:
			pc.data = d
			pc.padding = b""
	pad_to = 64
	mod = sum % pad_to
	if mod:
		padding = b"\x00" * (pad_to-mod)
	else:
		padding = b""
	for pc in p.copies:
		pc.padding = padding


def load_materialcollection(ovl_data, matcol_file_path, sized_str_entry):
	matcol_data = MatcolFile()
	matcol_data.load(matcol_file_path)

	if sized_str_entry.has_texture_list_frag:
		pointers = [tex_frag.pointers[1] for tex_frag in sized_str_entry.tex_frags]
		new_names = [n for t in matcol_data.texture_wrapper.textures for n in (t.fgm_name, t.texture_suffix, t.texture_type)]
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
