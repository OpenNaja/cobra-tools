import struct
import os
import io
import tempfile
import shutil
import pyffi

from pyffi_ext.formats.dds import DdsFormat
from pyffi_ext.formats.ms2 import Ms2Format
# from pyffi_ext.formats.bani import BaniFormat
# from pyffi_ext.formats.ovl import OvlFormat
from pyffi_ext.formats.fgm import FgmFormat
from pyffi_ext.formats.materialcollection import MaterialcollectionFormat
# from pyffi_ext.formats.assetpkg import AssetpkgFormat

from modules import extract
from util import texconv, imarray


def split_path(fp):
	in_dir, name_ext = os.path.split(fp)
	name, ext = os.path.splitext(name_ext)
	ext = ext.lower()
	return name_ext, name, ext


def inject(ovl_data, file_paths, show_dds, is_2K):

	# write modified version to tmp dir
	tmp_dir = tempfile.mkdtemp("-cobra-png")

	dupecheck = []
	mdl2_tups = []
	for file_path in file_paths:
		name_ext, name, ext = split_path(file_path)
		print("Injecting", name_ext)
		# check for separated array tiles & flipped channels
		if ext == ".png":
			out_path = imarray.inject_wrapper(file_path, dupecheck, tmp_dir)
			# skip dupes
			if not out_path:
				print("Skipping injection of", file_path)
				continue
			# update the file path to the temp file with flipped channels or rebuilt array
			file_path = out_path
			name_ext, name, ext = split_path(file_path)
		# image files are stored as tex files in the archive
		if ext in (".dds", ".png"):
			name_ext = name+".tex"
		elif ext == ".matcol":
			name_ext = name+".materialcollection"
		# find the sizedstr entry that refers to this file
		sized_str_entry = ovl_data.get_sized_str_entry(name_ext)
		if is_2K:
		# Grab OVS sized string for Textures
			if sized_str_entry.ext == "tex":
				for lod_i in range(1):
					for archive in ovl_data.archives[1:]:
						for other_sizedstr in archive.sized_str_entries:
							if sized_str_entry.basename in other_sizedstr.name and "_lod"+str(lod_i) in other_sizedstr.name:
								ovs_sized_str_entry = other_sizedstr
		else:
			ovs_sized_str_entry = sized_str_entry
		# do the actual injection, varies per file type
		if ext == ".mdl2":
			mdl2_tups.append((file_path, sized_str_entry))
		if ext == ".fgm":
			load_fgm(ovl_data, file_path, sized_str_entry)
		elif ext == ".png":
			load_png(ovl_data, file_path, sized_str_entry, show_dds, is_2K, ovs_sized_str_entry)
		elif ext == ".dds":
			load_dds(ovl_data, file_path, sized_str_entry, is_2K, ovs_sized_str_entry)
		elif ext == ".txt":
			load_txt(ovl_data, file_path, sized_str_entry)
		elif ext == ".xmlconfig":
			load_xmlconfig(ovl_data, file_path, sized_str_entry)
		elif ext == ".fdb":
			load_fdb(ovl_data, file_path, sized_str_entry, name)
		elif ext == ".matcol":
			load_materialcollection(ovl_data, file_path, sized_str_entry)
		elif ext == ".lua":
			load_lua(ovl_data, file_path, sized_str_entry)
		elif ext == ".assetpkg":
			load_assetpkg(ovl_data, file_path, sized_str_entry)

	load_mdl2(ovl_data, mdl2_tups)
	shutil.rmtree(tmp_dir)


def to_bytes(inst, data):
	"""helper that returns the bytes representation of a pyffi struct"""
	# we must make sure that pyffi arrays are not treated as a list although they are an instance of 'list'
	if isinstance(inst, list) and not isinstance(inst, pyffi.object_models.xml.array.Array):
		return b"".join(to_bytes(c, data) for c in inst)
	if isinstance(inst, bytes):
		return inst
	# zero terminated strings show up as strings
	if isinstance(inst, str):
		return inst.encode() + b"\x00"
	with io.BytesIO() as frag_writer:
		inst.write(frag_writer, data=data)
		return frag_writer.getvalue()


