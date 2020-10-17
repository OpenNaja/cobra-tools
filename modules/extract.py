import struct
import os
import traceback

from modules.formats.BANI import write_banis, write_bani
from modules.formats.BNK import write_bnk
from modules.formats.DDS import write_dds
from modules.formats.FCT import write_fct
from modules.formats.FDB import write_fdb
from modules.formats.FGM import write_fgm
from modules.formats.LUA import write_lua
from modules.formats.MANI import write_manis
from modules.formats.MATCOL import write_materialcollection
from modules.formats.MS2 import write_ms2

from modules.formats.TXT import write_txt

IGNORE_TYPES = ("mani", "mdl2", "texturestream", "datastreams")


def extract_names(archive, names, out_dir, progress_callback=None):

	def out_dir_func(n):
		"""Helper function to generate temporary output file name"""
		return os.path.join(out_dir, n)

	print("Extracting by name...")
	# the temporary file paths that are passed to windows to move the files to their final destination
	paths = []

	# the actual export, per file type
	error_files = []
	skip_files = []
	# data types that we export starting from other file types but are not caught as deliberate cases

	print("\nExtracting from archive", archive.archive_index)
	entry_dict = {entry.name: entry for entry in archive.sized_str_entries}
	# print(entry_dict)
	# print(names)
	# export all selected files
	for file_index, file in enumerate(names):
		print(file_index, file)
		if progress_callback:
			progress_callback(f"Extracting {file}", value=file_index, vmax=len(names))
		basename, ext = os.path.splitext(file)

		if ext[1:] in IGNORE_TYPES:
			print(f"Ignoring {file}, as it is not a standalone file!")
			continue

		if file in entry_dict:
			print("Found name", file)
			entry = entry_dict[file]

			if entry.ext == "banis":
				paths.extend(write_banis(archive, entry, out_dir_func))
			elif entry.ext == "bani":
				paths.extend(write_bani(archive, entry, out_dir_func))
			elif entry.ext == "manis":
				paths.extend(write_manis(archive, entry, out_dir_func))
			elif entry.ext == "fgm":
				paths.extend(write_fgm(archive, entry, out_dir_func))
			elif entry.ext == "ms2":
				paths.extend(write_ms2(archive, entry, out_dir_func))
			elif entry.ext == "materialcollection":
				paths.extend(write_materialcollection(archive, entry, out_dir_func))
			# elif entry.ext == "tex" and extract_tex == True:
			# 	write_dds(archive, entry, show_dds)
			elif entry.ext == "lua":
				paths.extend(write_lua(archive, entry, out_dir_func))
			# elif entry.ext == "assetpkg" and extract_misc == True:
			# 	write_assetpkg(archive, entry)
			elif entry.ext == "fdb":
				paths.extend(write_fdb(archive, entry, out_dir_func))
			# elif entry.ext == "xmlconfig" and extract_misc == True:
			# 	write_xmlconfig(archive, entry)
			# elif entry.ext == "userinterfaceicondata" and extract_misc == True:
			# 	write_userinterfaceicondata(archive, entry)
			elif entry.ext == "txt":
				paths.extend(write_txt(archive, entry, out_dir_func))
			elif entry.ext == "bnk":
				paths.extend(write_bnk(archive, entry, False, progress_callback, out_dir_func))
			# elif entry.ext == "prefab" and extract_misc == True:
			# 	write_prefab(archive, entry)
			# elif entry.ext == "voxelskirt" and extract_misc == True:
			# 	write_voxelskirt(archive, entry)
			# elif entry.ext == "gfx" and extract_misc == True:
			# 	write_gfx(archive, entry)
			elif entry.ext == "fct":
				paths.extend(write_fct(archive, entry, out_dir_func))
			# elif entry.ext == "scaleformlanguagedata" and extract_misc == True:
			# 	write_scaleform(archive, entry)
			else:
				print("\nSkipping", entry.name)
				skip_files.append(entry.name)
				continue

		else:
			print(f"ERROR: file {file} not found in archive")

		# except BaseException as error:
		# 	print(f"\nAn exception occurred while extracting {sized_str_entry.name}")
		# 	print(error)
		# 	traceback.print_exc()
		# 	error_files.append(sized_str_entry.name)

	return paths


