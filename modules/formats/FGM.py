import struct

from modules.formats.shared import pack_header, get_versions, djb
from modules.helpers import as_bytes
from generated.formats.fgm import FgmFile


def get_file_entry(ovl, sized_str_entry):
	for entry in ovl.files:
		if entry.name == sized_str_entry.name:
			return entry


def write_fgm(ovl, sized_str_entry, out_dir, show_temp_files, progress_callback):
	name = sized_str_entry.name
	print("\nWriting", name)
	try:
		buffer_data = sized_str_entry.data_entry.buffer_datas[0]
		print("buffer size", len(buffer_data))
	except:
		print("Found no buffer data for", name)
		buffer_data = b""
	# basic fgms
	if len(sized_str_entry.fragments) == 4:
		tex_info, attr_info, zeros, data_lib = sized_str_entry.fragments
		len_tex_info = tex_info.pointers[1].data_size
		len_zeros = zeros.pointers[1].data_size
	# no zeros, otherwise same as basic
	elif len(sized_str_entry.fragments) == 3:
		tex_info, attr_info, data_lib = sized_str_entry.fragments
		len_tex_info = tex_info.pointers[1].data_size
		len_zeros = 0
	# fgms for variants
	elif len(sized_str_entry.fragments) == 2:
		attr_info, data_lib = sized_str_entry.fragments
		len_tex_info = 0
		len_zeros = 0
	else:
		raise AttributeError("Fgm length is wrong")

	# grab the texture names that are linked to this fgm
	fgm_file_entry = get_file_entry(ovl, sized_str_entry)

	# write fgm
	fgm_header = struct.pack("<6I", len(sized_str_entry.fragments), len(fgm_file_entry.dependencies), len_tex_info, attr_info.pointers[1].data_size, len_zeros, data_lib.pointers[1].data_size,)

	# print(file_entry.textures)
	out_path = out_dir(name)
	# for i, f in enumerate(sized_str_entry.fragments):
	# 	with open(out_path+str(i), 'wb') as outfile:
	# 		outfile.write( f.pointers[1].data )
	with open(out_path, 'wb') as outfile:
		# write custom FGM header
		outfile.write(pack_header(ovl, b"FGM "))
		outfile.write(fgm_header)
		for tex in fgm_file_entry.dependencies:
			outfile.write(tex.basename.encode())
			outfile.write(b"\x00")
		outfile.write(sized_str_entry.pointers[0].data)
		# write each of the fragments
		for frag in sized_str_entry.fragments:
			outfile.write(frag.pointers[1].data)
		# write the buffer
		outfile.write(buffer_data)
	return out_path,


def load_fgm(ovl, fgm_file_path, fgm_sized_str_entry):

	versions = get_versions(ovl)
	fgm_data = FgmFile()
	fgm_data.load(fgm_file_path)

	sizedstr_bytes = as_bytes(fgm_data.fgm_info, version_info=versions) + as_bytes(fgm_data.two_frags_pad, version_info=versions)

	# todo - move texpad into fragment padding?
	textures_bytes = as_bytes(fgm_data.textures, version_info=versions) + as_bytes(fgm_data.texpad, version_info=versions)
	attributes_bytes = as_bytes(fgm_data.attributes, version_info=versions)

	# the actual injection
	fgm_sized_str_entry.data_entry.update_data((fgm_data.buffer_bytes,))
	fgm_sized_str_entry.pointers[0].update_data(sizedstr_bytes, update_copies=True)

	if len(fgm_sized_str_entry.fragments) == 4:
		datas = (textures_bytes, attributes_bytes, fgm_data.zeros_bytes, fgm_data.data_bytes)
	# fgms without zeros
	elif len(fgm_sized_str_entry.fragments) == 3:
		datas = (textures_bytes, attributes_bytes, fgm_data.data_bytes)
	# fgms for variants
	elif len(fgm_sized_str_entry.fragments) == 2:
		datas = (attributes_bytes, fgm_data.data_bytes)
	else:
		raise AttributeError("Unexpected fgm frag count")

	# inject fragment datas
	for frag, data in zip(fgm_sized_str_entry.fragments, datas):
		frag.pointers[1].update_data(data, update_copies=True)

	# update dependencies on ovl
	fgm_file_entry = get_file_entry(ovl, fgm_sized_str_entry)
	for dep_entry, tex_name in zip(fgm_file_entry.dependencies, fgm_data.texture_names):
		dep_entry.basename = tex_name
		dep_entry.name = dep_entry.basename + dep_entry.ext.replace(":", ".")
		dep_entry.file_hash = djb(tex_name.lower())
