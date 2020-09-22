import struct
import os
import io
import tempfile

from pyffi_ext.formats.dds import DdsFormat
# from pyffi_ext.formats.ms2 import Ms2Format
# from pyffi_ext.formats.bani import BaniFormat
from pyffi_ext.formats.manis import ManisFormat
from pyffi_ext.formats.ovl import OvlFormat
from pyffi_ext.formats.bnk import BnkFormat
# from pyffi_ext.formats.fgm import FgmFormat
# from pyffi_ext.formats.materialcollection import MaterialcollectionFormat

from generated.formats.bnk import BnkFile

from util import texconv, imarray

dds_types = {}
dds_enum = OvlFormat.DdsType
for k, v in zip(dds_enum._enumkeys, dds_enum._enumvalues):
	dds_types[v] = k


def write_sized_str(stream, s):
	"""Returns content of stream from pos"""
	size = struct.pack("<I", len(s))
	stream.write(size)
	stream.write(s.encode())


def read_sized_str(stream, pos, size):
	"""Returns content of stream from pos until pos+size"""
	stream.seek(pos)
	return stream.read(size)


def read_sized_str_at(stream, pos):
	"""Returns content of stream from pos"""
	stream.seek(pos)
	size = struct.unpack("<I", stream.read(4))[0]
	return stream.read(size)


def extract(archive, show_dds, only_types=[], progress_callback=None):
	"""Extract the files, after all archives have been read"""
	# the actual export, per file type
	error_files = []
	skip_files = []
	# data types that we export starting from other file types but are not caught as deliberate cases
	exported_types = ["mani", "mdl2", "texturestream"]
	print("\nExtracting from archive", archive.archive_index)
	ss_max = len(archive.sized_str_entries)
	for ss_index, sized_str_entry in enumerate(archive.sized_str_entries):
		# try:
		# for batch operations, only export those we need
		if only_types and sized_str_entry.ext not in only_types:
			continue
		# ignore types in the count that we export from inside other type exporters
		if sized_str_entry.ext in exported_types:
			continue
		elif sized_str_entry.ext == "banis":
			write_banis(archive, sized_str_entry)
		elif sized_str_entry.ext == "bani":
			write_bani(archive, sized_str_entry)
		elif sized_str_entry.ext == "manis":
			write_manis(archive, sized_str_entry)
		# elif sized_str_entry.ext == "mani":
		# 	write_mani(archive, sized_str_entry)
		elif sized_str_entry.ext == "fgm":
			write_fgm(archive, sized_str_entry)
		elif sized_str_entry.ext == "ms2":
			write_ms2(archive, sized_str_entry)
		elif sized_str_entry.ext == "materialcollection":
			write_materialcollection(archive, sized_str_entry)
		elif sized_str_entry.ext == "tex":
			write_dds(archive, sized_str_entry, show_dds )
		elif sized_str_entry.ext == "lua":
			write_lua(archive, sized_str_entry)
		elif sized_str_entry.ext == "assetpkg":
			write_assetpkg(archive, sized_str_entry)
		elif sized_str_entry.ext == "fdb":
			write_fdb(archive, sized_str_entry)
		elif sized_str_entry.ext == "xmlconfig":
			write_xmlconfig(archive, sized_str_entry)
		elif sized_str_entry.ext == "userinterfaceicondata":
			write_userinterfaceicondata(archive, sized_str_entry)
		elif sized_str_entry.ext == "txt":
			write_txt(archive, sized_str_entry)
		elif sized_str_entry.ext == "bnk":
			write_bnk(archive, sized_str_entry, show_dds)

		else:
			print("\nSkipping",sized_str_entry.name)
			skip_files.append(sized_str_entry.name)
			continue

		if progress_callback:
			progress_callback("Extracting " + sized_str_entry.name, value=ss_index, vmax=ss_max)
		# except:
		# 	print("\nAn exception occurred while extracting",sized_str_entry.name)
		# 	error_files.append(sized_str_entry.name)
			
	return error_files, skip_files


def write_bnk(archive, sized_str_entry, show_dds):
	bnk = os.path.splitext(sized_str_entry.name)[0]
	bnk_path = f"{archive.header.file_no_ext}_{bnk}_bnk_b.aux"
	if os.path.isfile(bnk_path):
		if "_media_" not in bnk_path:
			print("skipping events bnk", bnk_path)
			return
		print("exporting", bnk_path)

		data = BnkFile()
		data.load(bnk_path)

		# if we want to see the dds, write it to the output dir
		tmp_dir = texconv.make_tmp(archive.dir, show_dds)
		wem_files = data.extract_audio(tmp_dir, bnk)
		texconv.wem_handle(wem_files, archive.dir, show_dds)
	else:
		raise FileNotFoundError


