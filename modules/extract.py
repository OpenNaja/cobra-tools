import struct
import os
import traceback
import sys

import modules.formats.shared
import util.interaction
from modules.formats.BANI import write_banis, write_bani
from modules.formats.BNK import write_bnk
from modules.formats.DDS import write_dds
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


def extract_names(archive, names, out_dir, show_temp_files=False, progress_callback=None):
	def out_dir_func(n):
		"""Helper function to generate temporary output file name"""
		return os.path.normpath(os.path.join(out_dir, n))

	print("Extracting by name...")
	# the temporary file paths that are passed to windows to move the files to their final destination
	paths = []

	print("\nExtracting from archive", archive.archive_index)
	entry_dict = {entry.name: entry for entry in archive.sized_str_entries}
	# export all selected files
	for file_index, file in enumerate(names):
		print(file_index, file)
		basename, ext = os.path.splitext(file)

		if ext in IGNORE_TYPES:
			print(f"Ignoring {file}, as it is not a standalone file!")
			continue

		if file in entry_dict:
			print("Found name", file)
			entry = entry_dict[file]
			try:
				paths.extend(extract_kernel(archive, entry, out_dir_func, show_temp_files, progress_callback))
			except BaseException as error:
				print(f"\nAn exception occurred while extracting {entry.name}")
				traceback.print_exc()
				util.interaction.showdialog(str(error))

		else:
			print(f"ERROR: file {file} not found in archive")

		if progress_callback:
			progress_callback(f"Extracting {file}", value=file_index + 1, vmax=len(names))

	return paths


def extract_kernel(archive, entry, out_dir_func, show_temp_files, progress_callback):
	# try:
	# 	func_name = f"write_{entry.ext[1:]}"
	# 	print(func_name)
	# 	func = getattr(sys.modules[__name__], func_name)
	# except AttributeError:
	# 	print(f"No function to export {entry.name}")
	# return func(archive, entry, out_dir_func, )
	if entry.ext == ".banis":
		return write_banis(archive, entry, out_dir_func)
	elif entry.ext == ".bani":
		return write_bani(archive, entry, out_dir_func)
	elif entry.ext == ".manis":
		return write_manis(archive, entry, out_dir_func)
	elif entry.ext == ".fgm":
		return write_fgm(archive, entry, out_dir_func)
	elif entry.ext == ".ms2":
		return write_ms2(archive, entry, out_dir_func)
	elif entry.ext == ".materialcollection":
		return write_materialcollection(archive, entry, out_dir_func)
	elif entry.ext == ".tex":
		return write_dds(archive, entry, out_dir_func, show_temp_files)
	elif entry.ext == ".lua":
		return write_lua(archive, entry, out_dir_func)
	elif entry.ext == ".assetpkg":
		return write_assetpkg(archive, entry, out_dir_func)
	elif entry.ext == ".fdb":
		return write_fdb(archive, entry, out_dir_func)
	elif entry.ext == ".xmlconfig":
		return write_xmlconfig(archive, entry, out_dir_func)
	elif entry.ext == ".userinterfaceicondata":
		return write_userinterfaceicondata(archive, entry, out_dir_func)
	elif entry.ext == ".txt":
		return write_txt(archive, entry, out_dir_func)
	elif entry.ext == ".specdef":
		return write_specdef(archive, entry, out_dir_func)
	elif entry.ext == ".bnk":
		return write_bnk(archive, entry, out_dir_func, show_temp_files, progress_callback)
	# elif entry.ext == ".prefab" and extract_misc == True:
	# 	write_prefab(archive, entry)
	elif entry.ext == ".voxelskirt":
		return write_voxelskirt(archive, entry, out_dir_func)
	elif entry.ext == ".gfx":
		return write_gfx(archive, entry, out_dir_func)
	elif entry.ext == ".fct":
		return write_fct(archive, entry, out_dir_func)
	elif entry.ext == ".scaleformlanguagedata":
		return write_scaleform(archive, entry, out_dir_func)
	elif entry.ext == ".enumnamer":
		return write_enumnamer(archive, entry, out_dir_func)
	elif entry.ext == ".motiongraphvars":
		return write_motiongraphvars(archive, entry, out_dir_func)
	else:
		print("\nSkipping", entry.name)


def extract(archive, out_dir, only_types=(), show_temp_files=False, progress_callback=None):
	"""Extract the files, after all archives have been read"""

	def out_dir_func(n):
		"""Helper function to generate temporary output file name"""
		return os.path.normpath(os.path.join(out_dir, n))

	# the actual export, per file type
	error_files = []
	skip_files = []
	out_paths = []
	print("\nExtracting from archive", archive.archive_index)
	ss_max = len(archive.sized_str_entries)
	for ss_index, sized_str_entry in enumerate(archive.sized_str_entries):
		try:
			# for batch operations, only export those we need
			if only_types and sized_str_entry.ext not in only_types:
				continue
			# ignore types in the count that we export from inside other type exporters
			if sized_str_entry.ext in IGNORE_TYPES:
				continue
			out_paths.extend(extract_kernel(archive, sized_str_entry, out_dir_func, show_temp_files, progress_callback))

			if progress_callback:
				progress_callback("Extracting " + sized_str_entry.name, value=ss_index, vmax=ss_max)
		except BaseException as error:
			print(f"\nAn exception occurred while extracting {sized_str_entry.name}")
			print(error)
			traceback.print_exc()
			error_files.append(sized_str_entry.name)

	return error_files, skip_files


def write_gfx(archive, sized_str_entry, out_dir):
	name = sized_str_entry.name
	print(f"\nWriting {name}")

	out_path = out_dir(name)
	buffers = sized_str_entry.data_entry.buffer_datas
	with open(out_path, 'wb') as outfile:
		outfile.write(sized_str_entry.pointers[0].data)
		for buff in buffers:
			outfile.write(buff)
	return out_path,


def write_scaleform(archive, sized_str_entry, out_dir):
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


def write_prefab(archive, sized_str_entry):
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


def write_assetpkg(archive, sized_str_entry, out_dir):
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

def write_userinterfaceicondata(archive, sized_str_entry, out_dir):
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
