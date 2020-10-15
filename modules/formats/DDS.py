import io
import os
import struct

from generated.formats.dds import DdsFile
from generated.formats.dds.enum.FourCC import FourCC
from generated.formats.dds.enum.D3D10ResourceDimension import D3D10ResourceDimension
from generated.formats.dds.enum.DxgiFormat import DxgiFormat
from generated.formats.ovl.compound.Header3Data0 import Header3Data0
from generated.formats.ovl.compound.Header3Data0Pc import Header3Data0Pc
from generated.formats.ovl.compound.Header3Data1Pc import Header3Data1Pc
from generated.formats.ovl.compound.Header3Data1 import Header3Data1
from generated.formats.ovl.compound.Header7Data1 import Header7Data1

from util import texconv, imarray


def get_tex_structs(sized_str_entry):
	# we have exactly two fragments, pointing into these header types
	f_3_3, f_3_7 = sized_str_entry.fragments

	header_3_0 = f_3_7.pointers[0].load_as(Header3Data0)[0]
	headers_3_1 = f_3_3.pointers[1].load_as(Header3Data1, num=f_3_3.pointers[1].data_size // 24)
	header_7 = f_3_7.pointers[1].load_as(Header7Data1)[0]
	return header_3_0, headers_3_1, header_7


def get_tex_structs_pc(sized_str_entry):
	frag = sized_str_entry.fragments[0]
	header_3_0 = frag.pointers[0].load_as(Header3Data0Pc)[0]
	# headers_3_1 = frag.pointers[1].load_as(Header3Data1Pc, num=header_3_0.one_2)
	# alternative?
	headers_3_1 = frag.pointers[1].load_as(Header3Data1Pc, num=frag.pointers[1].data_size//8)
	print(header_3_0)
	print(headers_3_1)
	# this corresponds to a stripped down header_7
	header_7 = headers_3_1[0]
	return header_3_0, headers_3_1, header_7


def align_to(width, comp, alignment=64):
	"""Return input padded to the next closer multiple of alignment"""
	# get bpp from compression type
	if "BC1" in comp or "BC4" in comp:
		alignment *= 2
	# print("alignment",alignment)
	m = width % alignment
	if m:
		return width + alignment - m
	return width


def create_dds_struct():
	dds_file = DdsFile()
	dds_file.header_string.data = b"DDS "
	dds_file.reserved_1 = [0 for _ in range(11)]

	# header flags
	dds_file.flags.height = 1
	dds_file.flags.width = 1
	dds_file.flags.mipmap_count = 1
	dds_file.flags.linear_size = 1

	# pixel format flags
	dds_file.pixel_format.flags.four_c_c = 1
	dds_file.pixel_format.four_c_c = FourCC.DX10

	# possibly the two 1s in header_3_0
	dds_file.dx_10.resource_dimension = D3D10ResourceDimension.D3D10_RESOURCE_DIMENSION_TEXTURE2D
	# not properly supported by paint net and PS, only gimp
	# header.dx_10.array_size = header_7.array_size
	dds_file.dx_10.array_size = 1

	# caps 1
	dds_file.caps_1.texture = 0
	return dds_file


def write_dds(archive, sized_str_entry, show_dds):
	basename = os.path.splitext(sized_str_entry.name)[0]
	name = basename + ".dds"
	print("\nWriting", name)
	# get joined output buffer
	buffer_data = b"".join([b for b in sized_str_entry.data_entry.buffer_datas if b])
	dds_file = create_dds_struct()
	dds_file.buffer = buffer_data
	if archive.is_pc():
		header_3_0, headers_3_1, header_7 = get_tex_structs_pc(sized_str_entry)
		dds_file.width = header_7.width
		# hack until we have proper support for array_size on the image editors
		dds_file.height = header_7.height * header_7.array_size
		dds_file.mipmap_count = header_7.num_mips
		dds_file.linear_size = len(buffer_data)
		dds_file.depth = header_3_0.one_0

	else:
		header_3_0, headers_3_1, header_7 = get_tex_structs(sized_str_entry)

		sum_of_parts = sum(header_3_1.data_size for header_3_1 in headers_3_1)
		if not sum_of_parts == header_7.data_size:
			raise BufferError(
				f"Data sizes of all 3_1 structs ({sum_of_parts}) and 7_1 fragments ({header_7.data_size}) do not match up")

		if not len(buffer_data) == header_7.data_size:
			print(
				f"7_1 data size ({header_7.data_size}) and actual data size of combined buffers ({len(buffer_data)}) do not match up (bug)")

		dds_file.width = header_7.width
		# hack until we have proper support for array_size on the image editors
		dds_file.height = header_7.height * header_7.array_size
		dds_file.depth = header_7.depth
		dds_file.linear_size = header_7.data_size
		dds_file.mipmap_count = header_7.num_mips

	try:
		dds_compression_types = (header_3_0.compression_type.name,)
	except KeyError:
		dds_compression_types = [x.name for x in DxgiFormat]
		print(
			f"Unknown compression type {header_3_0.compression_type}, trying all compression types for your amusement")
	print("dds_compression_type", dds_compression_types)
	# write out everything for each compression type
	if header_3_0.compression_type.name == "DXGI_FORMAT_ALL":
		dds_compression_types = [x.name for x in DxgiFormat]
	if header_3_0.compression_type.name == "DXGI_FORMAT_BC4_UNORM_B":
		dds_compression_types = ("DXGI_FORMAT_BC4_UNORM",)
	for dds_compression_type in dds_compression_types:

		# header attribs
		dds_file.width = align_to(dds_file.width, dds_compression_type)

		# dx 10 stuff
		dds_file.dx_10.dxgi_format = DxgiFormat[dds_compression_type]

		# start out with the visible file path
		dds_file_path = archive.indir(name)
		out_dir, in_name = os.path.split(dds_file_path)
		# if we want to see the dds, write it to the output dir
		tmp_dir = texconv.make_tmp(out_dir, show_dds)
		dds_file_path = os.path.join(tmp_dir, in_name)
		if len(dds_compression_types) > 1:
			dds_file_path += "_" + dds_compression_type + ".dds"
		# write dds
		dds_file.save(dds_file_path)

		# convert the dds to PNG, PNG must be visible so put it in out_dir
		png_file_path = texconv.dds_to_png(dds_file_path, out_dir, dds_file.height, show_dds)

		# postprocessing of the png
		imarray.wrapper(png_file_path, header_7)


def load_png(ovl_data, png_file_path, tex_sized_str_entry, show_dds, is_2K, ovs_sized_str_entry):
	# convert the png into a dds, then inject that

	archive = ovl_data.ovs_files[0]
	if archive.is_pc():
		header_3_0, headers_3_1, header_7 = get_tex_structs_pc(tex_sized_str_entry)
	else:
		header_3_0, header_3_1, header_7 = get_tex_structs(tex_sized_str_entry)
		if is_2K:
			header_7.height = 2048
			header_7.num_mips = 12
	# texconv works without prefix
	dds_compression_type = header_3_0.compression_type.name
	compression = dds_compression_type.replace("DXGI_FORMAT_", "")
	dds_file_path = texconv.png_to_dds(png_file_path, header_7.height * header_7.array_size, show_dds,
									   codec=compression, mips=header_7.num_mips)

	# inject the dds generated by texconv
	load_dds(ovl_data, dds_file_path, tex_sized_str_entry, is_2K, ovs_sized_str_entry)
	# remove the temp file if desired
	texconv.clear_tmp(dds_file_path, show_dds)


def ensure_size_match(name, dds_header, tex_h, tex_w, tex_d, tex_a, comp):
	"""Check that DDS files have the same basic size"""
	dds_h = dds_header.height
	dds_w = dds_header.width
	dds_d = dds_header.depth
	dds_a = dds_header.dx_10.array_size

	if dds_h * dds_w * dds_d * dds_a != tex_h * tex_w * tex_d * tex_a:
		raise AttributeError(f"Dimensions do not match for {name}!\n\n"
							 f"Dimensions: height x width x depth [array size]\n"
							 f"OVL Texture: {tex_h} x {tex_w} x {tex_d} [{tex_a}]\n"
							 f"Injected texture: {dds_h} x {dds_w} x {dds_d} [{dds_a}]\n\n"
							 f"Make the external texture's dimensions match the OVL texture and try again!")


def tex_to_2K(tex_sized_str_entry, ovs_sized_str_entry):
	# Experimental Function to update the data of normal and diffuse maps
	# to be 2048 in JWE
	new_header_3_1 = struct.pack("<12I", 0, 0, 4194304, 0, 256, 0, 4194304, 0, 1401856, 0, 2817, 0)
	new_header_7 = struct.pack("<96I", 0, 0, 5596160, 2048, 2048, 1, 1, 12, 0, 4194304, 4194304, 8192, 4194304, 4194304 \
							   , 1048576, 1048576, 4096, 1048576, 5242880, 262144, 262144, 2048, 262144, 5505024, 65536,
							   65536 \
							   , 1024, 65536, 5570560, 16384, 16384, 512, 16384, 5586944, 4096, 4096, 256, 4096,
							   5591040, 2048, 2048, 256, 2048, 5593088, 1024, 1024 \
							   , 256, 1024, 5594112, 512, 512, 256, 512, 5594624, 512, 512, 256, 256, 5595136, 512, 512,
							   256, 256 \
							   , 5595648, 512, 512, 256, 256, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5596160, 2048,
							   2048, 1, 1, 12, 0, 4194304, 4194304, 8192, 4194304, 4194304 \
							   , 1048576, 1048576)

	tex_sized_str_entry.fragments[0].pointers[1].update_data(new_header_3_1, update_copies=True)
	tex_sized_str_entry.fragments[1].pointers[1].update_data(new_header_7, update_copies=True)
	tex_sized_str_entry.data_entry.buffers[0].size = 4194304
	tex_sized_str_entry.data_entry.buffers[1].size = 1401856
	ovs_sized_str_entry.data_entry.size_2 = 4194304
	ovs_sized_str_entry.data_entry.buffers[0].size = 4194304
	tex_sized_str_entry.data_entry.size_2 = 1401856


def load_dds(ovl_data, dds_file_path, tex_sized_str_entry, is_2K, ovs_sized_str_entry):
	archive = ovl_data.ovs_files[0]

	if archive.is_pc():
		header_3_0, headers_3_1, header_7 = get_tex_structs_pc(tex_sized_str_entry)
		tex_h = header_7.height
		tex_w = header_7.width
		tex_d = header_3_0.one_0
		tex_a = header_7.array_size
	else:
		header_3_0, header_3_1, header_7 = get_tex_structs(tex_sized_str_entry)
		tex_h = header_7.height
		tex_w = header_7.width
		tex_d = header_7.depth
		tex_a = header_7.array_size
	comp = header_3_0.compression_type.name
	tex_w = align_to(tex_w, comp)

	# read archive tex header to make sure we have the right mip count
	# even when users import DDS with mips when it should have none
	if is_2K:
		tex_to_2K(tex_sized_str_entry, ovs_sized_str_entry)

	# load dds
	dds_file = DdsFile()
	dds_file.load(dds_file_path)
	ensure_size_match(os.path.basename(dds_file_path), dds_file, tex_h, tex_w, tex_d, tex_a, comp)
	if archive.is_pc():
		for buffer, tex_header_3 in zip(tex_sized_str_entry.data_entry.buffers, headers_3_1):
			dds_buff = dds_file.pack_mips_pc(tex_header_3.num_mips)
			if len(dds_buff) < buffer.size:
				print(f"Last {buffer.size - len(dds_buff)} bytes of DDS buffer are not overwritten!")
				dds_buff = dds_buff + buffer.data[len(dds_buff):]
			buffer.update_data(dds_buff)
	else:
		out_bytes = dds_file.pack_mips(header_7.num_mips)
		# with dds_file.writer(dds_file_path+"dump.dds") as stream:
		# 	dds_file.write(stream)
		# 	stream.write(out_bytes)

		sum_of_buffers = sum(buffer.size for buffer in tex_sized_str_entry.data_entry.buffers)
		if len(out_bytes) != sum_of_buffers:
			print(
				f"Packing of MipMaps failed. OVL expects {sum_of_buffers} bytes, but packing generated {len(out_bytes)} bytes.")

		with io.BytesIO(out_bytes) as reader:
			for buffer in tex_sized_str_entry.data_entry.buffers:
				dds_buff = reader.read(buffer.size)
				if len(dds_buff) < buffer.size:
					print(f"Last {buffer.size - len(dds_buff)} bytes of DDS buffer are not overwritten!")
					dds_buff = dds_buff + buffer.data[len(dds_buff):]
				buffer.update_data(dds_buff)
