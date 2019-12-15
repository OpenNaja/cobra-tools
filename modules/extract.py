import struct
import os
import io
import tempfile

from pyffi_ext.formats.dds import DdsFormat
from pyffi_ext.formats.ms2 import Ms2Format
from pyffi_ext.formats.bani import BaniFormat
from pyffi_ext.formats.ovl import OvlFormat
from pyffi_ext.formats.fgm import FgmFormat

from util import texconv

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
	
def extract(archive, show_dds):
	"""Extract the files, after all archives have been read"""
	# the actual export, per file type
	print("\nExtracting from archive",archive.archive_index)
	for sized_str_entry in archive.sized_str_entries:
		
		if sized_str_entry.ext == "banis":
			write_banis(archive, sized_str_entry, archive.stream )
		elif sized_str_entry.ext == "bani":
			write_bani(archive, sized_str_entry, archive.stream )
		elif sized_str_entry.ext == "fgm":
			write_fgm(archive, sized_str_entry, archive.stream )
		elif sized_str_entry.ext == "ms2":
			write_ms2(archive, sized_str_entry, archive.stream )
		elif sized_str_entry.ext == "tex":
			write_dds(archive, sized_str_entry, archive.stream, show_dds )
		elif sized_str_entry.ext == "lua":
			write_lua(archive, sized_str_entry, archive.stream )
		elif sized_str_entry.ext == "assetpkg":
			write_assetpkg(archive, sized_str_entry, archive.stream )
		elif sized_str_entry.ext == "fdb":
			write_fdb(archive, sized_str_entry, archive.stream )
		elif sized_str_entry.ext == "xmlconfig":
			write_xmlconfig(archive, sized_str_entry, archive.stream )
		elif sized_str_entry.ext == "userinterfaceicondata":
			write_userinterfaceicondata(archive, sized_str_entry, archive.stream )
		elif sized_str_entry.ext == "txt":
			write_txt(archive, sized_str_entry, archive.stream )
				
		else:
			print("\nSkipping",sized_str_entry.name)
	

def write_txt(archive, txt_sized_str_entry, stream):
	# a bare sized str
	b = txt_sized_str_entry.pointers[0].data
	size = struct.unpack("<I", b[:4])[0]
	with open(archive.indir(txt_sized_str_entry.name), "wb") as f:
		f.write(b[4:4+size])
	