def write_txt(archive, txt_sized_str_entry):
	# a bare sized str
	b = txt_sized_str_entry.pointers[0].data
	size = struct.unpack("<I", b[:4])[0]
	with open(archive.indir(txt_sized_str_entry.name), "wb") as f:
		f.write(b[4:4+size])


def get_tex_structs(archive, sized_str_entry):
	# we have exactly two fragments, pointing into these header types
	f_3_3, f_3_7 = sized_str_entry.fragments
	
	header_3_0 = f_3_7.pointers[0].read_as( OvlFormat.Header3Data0, archive )[0]
	headers_3_1 = f_3_3.pointers[1].read_as( OvlFormat.Header3Data1, archive, num = f_3_3.pointers[1].data_size//24 )
	header_7 = f_3_7.pointers[1].read_as( OvlFormat.Header7Data1, archive )[0]
	return header_3_0, headers_3_1, header_7


def get_compression_type(header_3_0):
	ovl_compression_ind = header_3_0.compression_type
	print("ovl_compression_ind",ovl_compression_ind)
	return dds_types[ovl_compression_ind]


def align_to(input, comp, alignment=64):
	"""Return input padded to the next closer multiple of alignment"""
	# get bpp from compression type
	if "BC1" in comp or "BC4" in comp:
		alignment *= 2
	# print("alignment",alignment)
	m = input % alignment
	if m:
		return input + alignment - m
	return input


def write_dds(archive, sized_str_entry, show_dds):
	basename = os.path.splitext(sized_str_entry.name)[0]
	name = basename+".dds"
	print("\nWriting",name)
	header_3_0, headers_3_1, header_7 = get_tex_structs(archive, sized_str_entry)
	
	# print(header_3_0)
	# print(headers_3_1)
	# print(header_7)
	
	sum_of_parts = sum(header_3_1.data_size for header_3_1 in headers_3_1)
	if not sum_of_parts == header_7.data_size:
		raise BufferError("Data sizes of all 3_1 structs ({}) and 7_1 fragments ({}) do not match up".format(sum_of_parts, header_7.data_size) )

	# get joined output buffer
	buffer_data = b"".join([b for b in sized_str_entry.data_entry.buffer_datas if b])
	if not len(buffer_data) == header_7.data_size:
		print("7_1 data size ({}) and actual data size of combined buffers ({}) do not match up (bug)".format(header_7.data_size, len(buffer_data)) )

		# raise BufferError("7_1 data size ({}) and actual data size of combined buffers ({}) do not match up (bug)".format(header_7.data_size, len(buffer_data)) )
	# print("combined buffer size",len(buffer_data))
	try:
		dds_compression_types = ( get_compression_type(header_3_0), )
	except KeyError:
		dds_compression_types = DdsFormat.DxgiFormat._enumkeys
		print("Unknown compression type, trying all compression types for your amusement")
		# dds_compression_types = list(v for v in DdsFormat.DxgiFormat._enumkeys if v not in dds_types.values())
	print("dds_compression_type", dds_compression_types)

	for dds_compression_type in dds_compression_types:
		version = DdsFormat.version_number("DX10")
		dds_data = DdsFormat.Data(version=version)
		# no stream, but data version even though that's broken
		header = DdsFormat.Header(None, dds_data)

		# header attribs
		header.width = align_to(header_7.width, dds_compression_type)
		# hack until we have proper support for array_size on the image editors
		header.height = header_7.height * header_7.array_size
		header.depth = header_7.depth
		header.linear_size = header_7.data_size
		header.mipmap_count = header_7.num_mips
		
		# header flags
		header.flags.height = 1
		header.flags.width = 1
		header.flags.mipmap_count = 1
		header.flags.linear_size = 1
		
		# pixel format flags
		header.pixel_format.flags.four_c_c = 1
		header.pixel_format.four_c_c = "DX10"
		
		# dx 10 stuff
		header.dx_10.dxgi_format = dds_compression_type
		# possibly the two 1s in header_3_0
		header.dx_10.resource_dimension = "D3D10_RESOURCE_DIMENSION_TEXTURE2D"
		# not properly supported by paint net and PS, only gimp
		# header.dx_10.array_size = header_7.array_size
		header.dx_10.array_size = 1
		
		# caps 1
		header.caps_1.texture = 0

		# start out with the visible file path
		dds_file_path = archive.indir(name)
		out_dir, in_name = os.path.split(dds_file_path)
		# if we want to see the dds, write it to the output dir
		tmp_dir = texconv.make_tmp( out_dir, show_dds )
		dds_file_path = os.path.join(tmp_dir, in_name)
		if len(dds_compression_types) > 1:
			dds_file_path += "_"+dds_compression_type+".dds"
		# write dds
		with open(dds_file_path, 'wb') as stream:
			header.write(stream, dds_data)
			stream.write(buffer_data)
		
		# convert the dds to PNG, PNG must be visible so put it in out_dir
		png_file_path = texconv.dds_to_png( dds_file_path, out_dir, header_7.height*header_7.array_size, show_dds)

		# postprocessing of the png
		imarray.wrapper(png_file_path, header_7)


def write_ms2(archive, ms2_sized_str_entry):
	name = ms2_sized_str_entry.name
	if not ms2_sized_str_entry.data_entry:
		print("No data entry for ",name)
		return
	buffers = ms2_sized_str_entry.data_entry.buffer_datas
	if len(buffers) == 3:
		bone_names, bone_matrices, verts = buffers
	elif len(buffers) == 2:
		bone_names, verts = buffers
		bone_matrices = b""
	else:
		raise BufferError(f"Wrong amount of buffers for {name}\nWanted 2 or 3 buffers, got {len(buffers)}")

	print("\nWriting",name)
	# print("\nbuffers",len(buffers))
	# for i, buffer in enumerate(buffers):
	# 	with open(archive.indir(name+str(i)+".ms2"), 'wb') as outfile:
	# 		outfile.write(buffer)
	if len(ms2_sized_str_entry.fragments) != 3:
		print("must have 3 fragments")
		return
	f_0, f_1, f_2 = ms2_sized_str_entry.fragments

	# sizedstr data has bone count
	ms2_general_info_data = ms2_sized_str_entry.pointers[0].data[:24]
	# ms2_general_info = ms2_sized_str_entry.pointers[0].read_as(Ms2Format.Ms2SizedStrData, archive)
	# print("Ms2SizedStrData", ms2_sized_str_entry.pointers[0].address, ms2_general_info)

	# f0 has information on vert & tri buffer sizes
	ms2_buffer_info_data = f_0.pointers[1].data
	# this fragment informs us about the model count of the next mdl2 that is read
	# so we can use it to collect the variable mdl2 fragments describing a model each
	next_model_info_data = f_1.pointers[1].data
	# next_model_info = f_1.pointers[1].read_as(Ms2Format.CoreModelInfo, archive)
	# print("next_model_info", f_1.pointers[1].address, next_model_info)

	# ms2_header = struct.pack("<4s5I", b"MS2 ", archive.header.version, archive.header.flag_2, len(bone_names), len(bone_matrices), len(ms2_sized_str_entry.children))
	# with open(archive.indir(name), 'wb') as outfile:
	# 	outfile.write(ms2_header)
	# 	for mdl2_entry in ms2_sized_str_entry.children:
	# 		outfile.write(mdl2_entry.name.encode()[:-5]+b"\x00")

	ms2_header = struct.pack("<4s4I", b"MS2 ", archive.header.version, archive.header.flag_2, len(bone_names), len(bone_matrices))
	with open(archive.indir(name), 'wb') as outfile:
		outfile.write(ms2_header)
		outfile.write(ms2_general_info_data)
		outfile.write(ms2_buffer_info_data)
		outfile.write(bone_names)
		outfile.write(bone_matrices)
		outfile.write(verts)

	# export each mdl2
	for mdl2_index, mdl2_entry in enumerate(ms2_sized_str_entry.children):
		with open(archive.indir(mdl2_entry.name), 'wb') as outfile:
			print("Writing",mdl2_entry.name,mdl2_index)
			# the fixed fragments
			green_mats_0, blue_lod, orange_mats_1, yellow_lod0, pink = mdl2_entry.fragments
			print("model_count",mdl2_entry.model_count)

			mdl2_header = struct.pack("<4s3I", b"MDL2", archive.header.version, archive.header.flag_2, mdl2_index )
			outfile.write(mdl2_header)
			# pack ms2 name as a sized string
			write_sized_str(outfile, ms2_sized_str_entry.name)

			# write the model info for this model, buffered from the previous model or ms2 (pink fragments)
			outfile.write(next_model_info_data)
			# print("PINK",pink.pointers[0].address,pink.pointers[0].data_size,pink.pointers[1].address, pink.pointers[1].data_size)
			if pink.pointers[0].data_size == 40:
				pass
				# 40 bytes of 'padding' (0,1 or 0,0,0,0)
				# core_model_data = pink.pointers[0].read_as(Ms2Format.Mdl2FourtyInfo, archive)
				# print(core_model_data)
			elif (archive.header.flag_2 == 24724 and pink.pointers[0].data_size == 144) \
			or   (archive.header.flag_2 == 8340  and pink.pointers[0].data_size == 160):
				# read model info for next model, but just the core part without the 40 bytes of 'padding' (0,1,0,0,0)
				next_model_info_data = pink.pointers[0].data[40:]
				# core_model_data = pink.pointers[0].read_as(Ms2Format.Mdl2ModelInfo, archive)
				# print(core_model_data)
			else:
				print("unexpected size for pink")

			# avoid writing bad fragments that should be empty
			if mdl2_entry.model_count:
				# print("fixed fragments")
				# need not write lod0
				for f in (green_mats_0, blue_lod, orange_mats_1):
					# print(f.pointers[0].address,f.pointers[0].data_size,f.pointers[1].address, f.pointers[1].data_size)
					other_data = f.pointers[1].data
					outfile.write(other_data)

			# print("modeldata frags")
			for f in mdl2_entry.model_data_frags:
				# each address_0 points to ms2's f_0 address_1 (size of vert & tri buffer)
				# print(f.pointers[0].address,f.pointers[0].data_size,f.pointers[1].address, f.pointers[1].data_size)
				# model_data = f.pointers[0].read_as(Ms2Format.ModelData, archive)
				# print(model_data)

				model_data = f.pointers[0].data
				outfile.write(model_data)
				
	
def write_banis(archive, sized_str_entry):
	name = sized_str_entry.name
	if not sized_str_entry.data_entry:
		print("No data entry for ",name)
		return
	buffers = sized_str_entry.data_entry.buffer_datas
	if len(buffers) != 1:
		print("Wrong amount of buffers for",name)
		return
	print("\nWriting",name)
	with open(archive.indir(name), 'wb') as outfile:
		outfile.write(buffers[0])


def write_bani(archive, sized_str_entry):
	name = sized_str_entry.name
	print("\nWriting",name)
	if len(sized_str_entry.fragments) != 1:
		print("must have 1 fragment")
		return
	for other_sized_str_entry in archive.sized_str_entries:
		if other_sized_str_entry.ext == "banis":
			banis_name = other_sized_str_entry.name
			break
	else:
		print("Found no banis file for bani animation!")
		return

	f = sized_str_entry.fragments[0]

	# write banis file
	with open(archive.indir(name), 'wb') as outfile:
		outfile.write(b"BANI")
		write_sized_str(outfile, banis_name)
		outfile.write( f.pointers[0].data )
		outfile.write( f.pointers[1].data )


def write_manis(archive, sized_str_entry):
	name = sized_str_entry.name
	print("\nWriting", name)
	if not sized_str_entry.data_entry:
		print("No data entry for ", name)
		return
	ss_data = sized_str_entry.pointers[0].data
	print(len(ss_data),ss_data)
	buffers = sized_str_entry.data_entry.buffer_datas
	print(len(buffers))
	# if len(buffers) != 3:
	# 	print("Wrong amount of buffers for", name)
	# 	return
	names = [c.name for c in sized_str_entry.children]
	manis_header = struct.pack("<4s3I", b"MANI", archive.header.version, archive.header.flag_2, len(names) )

	# sizedstr data + 3 buffers
	# sized str data gives general info
	# buffer 0 holds all mani infos - weirdly enough, its first 10 bytes come from the sized str data!
	# buffer 1 is list of hashes and zstrs for each bone name
	# buffer 2 has the actual keys
	with open(archive.indir(name), 'wb') as outfile:
		outfile.write(manis_header)
		for mani in names:
			outfile.write(mani.encode()+b"\x00")
		outfile.write(ss_data)
		for buff in sized_str_entry.data_entry.buffers:
			outfile.write(buff.data)
	#
	# for i, buff in enumerate(sized_str_entry.data_entry.buffers):
	# 	with open(archive.indir(name)+str(i), 'wb') as outfile:
	# 		outfile.write(buff.data)
	# if "partials" in name:
		# data = ManisFormat.Data()
		# with open(archive.indir(name), "rb") as stream:
		# 	data.read(stream)

def write_mani(archive, sized_str_entry):
	name = sized_str_entry.name
	print("\nWriting", name)
	# not sure what the logic for these ones is, right now the only valid info is set membership
	print(sized_str_entry.pointers[0].data_offset)
	print(sized_str_entry.pointers[0].data)
	if len(sized_str_entry.fragments) != 0:
		print("must have 0 fragments")
		return
	with open(archive.indir(name), 'wb') as outfile:
		outfile.write(b"Probably missing data, uses manis file: "+sized_str_entry.parent.name.encode())


def write_fgm(archive, sized_str_entry):
	name = sized_str_entry.name
	print("\nWriting",name)
	
	try:
		buffer_data = sized_str_entry.data_entry.buffer_datas[0]
		print("buffer size",len(buffer_data))
	except:
		print("Found no buffer data for", name)
		buffer_data = b""
	# for i, f in enumerate(sized_str_entry.fragments):
	# 	with open(archive.indir(name)+str(i), 'wb') as outfile:
	# 		outfile.write( f.pointers[1].data )
	# basic fgms
	if len(sized_str_entry.fragments) == 4:
		tex_info, attr_info, zeros, data_lib  = sized_str_entry.fragments
		len_tex_info = tex_info.pointers[1].data_size
		len_zeros = zeros.pointers[1].data_size
	# no zeros, otherwise same as basic
	elif len(sized_str_entry.fragments) == 3:
		tex_info, attr_info, data_lib  = sized_str_entry.fragments
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
	fgm_header = struct.pack("<4s7I", b"FGM ", archive.header.version, archive.header.flag_2, len(sized_str_entry.fragments), len_tex_info, attr_info.pointers[1].data_size, len_zeros, data_lib.pointers[1].data_size, )

	with open(archive.indir(name), 'wb') as outfile:
		# write custom FGM header
		outfile.write( fgm_header )
		outfile.write( sized_str_entry.pointers[0].data )
		# write each of the fragments
		for frag in sized_str_entry.fragments:
			outfile.write( frag.pointers[1].data )
		# write the buffer
		outfile.write(buffer_data)


def write_materialcollection(archive, sized_str_entry):
	name = sized_str_entry.name.replace("materialcollection", "matcol")
	print("\nWriting",name)
	
	matcol_header = struct.pack("<4s 2I B", b"MATC ", archive.header.version, archive.header.flag_2, sized_str_entry.has_texture_list_frag )

	with open(archive.indir(name), 'wb') as outfile:
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
						outfile.write( pointer.data )

	
def write_lua(archive, sized_str_entry):
	name = sized_str_entry.name
	print("\nWriting",name)
	
	try:
		buffer_data = sized_str_entry.data_entry.buffer_datas[0]
		print("buffer size",len(buffer_data))
	except:
		print("Found no buffer data for",name)
		buffer_data = b""
	if len(sized_str_entry.fragments) != 2:
		print("must have 2 fragments")
		return
	# write lua
	with open(archive.indir(name), 'wb') as outfile:
		# write the buffer
		outfile.write(buffer_data)

	with open(archive.indir(name)+"meta", 'wb') as outfile:
		# write each of the fragments
		print(sized_str_entry.pointers[0].data)
		outfile.write( sized_str_entry.pointers[0].data )
		for frag in sized_str_entry.fragments:
			print(frag.pointers[0].data)
			print(frag.pointers[1].data)
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


def write_fdb(archive, sized_str_entry):
	name = sized_str_entry.name
	print("\nWriting",name)
	
	try:
		buff = sized_str_entry.data_entry.buffer_datas[1]
	except:
		print("Found no buffer data for",name)
		return
	
	with open(archive.indir(name), 'wb') as outfile:
		# write the buffer, only buffer 1
		# buffer 0 is just the bare file name, boring
		# sizedstr data is just size of the buffer
		outfile.write(buff)


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