def load_txt(ovl_data, txt_file_path, txt_sized_str_entry):
	txt_pointer = txt_sized_str_entry.pointers[0]
	# first make sure that the padding has been separated from the data
	size = struct.unpack("<I", txt_pointer.data[:4])[0]
	txt_pointer.split_data_padding(4+size)
	with open(txt_file_path, 'rb') as stream:
		raw_txt_bytes = stream.read()
		data = struct.pack("<I", len(raw_txt_bytes)) + raw_txt_bytes
	# make sure all are updated, and pad to 8 bytes, using old padding
	txt_pointer.update_data(data, update_copies=True, pad_to=8, include_old_pad=True)


def load_xmlconfig(ovl_data, xml_file_path, xml_sized_str_entry):
	with open(xml_file_path, 'rb') as stream:
		# add zero terminator
		data = stream.read() + b"\x00"
		# make sure all are updated, and pad to 8 bytes
		xml_sized_str_entry.fragments[0].pointers[1].update_data(data, update_copies=True, pad_to=8)


def load_png(ovl_data, png_file_path, tex_sized_str_entry, show_dds, is_2K, ovs_sized_str_entry):
	# convert the png into a dds, then inject that

	archive = ovl_data.archives[0]
	header_3_0, header_3_1, header_7 = extract.get_tex_structs(archive, tex_sized_str_entry)
	dds_compression_type = extract.get_compression_type(header_3_0)
	# texconv works without prefix
	compression = dds_compression_type.replace("DXGI_FORMAT_","")
	if is_2K:
		dds_file_path = texconv.png_to_dds( png_file_path, 2048*header_7.array_size, show_dds, codec = compression, mips = 12)
	else:   
		dds_file_path = texconv.png_to_dds( png_file_path, header_7.height*header_7.array_size, show_dds, codec = compression, mips = header_7.num_mips)
	
	# inject the dds generated by texconv
	load_dds(ovl_data, dds_file_path, tex_sized_str_entry, is_2K, ovs_sized_str_entry)
	# remove the temp file if desired
	texconv.clear_tmp(dds_file_path, show_dds)


def ensure_size_match(name, dds_header, tex_header, comp):
	"""Check that DDS files have the same basic size"""
	dds_h = dds_header.height
	dds_w = dds_header.width
	dds_d = dds_header.depth
	dds_a = dds_header.dx_10.array_size

	tex_h = tex_header.height
	tex_w = extract.align_to(tex_header.width, comp)
	tex_d = tex_header.depth
	tex_a = tex_header.array_size

	if dds_h * dds_w * dds_d * dds_a != tex_h * tex_w * tex_d * tex_a:
		raise AttributeError(f"Dimensions do not match for {name}!\n\n"
							 f"Dimensions: height x width x depth [array size]\n"
							 f"OVL Texture: {tex_h} x {tex_w} x {tex_d} [{tex_a}]\n"
							 f"Injected texture: {dds_h} x {dds_w} x {dds_d} [{dds_a}]\n\n"
							 f"Make the external texture's dimensions match the OVL texture and try again!" )


