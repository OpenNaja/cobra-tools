import struct


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