def extract(archive, extract_fdb, extract_lua, extract_anim, extract_model, extract_tex, extract_shader, extract_text, extract_aux, extract_fct, extract_misc, show_dds, only_types=[], progress_callback=None):
	"""Extract the files, after all archives have been read"""
	# the actual export, per file type
	error_files = []
	skip_files = []
	# data types that we export starting from other file types but are not caught as deliberate cases
	exported_types = ["mani", "mdl2", "texturestream"]
	print("\nExtracting from archive", archive.archive_index)
	ss_max = len(archive.sized_str_entries)
	for ss_index, sized_str_entry in enumerate(archive.sized_str_entries):
		try:
			# for batch operations, only export those we need
			if only_types and sized_str_entry.ext not in only_types:
				continue
			# ignore types in the count that we export from inside other type exporters
			if sized_str_entry.ext in exported_types:
				continue
			elif sized_str_entry.ext == "banis" and extract_anim == True:
				write_banis(archive, sized_str_entry)
			elif sized_str_entry.ext == "bani" and extract_anim == True:
				write_bani(archive, sized_str_entry)
			elif sized_str_entry.ext == "manis" and extract_anim == True:
				write_manis(archive, sized_str_entry)
			elif sized_str_entry.ext == "fgm" and extract_shader == True:
				write_fgm(archive, sized_str_entry)
			elif sized_str_entry.ext == "ms2" and extract_model == True:
				write_ms2(archive, sized_str_entry)
			elif sized_str_entry.ext == "materialcollection" and extract_shader == True:
				write_materialcollection(archive, sized_str_entry)
			elif sized_str_entry.ext == "tex" and extract_tex == True:
				write_dds(archive, sized_str_entry, show_dds)
			elif sized_str_entry.ext == "lua" and extract_lua == True:
				write_lua(archive, sized_str_entry)
			elif sized_str_entry.ext == "assetpkg" and extract_misc == True:
				write_assetpkg(archive, sized_str_entry)
			elif sized_str_entry.ext == "fdb" and extract_fdb == True:
				write_fdb(archive, sized_str_entry)
			elif sized_str_entry.ext == "xmlconfig" and extract_misc == True:
				write_xmlconfig(archive, sized_str_entry)
			elif sized_str_entry.ext == "userinterfaceicondata" and extract_misc == True:
				write_userinterfaceicondata(archive, sized_str_entry)
			elif sized_str_entry.ext == "txt" and extract_text == True:
				write_txt(archive, sized_str_entry)
			elif sized_str_entry.ext == "bnk" and extract_aux == True:
				write_bnk(archive, sized_str_entry, show_dds, progress_callback)
			elif sized_str_entry.ext == "prefab" and extract_misc == True:
				write_prefab(archive, sized_str_entry)
			elif sized_str_entry.ext == "voxelskirt" and extract_misc == True:
				write_voxelskirt(archive, sized_str_entry)
			elif sized_str_entry.ext == "gfx" and extract_misc == True:
				write_gfx(archive, sized_str_entry)
			elif sized_str_entry.ext == "fct" and extract_fct == True:
				write_fct(archive, sized_str_entry)
			elif sized_str_entry.ext == "scaleformlanguagedata" and extract_misc == True:
				write_scaleform(archive, sized_str_entry)
			else:
				print("\nSkipping",sized_str_entry.name)
				skip_files.append(sized_str_entry.name)
				continue

			if progress_callback:
				progress_callback("Extracting " + sized_str_entry.name, value=ss_index, vmax=ss_max)
		except BaseException as error:
			print(f"\nAn exception occurred while extracting {sized_str_entry.name}")
			print(error)
			traceback.print_exc()
			error_files.append(sized_str_entry.name)
			
	return error_files, skip_files


def write_voxelskirt(archive, sized_str_entry):
	name = sized_str_entry.name
	print("\nWriting",name)
	buffers = sized_str_entry.data_entry.buffer_datas
	# write voxelskirt
	with open(archive.indir(name), 'wb') as outfile:
		# write the sized str and buffers
		print(sized_str_entry.pointers[0].data)
		outfile.write( sized_str_entry.pointers[0].data )
		for buff in buffers:
			outfile.write(buff)
            
