import io
import logging
import os

from generated.formats.dds import DdsFile
from generated.formats.dds.enum.DxgiFormat import DxgiFormat
from generated.formats.ovl.versions import *
from generated.formats.tex import TexFile
from generated.formats.tex.compound.TexBuffer import TexBuffer
from generated.formats.tex.compound.SizeInfo import SizeInfo
from generated.formats.tex.compound.TexBufferPc import TexBufferPc
from generated.formats.tex.compound.TexHeader import TexHeader
from modules.formats.BaseFormat import MemStructLoader
from modules.formats.shared import get_versions
from modules.helpers import split_path, as_bytes

from ovl_util import texconv, imarray


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


class DdsLoader(MemStructLoader):
	target_class = TexHeader

	def _get_data(self, file_path):
		tex_file = TexFile(self.ovl.context)
		tex_file.load(file_path)
		# print(tex_file)
		ss = as_bytes(tex_file.tex_info)
		f01 = as_bytes(tex_file.frag_01)
		f11 = as_bytes(tex_file.frag_11) + as_bytes(tex_file.padding)
		buffers = tex_file.buffers
		return ss, f01, f11, buffers

	def create(self):
		name_ext, name, ext = split_path(self.file_entry.path)
		logging.debug(f"Creating image {name_ext}")
		if ext == ".tex":
			if is_jwe(self.ovl) or is_pz(self.ovl) or is_pz16(self.ovl) or is_jwe2(self.ovl):
				ss, f01, f11, buffers = self._get_data(self.file_entry.path)
				self.sized_str_entry = self.create_ss_entry(self.file_entry)
				frag0, frag1 = self.create_fragments(self.sized_str_entry, 2)
				ss_ptr = self.sized_str_entry.pointers[0]
				# pool type 3
				data3 = (ss, f01)
				ptrs3 = (ss_ptr, frag0.pointers[1])
				for ptr, data in zip(ptrs3, data3):
					self.write_to_pool(ptr, 3, data)

				self.ptr_relative(frag0.pointers[0], ss_ptr, rel_offset=16)
				self.ptr_relative(frag1.pointers[0], ss_ptr, rel_offset=24)

				if is_jwe(self.ovl):
					f11_pool_type = 7
				else:
					f11_pool_type = 4
				self.write_to_pool(frag1.pointers[1], f11_pool_type, f11)

				# decide where to store the buffers
				static_lods = 2
				streamed_lods = len(buffers) - static_lods
				logging.info(f"buffers: {len(buffers)} streamed lods: {streamed_lods}")
				ss_entries = [self.sized_str_entry, ]
				# ovs name generation only works for up to 2 streams
				assert streamed_lods < 3
				for i in range(streamed_lods):
					# generate ovs name - highly idiosyncratic
					# game expects to start with L1
					# if there are 2 lods
					# stock puts the first stream lod0 in L1, lod1 in L0
					# a file with just one stream lod0 goes into L1 too
					ovs_name = f"Textures_L{1-i}"
					# create texturestream file
					texstream_file = self.get_file_entry(f"test/{name}_lod{i}.texturestream")
					self.file_entry.streams.append(texstream_file)
					# ss entry
					texstream_ss = self.create_ss_entry(texstream_file, ovs=ovs_name)
					ss_entries.append(texstream_ss)
					self.write_to_pool(texstream_ss.pointers[0], 3, b"\x00" * 8, ovs=ovs_name)
					# data entry, assign buffer
					self.create_data_entry(texstream_ss, (buffers[i], ), ovs=ovs_name)
				self.create_data_entry(self.sized_str_entry, buffers[streamed_lods:])
				# patch buffer indices for PZ, JWE1
				if not is_jwe2(self.ovl):
					logging.debug(f"Using absolute buffer indices for streams")
					all_buffers = [buffer for ss in ss_entries for buffer in ss.data_entry.buffers]
					all_buffers.sort(key=lambda b: b.size, reverse=True)
					for i, buffer in enumerate(all_buffers):
						buffer.index = i
			elif is_pc(self.ovl) or is_ztuac(self.ovl):
				logging.error(f"Only modern texture format supported for now!")
		else:
			logging.error(f"Only .tex supported for now!")

	def collect(self):
		super().collect()
		# print(self.header)
		# all_buffers = self.get_sorted_streams()
		# for buff in all_buffers:
		# 	print(buff.index, buff.size)

	def load(self, file_path):
		logging.debug(f"Loading image {file_path}")
		name_ext, name, ext = split_path(file_path)
		if ext == ".png":
			self.load_png(file_path)
		elif ext == ".dds":
			self.load_dds(file_path)
		elif ext == ".tex":
			raise NotImplementedError(f"Can't inject .tex, only create them!")
			# self.load_dds(file_path)

	def get_sorted_streams(self):
		# lod0 | lod1 | static
		# PZ assigns the buffer index for the complete struct 0 | 1 | 2, 3
		# from JWE2, buffer index for streams is 0 | 0 | 0, 1
		# the last buffer is always 0 bytes
		return list(sorted(self.get_streams(), key=lambda buffer: buffer.size, reverse=True))

	def load_dds(self, file_path):
		logging.info(f"Loading DDS {file_path}")
		tex_buffers, size_info = self.get_tex_structs()
		# tex_d = self.header.one_0
		# tex_d = size_info.depth
		tex_d = 1
		tex_h = size_info.height
		tex_w = size_info.width
		tex_a = size_info.array_size
		comp = self.header.compression_type.name
		tex_w = align_to(tex_w, comp)
	
		# read archive tex header to make sure we have the right mip count
		# even when users import DDS with mips when it should have none
	
		# load dds
		dds_file = DdsFile()
		dds_file.load(file_path)
		self.ensure_size_match(dds_file, tex_h, tex_w, tex_d, tex_a, comp)
		sorted_streams = self.get_sorted_streams()
		if is_pc(self.ovl):
			for buffer, tex_header_3 in zip(sorted_streams, tex_buffers):
				dds_buff = dds_file.pack_mips_pc(tex_header_3.num_mips)
				self.overwrite_buffer(buffer, dds_buff)
		else:
			out_bytes = dds_file.pack_mips(size_info.num_mips)
			sum_of_buffers = sum(buffer.size for buffer in sorted_streams)
			if len(out_bytes) != sum_of_buffers:
				logging.warning(
					f"Packing of MipMaps failed. OVL expects {sum_of_buffers} bytes, but packing generated {len(out_bytes)} bytes.")
			with io.BytesIO(out_bytes) as reader:
				for buffer in sorted_streams:
					dds_buff = reader.read(buffer.size)
					self.overwrite_buffer(buffer, dds_buff)

	@staticmethod
	def overwrite_buffer(buffer, dds_buff):
		if len(dds_buff) < buffer.size:
			logging.warning(f"Last {buffer.size - len(dds_buff)} bytes of DDS buffer are not overwritten!")
			dds_buff = dds_buff + buffer.data[len(dds_buff):]
		buffer.update_data(dds_buff)

	def get_tex_structs(self):
		tex_buffers = self.header.buffer_infos.data
		if is_pc(self.ovl) or is_ztuac(self.ovl):
			# this corresponds to a stripped down size_info
			size_info = self.header.buffer_infos.data[0]
		else:
			size_info = self.header.size_info.data
		return tex_buffers, size_info

	def extract(self, out_dir, show_temp_files, progress_callback):
		tex_name = self.sized_str_entry.name
		basename = os.path.splitext(tex_name)[0]
		dds_name = basename + ".dds"
		logging.info(f"Writing {tex_name}")

		# get joined output buffer
		buffer_data = b"".join([buffer.data for buffer in self.get_sorted_streams()])

		out_files = []
		tex_path = out_dir(tex_name)
		if show_temp_files:
			out_files.append(tex_path)
		with open(tex_path, "wb") as tex_file:
			tex_file.write(self.pack_header(b"TEX"))
			# num_buffers
			# tex_file.write(struct.pack("I", 1+len(self.file_entry.streams)))
			tex_file.write(self.sized_str_entry.pointers[0].data)
			for frag in self.sized_str_entry.fragments:
				tex_file.write(frag.pointers[1].data)
			tex_file.write(buffer_data)

		tex_file = TexFile(self.ovl.context)
		tex_file.load(tex_path)
		# print(tex_file)
		# return out_files
		dds_file = DdsFile()
		dds_file.buffer = buffer_data

		if is_dla(self.ovl):
			tex_info = tex_file.tex_info
			dds_file.width = tex_info.width
			dds_file.height = tex_info.height
			dds_file.mipmap_count = tex_info.num_mips
			dds_file.linear_size = len(buffer_data)
			dds_file.depth = 1
		elif is_pc(self.ovl) or is_ztuac(self.ovl):
			tex_info = tex_file.frag_01[0]
			dds_file.width = tex_info.width
			# hack until we have proper support for array_size on the image editors
			# todo - this is most assuredly not array size for ED
			dds_file.height = tex_info.height  # * max(1, size_info.array_size)
			dds_file.mipmap_count = tex_info.mip_index
			dds_file.linear_size = len(buffer_data)
			dds_file.depth = 1
		else:
			tex_info = tex_file.frag_11
			if not len(buffer_data) == tex_info.data_size:
				print(
					f"7_1 data size ({tex_info.data_size}) and actual data size of combined buffers ({len(buffer_data)}) do not match up (bug)")
			dds_file.width = tex_info.width
			# hack until we have proper support for array_size on the image editors
			dds_file.height = tex_info.height * tex_info.array_size
			dds_file.depth = tex_info.depth
			dds_file.linear_size = tex_info.data_size
			dds_file.mipmap_count = tex_info.num_mips
	
		try:
			dds_type = tex_file.tex_info.compression_type.name
			logging.info(tex_file.tex_info.compression_type)
			# account for aliases
			if dds_type.endswith(("_B", "_C")):
				dds_type = dds_type[:-2]
			dds_compression_types = ((dds_type, DxgiFormat[dds_type]),)
		except KeyError:
			dds_compression_types = [(x.name, x) for x in DxgiFormat]
			logging.warning(f"Unknown compression type {tex_file.tex_info.compression_type}, trying all compression types")
		logging.debug(f"dds_compression_type {dds_compression_types}")

		# write out everything for each compression type
		for dds_type, dds_value in dds_compression_types:
			# print(dds_file.width)
			# header attribs
			if not is_ztuac(self.ovl):
				dds_file.width = align_to(dds_file.width, dds_type)
	
			# dx 10 stuff
			dds_file.dx_10.dxgi_format = dds_value
	
			# start out
			dds_path = out_dir(dds_name)
			if len(dds_compression_types) > 1:
				dds_path += f"_{dds_type}.dds"
	
			# write dds
			dds_file.save(dds_path)
			# print(dds_file)
			if show_temp_files:
				out_files.append(dds_path)
	
			# convert the dds to PNG, PNG must be visible so put it in out_dir
			png_file_path = texconv.dds_to_png(dds_path, dds_file.height)
	
			if os.path.isfile(png_file_path):
				# postprocessing of the png
				out_files.extend(imarray.wrapper(png_file_path, tex_file.frag_11, self.ovl))
		return out_files

	def load_png(self, file_path):
		logging.info(f"Loading PNG {file_path}")
		# convert the png into a dds, then inject that
		tex_buffers, size_info = self.get_tex_structs()
		compression = self.header.compression_type.name
		show_temp = False
		dds_file_path = texconv.png_to_dds(
			file_path, size_info.height * size_info.array_size, show_temp, codec=compression, mips=size_info.num_mips)
	
		# inject the dds generated by texconv
		self.load_dds(dds_file_path)
		# remove the temp file if desired
		texconv.clear_tmp(dds_file_path, show_temp)

	def ensure_size_match(self, dds_header, tex_h, tex_w, tex_d, tex_a, comp):
		"""Check that DDS files have the same basic size"""
		dds_h = dds_header.height
		dds_w = dds_header.width
		dds_d = dds_header.depth
		dds_a = dds_header.dx_10.array_size
	
		if dds_h * dds_w * dds_d * dds_a != tex_h * tex_w * tex_d * tex_a:
			raise AttributeError(
				f"Dimensions do not match for {self.file_entry.name}!\n\n"
				f"Dimensions: height x width x depth [array size]\n"
				f"OVL Texture: {tex_h} x {tex_w} x {tex_d} [{tex_a}]\n"
				f"Injected texture: {dds_h} x {dds_w} x {dds_d} [{dds_a}]\n\n"
				f"Make the external texture's dimensions match the OVL texture and try again!")
