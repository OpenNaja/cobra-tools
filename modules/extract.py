import struct
import os
import traceback
import sys

import util.interaction
import modules.formats.shared
from modules.formats.BANI import write_banis, write_bani
from modules.formats.BNK import write_bnk
from modules.formats.DDS import write_tex
from modules.formats.ENUMNAMER import write_enumnamer
from modules.formats.FCT import write_fct
from modules.formats.FDB import write_fdb
from modules.formats.FGM import write_fgm
from modules.formats.LUA import write_lua
from modules.formats.MANI import write_manis
from modules.formats.MATCOL import write_materialcollection
from modules.formats.MOTIONGRAPHVARS import write_motiongraphvars
from modules.formats.MS2 import write_ms2
from modules.formats.SPECDEF import write_specdef
from modules.formats.TXT import write_txt
from modules.formats.VOXELSKIRT import write_voxelskirt
from modules.formats.XMLCONFIG import write_xmlconfig
from util import widgets


IGNORE_TYPES = (".mani", ".mdl2", ".texturestream", ".datastreams")
SUPPORTED_TYPES = (".dds", ".png", ".mdl2", ".txt", ".fgm", ".fdb", ".matcol", ".xmlconfig", ".assetpkg", ".lua", ".wem", ".otf", ".ttf")


def extract_kernel(archive, entry, out_dir_func, show_temp_files, progress_callback):
	# automatically call the extract function, if it has been defined
	try:
		func_name = f"write_{entry.ext[1:]}"
		# print(func_name)
		# print(__name__)
		func = getattr(sys.modules[__name__], func_name)
		return func(archive, entry, out_dir_func, show_temp_files, progress_callback)
	except AttributeError:
		print(f"No function to export {entry.name}")
		return ()


def write_gfx(archive, sized_str_entry, out_dir, show_temp_files, progress_callback):
	name = sized_str_entry.name
	print(f"\nWriting {name}")

	out_path = out_dir(name)
	buffers = sized_str_entry.data_entry.buffer_datas
	with open(out_path, 'wb') as outfile:
		outfile.write(sized_str_entry.pointers[0].data)
		for buff in buffers:
			outfile.write(buff)
	return out_path,


def write_scaleform(archive, sized_str_entry, out_dir, show_temp_files, progress_callback):
	name = sized_str_entry.name
	print(f"\nWriting {name}")

	out_path = out_dir(name)
	with open(out_path, 'wb') as outfile:
		# write each of the fragments
		outfile.write(sized_str_entry.pointers[0].data)
		for frag in sized_str_entry.fragments:
			outfile.write(frag.pointers[0].data)
			outfile.write(frag.pointers[1].data)
	return out_path,


def write_prefab(archive, sized_str_entry, out_dir, show_temp_files, progress_callback):
	name = sized_str_entry.name
	print("\nWriting", name)

	try:
		buffer_data = sized_str_entry.data_entry.buffer_datas[0]
		print("buffer size", len(buffer_data))
	except:
		print("Found no buffer data for", name)
		buffer_data = b""
	# if len(sized_str_entry.fragments) != 2:
	#	print("must have 2 fragments")
	#	return
	# write lua
	# with open(archive.indir(name), 'wb') as outfile:
	#	# write the buffer
	#	outfile.write(buffer_data)

	with open(archive.indir(name), 'wb') as outfile:
		# write each of the fragments
		# print(sized_str_entry.pointers[0].data)
		outfile.write(sized_str_entry.pointers[0].data)
		for frag in sized_str_entry.fragments:
			# print(frag.pointers[0].data)
			# print(frag.pointers[1].data)
			outfile.write(frag.pointers[0].data)
			outfile.write(frag.pointers[1].data)


def write_assetpkg(archive, sized_str_entry, out_dir, show_temp_files, progress_callback):
	name = sized_str_entry.name
	print("\nWriting", name)
	#if len(sized_str_entry.fragments) == 1:
		#print(len(sized_str_entry.fragments))
	f_0 = sized_str_entry.fragments[0]
	#else:
		#print("Found wrong amount of frags for", name)
		#return
	out_path=out_dir(name)
	with open(out_path, 'wb') as outfile:
		f_0.pointers[1].strip_zstring_padding()
		outfile.write(f_0.pointers[1].data[:-1])

	return out_path,


def write_userinterfaceicondata(archive, sized_str_entry, out_dir, show_temp_files, progress_callback):
	name = sized_str_entry.name
	print("\nWriting", name)
	out_path=out_dir(name)
	try:
		buffer_data = sized_str_entry.data_entry.buffer_datas[0]
		print("buffer size", len(buffer_data))
	except:
		print("Found no buffer data for", name)
		buffer_data = b""
	if len(sized_str_entry.fragments) == 2:
		f_0, f_1 = sized_str_entry.fragments
	else:
		print("Found wrong amount of frags for", name)
		#return
	# write xml
	xml_header = struct.pack("<12s3I", b"USERICONDATA", f_0.pointers[1].data_size,
							 f_1.pointers[1].data_size, len(buffer_data))
	f_0 = sized_str_entry.fragments[0]
	f_1 = sized_str_entry.fragments[1]
	with open(out_path, 'wb') as outfile:
		# write custom FGM header
		#outfile.write(xml_header)
		# write each of the fragments
		#outfile.write(sized_str_entry.pointers[0].data)
		#for frag in sized_str_entry.fragments:
			#outfile.write(frag.pointers[0].data)
		f_0.pointers[1].strip_zstring_padding()
		outfile.write(f_0.pointers[1].data[:-1])
		# write the buffer
		#outfile.write(buffer_data)
	with open(out_path+"_b", 'wb') as outfile:
		f_1.pointers[1].strip_zstring_padding()
		outfile.write(f_1.pointers[1].data[:-1])
	return out_path, out_path+"_b"