def write_gfx(archive, sized_str_entry):
	name = sized_str_entry.name
	print("\nWriting",name)
	buffers = sized_str_entry.data_entry.buffer_datas
	# write voxelskirt
	with open(archive.indir(name), 'wb') as outfile:
		# write the sized str and buffers
		print(sized_str_entry.pointers[0].data)
		outfile.write( sized_str_entry.pointers[0].data )
		for buff in buffers:
			outfile.write(buff)


def write_scaleform(archive, sized_str_entry):
	name = sized_str_entry.name
	print("\nWriting",name)

	with open(archive.indir(name), 'wb') as outfile:
		# write each of the fragments
		# print(sized_str_entry.pointers[0].data)
		outfile.write( sized_str_entry.pointers[0].data )
		for frag in sized_str_entry.fragments:
			# print(frag.pointers[0].data)
			# print(frag.pointers[1].data)
			outfile.write(frag.pointers[0].data)
			outfile.write(frag.pointers[1].data)


def write_prefab(archive, sized_str_entry):
	name = sized_str_entry.name
	print("\nWriting",name)
	
	try:
		buffer_data = sized_str_entry.data_entry.buffer_datas[0]
		print("buffer size",len(buffer_data))
	except:
		print("Found no buffer data for",name)
		buffer_data = b""
	#if len(sized_str_entry.fragments) != 2:
	#	print("must have 2 fragments")
	#	return
	# write lua
	#with open(archive.indir(name), 'wb') as outfile:
	#	# write the buffer
	#	outfile.write(buffer_data)

	with open(archive.indir(name), 'wb') as outfile:
		# write each of the fragments
		#print(sized_str_entry.pointers[0].data)
		outfile.write( sized_str_entry.pointers[0].data )
		for frag in sized_str_entry.fragments:
			#print(frag.pointers[0].data)
			#print(frag.pointers[1].data)
			outfile.write( frag.pointers[0].data )
			outfile.write( frag.pointers[1].data )


def write_assetpkg(archive, sized_str_entry):
	name = sized_str_entry.name
	print("\nWriting",name)
	if len(sized_str_entry.fragments) == 1:
		print(len(sized_str_entry.fragments))
		f_0 = sized_str_entry.fragments[0]
	else:
		print("Found wrong amount of frags for",name)
		return
	with open(archive.indir(name), 'wb') as outfile:
		f_0.pointers[1].strip_zstring_padding()
		outfile.write(f_0.pointers[1].data[:-1])


def write_xmlconfig(archive, sized_str_entry):
	name = sized_str_entry.name
	print("\nWriting",name)

	if len(sized_str_entry.fragments) == 1:
		f_0 = sized_str_entry.fragments[0]
	else:
		print("Found wrong amount of frags for",name)
		return
	# write xml
	with open(archive.indir(name), 'wb') as outfile:
		# 8 x b00
		# sized_str_entry.pointers[0].data
		# 8 x b00
		# outfile.write( f_0.pointers[0].data )
		# the actual xml data
		# often with extra junk at the end (probably z str)
		f_0.pointers[1].strip_zstring_padding()
		# strip the b00 zstr terminator byte
		outfile.write( f_0.pointers[1].data[:-1] )


def write_userinterfaceicondata(archive, sized_str_entry):
	name = sized_str_entry.name
	print("\nWriting",name)
	
	try:
		buffer_data = sized_str_entry.data_entry.buffer_datas[0]
		print("buffer size",len(buffer_data))
	except:
		print("Found no buffer data for",name)
		buffer_data = b""
	if len(sized_str_entry.fragments) == 2:
		f_0, f_1 = sized_str_entry.fragments
	else:
		print("Found wrong amount of frags for",name)
		return
	# write xml
	xml_header = struct.pack("<12s5I", b"USERICONDATA", f_0.pointers[0].data_size, f_0.pointers[1].data_size, f_1.pointers[0].data_size, f_1.pointers[1].data_size, len(buffer_data))
	with open(archive.indir(name), 'wb') as outfile:
		# write custom FGM header
		outfile.write(xml_header)
		# write each of the fragments
		for frag in (f_0,f_1):
			outfile.write( frag.pointers[0].data )
			outfile.write( frag.pointers[1].data )
		# write the buffer
		outfile.write(buffer_data)
