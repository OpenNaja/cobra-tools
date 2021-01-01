import struct

from modules.util import as_bytes
from generated.formats.fgm import FgmFile


def write_fgm(archive, sized_str_entry, out_dir):
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
	fgm_file_entry = [file for file in archive.ovl.files if f"{file.name}.{file.ext}" == sized_str_entry.name][0]

	# write fgm
	ovl = archive.ovl
	fgm_header = struct.pack("<4s4B7I", b"FGM ", ovl.version_flag, ovl.version, ovl.bitswap, ovl.seventh_byte, int(ovl.user_version), len(sized_str_entry.fragments), len(fgm_file_entry.textures), len_tex_info, attr_info.pointers[1].data_size, len_zeros, data_lib.pointers[1].data_size,)

	# print(file_entry.textures)
	out_path = out_dir(name)
	# for i, f in enumerate(sized_str_entry.fragments):
	# 	with open(out_path+str(i), 'wb') as outfile:
	# 		outfile.write( f.pointers[1].data )
	with open(out_path, 'wb') as outfile:
		# write custom FGM header
		outfile.write(fgm_header)
		for tex in fgm_file_entry.textures:
			outfile.write(tex.name.encode())
			outfile.write(b"\x00")
		outfile.write(sized_str_entry.pointers[0].data)
		# write each of the fragments
		for frag in sized_str_entry.fragments:
			outfile.write(frag.pointers[1].data)
		# write the buffer
		outfile.write(buffer_data)
	return out_path,


def load_fgm(ovl_data, fgm_file_path, fgm_sized_str_entry):

	fgm_data = FgmFile()
	fgm_data.load(fgm_file_path)

	sizedstr_bytes = as_bytes(fgm_data.fgm_info) + as_bytes(fgm_data.two_frags_pad)

	# todo - move texpad into fragment padding?
	textures_bytes = as_bytes(fgm_data.textures) + as_bytes(fgm_data.texpad)
	attributes_bytes = as_bytes(fgm_data.attributes)

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