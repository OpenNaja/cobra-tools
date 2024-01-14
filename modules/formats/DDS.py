import io
import logging
import os

from generated.formats.dds import DdsFile
from generated.formats.dds.enums.DxgiFormat import DxgiFormat
from generated.formats.ovl.versions import *
from generated.formats.tex.compounds.TexHeader import TexHeader
from generated.formats.tex.compounds.TexturestreamHeader import TexturestreamHeader
from modules.formats.BaseFormat import MemStructLoader

from ovl_util import texconv, imarray

logging.getLogger('PIL').setLevel(logging.WARNING)

pow2 = [2**i for i in range(16)]


class TexturestreamLoader(MemStructLoader):
	extension = ".texturestream"
	can_extract = False
	target_class = TexturestreamHeader

	def create(self, file_path):
		self.header = self.target_class(self.context)
		if is_jwe2(self.ovl):
			self.header.lod_index = int(self.basename[-1])
		self.write_memory_data()
		# data entry, assign buffer
		self.create_data_entry((b"", ))


class DdsLoader(MemStructLoader):
	target_class = TexHeader
	extension = ".tex"
	temp_extensions = (".dds", )

	def link_streams(self):
		"""Collect other loaders"""
		self._link_streams(f"{self.basename}_lod{lod_i}.texturestream" for lod_i in range(3))

	def increment_buffers(self, loader, buffer_i):
		"""Linearly increments buffer indices for games that need it"""
		# create increasing buffer indices for PZ (still needed 22-05-10), JWE
		if not is_jwe2(self.ovl):
			for buff in loader.data_entry.buffers:
				buff.index = buffer_i
				buffer_i += 1
		return buffer_i

	def create(self, file_path):
		in_dir, name_ext, basename, ext = self.get_names(file_path)
		# don't write header yet, might make changes to it
		self.header = self.target_class.from_xml_file(file_path, self.context)
		logging.debug(f"Creating image {name_ext}")
		# create the image before creating the streams
		buffer_bytes = self.get_image_bytes(file_path)
		# changes may have been made to tex header
		self.write_memory_data()
		# print(self.header)
		self.prepare_buffers_and_streams(basename, buffer_bytes, name_ext)

	def prepare_buffers_and_streams(self, basename, buffer_bytes, name_ext):
		# there's one empty buffer at the end!
		buffers = [b"" for _ in range(self.header.stream_count + 1)]
		# decide where to store the buffers
		static_lods = 2
		streamed_lods = len(buffers) - static_lods
		# logging.debug(f"buffers: {len(buffers)} streamed lods: {streamed_lods}")
		buffer_i = 0
		# generate ovs and lod names - highly idiosyncratic
		# checked for PZ, JWE2, PC
		if streamed_lods == 0:
			indices = ()
		elif streamed_lods == 1:
			# 1 lod: lod0 -> L1
			indices = ((0, 1),)
		elif streamed_lods == 2:
			# 2 lods: lod0 -> L0, lod1 -> L1
			indices = ((0, 0), (1, 1),)
		else:
			raise IndexError(f"Don't know how to handle more than 2 streams for {name_ext}")
		for lod_i, ovs_i in indices:
			ovs_name = f"Textures_L{ovs_i}"
			# create texturestream file - dummy_dir is ignored
			texstream_name = f"{basename}_lod{lod_i}.texturestream"
			texstream_loader = self.ovl.create_file(f"dummy_dir/{texstream_name}", texstream_name, ovs_name=ovs_name)
			self.streams.append(texstream_loader)
			buffer_i = self.increment_buffers(texstream_loader, buffer_i)
		self.create_data_entry(buffers[streamed_lods:])
		self.increment_buffers(self, buffer_i)
		# set data on the buffers
		for buffer_entry, b_slice in zip(self.get_sorted_streams(), buffer_bytes):
			buffer_entry.update_data(b_slice)
		# fix as we don't use the data.update_data api here
		for data_entry in self.get_sorted_datas():
			data_entry.size_1 = 0
			data_entry.size_2 = sum(buffer.size for buffer in data_entry.buffers)

	def get_image_bytes(self, tex_path):
		"""Returns a list of packed dds bytes, split for tex and texturestream buffers"""
		# logging.debug(f"Loading image {tex_path}")
		in_dir, name_ext, basename, ext = self.get_names(tex_path)
		with self.get_tmp_dir() as tmp_dir:
			size_info = self.get_tex_structs()
			# load all DDS files we need
			dds_files = []
			# ignore num_tiles from tex
			# try without array tile suffix
			dds_file = self.get_dds_file(basename, in_dir, tmp_dir)
			if dds_file:
				dds_files.append(dds_file)
			else:
				# try to find array tiles
				tile_i = 0
				while True:
					tile_name = f"{basename}_[{tile_i:02}]"
					dds_file = self.get_dds_file(tile_name, in_dir, tmp_dir)
					if dds_file:
						dds_files.append(dds_file)
					else:
						break
					tile_i += 1
			# start updating the tex
			assert dds_files, f"Found no dds files for {tex_path}"
			assert len(set(dds.mipmap_count for dds in dds_files)) == 1, f"DDS files for {tex_path} have varying mip map counts"
			# by now the dds is set in stone, and we can update the tex header with data from the dds
			dds = dds_files[0]
			# handle pre-DX10 compressions in dds files authored by legacy programs
			comp = dds.compression_format
			if comp.startswith("DXT"):
				comp = comp.replace("DXT", "BC") + "_UNORM"
			# update tex header
			self.header.compression_type = type(self.header.compression_type)[comp]
			# only update mips count if they are supposed to be present to keep UI images free from mips
			if size_info.num_mips != 1:
				size_info.num_mips = dds.mipmap_count
				# mip maps for tex sizes that are not power of 2 are uncommon
				# however they are found in ed_infoboard_custom.pbasecolourtexture
				if dds.width not in pow2 or dds.height not in pow2:
					logging.warning(f"Non-power-of-2 dimensions ({dds.width}x{dds.height}) with MIP maps for {tex_path}")
			size_info.width = dds.width
			size_info.height = dds.height
			size_info.depth = dds.depth
			size_info.num_tiles = len(dds_files)
			size_info.reset_field("mip_maps")
			# pack the different tiles into the tex buffer, pad the mips
			# create list of bytes for each buffer
			tex_buffers = self.header.buffer_infos.data
			if is_pc(self.ovl):
				# todo PC array textures
				return dds_files[0].pack_mips_pc(tex_buffers)
			else:
				# padding depends on io_size being updated
				size_info.io_size = size_info.get_size(size_info, size_info.context)
				self.header.size_info.data.reset_field("padding")
				logging.debug("Packing mip maps")
				# pack mips for all array tiles
				mips_per_tiles = [dds.get_packed_mips(size_info.mip_maps) for dds in dds_files]
				with io.BytesIO() as tex:
					# write the packed tex buffer: for each mip level, write all its tiles consecutively
					for mip_level, mip_info in zip(zip(*mips_per_tiles), size_info.mip_maps):
						mip_info.offset = tex.tell()
						for tile in mip_level:
							tex.write(tile)
						mip_info.size = len(tile)
						mip_info.size_array = tex.tell() - mip_info.offset
					packed = tex.getvalue()
				size_info.data_size = sum(m.size_array for m in size_info.mip_maps)
				# update tex buffer infos - all but the last correspond to one mip level
				for buffer_i, buffer in enumerate(tex_buffers):
					mip = size_info.mip_maps[buffer_i]
					buffer.first_mip = buffer_i
					# last tex buffer gets all remaining mips
					if buffer_i == len(tex_buffers) - 1:
						buffer.mip_count = len(size_info.mip_maps) - buffer.first_mip
						buffer.size = size_info.data_size - mip.offset
					else:
						buffer.mip_count = 1
						buffer.size = mip.size_array
					buffer.offset = mip.offset
				# slice packed bytes according to tex header buffer specifications
				return [packed[b.offset: b.offset + b.size] for b in tex_buffers]

	def get_dds_file(self, tile_name, in_dir, tmp_dir):
		"""Returns a valid dds file object, or None"""
		bare_path = os.path.join(in_dir, tile_name)
		dds_path = f"{bare_path}.dds"
		# prioritize dds files if they exist
		if os.path.isfile(dds_path):
			return self.load_dds(dds_path)
		else:
			try:
				# try to reassemble a flat PNG for this tile, and then convert it to DDS
				png_path = imarray.join_png(bare_path, tmp_dir, self.compression_name)
				return self.load_png(png_path, tmp_dir)
			except FileNotFoundError:
				# logging.exception("file missing")
				return None

	def get_names(self, file_path):
		assert file_path == os.path.normpath(file_path)
		in_dir, name_ext = os.path.split(file_path)
		basename, ext = os.path.splitext(name_ext.lower())
		return in_dir, name_ext, basename, ext

	def load_png(self, png_path, tmp_dir):
		logging.info(f"Loading {png_path}")
		# convert the png into a dds

		# as of 2023-12-02, texconv does not seem to store or recognize an sRGB flag in the pngs in creates
		# a PR that seems to touch that is open (407)
		# import io
		# import imageio.v3 as iio
		# from PIL import Image, ImageCms
		# current_image = Image.open(png_path)
		# profile = current_image.info.get("icc_profile")
		# print(profile)
		# current_image.close()
		# print(iio.immeta(png_path))

		size_info = self.get_tex_structs()
		compression = self.header.compression_type.name
		# texconv can't create mips for images with arbitrary size (often used for UI), so don't even create mips
		num_mips = 1 if size_info.num_mips == 1 else 0
		# compress and generate mips if needed
		dds_file_path = texconv.png_to_dds(png_path, tmp_dir, codec=compression, num_mips=num_mips)
		# inject the dds generated by texconv
		return self.load_dds(dds_file_path)

	def load_dds(self, dds_path):
		logging.info(f"Loading {dds_path}")
		# load dds
		dds_file = DdsFile()
		dds_file.load(dds_path)
		# print(dds_file)
		return dds_file

	def get_sorted_datas(self):
		# lod0 | lod1 | static
		return [loader.data_entry for loader in sorted(self.streams, key=lambda l: l.name)] + [self.data_entry, ]

	def get_sorted_streams(self):
		# PZ assigns the buffer index for the complete struct 0 | 1 | 2, 3
		# from JWE2, buffer index for streams is 0 | 0 | 0, 1
		# the last buffer is always 0 bytes
		# seen 1 buffer per stream
		# seen 2 buffer for static
		return [b for data_entry in self.get_sorted_datas() for b in data_entry.buffers]

	def get_tex_structs(self):
		if is_dla(self.ovl):
			return self.header
		if self.ovl.version < 19:
			# this corresponds to a stripped down size_info
			return self.header.buffer_infos.data[0]
		else:
			return self.header.size_info.data.data

	def get_tile_names(self, tiles, basename):
		tile_names = []
		for tile_i in tiles:
			# when there are tiles, add a tile infix
			infix = f"_[{tile_i:02}]" if len(tiles) > 1 else ""
			tile_name = f"{basename}{infix}"
			tile_names.append(tile_name)
		return tile_names

	def extract(self, out_dir):
		out_files = list(super().extract(out_dir))
		tex_name = self.name
		basename = os.path.splitext(tex_name)[0]
		logging.info(f"Writing {tex_name}")

		# get joined output buffer
		buffer_data = b"".join([buffer.data for buffer in self.get_sorted_streams()])
		size_info = self.get_tex_structs()

		dds_file = DdsFile()
		dds_file.width = size_info.width
		dds_file.height = size_info.height
		dds_file.mipmap_count = size_info.num_mips
		if hasattr(size_info, "depth") and size_info.depth:
			dds_file.depth = size_info.depth

		compression_type = DxgiFormat[self.compression_name]

		# set compression
		dds_file.dx_10.dxgi_format = compression_type

		tiles = self.get_tiles(size_info)
		# set num_tiles to unpack the mips
		if hasattr(size_info, "num_tiles"):
			dds_file.dx_10.num_tiles = size_info.num_tiles
		else:
			# DLA has no num_tiles
			dds_file.dx_10.num_tiles = 1
		if is_dla(self.ovl) or is_ztuac(self.ovl) or is_pc(self.ovl):
			# not sure how / if texture arrays are packed for PC - this works for flat textures
			tile_datas = (buffer_data, )
		else:
			tile_datas = dds_file.unpack_mips(buffer_data)
		# set to no tiles for dds export
		dds_file.dx_10.num_tiles = 1
		# export all tiles as separate dds files
		for tile_i, tile_name, tile_data in zip(tiles, self.get_tile_names(tiles, basename), tile_datas):
			dds_file.buffer = tile_data
			dds_file.linear_size = len(buffer_data)
			dds_path = out_dir(f"{tile_name}.dds")
			# write dds
			dds_file.save(dds_path)
			out_files.append(dds_path)
			try:
				# convert the dds to png
				png_path = texconv.dds_to_png(dds_path, self.compression_name)
				# postprocessing of the png
				if os.path.isfile(png_path):
					out_files.extend(imarray.split_png(png_path, self.ovl, self.compression_name))
			except:
				logging.exception(f"Postprocessing of {dds_path} failed!")
		return out_files

	@property
	def compression_name(self):
		name = self.header.compression_type.name
		# account for aliases
		if name.endswith(("_B", "_C")):
			name = name[:-2]
		return name

	def get_tiles(self, size_info):
		if hasattr(size_info, "num_tiles") and size_info.num_tiles:
			tiles = list(range(size_info.num_tiles))
		else:
			tiles = (0,)
		return tiles
