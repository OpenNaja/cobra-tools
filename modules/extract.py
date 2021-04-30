import struct
import os
import traceback
import sys

import ovl_util.interaction
import modules.formats.shared
from modules.formats.ASSETPKG import write_assetpkg
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
from ovl_util import widgets

IGNORE_TYPES = (".mani", ".mdl2", ".texturestream", ".datastreams", ".model2stream")
SUPPORTED_TYPES = (".dds", ".png", ".ms2", ".txt", ".fgm", ".fdb", ".matcol", ".xmlconfig", ".assetpkg", ".lua", ".wem", ".otf", ".ttf")


def extract_kernel(ovl, entry, out_dir_func, show_temp_files, progress_callback):
	# automatically call the extract function, if it has been defined
	namespace = sys.modules[__name__]
	func_name = f"write_{entry.ext[1:]}"
	func = getattr(namespace, func_name, None)
	if func:
		return func(ovl, entry, out_dir_func, show_temp_files, progress_callback)
	else:
		print(f"No function to export {entry.name}")


def write_gfx(ovl, sized_str_entry, out_dir, show_temp_files, progress_callback):
	name = sized_str_entry.name
	print(f"\nWriting {name}")

	out_path = out_dir(name)
	buffers = sized_str_entry.data_entry.buffer_datas
	with open(out_path, 'wb') as outfile:
		outfile.write(sized_str_entry.pointers[0].data)
		for buff in buffers:
			outfile.write(buff)
	return out_path,


def write_scaleform(ovl, sized_str_entry, out_dir, show_temp_files, progress_callback):
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


def write_prefab(ovl, sized_str_entry, out_dir, show_temp_files, progress_callback):
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

	with open(out_dir(name), 'wb') as outfile:
		# write each of the fragments
		# print(sized_str_entry.pointers[0].data)
		outfile.write(sized_str_entry.pointers[0].data)
		for frag in sized_str_entry.fragments:
			# print(frag.pointers[0].data)
			# print(frag.pointers[1].data)
			outfile.write(frag.pointers[0].data)
			outfile.write(frag.pointers[1].data)


def write_userinterfaceicondata(ovl, sized_str_entry, out_dir, show_temp_files, progress_callback):
	name = sized_str_entry.name
	print("\nWriting", name)
	out_path = out_dir(name)
	with open(out_path, 'wb') as outfile:
		for frag in sized_str_entry.fragments:
			frag.pointers[1].strip_zstring_padding()
			outfile.write(frag.pointers[1].data[:-1])
			outfile.write(b"\n")
	return out_path,
