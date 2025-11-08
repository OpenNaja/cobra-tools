import io
import logging
import os

from generated.formats.dds import DdsFile
from generated.formats.dds.enums.DxgiFormat import DxgiFormat
from generated.formats.ovl.versions import *
from generated.formats.tex.structs.Pc2TexBuffer import Pc2TexBuffer
from generated.formats.tex.structs.TexHeader import TexHeader
from generated.formats.tex.structs.TexelHeader import TexelHeader
from generated.formats.tex.structs.TexturestreamHeader import TexturestreamHeader
from generated.formats.tex.enums.DdsType import DdsType
from modules.formats.BaseFormat import MemStructLoader, BaseFile
from modules.formats.shared import fnv64, encode_int64_base32
from modules.helpers import as_bytes

from ovl_util import texconv, imarray

logging.getLogger('PIL').setLevel(logging.WARNING)

pow2 = [2 ** i for i in range(16)]


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
		self.create_data_entry((b"",))


class DdsLoader(MemStructLoader):
	target_class = TexHeader
	extension = ".tex"
	temp_extensions = (".dds",)

	@property
	def show_temp_files(self):
		return self.ovl.cfg.get("dds_extract", False)

	def link_streams(self):
		"""Collect other loaders"""
		self._link_streams(f"{self.basename}_lod{lod_i}.texturestream" for lod_i in range(3))

	def __eq__(self, other):
		super().__eq__(other)
		if self.context.is_pc_2:
			self.check([m.offset for m in self.texbuffer.mip_maps], [m.offset for m in other.texbuffer.mip_maps],
					   "Mip map offsets")
			self.check(self.raw_bytes, other.raw_bytes, "Texture data")
		return self.same

	def get_dummy_dds_file(self):
		"""Used for alignment in shuffling mip blocks around"""
		dds_file = DdsFile()
		dds_file.dx_10.dxgi_format = DxgiFormat[self.compression_name]
		dds_file.get_pixel_fmt()
		return dds_file

	def collect(self):
		super(DdsLoader, self).collect()

		if self.context.is_pc_2:
			# texbuffer data is in the second buffer (index 2)
			buffer_data = b"".join([buffer.data for buffer in self.get_sorted_streams()])
			with io.BytesIO(buffer_data) as f:
				self.texbuffer = Pc2TexBuffer.from_stream(f, self.context, self.header)
				texel_loader = self.get_texel()
				# packed, weaved
				self.raw_bytes = texel_loader.get_aux_data("", self.texbuffer.mip_maps[0].offset, self.texbuffer.buffer_size)
			# t = self.texbuffer
			# print(t.num_mips, t.num_mips_low, t.num_mips_high, dds_file.block_byte_size, t.width, t.height, self.name)
			# print(t.flag, len(set((t.num_mips, t.num_mips_low, t.num_mips_high))))
			# print(t.flag, dds_file.block_byte_size)
			# print(t.flag, self.name)
			# print(t.can_weave, self.name)
			# print(t.can_weave, t.num_mips, self.name)
			# print(t.flag, t.can_weave, t.weave_width, t.weave_height, t.width, t.height, dds_file.block_byte_size, self.name)
			# print(self.header.texel, t.mip_maps[0].offset, self.file_hash, self.name)

	def unweave(self, dds_file):
		logging.info(f"Unweaving {self.name}")
		dds_file.get_pixel_fmt()
		unweaved_bytes = bytearray(self.raw_bytes)
		for unpacked_offset, shuffled_offset, size in self.weave_generator(dds_file):
			unweaved_bytes[unpacked_offset: unpacked_offset + size] = self.raw_bytes[shuffled_offset: shuffled_offset + size]
		return unweaved_bytes

	def weave(self, dds_file, unweaved_bytes):
		logging.info(f"Weaving {self.name}")
		dds_file.get_pixel_fmt()
		self.raw_bytes = bytearray(unweaved_bytes)
		for unpacked_offset, shuffled_offset, size in self.weave_generator(dds_file):
			self.raw_bytes[shuffled_offset: shuffled_offset + size] = unweaved_bytes[unpacked_offset: unpacked_offset + size]

	def create(self, file_path):
		in_dir, name_ext, basename, ext = self.get_names(file_path)
		# don't write header yet, might make changes to it
		self.header = self.target_class.from_xml_file(file_path, self.context)
		# override ovs membership
		if self.context.is_pc_2:
			self.set_ovs(self.header.ovs)
		logging.debug(f"Creating image {name_ext}")
		# create the image before creating the streams
		buffer_bytes = self.get_image_bytes(file_path)
		# changes may have been made to tex header
		self.write_memory_data()
		# print(self.header)
		self.prepare_buffers_and_streams(basename, buffer_bytes, name_ext)

	def flush_to_aux(self):
		"""Writes PC2 and JWE3 mips to texel's aux and updates their offsets"""
		if self.context.is_pc_2:
			texel_loader = self.get_texel()
			offset, self.texbuffer.buffer_size = texel_loader.write_aux_data("", self.raw_bytes)
			# do inverse of swizzling transform from get_mip_bytes
			for mip_i, mip_info in enumerate(self.texbuffer.mip_maps):
				# only update offset on valid mips
				if mip_i < self.texbuffer.num_mips:
					mip_info.offset = offset
					offset += mip_info.size
			for lod, mip_offset in zip(self.texbuffer.main,
									   (self.texbuffer.num_mips_low, self.texbuffer.num_mips_high)):
				first_index = self.texbuffer.num_mips - mip_offset
				mip0 = self.texbuffer.mip_maps[first_index]
				lod.offset = mip0.offset
			# update buffer data of tex
			texbuffer_bytes = [b"", as_bytes(self.texbuffer)]
			# both root and data are in the same ovs
			self.create_data_entry(texbuffer_bytes, self.ovs.arg.name)
			self.increment_buffers(1)
			for data_entry in self.get_sorted_datas():
				data_entry.size_1 = data_entry.size_2 = 0

	def prepare_buffers_and_streams(self, basename, buffer_bytes, name_ext):
		if not self.context.is_pc_2:
			# there's one empty buffer at the end!
			buffers = [b"" for _ in range(self.header.stream_count + 1)]
			# decide where to store the buffers
			static_lods = 2
			streamed_lods = len(buffers) - static_lods
			# logging.debug(f"buffers: {len(buffers)} streamed lods: {streamed_lods}")
			buffer_i = 0
			# generate ovs and lod names - highly idiosyncratic
			# checked for PZ, JWE2, PC1
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
				texstream_loader = self.ovl.create_file(f"dummy_dir/{texstream_name}", texstream_name,
														ovs_name=ovs_name)
				self.streams.append(texstream_loader)
				buffer_i = texstream_loader.increment_buffers(buffer_i)
			self.create_data_entry(buffers[streamed_lods:])
			self.increment_buffers(buffer_i)
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
			dds_paths = []
			png_paths = []
			# ignore num_tiles from tex
			# try to get an image without array tile suffix
			if not self.get_image_files(basename, in_dir, tmp_dir, dds_paths, png_paths):
				# try to find array tiles
				tile_i = 0
				while True:
					tile_name = f"{basename}_[{tile_i:02}]"
					if not self.get_image_files(tile_name, in_dir, tmp_dir, dds_paths, png_paths):
						break
					tile_i += 1
			if png_paths:
				for png_path in self.ovl.reporter.iter_progress(png_paths, "Converting", cond=len(png_paths) > 1):
					dds_path = self.convert_png(png_path, tmp_dir)
					dds_paths.append(dds_path)
			dds_files = [self.load_dds(dds_path) for dds_path in dds_paths]
			# start updating the tex
			assert dds_files, f"Found no dds files for {tex_path}"
			assert len(set(
				dds.mipmap_count for dds in dds_files)) == 1, f"DDS files for {tex_path} have varying mip map counts"
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
					logging.warning(
						f"Non-power-of-2 dimensions ({dds.width}x{dds.height}) with MIP maps for {tex_path}")
			size_info.width = dds.width
			size_info.height = dds.height
			size_info.depth = dds.depth
			size_info.num_tiles = len(dds_files)
			size_info.reset_field("mip_maps")
			# pack the different tiles into the tex buffer, pad the mips
			# create list of bytes for each buffer
			texbuffers = self.header.buffer_infos.data
			if is_pc(self.ovl):
				# todo create self.header.buffer_infos.data for PC
				#  however note that size_info = self.get_tex_structs() is the first entry of the array
				#  maybe even pick stream count according to dimensions
				# for 2048, 3 buffers
				# for 1024-256, 2 buffers
				# for 128, 1 buffer
				# last buffer is 128 regardless of full size eg:
				# 		<texbufferpc width="2048" height="2048" num_tiles="1" num_mips="12" />
				# 		<texbufferpc width="1024" height="1024" num_tiles="1" num_mips="11" />
				# 		<texbufferpc width="128" height="128" num_tiles="1" num_mips="8" />
				# todo how to pack PC array textures
				return dds_files[0].pack_mips_pc(texbuffers)
			elif self.context.is_pc_2:
				dds_file = dds_files[0]
				dds_file.get_pixel_fmt()
				self.texbuffer = Pc2TexBuffer(self.context, self.header)
				self.texbuffer.compression_type = size_info.compression_type
				self.texbuffer.width = size_info.width
				self.texbuffer.height = size_info.height
				self.texbuffer.depth = size_info.depth
				self.texbuffer.num_tiles = size_info.num_tiles
				# mip maps
				self.texbuffer.num_mips = size_info.num_mips
				if self.texbuffer.num_mips > 1:
					# single channel
					if self.header.compression_type in (DdsType.BC4_UNORM, DdsType.BC4_SNORM):
						self.texbuffer.flag = 32
					# RGB
					else:
						self.texbuffer.flag = 96
				# these appear not to be easily predictable, so retrieve those manually added to tex
				self.texbuffer.num_mips_high = int(self.header.num_mips_high)
				self.texbuffer.num_mips_low = int(self.header.num_mips_low)
				# # surprisingly, incorrect values for num_mips_low and num_mips_high crash
				# # to keep it safe, only update them for creating rather than saving
				# self.texbuffer.num_mips_high = self.texbuffer.num_mips_low = self.texbuffer.num_mips
				# if self.texbuffer.num_mips > 7:
				# 	delta_high = 3
				# 	delta_low = 5
				# 	if dds_file.block_byte_size == 8:
				# 		delta_high -= 1
				# 		delta_low -= 1
				# 		if self.texbuffer.width == 512:
				# 			# JWE2: 7 = 64; 9 = 256
				# 			delta_high -= 1
				# 			delta_low -= 1
				# 		if self.texbuffer.width == 2048:
				# 			# JWE2: 7 = 64; 9 = 256
				# 			delta_high += 1
				# 			delta_low += 1
				# 	self.texbuffer.num_mips_high = self.texbuffer.num_mips - delta_high
				# 	self.texbuffer.num_mips_low = self.texbuffer.num_mips - delta_low
				# 	if self.texbuffer.width == 256:
				# 		self.texbuffer.num_mips_low = self.texbuffer.num_mips

				# weaving
				# 512 is used for 8 bytes, 256 for 16 bytes
				if dds_file.block_byte_size == 8:
					self.texbuffer.weave_width = 512
				if self.texbuffer.width < 256 or self.texbuffer.height < 256:
					self.texbuffer.weave_width = 0
					self.texbuffer.weave_height = 0
				self.texbuffer.can_weave = 1 if self.texbuffer.weave_width else 0
				# pack mips for all array tiles
				mips_per_tiles = [dds.get_packed_mips(self.texbuffer.mip_maps) for dds in dds_files]
				packed_mips = []
				# write the packed tex buffer: for each mip level, write all its tiles consecutively
				for mip_level in zip(*mips_per_tiles):
					mip_bytes = b"".join(mip_level)
					packed_mips.append(mip_bytes)
				# update mip data
				height = self.texbuffer.height
				width = self.texbuffer.width
				for mip_i, (mip_bytes, mip_info) in enumerate(zip(mips_per_tiles[0], self.texbuffer.mip_maps)):
					# only set size + offset on valid mips
					if mip_i < self.texbuffer.num_mips:
						# UI mip 0 ignores the settings from the header
						if self.texbuffer.num_mips > 1 and self.texbuffer.weave_width and self.texbuffer.weave_height:
							mip_info.num_weaves_x = width // self.texbuffer.weave_width
							mip_info.num_weaves_y = height // self.texbuffer.weave_height
							if mip_info.num_weaves_x and mip_info.num_weaves_y:
								mip_info.do_weave = 1
							else:
								# e.g. PC2 aflegs04.pbasecolourtexture, set all to 0 if one of them is 0
								mip_info.num_weaves_x = mip_info.num_weaves_y = mip_info.do_weave = 0
						mip_info.size = len(mip_bytes)
						height //= 2
						width //= 2
					mip_info.ff = -1
				for lod, mip_offset in zip(self.texbuffer.main,
										   (self.texbuffer.num_mips_low, self.texbuffer.num_mips_high)):
					first_index = self.texbuffer.num_mips - mip_offset
					mip0 = self.texbuffer.mip_maps[first_index]
					lod.size = sum(mip.size for mip in self.texbuffer.mip_maps[first_index:])
					lod.num_weaves_x = mip0.num_weaves_x
					lod.num_weaves_y = mip0.num_weaves_y
					lod.do_weave = mip0.do_weave
					lod.ff = 0
				unweaved_bytes = b"".join(packed_mips)
				self.weave(dds_file, unweaved_bytes)
				self.texbuffer.buffer_size = len(self.raw_bytes)
				return self.raw_bytes
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
				for buffer_i, buffer in enumerate(texbuffers):
					mip = size_info.mip_maps[buffer_i]
					buffer.first_mip = buffer_i
					# last tex buffer gets all remaining mips
					if buffer_i == len(texbuffers) - 1:
						buffer.mip_count = len(size_info.mip_maps) - buffer.first_mip
						buffer.size = size_info.data_size - mip.offset
					else:
						buffer.mip_count = 1
						buffer.size = mip.size_array
					buffer.offset = mip.offset
				# slice packed bytes according to tex header buffer specifications
				return [packed[b.offset: b.offset + b.size] for b in texbuffers]

	def get_image_files(self, tile_name, in_dir, tmp_dir, dds_paths, png_paths):
		"""Returns a valid dds file object, or None"""
		bare_path = os.path.join(in_dir, tile_name)
		dds_path = f"{bare_path}.dds"
		# prioritize dds files if they exist
		if os.path.isfile(dds_path):
			dds_paths.append(dds_path)
			return True
		else:
			try:
				# try to reassemble a flat PNG for this tile, and then convert it to DDS
				png_path = imarray.join_png(self.ovl.game, bare_path, tmp_dir, self.compression_name)
				png_paths.append(png_path)
				return True
			except FileNotFoundError:
				logging.exception("Could not convert to .dds due to missing .png")
		return False

	def get_names(self, file_path):
		assert file_path == os.path.normpath(file_path)
		in_dir, name_ext = os.path.split(file_path)
		basename, ext = os.path.splitext(name_ext.lower())
		return in_dir, name_ext, basename, ext

	def convert_png(self, png_path, tmp_dir):
		logging.info(f"Converting {png_path}")
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
		dds_file_path = texconv.png_to_dds(
			png_path, tmp_dir,
			codec=compression,
			num_mips=num_mips,
			dds_use_gpu=self.ovl.cfg.get("dds_use_gpu", True))
		return dds_file_path

	def load_dds(self, dds_path):
		logging.info(f"Loading {dds_path}")
		# load dds
		dds_file = DdsFile()
		dds_file.load(dds_path)
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
		if is_dla(self.ovl) or self.context.is_pc_2:
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

	def get_texel(self):
		# get texel file from ovl to read external image buffer from aux
		texel_name = f"/{self.header.texel}.texel"
		if texel_name in self.ovl.loaders:
			texel_loader = self.ovl.loaders[texel_name]
		else:
			texel_loader = self.ovl.create_file(f"dummy_dir/{texel_name}", texel_name)
			self.ovl.register_loader(texel_loader)
		return texel_loader


	def weave_generator(self, dds_file):
		"""Shuffle a single mip at a time"""
		offset = 0
		dds_file.get_pixel_fmt()
		for tile_i in range(self.texbuffer.num_tiles):
			height = self.texbuffer.height
			width = self.texbuffer.width
			for mip_i, mip in enumerate(self.texbuffer.mip_maps):
				if mip.size == 0:
					continue

				# logging.debug(f"MIP{mip_i}")
				if mip.num_weaves_x > 1 and mip.num_weaves_y > 1:
					seek = 0
					tile_row_count = height // self.texbuffer.weave_height  # or mip.num_weaves_y?
					tile_col_count = width // self.texbuffer.weave_width  # or mip.num_weaves_x?
					if tile_row_count != mip.num_weaves_y:
						logging.warning(f"tile_row_count {tile_row_count} != mip.num_weaves_y {mip.num_weaves_y}")
					if tile_col_count != mip.num_weaves_x:
						logging.warning(f"tile_col_count {tile_col_count} != mip.num_weaves_x {mip.num_weaves_x}")

					tile_scanline_count = self.texbuffer.weave_height // tile_col_count // dds_file.block_len_pixels_1d
					tile_scanline_size = int(round(self.texbuffer.weave_width / 4 * dds_file.block_byte_size))
					scanline_size = tile_col_count * tile_scanline_size

					tile_size = scanline_size * tile_col_count
					tile_row_size = tile_size * tile_scanline_count

					# logging.debug(f"tile_row_count = {tile_row_count}")
					# logging.debug(f"tile_col_count = {tile_col_count}")
					# logging.debug(f"tile_col_count = {tile_col_count}")
					# logging.debug(f"tile_scanline_count = {tile_scanline_count}")
					# logging.debug(f"tile_scanline_size = {tile_scanline_size}")
					# logging.debug(f"tile_row_size = {tile_row_size}")
					# logging.debug(f"tile_size = {tile_size}")
					# logging.debug(f"scanline_size = {scanline_size}")
					for block_row_i in range(tile_row_count):
						for block_col_i in range(tile_col_count):
							for row_i in range(tile_scanline_count):
								for col_i in range(tile_col_count):
									# print(f"block_row {block_row_i} block_col {block_col_i} row {row_i} col {col_i} ")
									target_offset = (tile_row_size * block_row_i) + (row_i * tile_size) + (
												col_i * scanline_size) + (block_col_i * tile_scanline_size)
									yield offset + target_offset, offset + seek, tile_scanline_size
									seek += tile_scanline_size
				offset += mip.size
				height //= 2
				width //= 2

	def extract(self, out_dir):
		# override super to store ovs name for PC2
		# out_files = list(super().extract(out_dir))
		if self.header:
			out_path = out_dir(self.name)
			with self.header.to_xml_file(self.header, out_path, debug=self.ovl.do_debug) as xml_root:
				if self.ovl.do_debug:
					pool, offset = self.root_ptr
					xml_root.set("_address", f"{pool.i} | {offset}")
					xml_root.set("_size", f"{pool.size_map.get(offset, -1)}")
				if self.context.is_pc_2:
					xml_root.set("ovs", self.ovs.arg.name)
					xml_root.set("num_mips_low", str(self.texbuffer.num_mips_low))
					xml_root.set("num_mips_high", str(self.texbuffer.num_mips_high))
			out_files = [out_path, ]
		else:
			logging.warning(f"File '{self.name}' has no header - has the OVL finished loading?")
			return ()

		dds_paths = []
		tex_name = self.name
		basename = os.path.splitext(tex_name)[0]
		logging.info(f"Writing {tex_name}")

		size_info = self.get_tex_structs()

		dds_file = DdsFile()
		dds_file.width = size_info.width
		dds_file.height = size_info.height
		dds_file.mipmap_count = size_info.num_mips
		if hasattr(size_info, "depth") and size_info.depth:
			dds_file.depth = size_info.depth

		# set compression
		dds_file.dx_10.dxgi_format = DxgiFormat[self.compression_name]
		tiles = self.get_tiles(size_info)
		# set num_tiles to unpack the mips
		dds_file.dx_10.num_tiles = len(tiles)
		if not self.context.is_pc_2:
			# get joined output buffer
			buffer_data = b"".join([buffer.data for buffer in self.get_sorted_streams()])
			image_buffer = buffer_data
		else:
			# take the unweaved mip data
			image_buffer = self.unweave(dds_file)
			if self.ovl.do_debug:
				texbuffer_path = out_dir(f"{self.basename}.texbuffer")
				with self.texbuffer.to_xml_file(self.texbuffer, texbuffer_path, debug=self.ovl.do_debug) as xml_root:
					pass
				out_files.append(texbuffer_path)
				img_path = out_dir(f"{self.basename}.img")
				with open(img_path, "wb") as img:
					img.write(self.raw_bytes)
				out_files.append(img_path)
		if is_dla(self.ovl) or is_ztuac(self.ovl) or is_pc(self.ovl):
			# not sure how / if texture arrays are packed for PC - this works for flat textures
			tile_datas = (image_buffer,)
		else:
			# PC2 swaps nesting of tiles and mips
			tile_datas = dds_file.unpack_mips(image_buffer, debug=self.ovl.do_debug, is_pc_2=self.context.is_pc_2)
		# set to no tiles for dds export
		dds_file.dx_10.num_tiles = 1
		# export all tiles as separate dds files
		for tile_i, tile_name, tile_data in zip(tiles, self.get_tile_names(tiles, basename), tile_datas):
			dds_file.buffer = tile_data
			dds_file.linear_size = len(tile_data)
			dds_path = out_dir(f"{tile_name}.dds")
			# write dds
			dds_file.save(dds_path)
			dds_paths.append(dds_path)
		# decompress dds to png
		for dds_path in self.ovl.reporter.iter_progress(dds_paths, "Converting", cond=len(dds_paths) > 1):
			try:
				# convert the dds to png
				png_path = texconv.dds_to_png(dds_path, self.compression_name)
				# postprocessing of the png
				if os.path.isfile(png_path):
					out_files.extend(imarray.split_png(png_path, self.ovl, self.compression_name))
			except:
				logging.exception(f"Postprocessing of {dds_path} failed!")
		return out_files + dds_paths

	def get_extract_paths(self, out_dir):
		if self.header:
			out_path = out_dir(self.name)
			out_files = [out_path, ]
		else:
			return ()
		dds_paths = []
		tex_name = self.name
		basename = os.path.splitext(tex_name)[0]
		size_info = self.get_tex_structs()
		tiles = self.get_tiles(size_info)
		for tile_name in self.get_tile_names(tiles, basename):
			dds_path = out_dir(f"{tile_name}.dds")
			dds_paths.append(dds_path)
		for dds_path in dds_paths:
			png_path = os.path.splitext(dds_path)[0] + ".png"
			out_files.extend(imarray.get_extract_paths(png_path, self.ovl, self.compression_name))
		if self.context.is_pc_2:
			if self.ovl.do_debug:
				texbuffer_path = out_dir(f"{self.basename}.texbuffer")
				out_files.append(texbuffer_path)
				img_path = out_dir(f"{self.basename}.img")
				out_files.append(img_path)
		return out_files + dds_paths

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


class TexelLoader(MemStructLoader):
	extension = ".texel"
	can_extract = False
	target_class = TexelHeader

	def get_aux_name(self, aux_suffix, aux_size=0):
		"""Get path of aux file from ovl name and texel name"""
		# Full Archive path:
		#   Win64\ovldata\Content0\Worlds\DefaultSandbox.ovl
		# File in Archive:
		#   /zz159oeel9rhs8ex.texel
		# File in tex header:
		#   zz159oeel9rhs8ex
		# Input Text
		# text = b"defaultsandbox_/zz159oeel9rhs8ex_texel"
		# Resulting Lookup:
		#   XERY2OUE5ECDC_.aux
		# Result:
		# XERY2OUE5ECDC
		assert aux_suffix == ""
		text = f"{self.ovl.basename}_{self.name.replace('.', '_')}".lower().encode()
		hash_value = fnv64(text)
		return f"{encode_int64_base32(hash_value)}_.aux"

	def create(self, file_path):
		self.header = self.target_class(self.context)
		self.write_memory_data()

	def delete_unused(self):
		if not self.aux_handles:
			logging.info(f"Deleting {self.name} as it is no longer used")
			self.ovl.loaders.pop(self.name)
