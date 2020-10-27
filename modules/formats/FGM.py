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
	# for i, f in enumerate(sized_str_entry.fragments):
	# 	with open(archive.indir(name)+str(i), 'wb') as outfile:
	# 		outfile.write( f.pointers[1].data )
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
	# write fgm
	fgm_header = struct.pack("<4s7I", b"FGM ", archive.ovl.version, archive.ovl.flag_2, len(sized_str_entry.fragments), len_tex_info, attr_info.pointers[1].data_size, len_zeros, data_lib.pointers[1].data_size, )

	out_path = out_dir(name)
	with open(out_path, 'wb') as outfile:
		# write custom FGM header
		outfile.write(fgm_header)
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