def get_tex_structs(archive, sized_str_entry):
	# we have exactly two fragments, pointing into these header types
	f_3_7, f_3_3 = sized_str_entry.fragments
	
	header_3_0 = f_3_7.pointers[0].read_as( OvlFormat.Header3Data0, archive )[0]
	headers_3_1 = f_3_3.pointers[1].read_as( OvlFormat.Header3Data1, archive, num = f_3_3.pointers[1].data_size//24 )
	header_7 = f_3_7.pointers[1].read_as( OvlFormat.Header7Data1, archive )[0]
	return header_3_0, headers_3_1, header_7
	
def get_compression_type(archive, header_3_0):
	ovl_compression_ind = header_3_0.compression_type
	print("ovl_compression_ind",ovl_compression_ind)
	return dds_types[ovl_compression_ind]
	
def align_to(input, alignment=64):
	"""Return input padded to the next closer multiple of alignment"""
	m = input % alignment
	if m:
		return input + alignment - m
	return input

def write_dds(archive, sized_str_entry, stream, show_dds):
	basename = os.path.splitext(sized_str_entry.name)[0]
	name = basename+".dds"
	print("\nWriting",name)
	# todo 3_0 is actually a bad struct and extends over frag boundaries
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
		raise BufferError("7_1 data size ({}) and actual data size of combined buffers ({}) do not match up (bug)".format(header_7.data_size, len(buffer_data)) )
	# print("combined buffer size",len(buffer_data))
	try:
		dds_compression_types = ( get_compression_type(archive, header_3_0), )
	except:
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
		header.width = align_to(header_7.width)
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
		texconv.dds_to_png( dds_file_path, out_dir, show_dds)
	
def write_ms2(archive, ms2_sized_str_entry, stream):
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
		# with open(archive.indir(name+str(i)+".ms2"), 'wb') as outfile:
			# outfile.write(buffer)
	if len(ms2_sized_str_entry.fragments) != 3:
		print("must have 3 fragments")
		return
	f_2, f_1, f_0 = ms2_sized_str_entry.fragments
	
	ms2_buffer_info_data = f_0.pointers[1].data
	
	# sizedstr data has bone count
	ms2_general_info_data = ms2_sized_str_entry.pointers[0].data[:24]
	# next_model_info = archive.get_at_addr(Ms2Format.Ms2SizedStrData, stream, address)
	# print("Ms2SizedStrData", address, next_model_info)
	
	
	# this fragment informs us about the model count of the next mdl2 that is read
	# so we can use it to collect the variable mdl2 fragments describing a model each
	next_model_info_data = f_1.pointers[1].data
	# next_model_info = archive.get_at_addr(Ms2Format.CoreModelInfo, stream, f_1.pointers[1].address)
	# print("next_model_info", f_1.pointers[1].address, next_model_info)
	
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
			
			#write the model info for this model, buffered from the previous model or ms2 (pink fragments)
			outfile.write(next_model_info_data)
			# print("PINK",pink.pointers[0].address,pink.pointers[0].data_size,pink.pointers[1].address, pink.pointers[1].data_size)
			if pink.pointers[0].data_size == 40:
				pass
				# 40 bytes of 'padding' (0,1 or 0,0,0,0)
				# core_model_data = archive.get_at_addr(Ms2Format.Mdl2FourtyInfo, stream, pink.pointers[0].address)
				# print(core_model_data)
			elif (archive.header.flag_2 == 24724 and pink.pointers[0].data_size == 144) \
			or   (archive.header.flag_2 == 8340  and pink.pointers[0].data_size == 160):
				# read model info for next model, but just the core part without the 40 bytes of 'padding' (0,1,0,0,0)
				next_model_info_data = pink.pointers[0].data[40:]
				# core_model_data = archive.get_at_addr(Ms2Format.Mdl2ModelInfo, stream, pink.pointers[0].address)
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
				# model_data = archive.get_at_addr(Ms2Format.ModelData, stream, f.pointers[0].address)
				# print(model_data)
				
				model_data = f.pointers[0].data
				outfile.write(model_data)
				
	
def write_banis(archive, sized_str_entry, stream):
	name = sized_str_entry.name
	if not sized_str_entry.data_entry:
		print("No data entry for ",name)
		return
	buffers = sized_str_entry.data_entry.buffer_datas
	buffer_entry = sized_str_entry.data_entry.buffers[0]
	if len(buffers) != 1:
		print("Wrong amount of buffers for",name)
		return
	print("\nWriting",name)
	with open(archive.indir(name), 'wb') as outfile:
		outfile.write(buffers[0])
	
def write_bani(archive, sized_str_entry, stream):
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
	
	f_data0 = f.pointers[0].data
	f_data1 = f.pointers[1].data

	# write banis file
	with open(archive.indir(name), 'wb') as outfile:
		outfile.write(b"BANI")
		write_sized_str(outfile, banis_name)
		outfile.write(f_data0)
		outfile.write(f_data1)
	
def write_fgm(archive, sized_str_entry, stream):
	name = sized_str_entry.name
	print("\nWriting",name)
	
	try:
		buffer_data = sized_str_entry.data_entry.buffer_datas[0]
		print("buffer size",len(buffer_data))
	except:
		print("Found no buffer data for",name)
		buffer_data = b""
	# for i, f in enumerate(sized_str_entry.fragments):
	# 	with open(archive.indir(name)+str(i), 'wb') as outfile:
	# 		stream.seek(f.pointers[1].address)
	# 		outfile.write( stream.read(f.pointers[1].data_size) )
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
		tex_info = b""
		zeros = b""
		len_tex_info = 0
		len_zeros = 0
	else:
		raise AttributeError("Fgm length is wrong")
	# write fgm
	fgm_header = struct.pack("<4s5I", b"FGM", len(sized_str_entry.fragments), len_tex_info, attr_info.pointers[1].data_size, len_zeros, data_lib.pointers[1].data_size, )

	with open(archive.indir(name), 'wb') as outfile:
		# write custom FGM header
		outfile.write(fgm_header)
		# outfile.write(sized_str_entry.pointers[0].data)
		stream.seek(sized_str_entry.pointers[0].address)
		outfile.write( stream.read(sized_str_entry.pointers[0].data_size) )
		# write each of the fragments
		for frag in sized_str_entry.fragments:
			stream.seek(frag.pointers[1].address)
			outfile.write( stream.read(frag.pointers[1].data_size) )
		# write the buffer
		outfile.write(buffer_data)

	
def write_lua(archive, sized_str_entry, stream):
	name = sized_str_entry.name
	print("\nWriting",name)
	
	try:
		buffer_data = sized_str_entry.data_entry.buffer_datas[0]
		print("buffer size",len(buffer_data))
	except:
		print("Found no buffer data for",name)
		buffer_data = b""
	if len(sized_str_entry.fragments) == 2:
		f_1, f_0 = sized_str_entry.fragments
	# the supposed mapping entry
	# write lua
	lua_header = struct.pack("<3s5I", b"LUA", f_0.pointers[0].data_size, f_0.pointers[1].data_size, f_1.pointers[0].data_size, f_1.pointers[1].data_size, len(buffer_data))
	with open(archive.indir(name), 'wb') as outfile:
		# write custom FGM header
		outfile.write(lua_header)
		# write each of the archive.fragments
		for frag in (f_0, f_1,):
			stream.seek(frag.pointers[0].address)
			outfile.write( stream.read(frag.pointers[0].data_size) )
			stream.seek(frag.pointers[1].address)
			outfile.write( stream.read(frag.pointers[1].data_size) )
		# write the buffer
		outfile.write(buffer_data)
		
def write_assetpkg(archive, sized_str_entry, stream):
	name = sized_str_entry.name
	print("\nWriting",name)
	
	try:
		buffer_data = sized_str_entry.data_entry.buffer_datas[0]
		print("buffer size",len(buffer_data))
	except:
		print("Found no buffer data for",name)
		buffer_data = b""
	if len(sized_str_entry.fragments) == 1:
		print(len(sized_str_entry.fragments))
		f_0 = sized_str_entry.fragments[0]
	# the supposed mapping entry
	# write assetpkg
	asset_header = struct.pack("<8s3I", b"ASSETPKG", f_0.pointers[0].data_size, f_0.pointers[1].data_size, len(buffer_data))
	with open(archive.indir(name), 'wb') as outfile:
		# write custom FGM header
		outfile.write(asset_header)
		# write each of the archive.fragments
		#for frag in (f_0,):
		stream.seek(f_0.pointers[0].address)
		outfile.write( stream.read(f_0.pointers[0].data_size) )
		stream.seek(f_0.pointers[1].address)
		outfile.write( stream.read(f_0.pointers[1].data_size) )
		# write the buffer
		outfile.write(buffer_data)
	
def write_fdb(archive, sized_str_entry, stream):
	name = sized_str_entry.name
	print("\nWriting",name)
	
	try:
		buff_datas = sized_str_entry.data_entry.buffer_datas
		print("buffer size",len(buff_datas))
	except:
		print("Found no buffer data for",name)
		buffer_data = b""
	#if len(sized_str_entry.fragments) == 1:
		# f_0, f_1, f_2, f_3 = sized_str_entry.fragments
		#f_0 = sized_str_entry.fragments
	# the supposed mapping entry
	# write assetpkg
	asset_header = struct.pack("<3s2I", b"FDB", len(buff_datas[0]),len(buff_datas[1]))
	with open(archive.indir(name), 'wb') as outfile:
		# write custom FGM header
		outfile.write(asset_header)
		# write each of the archive.fragments
		#for frag in (f_0,):
			#stream.seek(frag.pointers[0].address)
			#outfile.write( stream.read(frag.pointers[0].data_size) )
			#stream.seek(frag.pointers[1].address)
			#outfile.write( stream.read(frag.pointers[1].data_size) )
		# write the buffer
		for buffer in buff_datas:
			outfile.write(buffer)
	
def write_xmlconfig(archive, sized_str_entry, stream):
	name = sized_str_entry.name
	print("\nWriting",name)
	
	try:
		buffer_data = sized_str_entry.data_entry.buffer_datas[0]
		print("buffer size",len(buffer_data))
	except:
		print("Found no buffer data for",name)
		buffer_data = b""
	if len(sized_str_entry.fragments) == 1:
		f_0 = sized_str_entry.fragments[0]
	# write xml
	xml_header = struct.pack("<3s2I", b"XML", f_0.pointers[0].data_size, f_0.pointers[1].data_size)
	with open(archive.indir(name), 'wb') as outfile:
		# write custom FGM header
		outfile.write(xml_header)
		# write each of the archive.fragments
		#for frag in (f_0,):
		stream.seek(f_0.pointers[0].address)
		outfile.write( stream.read(f_0.pointers[0].data_size) )
		stream.seek(f_0.pointers[1].address)
		outfile.write( stream.read(f_0.pointers[1].data_size) )
		# write the buffer
		#outfile.write(buffer_data)
	
def write_userinterfaceicondata(archive, sized_str_entry, stream):
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
	# the supposed mapping entry
	# write xml
	xml_header = struct.pack("<12s5I", b"USERICONDATA", f_0.pointers[0].data_size, f_0.pointers[1].data_size, f_1.pointers[0].data_size, f_1.pointers[1].data_size, len(buffer_data))
	with open(archive.indir(name), 'wb') as outfile:
		# write custom FGM header
		outfile.write(xml_header)
		# write each of the archive.fragments
		for frag in (f_0,f_1):
			stream.seek(frag.pointers[0].address)
			outfile.write( stream.read(frag.pointers[0].data_size) )
			stream.seek(frag.pointers[1].address)
			outfile.write( stream.read(frag.pointers[1].data_size) )
		# write the buffer
		outfile.write(buffer_data)