def pack_mips(stream, header, num_mips):
	"""From a standard DDS stream, pack the lower mip levels into one image and pad with empty bytes"""
	print("\nPacking mips")

	normal_levels = []
	packed_levels = []

	# get compression type
	dds_types = {}
	dds_enum = DdsFormat.DxgiFormat
	for k, v in zip(dds_enum._enumkeys, dds_enum._enumvalues):
		dds_types[v] = k
	comp = dds_types[header.dx_10.dxgi_format]

	# get bpp from compression type
	if "BC1" in comp or "BC4" in comp:
		pixels_per_byte = 2
		empty_block = bytes.fromhex("00 00 00 00 00 00 00 00")
	else:
		pixels_per_byte = 1
		empty_block = bytes.fromhex("00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00")

	h = header.height
	w = header.width
	mip_i = 0

	# print("\nstandard mips")
	# the last normal mip is 64x64
	# no, wrong, check herrera pbasecolor
	# start packing when one line of the mip == 128 bytes
	while w // pixels_per_byte > 32:
		# print(mip_i, h, w)
		num_pixels = h * w * header.dx_10.array_size
		num_bytes = num_pixels // pixels_per_byte
		address = stream.tell()
		# print(address, num_pixels, num_bytes)
		normal_levels.append( (h, w, stream.read(num_bytes)) )
		h //= 2
		w //= 2
		mip_i += 1

		# no packing at all, just grab desired mips and done
		if num_mips == mip_i:
			print(f"Info: MIP packing is not needed. Grabbing MIP level {mip_i} directly.")
			return b"".join( x[2] for x in normal_levels )

	# print("\npacked mips")
	# compression blocks are 4x4 pixels
	while h > 2 and w > 2:
		# print(mip_i, h, w)
		num_pixels = h * w * header.dx_10.array_size
		num_bytes = num_pixels // pixels_per_byte
		address = stream.tell()
		# print(address, num_pixels, num_bytes)
		packed_levels.append( (h, w, stream.read(num_bytes)) )
		h //= 2
		w //= 2
		mip_i += 1

	with io.BytesIO() as packed_writer:
		# 1 byte per pixel = 64 px
		# 0.5 bytes per pixel = 128 px
		total_width = 64 * pixels_per_byte
		# pack the last mips into one image
		for i, (height, width, level_bytes) in enumerate(packed_levels):

			# write horizontal lines

			# get count of h slices, 1 block is 4x4 px
			num_slices_y = height // 4
			num_pad_x = (total_width - width) // 4
			bytes_per_line = len(level_bytes) // num_slices_y

			# write the bytes for this line from the mip bytes
			for slice_i in range(num_slices_y):
				# get the bytes that represent the blocks of this line
				sl = level_bytes[ slice_i*bytes_per_line : (slice_i+1)*bytes_per_line ]
				packed_writer.write( sl )
				# fill the line with padding blocks
				for k in range(num_pad_x):
					packed_writer.write( empty_block )

		# weird stuff at the end
		for j in range(2):
			# empty line
			for k in range(64 // 4):
				packed_writer.write( empty_block )

			# write 4x4 lod
			packed_writer.write( level_bytes )

			# pad line
			for k in range(60 // 4):
				packed_writer.write( empty_block )
		# empty line
		for k in range(64 // 4):
			packed_writer.write( empty_block )

		# still gotta add one more lod here
		if pixels_per_byte == 2:
			# empty line
			for k in range(16):
				packed_writer.write( empty_block )
			# write 4x4 lod
			packed_writer.write( level_bytes )
			# padding
			for k in range(63):
				packed_writer.write( empty_block )

		packed_mip_bytes = packed_writer.getvalue()

	out_mips = [ x[2] for x in normal_levels ]
	out_mips.append(packed_mip_bytes)

	# get final merged output bytes
	return b"".join( out_mips )

def tex_to_2K(tex_sized_str_entry,ovs_sized_str_entry):
	#Experimental Function to update the data of normal and diffuse maps
	#to be 2048 in JWE
	new_header_3_1 = struct.pack("<12I", 0, 0, 4194304, 0, 256, 0, 4194304, 0, 1401856, 0, 2817, 0 )
	new_header_7 = struct.pack("<96I", 0,0,5596160,2048,2048,1,1,12,0,4194304,4194304,8192,4194304,4194304\
	,1048576,1048576,4096,1048576,5242880,262144,262144,2048,262144,5505024,65536,65536\
	,1024,65536,5570560,16384,16384,512,16384,5586944,4096,4096,256,4096,5591040,2048,2048,256,2048,5593088,1024,1024\
	,256,1024,5594112,512,512,256,512,5594624,512,512,256,256,5595136,512,512,256,256\
	,5595648,512,512,256,256,0,0,0,0,0,0,0,0,0,0,0,0,0,0,5596160,2048,2048,1,1,12,0,4194304,4194304,8192,4194304,4194304\
	,1048576,1048576)
	
	tex_sized_str_entry.fragments[0].pointers[1].update_data(new_header_3_1, update_copies=True)
	tex_sized_str_entry.fragments[1].pointers[1].update_data(new_header_7, update_copies=True)
	tex_sized_str_entry.data_entry.buffers[0].size = 4194304
	tex_sized_str_entry.data_entry.buffers[1].size = 1401856
	ovs_sized_str_entry.data_entry.size_2 = 4194304
	ovs_sized_str_entry.data_entry.buffers[0].size = 4194304
	tex_sized_str_entry.data_entry.size_2 = 1401856

def load_dds(ovl_data, dds_file_path, tex_sized_str_entry, is_2K, ovs_sized_str_entry):

	# read archive tex header to make sure we have the right mip count
	# even when users import DDS with mips when it should have none
	archive = ovl_data.archives[0]
	
	if is_2K:
		tex_to_2K(tex_sized_str_entry, ovs_sized_str_entry)
	
	header_3_0, header_3_1, header_7 = extract.get_tex_structs(archive, tex_sized_str_entry)

	# load dds
	with open(dds_file_path, 'rb') as stream:
		version = DdsFormat.version_number("DX10")
		dds_data = DdsFormat.Data(version=version)
		# no stream, but data version even though that's broken
		header = DdsFormat.Header(stream, dds_data)
		header.read(stream, dds_data)
		comp = extract.get_compression_type(header_3_0)
		ensure_size_match(os.path.basename(dds_file_path), header, header_7, comp)
		# print(header)
		out_bytes = pack_mips(stream, header, header_7.num_mips)
		# with open(dds_file_path+"dump.dds", 'wb') as stream:
		# 	header.write(stream, dds_data)
		# 	stream.write(out_bytes)

	sum_of_buffers = sum(buffer.size for buffer in tex_sized_str_entry.data_entry.buffers)
	if len(out_bytes) != sum_of_buffers:
		print(f"Packing of MipMaps failed. OVL expects {sum_of_buffers} bytes, but packing generated {len(out_bytes)} bytes." )

	with io.BytesIO(out_bytes) as reader:
		for buffer in tex_sized_str_entry.data_entry.buffers:
			dds_buff = reader.read(buffer.size)
			if len(dds_buff) < buffer.size:
				print(f"Last {buffer.size - len(dds_buff)} bytes of DDS buffer are not overwritten!")
				dds_buff = dds_buff + buffer.data[len(dds_buff):]
			buffer.update_data(dds_buff)


class Mdl2Holder:
	"""Used to handle injection of mdl2 files"""
	def __init__(self, archive):
		self.name = "NONE"
		self.lodinfo = b""
		self.mdl2_data = Ms2Format.Data()
		self.model_data_frags = []
		self.archive = archive
		self.source = "NONE"
		self.mdl2_entry = None

		# list or array of pyffi modeldata structs
		self.models = []
		# one per model
		self.verts_bytes = []
		self.tris_bytes = []

		self.lods = []

	def from_file(self, mdl2_file_path):
		"""Read a mdl2 + ms2 file"""
		print(f"Reading {mdl2_file_path} from file")
		self.name = os.path.basename(mdl2_file_path)
		self.source = "EXT"
		with open(mdl2_file_path, "rb") as mdl2_stream:
			self.mdl2_data.inspect(mdl2_stream)
			ms2_name = self.mdl2_data.mdl2_header.name.decode()
			self.models = self.mdl2_data.mdl2_header.models
			self.lods = self.mdl2_data.mdl2_header.lods

		# get ms2 buffers
		ms2_dir = os.path.dirname(mdl2_file_path)
		ms2_path = os.path.join(ms2_dir, ms2_name)
		with open(ms2_path, "rb") as ms2_stream:
			ms2_header = Ms2Format.Ms2InfoHeader()
			ms2_header.read(ms2_stream, data=self.mdl2_data)
			eoh = ms2_stream.tell() + ms2_header.bone_info_size

			self.read_verts_tris(ms2_stream, ms2_header.buffer_info, eoh)

	def read_verts_tris(self, ms2_stream, buffer_info, eoh=0, ):
		"""Reads vertices and triangles into list of bytes for all models of this file"""
		print("reading verts and tris")
		self.verts_bytes = []
		self.tris_bytes = []
		for model in self.models:
			# first, get the buffers for this model from the input
			ms2_stream.seek(eoh + model.vertex_offset)
			verts = ms2_stream.read(model.size_of_vertex * model.vertex_count)

			ms2_stream.seek(eoh + buffer_info.vertexdatasize + model.tri_offset)
			tris = ms2_stream.read(2 * model.tri_index_count)
			self.verts_bytes.append(verts)
			self.tris_bytes.append(tris)
		# print(len(self.tris_bytes))

	def from_entry(self, mdl2_entry):
		"""Reads the required data to represent this model from the archive"""
		print(f"Reading {mdl2_entry.name} from archive")
		self.name = mdl2_entry.name
		self.source = "OVL"
		self.mdl2_entry = mdl2_entry
		ms2_entry = mdl2_entry.parent

		# read the vertex data for this from the archive's ms2
		buffer_info_frag = ms2_entry.fragments[0]
		buffer_info = buffer_info_frag.pointers[1].read_as(Ms2Format.Ms2BufferInfo, self.archive)[0]
		print(buffer_info)

		verts_tris_buffer = ms2_entry.data_entry.buffer_datas[-1]

		lod_pointer = mdl2_entry.fragments[1].pointers[1]
		lod_count = len(lod_pointer.data) // 20
		# todo get count from CoreModelInfo
		self.lods = lod_pointer.read_as(Ms2Format.LodInfo, self.archive, num=lod_count)
		print(self.lods)
		self.models = []
		for f in mdl2_entry.model_data_frags:
			model = f.pointers[0].read_as(Ms2Format.ModelData, self.archive)[0]
			self.models.append(model)

		with io.BytesIO(verts_tris_buffer) as ms2_stream:
			self.read_verts_tris(ms2_stream, buffer_info)

	def update_entry(self):
		# overwrite mdl2 modeldata frags
		for frag, modeldata in zip(self.mdl2_entry.model_data_frags, self.models):
			frag_data = to_bytes(modeldata, self.mdl2_data)
			frag.pointers[0].update_data(frag_data, update_copies=True)

		self.lodinfo = to_bytes(self.lods, self.mdl2_data)
		# overwrite mdl2 lodinfo frag
		self.mdl2_entry.fragments[1].pointers[1].update_data(self.lodinfo, update_copies=True)

	def __repr__(self):
		return f"<Mdl2Holder: {self.name} [{self.source}], V{len(self.verts_bytes)}, T{len(self.tris_bytes)}, M{len(self.models)}, L{len(self.lods)}>"


class Ms2Holder:
	"""Used to handle injection of ms2 files"""
	def __init__(self, archive):
		self.name = "NONE"
		self.buffer_info = None
		self.buff_datas = []
		self.mdl2s = []
		self.archive = archive
		self.ms2_entry = None

	def __repr__(self):
		return f"<Ms2Holder: {self.name}, Models: {len(self.mdl2s)}>"

	def from_mdl2_file(self, mdl2_file_path):
		new_name = os.path.basename(mdl2_file_path)

		for i, mdl2 in enumerate(self.mdl2s):
			if mdl2.name == new_name:
				print(f"Match, slot {i}")
				mdl2.from_file(mdl2_file_path)
				break
		else:
			raise AttributeError(f"No match for {mdl2}")
		return mdl2

	def from_entry(self, ms2_entry):
		"""Read from the archive"""
		print(f"Reading {ms2_entry.name} from archive")
		self.name = ms2_entry.name
		self.mdl2s = []
		self.ms2_entry = ms2_entry

		buffer_info_frag = self.ms2_entry.fragments[0]
		# print(buffer_info_frag.pointers[1].data)
		if not buffer_info_frag.pointers[1].data:
			raise AttributeError("No buffer info, aborting merge")
		self.buffer_info = buffer_info_frag.pointers[1].read_as(Ms2Format.Ms2BufferInfo, self.archive)[0]
		# print(self.buffer_info)

		for mdl2_entry in self.ms2_entry.children:
			mdl2 = Mdl2Holder(self.archive)
			mdl2.from_entry(mdl2_entry)
			self.mdl2s.append(mdl2)
		print(self.mdl2s)

	def update_entry(self):
		print(f"Updating {self}")
		# adapted from old merger code

		# write each model's vert & tri block to a temporary buffer
		temp_vert_writer = io.BytesIO()
		temp_tris_writer = io.BytesIO()

		# set initial offset for the first modeldata
		vert_offset = 0
		tris_offset = 0

		# go over all input mdl2 files
		for mdl2 in self.mdl2s:
			print(f"Flushing {mdl2}")
			# read the mdl2
			for model, verts, tris in zip(mdl2.models, mdl2.verts_bytes, mdl2.tris_bytes):
				print(vert_offset)
				print(tris_offset)
				# write buffer to each output
				temp_vert_writer.write(verts)
				temp_tris_writer.write(tris)

				# update mdl2 offset values
				model.vertex_offset = vert_offset
				model.tri_offset = tris_offset

				# get offsets for the next model
				vert_offset = temp_vert_writer.tell()
				tris_offset = temp_tris_writer.tell()

		# get bytes from IO object
		vert_bytes = temp_vert_writer.getvalue()
		tris_bytes = temp_tris_writer.getvalue()

		buffers = self.ms2_entry.data_entry.buffer_datas[:-1]
		buffers.append(vert_bytes+tris_bytes)

		# modify buffer size
		self.buffer_info.vertexdatasize = len(vert_bytes)
		self.buffer_info.facesdatasize = len(tris_bytes)
		# overwrite ms2 buffer info frag
		buffer_info_frag = self.ms2_entry.fragments[0]
		buffer_info_frag.pointers[1].update_data(to_bytes(self.buffer_info, self.archive), update_copies=True)

		# update data
		self.ms2_entry.data_entry.update_data(buffers)

		# also flush the mdl2s
		for mdl2 in self.mdl2s:
			mdl2.update_entry()


def load_mdl2(ovl_data, mdl2_tups):

	# first resolve tuples to associated ms2 entry
	ms2_mdl2_dic = {}
	for mdl2_file_path, mdl2_entry in mdl2_tups:
		ms2_entry = mdl2_entry.parent
		if ms2_entry not in ms2_mdl2_dic:
			ms2_mdl2_dic[ms2_entry] = []
		ms2_mdl2_dic[ms2_entry].append(mdl2_file_path)

	# then read the ms2 and all associated new mdl2 files for it
	for ms2_entry, mdl2_file_paths in ms2_mdl2_dic.items():

		# first read the ms2 and all of its mdl2s from the archive
		ms2 = Ms2Holder(ovl_data)
		ms2.from_entry(ms2_entry)

		# load new input
		for mdl2_file_path in mdl2_file_paths:
			ms2.from_mdl2_file(mdl2_file_path)

		# the actual injection
		ms2.update_entry()


def load_fgm(ovl_data, fgm_file_path, fgm_sized_str_entry):

	fgm_data = FgmFormat.Data()
	# open file for binary reading
	with open(fgm_file_path, "rb") as stream:
		fgm_data.read(stream, fgm_data, file=fgm_file_path)

		sizedstr_bytes = to_bytes(fgm_data.fgm_header.fgm_info, fgm_data) + to_bytes(fgm_data.fgm_header.two_frags_pad, fgm_data)

		# todo - move texpad into fragment padding?
		textures_bytes = to_bytes(fgm_data.fgm_header.textures, fgm_data) + to_bytes(fgm_data.fgm_header.texpad, fgm_data)
		attributes_bytes = to_bytes(fgm_data.fgm_header.attributes, fgm_data)

		# read the other datas
		stream.seek(fgm_data.eoh)
		zeros_bytes = stream.read(fgm_data.fgm_header.zeros_size)
		data_bytes = stream.read(fgm_data.fgm_header.data_lib_size)
		buffer_bytes = stream.read()

	# the actual injection
	fgm_sized_str_entry.data_entry.update_data( (buffer_bytes,) )
	fgm_sized_str_entry.pointers[0].update_data(sizedstr_bytes, update_copies=True)

	if len(fgm_sized_str_entry.fragments) == 4:
		datas = (textures_bytes, attributes_bytes, zeros_bytes, data_bytes)
	# fgms without zeros
	elif len(fgm_sized_str_entry.fragments) == 3:
		datas = (textures_bytes, attributes_bytes, data_bytes)
	# fgms for variants
	elif len(fgm_sized_str_entry.fragments) == 2:
		datas = (attributes_bytes, data_bytes)
	else:
		raise AttributeError("Unexpected fgm frag count")

	# inject fragment datas
	for frag, data in zip(fgm_sized_str_entry.fragments, datas):
		frag.pointers[1].update_data(data, update_copies=True)


def update_matcol_pointers(pointers, new_names):
	# it looks like fragments are not reused here, and not even pointers are
	# but as they point to the same address the writer treats them as same
	# so the pointer map has to be updated for the involved header entries
	# also the copies list has to be adjusted

	# so this is a hack that only considers one entry for each union of pointers
	# map doffset to tuple of pointer and new data
	dic = {}
	for p, n in zip(pointers, new_names):
		dic[p.data_offset] = (p, n.encode() + b"\x00")
	sorted_keys = list(sorted(dic))
	# print(sorted_keys)
	print("Names in ovl order:", list(dic[k][1] for k in sorted_keys))
	sum = 0
	for k in sorted_keys:
		p, d = dic[k]
		sum += len(d)
		for pc in p.copies:
			pc.data = d
			pc.padding = b""
	pad_to = 64
	mod = sum % pad_to
	if mod:
		padding = b"\x00" * (pad_to-mod)
	else:
		padding = b""
	for pc in p.copies:
		pc.padding = padding


def load_materialcollection(ovl_data, matcol_file_path, sized_str_entry):
	matcol_data = MaterialcollectionFormat.Data()
	# open file for binary reading
	with open(matcol_file_path, "rb") as stream:
		matcol_data.read(stream)
		# print(matcol_data.header)

		if sized_str_entry.has_texture_list_frag:
			pointers = [tex_frag.pointers[1] for tex_frag in sized_str_entry.tex_frags]
			new_names = [n for t in matcol_data.header.texture_wrapper.textures for n in (t.fgm_name, t.texture_suffix, t.texture_type)]
		else:
			pointers = []
			new_names = []

		if sized_str_entry.is_variant:
			for (m0,), variant in zip(sized_str_entry.mat_frags, matcol_data.header.variant_wrapper.materials):
				# print(layer.name)
				pointers.append(m0.pointers[1])
				new_names.append(variant)
		elif sized_str_entry.is_layered:
			for (m0, info, attrib), layer in zip(sized_str_entry.mat_frags, matcol_data.header.layered_wrapper.layers):
				# print(layer.name)
				pointers.append(m0.pointers[1])
				new_names.append(layer.name)
				for frag, wrapper in zip(info.children, layer.infos):
					frag.pointers[0].update_data( to_bytes(wrapper.info, matcol_data), update_copies=True )
					frag.pointers[1].update_data( to_bytes(wrapper.name, matcol_data), update_copies=True )
					pointers.append(frag.pointers[1])
					new_names.append(wrapper.name)
				for frag, wrapper in zip(attrib.children, layer.attribs):
					frag.pointers[0].update_data( to_bytes(wrapper.attrib, matcol_data), update_copies=True )
					frag.pointers[1].update_data( to_bytes(wrapper.name, matcol_data), update_copies=True )
					pointers.append(frag.pointers[1])
					new_names.append(wrapper.name)

		update_matcol_pointers(pointers, new_names)


def load_fdb(ovl_data, fdb_file_path, fdb_sized_str_entry, fdb_name):
	# read fdb
	# inject fdb buffers
	# update sized string

	with open(fdb_file_path, "rb") as fdb_stream:
		# load the new buffers
		buffer1_bytes = fdb_stream.read()
		buffer0_bytes = fdb_name.encode()
		# update the buffers
		fdb_sized_str_entry.data_entry.update_data( (buffer0_bytes, buffer1_bytes) )
		# update the sizedstring entry
		data = struct.pack("<8I", len(buffer1_bytes), 0, 0, 0, 0, 0, 0, 0)
		fdb_sized_str_entry.pointers[0].update_data(data, update_copies=True)

def load_assetpkg(ovl_data, assetpkg_file_path, sized_str_entry):
	with open(assetpkg_file_path, "rb") as stream:
		b = stream.read()
		sized_str_entry.fragments[0].pointers[1].update_data( b + b"\x00", update_copies=True, pad_to=64)
        
def load_lua(ovl_data, lua_file_path, lua_sized_str_entry):
	# read lua
	# inject lua buffer
	# update sized string
	#IMPORTANT: all meta data of the lua except the sized str entries lua size value seems to just be meta data, can be zeroed
	with open(lua_file_path, "rb") as lua_stream:
		# load the new buffer
		buffer_bytes = lua_stream.read()
		# update the buffer
		lua_sized_str_entry.data_entry.update_data( (buffer_bytes,))
		# update the sizedstring entry
	with open(lua_file_path+"meta","rb") as luameta_stream:
		string_data = luameta_stream.read(16)
		print(string_data) #4 uints: size,unknown,hash,zero. only size is used by game.
		frag0_data0 = luameta_stream.read(8)
		print(frag0_data0)
		frag0_data1 = luameta_stream.read(lua_sized_str_entry.fragments[0].pointers[1].data_size)
		print(frag0_data1)
		frag1_data0 = luameta_stream.read(24)
		print(frag1_data0)
		frag1_data1 = luameta_stream.read(lua_sized_str_entry.fragments[1].pointers[1].data_size)
		print(frag1_data1)
		lua_sized_str_entry.pointers[0].update_data(string_data, update_copies=True)
		lua_sized_str_entry.fragments[0].pointers[1].update_data(frag0_data1, update_copies=True)
		lua_sized_str_entry.fragments[1].pointers[1].update_data(frag1_data1, update_copies=True)  
