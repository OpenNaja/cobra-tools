import os
import itertools
import shutil
import struct
import tempfile
import zlib
import io
import time
import traceback
import logging
from contextlib import contextmanager

from generated.formats.ovl.compound.DependencyEntry import DependencyEntry
from generated.formats.ovl.compound.Fragment import Fragment
from generated.formats.ovl.compound.PoolGroup import PoolGroup
from generated.formats.ovl.compound.StreamEntry import StreamEntry
from generated.formats.ovl_base import OvlContext
from generated.formats.ovl_base.enum.Compression import Compression
from ovl_util.oodle.oodle import OodleDecompressEnum, oodle_compressor

from generated.io import IoFile, BinaryStream
from generated.formats.ovl.versions import *
from generated.formats.ovl.compound.AssetEntry import AssetEntry
from generated.formats.ovl.compound.Header import Header
from generated.formats.ovl.compound.OvsHeader import OvsHeader
from generated.formats.ovl.compound.SetEntry import SetEntry
from generated.formats.ovl.compound.ArchiveEntry import ArchiveEntry
from generated.formats.ovl.compound.IncludedOvl import IncludedOvl
from generated.formats.ovl.compound.FileEntry import FileEntry
from generated.formats.ovl.compound.MimeEntry import MimeEntry
from generated.formats.ovl.compound.BufferGroup import BufferGroup
from generated.formats.ovl.compound.ZlibInfo import ZlibInfo

from modules.formats.shared import get_versions, djb, assign_versions
from modules.helpers import split_path

OODLE_MAGIC = (b'\x8c', b'\xcc')

REVERSED_TYPES = (
	".animalresearchunlockssettings",
	".assetpkg",
	".curve",
	".fdb",
	".fgm",
	".gfx",
	".island",
	".logicalcontrols",
	".lua",
	".materialcollection",
	".mdl2",
	".mergedetails",
	".ms2",
	".pscollection",
	".spl",
	".tex",
	".texturestream",
	".txt",
	".uimovidefinition",
	".userinterfaceicondata",
	".world"
	".xmlconfig",
)
# types that have no loader themselves, but are handled by other classes
IGNORE_TYPES = (".mani", ".mdl2", ".bani", ".texturestream", ".datastreams", ".model2stream")

aliases = {
	".matcol": ".materialcollection",
	".png": ".tex",
	".dds": ".tex",
	".otf": ".fct",
	".ttf": ".fct",
}


def get_loader(ext, ovl, file_entry):
	from modules.formats.ANIMALRESEARCHUNLOCKSSETTINGS import AnimalresearchstartunlockedssettingsLoader
	from modules.formats.ANIMALRESEARCHUNLOCKSSETTINGS import AnimalresearchunlockssettingsLoader
	from modules.formats.ASSETPKG import AssetpkgLoader
	from modules.formats.BANI import BanisLoader
	from modules.formats.BNK import BnkLoader
	from modules.formats.CURVE import CurveLoader
	from modules.formats.DDS import DdsLoader
	from modules.formats.ENUMNAMER import EnumnamerLoader
	from modules.formats.FCT import FctLoader
	from modules.formats.FDB import FdbLoader
	from modules.formats.FGM import FgmLoader
	from modules.formats.GFX import GfxLoader
	from modules.formats.ISLAND import IslandLoader
	from modules.formats.LOGICALCONTROLS import LogicalControlsLoader
	from modules.formats.LUA import LuaLoader
	from modules.formats.MANI import ManisLoader
	from modules.formats.MATCOL import MatcolLoader
	from modules.formats.MATLAYERS import MateffsLoader
	from modules.formats.MATLAYERS import MatlayersLoader
	from modules.formats.MATLAYERS import MatpatsLoader
	from modules.formats.MATLAYERS import MatvarsLoader
	from modules.formats.MERGEDETAILS import MergeDetailsLoader
	from modules.formats.MOTIONGRAPHVARS import MotiongraphvarsLoader
	from modules.formats.MS2 import Ms2Loader
	from modules.formats.POSEDRIVERDEF import PosedriverdefLoader
	from modules.formats.PREFAB import PrefabLoader
	from modules.formats.PSCOLLECTION import PSCollectionLoader
	from modules.formats.SCALEFORMLANGUAGEDATA import ScaleformLoader
	from modules.formats.SPECDEF import SpecdefLoader
	from modules.formats.SPL import SplineLoader
	from modules.formats.TXT import TxtLoader
	from modules.formats.UIMOVIEDEFINITION import UIMovieDefinitionLoader
	from modules.formats.USERINTERFACEICONDATA import UserinterfaceicondataLoader
	from modules.formats.VOXELSKIRT import VoxelskirtLoader
	from modules.formats.WMETA import WmetaLoader
	from modules.formats.WORLD import WorldLoader
	from modules.formats.WSM import WsmLoader
	from modules.formats.XMLCONFIG import XmlconfigLoader
	ext_2_class = {
		".animalresearchstartunlockedsettings": AnimalresearchstartunlockedssettingsLoader,
		".animalresearchunlockssettings": AnimalresearchunlockssettingsLoader,
		".assetpkg": AssetpkgLoader,
		".banis": BanisLoader,
		".bnk": BnkLoader,
		".curve": CurveLoader,
		".dinosaurmaterialeffects": MateffsLoader,
		".dinosaurmateriallayers": MatlayersLoader,
		".dinosaurmaterialpatterns": MatpatsLoader,
		".dinosaurmaterialvariants": MatvarsLoader,
		".enumnamer": EnumnamerLoader,
		".fct": FctLoader,
		".fdb": FdbLoader,
		".fgm": FgmLoader,
		".gfx": GfxLoader,
		".island": IslandLoader,
		".logicalcontrols": LogicalControlsLoader,
		".lua": LuaLoader,
		".manis": ManisLoader,
		".materialcollection": MatcolLoader,
		".mergedetails": MergeDetailsLoader,
		".motiongraphvars": MotiongraphvarsLoader,
		".ms2": Ms2Loader,
		".posedriverdef": PosedriverdefLoader,
		".prefab": PrefabLoader,
		".pscollection": PSCollectionLoader,
		".scaleformlanguagedata": ScaleformLoader,
		".specdef": SpecdefLoader,
		".spl": SplineLoader,
		".tex": DdsLoader,
		".txt": TxtLoader,
		".uimoviedefinition": UIMovieDefinitionLoader,
		".userinterfaceicondata": UserinterfaceicondataLoader,
		".voxelskirt": VoxelskirtLoader,
		".wmetasb": WmetaLoader,
		".world": WorldLoader,
		".wsm": WsmLoader,
		".xmlconfig": XmlconfigLoader,
	}
	cls = ext_2_class.get(ext, None)
	if cls:
		return cls(ovl, file_entry)


class OvsFile(OvsHeader):

	def __init__(self, context, ovl_inst, archive_entry):
		super().__init__(context)
		self.ovl = ovl_inst
		self.arg = archive_entry

	@staticmethod
	def add_pointer(pointer, ss_entry, pointers_to_ss):
		if pointer.pool_index != -1:
			pointers_to_ss[pointer.pool_index][pointer.data_offset] = ss_entry

	def header_name_finder(self):
		# this algorithm depends on every fragment being assigned to the correct sized string entries
		logging.info("Updating pool names")
		pointers_to_ss = [{} for _ in self.pools]
		pointers_to_ss_frag = [{} for _ in self.pools]
		for sized_str_entry in self.sized_str_entries:
			self.add_pointer(sized_str_entry.pointers[0], sized_str_entry, pointers_to_ss)
			for frag in sized_str_entry.fragments:
				for pointer in frag.pointers:
					self.add_pointer(pointer, sized_str_entry, pointers_to_ss_frag)
		for pool_index, pool in enumerate(self.pools):
			logging.debug(f"pool_index {pool_index}")
			# if we are dealing with a pool loaded from an ovl, see if its extension has been figured out
			if hasattr(pool, "ext") and pool.ext not in REVERSED_TYPES:
				logging.debug(f"Keeping pool name {pool.name} as it has not been reverse engineered!")
				continue
			ss_map = pointers_to_ss[pool_index]
			results = tuple(sorted(ss_map.items()))
			if not results:
				logging.debug("No ss pointer found, checking frag pointers!")
				ss_map = pointers_to_ss_frag[pool_index]
				results = tuple(sorted(ss_map.items()))
				if not results:
					logging.error(f"No pointer found for pool {pool_index}, error!")
					continue
			ss = results[0][1]
			logging.debug(f"Header[{pool_index}]: {pool.name} -> {ss.name}")
			self.transfer_identity(pool, ss)

	def get_bytes(self, external_path):
		# load external uncompressed data
		if external_path and self.arg.name == "STATIC":
			with open(external_path, "rb") as f:
				return f.read()
		# write the internal data
		else:
			stream = BinaryStream()
			assign_versions(stream, get_versions(self.ovl))
			self.write_archive(stream)
			return stream.getbuffer()

	@contextmanager
	def unzipper(self, compressed_bytes, uncompressed_size, save_temp_dat=""):
		self.compression_header = compressed_bytes[:2]
		logging.debug(f"Compression magic bytes: {self.compression_header}")
		if self.ovl.user_version.compression == Compression.OODLE:
			logging.debug("Oodle compression")
			decompressed = oodle_compressor.decompress(compressed_bytes, len(compressed_bytes), uncompressed_size)
		elif self.ovl.user_version.compression == Compression.ZLIB:
			logging.debug("Zlib compression")
			# https://stackoverflow.com/questions/1838699/how-can-i-decompress-a-gzip-stream-with-zlib
			# we avoid the two zlib magic bytes to get our unzipped content
			decompressed = zlib.decompress(compressed_bytes[2:], wbits=-zlib.MAX_WBITS)
		# uncompressed archive
		else:
			logging.debug("No compression")
			decompressed = compressed_bytes
		if save_temp_dat:
			# for debugging, write deflated content to dat
			with open(save_temp_dat, 'wb') as out:
				out.write(decompressed)
		with BinaryStream(decompressed) as stream:
			yield stream

	def compress(self, uncompressed_bytes):
		# compress data
		# change to zipped format for saving of oodled ovls
		if self.ovl.user_version.compression == Compression.OODLE:
			logging.info("HACK: setting compression to zlib")
			self.ovl.user_version.compression = Compression.ZLIB
		if self.ovl.user_version.compression == Compression.OODLE:
			assert self.compression_header.startswith(OODLE_MAGIC)
			a, raw_algo = struct.unpack("BB", self.compression_header)
			algo = OodleDecompressEnum(raw_algo)
			logging.debug(f"Oodle compression {a} {raw_algo} {algo.name}")
			compressed = oodle_compressor.compress(bytes(uncompressed_bytes), algo.name)
		elif self.ovl.user_version.compression == Compression.ZLIB:
			compressed = zlib.compress(uncompressed_bytes)
		else:
			# uncompressed only stores the raw length, 0 for decompressed size
			return 0, len(uncompressed_bytes), uncompressed_bytes
		return len(uncompressed_bytes), len(compressed), compressed

	def update_hashes(self, file_name_lut):
		logging.info(f"Updating hashes for {self.arg.name}")
		logging.debug(f"Game: {get_game(self.ovl)}")
		self.header_name_finder()
		entry_lists = (
			self.pools,
			self.sized_str_entries,
			self.data_entries,
			self.set_header.sets,
			self.set_header.assets,
			self.buffer_entries
		)
		for entry_list in entry_lists:
			for entry in entry_list:
				if not entry.name:
					logging.warning(f"{entry} has no name assigned to it, cannot assign proper ID")
					continue
				if entry.name in file_name_lut:
					file_index = file_name_lut[entry.name]
				else:
					logging.debug(file_name_lut)
					raise KeyError(f"Can't find '{entry.name}' [{entry.__class__.__name__}] in name LUT")
				file = self.ovl.files[file_index]
				if self.ovl.user_version.is_jwe:
					entry.file_hash = file.file_hash
				else:
					entry.file_hash = file_index
				entry.ext_hash = file.ext_hash

	def update_counts(self):
		"""Update counts of this archive"""
		# make sure that all pools are padded
		for pool in self.pools:
			pool.pad()
		# adjust the counts
		self.arg.num_pools = len(self.pools)
		self.arg.num_datas = len(self.data_entries)
		self.arg.num_pool_groups = len(self.pool_groups)
		self.arg.num_buffers = len(self.buffer_entries)
		self.arg.num_fragments = len(self.fragments)
		self.arg.num_files = len(self.sized_str_entries)
		self.arg.num_buffer_groups = len(self.buffer_groups)
	# todo - self.arg.ovs_offset

	def unzip(self, archive_entry, start):
		filepath = archive_entry.ovs_path
		save_temp_dat = f"{filepath}_{self.arg.name}.dat" if "write_dat" in self.ovl.commands else ""
		stream = self.ovl.ovs_dict[filepath]
		stream.seek(start)
		logging.debug(f"Compressed stream in {os.path.basename(filepath)} starts at {stream.tell()}")
		compressed_bytes = stream.read(archive_entry.compressed_size)
		with self.unzipper(compressed_bytes, archive_entry.uncompressed_size, save_temp_dat=save_temp_dat) as stream:
			logging.debug("Reading unzipped stream")
			assign_versions(stream, get_versions(self.ovl))
			super().read(stream)
			# print(self)
			# print(self.buffer_groups)
			pool_index = 0
			for pool_type in self.pool_groups:
				for i in range(pool_type.num_pools):
					pool = self.pools[pool_index]
					pool.type = pool_type.type
					self.assign_name(pool)
					pool_index += 1

			for data_entry in self.data_entries:
				self.assign_name(data_entry)
			for sized_str_entry in self.sized_str_entries:
				self.assign_name(sized_str_entry)
				sized_str_entry.children = []
				sized_str_entry.fragments = []
				# get data entry for link to buffers, or none
				sized_str_entry.data_entry = self.find_entry(self.data_entries, sized_str_entry)

			if not (self.set_header.sig_a == 1065336831 and self.set_header.sig_b == 16909320):
				raise AttributeError("Set header signature check failed!")
			if self.set_header.io_size != self.arg.set_data_size:
				raise AttributeError(
					f"Set data size incorrect (got {self.set_header.io_size}, expected {self.arg.set_data_size})!")

			for set_entry in self.set_header.sets:
				self.assign_name(set_entry)
				set_entry.entry = self.find_entry(self.sized_str_entries, set_entry)

			for asset_entry in self.set_header.assets:
				self.assign_name(asset_entry)
				try:
					asset_entry.entry = self.sized_str_entries[asset_entry.file_index]
				except:
					raise IndexError(
						f"Could not find a sizedstr entry for asset {asset_entry} in {len(self.sized_str_entries)}")

			self.map_assets()

			# up to here was data defined by the OvsHeader class, ending with the AssetEntries
			self.start_of_pools = stream.tell()
			logging.debug(f"Start of pools data: {self.start_of_pools}")

			# doesn't work for 1.6
			# # another integrity check
			# if self.arg.uncompressed_size and not is_pc(self.ovl) and self.calc_uncompressed_size() != self.arg.uncompressed_size:
			# 	raise AttributeError(
			# 		f"Archive.uncompressed_size ({self.arg.uncompressed_size}) "
			# 		f"does not match calculated size ({self.calc_uncompressed_size()})")

			# add IO object to every pool
			self.read_pools(stream)
			self.map_buffers()
			self.read_buffer_datas(stream)

	def read_pools(self, stream):
		for pool in self.pools:
			pool.address = stream.tell()
			pool.data = BinaryStream(stream.read(pool.size))
			assign_versions(pool.data, get_versions(self.ovl))

	def map_assets(self):
		"""Store start and stop indices to asset entries, translate hierarchy to sizedstr entries"""
		# store start and stop asset indices
		for i, set_entry in enumerate(self.set_header.sets):
			# for the last entry
			if i == self.set_header.set_count - 1:
				set_entry.end = self.set_header.asset_count
			# store start of the next one as this one's end
			else:
				set_entry.end = self.set_header.sets[i + 1].start
			# map assets to entry
			assets = self.set_header.assets[set_entry.start: set_entry.end]
			logging.debug(f"SET: {set_entry.name}")
			logging.debug(f"ASSETS: {[a.name for a in assets]}")
			# store the references on the corresponding sized str entry
			assert set_entry.entry
			set_entry.entry.children = [self.sized_str_entries[a.file_index] for a in assets]

	@staticmethod
	def transfer_identity(source_entry, target_entry):
		source_entry.basename = target_entry.basename
		source_entry.ext = target_entry.ext
		source_entry.name = target_entry.name

	def rebuild_assets(self):
		"""Update archive asset grouping from children list on sized str entries"""
		logging.info(f"Updating assets for {self.arg.name}")
		self.set_header.sets.clear()
		self.set_header.assets.clear()
		self.set_header.set_count = 0
		self.set_header.asset_count = 0
		start = 0
		ss_index_table = {file.name: i for i, file in enumerate(self.sized_str_entries)}
		for ss_entry in self.sized_str_entries:
			if ss_entry.children:
				set_entry = SetEntry(self.context)
				set_entry.start = start
				set_entry.end = start + len(ss_entry.children)
				self.transfer_identity(set_entry, ss_entry)
				self.set_header.sets.append(set_entry)
				for ss_child in ss_entry.children:
					asset_entry = AssetEntry(self.context)
					asset_entry.file_index = ss_index_table[ss_child.name]
					self.transfer_identity(asset_entry, ss_child)
					self.set_header.assets.append(asset_entry)
				start += len(ss_entry.children)
				self.set_header.set_count += 1
				self.set_header.asset_count += len(ss_entry.children)
				# set_index is 1-based, so the first set = 1, so we do it after the increment
				ss_entry.data_entry.set_index = self.set_header.set_count

	def rebuild_buffer_groups(self):
		logging.info(f"Updating buffer groups for {self.arg.name}")
		self.buffer_groups.clear()
		self.sized_str_entries.sort(key=lambda b: (b.ext, b.file_hash))
		self.data_entries.sort(key=lambda b: (b.ext, b.file_hash))
		if (is_pz16(self.ovl) or is_jwe2(self.ovl)) and self.data_entries:
			for data_entry in self.data_entries:
				for buffer in data_entry.buffers:
					self.transfer_identity(buffer, data_entry)
			# sort datas and buffers to be what 1.6 needs
			# cobra < 20 used buffer index per data entry
			self.buffer_entries.sort(key=lambda b: (b.ext, b.index, b.file_hash))

			# print("AYAYA\n", self.data_entries, "AYAYA\n", self.buffer_entries)
			# generate a mime lut to know the index of the mimes
			mime_lut = {mime.ext: i for i, mime in enumerate(self.ovl.mimes)}
			# generate the buffergroup entries

			last_ext = None
			last_index = None
			buffer_group = None
			buffer_offset = 0
			data_offset = 0
			for i, buffer in enumerate(self.buffer_entries):
				logging.debug(f"Buffer {i}, last: {last_ext} this: {buffer.ext}")
				# we have to create a new group
				if buffer.ext != last_ext or buffer.index != last_index:
					# if we already have a buffer_group declared, update offsets for the next one
					# if buffer_group:
					# 	logging.debug(f"Updating offsets {buffer_offset}, {data_offset}")
					# 	buffer_offset += buffer_group.buffer_count
					# 	# only change data offset if ext changes
					# 	if buffer.ext != last_ext:
					# 		data_offset += buffer_group.data_count
					# now create the new buffer_group and update its initial data
					buffer_group = BufferGroup(self.context)
					buffer_group.ext = buffer.ext
					buffer_group.ext_index = mime_lut.get(buffer.ext)
					buffer_group.buffer_index = buffer.index
					buffer_group.buffer_offset = buffer_offset
					buffer_group.data_offset = data_offset
					self.buffer_groups.append(buffer_group)
				# gotta add this buffer to the current group
				buffer_group.buffer_count += 1
				buffer_group.size += buffer.size
				buffer_group.data_count += 1
				# change buffer identity for next loop
				last_ext = buffer.ext
				last_index = buffer.index

			# fix the offsets of the buffergroups
			for x, buffer_group in enumerate(self.buffer_groups):
				if x > 0:
					buffer_group.buffer_offset = self.buffer_groups[x - 1].buffer_offset + self.buffer_groups[
						x - 1].buffer_count
					if buffer_group.ext != self.buffer_groups[x - 1].ext:
						buffer_group.data_offset = self.buffer_groups[x - 1].data_offset + self.buffer_groups[
							x - 1].data_count
					else:
						buffer_group.data_offset = self.buffer_groups[x - 1].data_offset
						if buffer_group.data_count < self.buffer_groups[x - 1].data_count:
							buffer_group.data_count = self.buffer_groups[x - 1].data_count
			# tex buffergroups sometimes are 0,1 instead of 1,2 so the offsets need additional correction
			tex_fixa = 0
			tex_fixb = 0
			tex_fixc = 0
			for buffer_group in self.buffer_groups:
				if ".tex" == buffer_group.ext:
					if buffer_group.buffer_count > tex_fixb:
						tex_fixb = buffer_group.buffer_count
					if buffer_group.data_offset > tex_fixa:
						tex_fixa = buffer_group.data_offset
				elif ".texturestream" == buffer_group.ext:
					tex_fixc += buffer_group.buffer_count
			for buffer_group in self.buffer_groups:
				if ".tex" == buffer_group.ext:
					buffer_group.data_offset = tex_fixa
					buffer_group.data_count = tex_fixb
				elif ".texturestream" == buffer_group.ext:
					buffer_group.data_count = tex_fixc

			if (self.buffer_groups[-1].data_count + self.buffer_groups[-1].data_offset) < len(self.data_entries):
				for x in range(self.buffer_groups[-1].buffer_index + 1):
					self.buffer_groups[-1 - x].data_count = len(self.data_entries) - self.buffer_groups[
						-1 - x].data_offset

	def frags_accumulate(self, p, d_size, frags=None):
		# get frags whose pointers 0 datas together occupy d_size bytes
		fs = []
		# the frag list crosses header borders at Deinonychus_events, so use full frag list
		if frags is None:
			frags = self.fragments
		for frag in frags:
			if frag.done:
				continue
			if sum((f.pointers[0].data_size for f in fs)) >= d_size:
				# we now have the data size that we need
				break
			if frag.pointers[0].data_offset >= p.data_offset:
				frag.done = True
				fs.append(frag)
		return fs

	def frags_accumulate_from_pointer(self, p, d_size):
		return self.frags_accumulate(p, d_size, self.frags_for_pointer(p))

	def frags_accumulate_from_pointer_till_count(self, p, d_size, count):
		frags = self.frags_accumulate(p, d_size, self.frags_for_pointer(p))
		if len(frags) > count:
			frags[-1].done = False
			return frags[0:count]
		else:
			return frags

	def frag_at_pointer(self, ptr, offset=0):
		frags = self.frags_for_pointer(ptr)
		for frag in frags:
			if frag.pointers[0].pool_index == ptr.pool_index and frag.pointers[0].data_offset == ptr.data_offset + offset:
				frag.done = True
				return frag

	def frags_from_pointer(self, ptr, count, reuse=False):
		frags = self.frags_for_pointer(ptr)
		return self.get_frags_after_count(frags, ptr.data_offset, count, reuse=reuse)

	def frags_from_pointer_equals(self, p):
		frags = self.frags_for_pointer(p)
		return self.get_frag_equal(frags, p.address)

	def frags_from_pointer_equals_counts(self, p, count):
		frags = self.frags_for_pointer(p)
		return self.get_frag_equal_counts(frags, p.address, count)

	def frags_from_pointer_equalsb(self, p):
		frags = self.frags_for_pointer(p)
		return self.get_frag_equalb(frags, p.address, len(p.data))

	def frags_from_pointer_equalsb_counts(self, p, count):
		frags = self.frags_for_pointer(p)
		return self.get_frag_equalb_counts(frags, p.address, len(p.data), count)

	def frags_for_pointer(self, p):
		return self.pools[p.pool_index].fragments

	def assign_frag_names(self):
		# for debugging only:
		for sized_str_entry in self.sized_str_entries:
			try:
				for frag in sized_str_entry.fragments:
					frag.name = sized_str_entry.name
			except BaseException as err:
				logging.error(f"Assigning frag names failed for {sized_str_entry.name}")
				logging.error(sized_str_entry.fragments)
				traceback.print_exc()

	def map_buffers(self):
		"""Map buffers to data entries"""
		logging.info("Mapping buffers")
		# print(self.data_entries)
		# print(self.buffer_entries)
		# print(self.buffer_groups)
		if is_pz16(self.ovl) or is_jwe2(self.ovl):
			for data in self.data_entries:
				data.buffers = []
			logging.debug("Assigning buffer indices")
			for b_group in self.buffer_groups:
				b_group.ext = self.ovl.mimes[b_group.ext_index].ext
				# logging.debug(f"Buffer group {b_group.ext}, index {b_group.buffer_index}")
				# print(b_group)
				# print(b_group.buffer_count, b_group.data_count)
				# note that datas can be bigger than buffers
				buffers = self.buffer_entries[b_group.buffer_offset: b_group.buffer_offset + b_group.buffer_count]
				datas = self.data_entries[b_group.data_offset: b_group.data_offset + b_group.data_count]
				for buffer in buffers:
					buffer.index = b_group.buffer_index
					# logging.debug(f"Buffer hash {buffer.file_hash}")
					for data in datas:
						if buffer.file_hash == data.file_hash:
							buffer.name = data.name
							buffer.ext = data.ext
							data.buffers.append(buffer)
							# logging.debug(f"Buffer group match {buffer.name}")
							break
					else:
						raise BufferError(
							f"Buffer group {b_group.ext}, index {b_group.buffer_index} did not find a data entry for buffer {buffer.file_hash}")
		else:
			# sequentially attach buffers to data entries by each entry's buffer count
			buff_ind = 0
			for i, data in enumerate(self.data_entries):
				data.buffers = []
				for j in range(data.buffer_count):
					# print("data",i,"buffer",j, "buff_ind",buff_ind)
					buffer = self.buffer_entries[buff_ind]
					buffer.name = data.name
					buffer.ext = data.ext
					data.buffers.append(buffer)
					buff_ind += 1

	@property
	def buffers_io_order(self):
		"""sort buffers into load order"""
		if is_pz16(self.ovl) or is_jwe2(self.ovl):
			return self.buffer_entries
		else:
			# this holds the buffers in the order they are read from the file
			io_order = []
			# only do this if there are any data entries so that max() doesn't choke
			if self.data_entries:
				# check how many buffers occur at max in one data block
				max_buffers_per_data = max([data.buffer_count for data in self.data_entries])
				# first read the first buffer for every file
				# then the second if it has any
				# and so on, until there is no data entry left with unprocessed buffers
				for i in range(max_buffers_per_data):
					for j, data in enumerate(self.data_entries):
						if i < data.buffer_count:
							io_order.append(data.buffers[i])
			return io_order

	def read_buffer_datas(self, stream):
		# finally, we have the buffers in the correct sorting so we can read their contents
		logging.info("Reading from buffers")
		for buffer in self.buffers_io_order:
			# read buffer data and store it in buffer object
			buffer.read_data(stream)

	def dump_pools(self):
		"""for debugging"""
		logging.info(f"Dumping pools to {self.ovl.dir}")
		for i, pool in enumerate(self.pools):
			pool_path = os.path.join(self.ovl.dir, f"{self.ovl.basename}_{self.arg.name}_pool[{i}].dmp")
			with open(pool_path, "wb") as f:
				f.write(pool.data.getvalue())

	def dump_buffer_groups_log(self):
		buff_log_path = os.path.join(self.ovl.dir, f"{self.ovl.basename}_{self.arg.name}_buffers.log")
		logging.info(f"Dumping buffer log to {buff_log_path}")
		with open(buff_log_path, "w") as f:
			for x, buffer_group in enumerate(self.buffer_groups):
				f.write(
					f"\n{buffer_group.ext} {buffer_group.buffer_offset} {buffer_group.buffer_count} {buffer_group.buffer_index} | {buffer_group.size} {buffer_group.data_offset} {buffer_group.data_count} ")

	@staticmethod
	def get_ptr_debug_str(entry):
		# d_str = ""
		# if len(entry.pointers) == 2:
		#     d_str = str(entry.pointers[1].data)
		ptr_str = ' '.join((f'[{p.pool_index} {p.data_offset} | {p.data_size} ({len(p.padding)})]' for p in entry.pointers))
		if isinstance(entry, Fragment):
			p0, p1 = entry.pointers
			ptr_str = f"@ {p0.pool_index} {p0.data_offset} -> [{p1.pool_index} {p1.data_offset} | {p1.data_size} ({len(p1.padding)})]"\

		infix = ""
		if isinstance(entry, DependencyEntry):
			infix = "->"
		return f"{ptr_str} {infix} {entry.name}"

	def dump_frag_log(self):
		"""for development; collect info about fragment types"""
		frag_log_path = os.path.join(self.ovl.dir, f"{self.ovl.basename}_{self.arg.name}.log")
		logging.info(f"Dumping fragment log to {frag_log_path}")
		with open(frag_log_path, "w") as f:
			f.write(f"Overview\n")
			for i, pool in enumerate(self.pools):
				f.write(f"Pool[{i}] (type: {pool.type}) {pool.name}\n")
			for i, pool in enumerate(self.pools):
				f.write(f"\n\nPool[{i}] (type: {pool.type}) size: {pool.size} at {pool.offset} with {len(pool.fragments)} fragments\n")
				entries = pool.fragments + [ss for ss in self.sized_str_entries if ss.pointers[0].pool_index == i] + [dep for dep in self.ovl.dependencies if dep.pointers[0].pool_index == i + self.arg.pools_offset]
				entries.sort(key=lambda entry: entry.pointers[0].data_offset)
				lines = [self.get_ptr_debug_str(entry) for entry in entries]
				f.write("\n".join(lines))

	@staticmethod
	def get_frags_after_count(frags, initpos, count, reuse=False):
		"""Returns count entries of frags that have not been processed and occur after initpos."""
		out = []
		for f in frags:
			# check length of fragment, grab good ones
			if len(out) == count:
				break
			# can't add fragments that have already been added elsewhere
			if f.done and not reuse:
				continue
			if f.pointers[0].data_offset >= initpos:
				f.done = True
				out.append(f)
				if f.done and reuse:
					logging.debug(
						f"Reusing fragment {f.pointers[0].pool_index} | {f.pointers[0].data_offset} for count {count}, initpos {initpos}")
		else:
			if len(out) != count:
				raise AttributeError(
					f"Could not find {count} fragments in {len(frags)} frags after initpos {initpos}, only found {len(out)}!")
		return out

	@staticmethod
	def get_frag_equal(frags, initpos):
		"""Get frag whose ptr 0 is at initpos."""
		out = []
		for f in frags:
			# can't add fragments that have already been added elsewhere
			if f.done:
				continue
			if f.pointers[0].address == initpos:
				f.done = True
				out.append(f)
				break
		return out

	@staticmethod
	def get_frag_equal_counts(frags, initpos, count):
		"""Returns count entries of frags that have not been processed and occur after initpos."""
		out = []
		first = 1
		for f in frags:
			if first == 1:
				if f.done:
					continue
				if f.pointers[0].address == initpos:
					f.done = True
					out.append(f)
					first = 0
			else:
				# check length of fragment, grab good ones
				if len(out) == count:
					break
				# can't add fragments that have already been added elsewhere
				if f.done:
					continue
				if f.pointers[0].address >= initpos:
					f.done = True
					out.append(f)
		return out

	@staticmethod
	def get_frag_equalb(frags, initpos, datalength):
		"""Returns count entries of frags that have not been processed and occur after initpos."""
		out = []
		for f in frags:
			# can't add fragments that have already been added elsewhere
			if f.done:
				continue
			if (f.pointers[0].address == initpos) or (f.pointers[0].address == initpos + datalength):
				f.done = True
				out.append(f)
				break
		return out

	@staticmethod
	def get_frag_equalb_counts(frags, initpos, datalength, count):
		"""Returns count entries of frags that have not been processed and occur after initpos."""
		out = []
		first = 1
		for f in frags:
			if first == 1:
				if f.done:
					continue
				if (f.pointers[0].address == initpos) or (f.pointers[0].address == initpos + datalength):
					f.done = True
					out.append(f)
					first = 0
			else:
				# check length of fragment, grab good ones
				if len(out) == count:
					break
				# can't add fragments that have already been added elsewhere
				if f.done:
					continue
				if f.pointers[0].address >= initpos:
					f.done = True
					out.append(f)
		return out

	@staticmethod
	def find_entry(entries, src_entry):
		""" returns entry from list l whose file hash matches hash, or none"""
		for entry in entries:
			if entry.name == src_entry.name:
				return entry

	def assign_name(self, entry):
		"""Fetch a filename for an entry"""
		# JWE style
		if self.ovl.user_version.is_jwe:
			try:
				n = self.ovl.hash_table_local[entry.file_hash]
				e = self.ovl.hash_table_local[entry.ext_hash]
			except KeyError:
				raise KeyError(f"No match for entry!\n{entry}")
		# PZ Style and PC Style
		else:
			# file_hash is an index into ovl files
			try:
				file = self.ovl.files[entry.file_hash]
			except IndexError:
				raise IndexError(
					f"Entry ID {entry.file_hash} does not index into ovl file table of length {len(self.ovl.files)}")
			n = file.basename
			e = file.ext
		# fix for island.island, force extension to start with .
		if e[0] != ".":
			e = f".{e}"
		entry.ext = e
		entry.basename = n
		entry.name = f"{n}{e}"

	def calc_uncompressed_size(self, ):
		"""Calculate the size of the whole decompressed stream for this archive"""
		return self.start_of_pools + sum(pool.size for pool in self.pools) + sum(
			buffer.size for buffer in self.buffer_entries)

	def write_pools(self):
		logging.debug(f"Writing pools for {self.arg.name}")
		# do this first so pools can be updated
		pools_data_writer = io.BytesIO()
		for pool in self.pools:
			pool_bytes = pool.data.getvalue()
			# JWE, JWE2: relative offset for each pool
			if self.ovl.user_version.is_jwe:
				pool.offset = pools_data_writer.tell()
			# PZ, PC: offsets relative to the whole pool block
			else:
				pool.offset = self.arg.pools_start + pools_data_writer.tell()
			logging.debug(f"pool.offset {pool.offset}, pools_start {self.arg.pools_start}")
			pool.size = len(pool_bytes)
			pools_data_writer.write(pool_bytes)
		self.pools_data = pools_data_writer.getvalue()

	def write_archive(self, stream):
		logging.info(f"Writing archive {self.arg.name}")
		# write out all entries
		super().write(stream)
		# write the header data containing all the pointers' datas
		stream.write(self.pools_data)
		# write buffer data
		for b in self.buffers_io_order:
			stream.write(b.data)


class OvlFile(Header, IoFile):

	def __init__(self, progress_callback=None):
		# create a context
		super().__init__(OvlContext())
		self.magic.data = b'FRES'
		self.hash_table_global = {}

		self.last_print = None
		if progress_callback:
			self.progress_callback = progress_callback
		else:
			self.progress_callback = self.dummy_callback

	def get_extract_files(self, only_names, only_types, skip_files, ignore=True):
		"""Returns files that are suitable for extraction"""
		extract_files = []
		for file in self.files:
			# for batch operations, only export those that we need
			if only_types and file.ext not in only_types:
				skip_files.append(file.name)
				continue
			if only_names and file.name not in only_names:
				skip_files.append(file.name)
				continue
			# ignore types in the count that we export from inside other type exporters
			if ignore and file.ext in IGNORE_TYPES:
				continue
			extract_files.append(file)
		return extract_files

	def get_loaders(self):
		"""Returns all loader instances for this ovl"""
		return [file.loader for file in self.files if hasattr(file, 'loader') and file.loader is not None]

	def rename(self, name_tups, animal_mode=False):
		logging.info(f"Renaming for {name_tups}, animal mode = {animal_mode}")
		lists = [self.files, self.dependencies, self.included_ovls]
		for archive in self.archives:
			ovs = archive.content
			lists.extend((
				ovs.data_entries,
				ovs.buffer_entries,
				ovs.set_header.sets,
				ovs.set_header.assets,
				ovs.pools,
				ovs.sized_str_entries
			))
		for entry_list in lists:
			for entry in entry_list:
				if animal_mode and entry.ext not in (".ms2", ".mdl2", ".motiongraph"):
					continue
				rename_entry(entry, name_tups)
		self.update_hashes()
		self.update_ss_dict()
		logging.info("Finished renaming!")

	def get_children(self, file_entry):
		children_names = []
		ss_entry = self.get_sized_str_entry(file_entry.name)
		children_names.extend([ss.name for ss in ss_entry.children])
		children_names.extend([stream.name for stream in file_entry.streams])
		return children_names

	def rename_contents(self, name_tups):
		logging.info(f"Renaming contents for {name_tups}")
		name_tuple_bytes = [(o.encode(), n.encode()) for o, n in name_tups]
		for loader in self.get_loaders():
			loader.rename_content(name_tups)
		# old style
		# hash all the pools
		for pool in self.pools:
			pool.data = BinaryStream(replace_bytes(pool.data.getvalue(), name_tuple_bytes))
		logging.info("Finished renaming contents!")

	def extract(self, out_dir, only_names=(), only_types=(), show_temp_files=False):
		"""Extract the files, after all archives have been read"""
		# create output dir
		logging.info(f"Extracting from {len(self.files)} files")
		os.makedirs(out_dir, exist_ok=True)

		def out_dir_func(n):
			"""Helper function to generate temporary output file name"""
			return os.path.normpath(os.path.join(out_dir, n))

		# the actual export, per file type
		error_files = []
		skip_files = []
		out_paths = []
		extract_files = self.get_extract_files(only_names, only_types, skip_files)
		for file_index, file in enumerate(extract_files):
			self.progress_callback("Extracting", value=file_index, vmax=len(extract_files))
			try:
				out_paths.extend(file.loader.extract(out_dir_func, show_temp_files, self.progress_callback))
			except BaseException as error:
				logging.error(f"An exception occurred while extracting {file.name}")
				logging.error(error)
				traceback.print_exc()
				error_files.append(file.name)

		self.progress_callback("Extraction completed!", value=1, vmax=1)
		return out_paths, error_files, skip_files

	def preprocess_files(self, file_paths, tmp_dir):
		"""Check the files that should be injected and piece them back together"""
		# only import locally to avoid dependency on imageio for plugin
		# logging.debug(f"file_paths {file_paths}")
		from ovl_util import imarray
		out_file_paths = set()
		for file_path in file_paths:
			name_ext, name, ext = split_path(file_path)
			if ext == ".png":
				imarray.inject_wrapper(file_path, out_file_paths, tmp_dir)
			else:
				out_file_paths.add(file_path)
		# logging.debug(f"out_file_paths {out_file_paths}")
		return out_file_paths

	def inject(self, file_paths, show_temp_files):
		"""Inject files into archive"""
		logging.info(f"Injecting {len(file_paths)} files")
		tmp_dir = tempfile.mkdtemp("-cobra-tools")
		error_files = []
		foreign_files = []
		# key with name+ext
		_files_dict = {file.name.lower(): file for file in self.files}
		# handle dupes and piece separated files back together
		file_paths = self.preprocess_files(file_paths, tmp_dir)
		for file_index, file_path in enumerate(file_paths):
			self.progress_callback("Injecting", value=file_index, vmax=len(file_paths))
			name_ext, name, ext = split_path(file_path)
			name_lower = name_ext.lower()
			if ext in aliases:
				name_lower = name_lower.replace(ext, aliases[ext])
			# check if this file exists in this ovl
			if name_lower in _files_dict:
				file = _files_dict[name_lower]
			else:
				foreign_files.append(file_path)
				continue
			try:
				file.loader.load(file_path)
			except BaseException as error:
				logging.error(f"An exception occurred while injecting {name_ext}")
				logging.error(error)
				traceback.print_exc()
				error_files.append(name_ext)
		for pool in self.pools:
			# if the pool has editable pointers, flush them to the pool writer first
			pool.flush_pointers()
		shutil.rmtree(tmp_dir)
		self.progress_callback("Injection completed!", value=1, vmax=1)
		return error_files, foreign_files

	def create_file_entry(self, file_path):
		"""Create a file entry from a file path"""
		# capital letters in the name buffer crash JWE2, apparently
		file_path = file_path.lower()
		filename = os.path.basename(file_path)
		logging.info(f"Creating {filename}")
		file_entry = FileEntry(self.context)
		file_entry.path = file_path
		file_entry.name = filename
		file_entry.basename, file_entry.ext = os.path.splitext(filename)
		file_entry.dependencies = []
		file_entry.aux_entries = []
		file_entry.streams = []
		try:
			file_entry.update_constants(self)
			return file_entry
		except KeyError:
			logging.warning(f"Unsupported file type: {filename}")
			return

	def create_file(self, file_path):
		"""Register a file entry from a file path, add a loader"""
		file_entry = self.create_file_entry(file_path)
		if not file_entry:
			return
		file_entry.loader = get_loader(file_entry.ext, self, file_entry)
		if not file_entry.loader:
			return
		try:
			file_entry.loader.create()
		except NotImplementedError:
			logging.warning(f"Creation not implemented for {file_entry.ext}")
			return
		except BaseException as err:
			logging.warning(f"Could not create: {file_entry.name}")
			traceback.print_exc()
			return
		self.files.append(file_entry)

	def create(self, ovl_dir):
		logging.info(f"Creating OVL from {ovl_dir}")
		file_paths = [os.path.join(ovl_dir, file_name) for file_name in os.listdir(ovl_dir)]
		self.add_files(file_paths)
		self.load_included_ovls(os.path.join(ovl_dir, "ovls.include"))

	def add_files(self, file_paths):
		logging.info(f"Adding {len(file_paths)} files to OVL")
		logging.info(f"Game: {get_game(self)}")
		for file_path in file_paths:
			self.create_file(file_path)
		self.update_hashes()
		self.update_counts()
		self.postprocessing()

	def create_archive(self, name="STATIC"):
		# logging.debug(f"Getting archive '{name}'")
		# see if it exists
		for archive in self.archives:
			if archive.name == name:
				return archive.content
		# nope, gotta create it
		logging.debug(f"Creating archive '{name}'")
		archive = ArchiveEntry(self.context)
		self.archives.append(archive)
		if name == "STATIC":
			self.static_archive = archive
		archive.name = name
		content = OvsFile(self.context, self, archive)
		archive.content = content
		new_zlib = ZlibInfo(self.context)
		self.zlibs.append(new_zlib)
		return content

	# dummy (black hole) callback for if we decide we don't want one
	def dummy_callback(self, *args, **kwargs):
		return

	def print_and_callback(self, message, value=None, max_value=None):
		# don't print the message if it is identical to the last one - it
		# will slow down massively repetitive tasks
		if self.last_print != message:
			logging.info(message)
			self.last_print = message

		# call the callback
		self.progress_callback(message, value, max_value)

	def store_filepath(self, filepath):
		# store file name for later
		self.filepath = filepath
		self.dir, self.basename = os.path.split(filepath)
		self.file_no_ext = os.path.splitext(self.filepath)[0]

	@property
	def included_ovl_names(self):
		return [included_ovl.name for included_ovl in self.included_ovls]

	# @included_ovl_names.setter
	def set_included_ovl_names(self, ovl_names):
		# remove duplicates
		ovl_names = set(ovl_names)
		logging.debug(f"Setting {len(ovl_names)} included OVLs")
		self.included_ovls.clear()
		for ovl_name in ovl_names:
			ovl_name = ovl_name.strip()
			if not ovl_name.lower().endswith(".ovl"):
				ovl_name += ".ovl"
			included_ovl = IncludedOvl(self.context)
			included_ovl.name = ovl_name
			included_ovl.basename, included_ovl.ext = os.path.splitext(included_ovl.name)
			logging.debug(f"Including {included_ovl.name}")
			self.included_ovls.append(included_ovl)

	def load_included_ovls(self, path):
		if os.path.isfile(path):
			with open(path) as f:
				self.set_included_ovl_names(f.readlines())

	def save_included_ovls(self, path):
		with open(path, "w") as f:
			# f.writelines(self.included_ovl_names)
			for ovl_name in self.included_ovl_names:
				f.write(f"{ovl_name}\n")

	def add_included_ovl(self, included_ovl_name):
		if not included_ovl_name.lower().endswith(".ovl"):
			included_ovl_name += ".ovl"
		included_ovl_basename, ext = os.path.splitext(included_ovl_name)
		# validate can't insert same included ovl twice
		if included_ovl_name in self.included_ovl_names:
			return

		# store file name
		included_ovl = IncludedOvl(self.context)
		included_ovl.name = included_ovl_name
		included_ovl.basename = included_ovl_basename
		included_ovl.ext = ext
		self.included_ovls.append(included_ovl)

	def remove_included_ovl(self, included_ovl_name):
		for included_ovl in self.included_ovls:
			if included_ovl.name == included_ovl_name:
				self.included_ovls.remove(included_ovl)

	def rename_included_ovl(self, included_ovl_name, included_ovl_name_new):
		# find an existing entry in the list
		for included_ovl in self.included_ovls:
			if included_ovl.name == included_ovl_name:
				included_ovl.name = included_ovl_name_new
				included_ovl.basename = included_ovl_name_new

	def update_names(self):
		"""Update the name buffers with names from list entries, and update the name offsets on those entries"""
		# update ext dependencies with : prefix instead of .
		for dependency in self.dependencies:
			dependency.ext = dependency.ext.replace(".", ":")
		# regenerate the name buffer
		self.names.update_with((
			(self.dependencies, "ext"),
			(self.included_ovls, "basename"),
			(self.mimes, "name"),
			(self.files, "basename")
		))
		self.archive_names.update_with((
			(self.archives, "name"),
		))
		self.len_names = len(self.names.data)
		self.len_archive_names = len(self.archive_names.data)

		# catching ovl files without entries, default len_type_names is 0
		if self.files:
			self.len_type_names = min(file.offset for file in self.files)
		else:
			self.len_type_names = 0

	def load_hash_table(self):
		logging.info("Loading hash table...")
		start_time = time.time()
		self.hash_table_global = {}
		hashes_dir = os.path.join(os.getcwd(), "hashes")
		try:
			for file in os.listdir(hashes_dir):
				fp = os.path.join(hashes_dir, file)
				if fp.endswith(".txt"):
					with open(fp, "r") as f:
						for line in f:
							line = line.strip()
							if line:
								k, v = line.split(" = ")
								self.hash_table_global[int(k)] = v
		except:
			pass
		logging.info(
			f"Loaded {len(self.hash_table_global)} hash - name pairs in {time.time() - start_time:.2f} seconds.")

	def load(self, filepath, commands=()):
		start_time = time.time()
		# store commands
		self.commands = commands
		self.store_filepath(filepath)
		logging.info(f"Loading {self.basename}")
		self.eof = super().load(filepath)
		logging.info(f"Game: {get_game(self)}")

		# maps djb hash to string
		self.hash_table_local = {}
		# print(self)
		# add extensions to hash dict
		hm_max = len(self.mimes)
		for hm_index, mime_entry in enumerate(self.mimes):
			self.print_and_callback("Loading extensions", value=hm_index, max_value=hm_max)
			# get the whole mime type string
			mime_entry.name = self.names.get_str_at(mime_entry.offset)
			# only get the extension
			mime_entry.ext = f".{mime_entry.name.split(':')[-1]}"
			# the stored mime hash is not used anywhere
			# self.hash_table_local[mime_entry.mime_hash] = mime_type
			# instead we must calculate the DJB hash of the extension and store that
			# because this is how we find the extension from inside the archive
			self.hash_table_local[djb(mime_entry.ext[1:])] = mime_entry.ext
			mime_entry.triplets = self.triplets[
								  mime_entry.triplet_offset: mime_entry.triplet_offset + mime_entry.triplet_count]

		# add file name to hash dict; ignoring the extension pointer
		hf_max = len(self.files)
		for hf_index, file_entry in enumerate(self.files):
			self.print_and_callback("Loading files", value=hf_index, max_value=hf_max)
			# get file name from name table
			file_name = self.names.get_str_at(file_entry.offset)
			file_entry.ext = self.mimes[file_entry.extension].ext
			# store this so we can use it
			file_entry.ext_hash = djb(file_entry.ext[1:])
			file_entry.basename = file_name
			file_entry.name = file_name + file_entry.ext
			file_entry.dependencies = []
			file_entry.aux_entries = []
			self.hash_table_local[file_entry.file_hash] = file_name
		if "generate_hash_table" in self.commands:
			return self.hash_table_local

		# get included ovls
		hd_max = len(self.included_ovls)
		for hd_index, included_ovl in enumerate(self.included_ovls):
			self.print_and_callback("Loading includes", value=hd_index, max_value=hd_max)
			included_ovl.basename = self.names.get_str_at(included_ovl.offset)
			included_ovl.ext = ".ovl"
			included_ovl.name = included_ovl.basename + included_ovl.ext

		# get names of all dependencies
		ht_max = len(self.dependencies)
		for ht_index, dependency_entry in enumerate(self.dependencies):
			self.print_and_callback("Loading dependencies", value=ht_index, max_value=ht_max)
			file_entry = self.files[dependency_entry.file_index]
			file_entry.dependencies.append(dependency_entry)
			# nb: these use : instead of . at the start, eg. :tex
			dependency_entry.ext = self.names.get_str_at(dependency_entry.offset)
			h = dependency_entry.file_hash
			if h in self.hash_table_local:
				dependency_entry.basename = self.hash_table_local[h]
			# logging.debug(f"LOCAL: {h} -> {dependency_entry.basename}")
			elif h in self.hash_table_global:
				dependency_entry.basename = self.hash_table_global[h]
			# logging.debug(f"GLOBAL: {h} -> {dependency_entry.basename}")
			else:
				logging.warning(f"Unresolved dependency [{h}] for {file_entry.name}")
				dependency_entry.basename = "bad hash"

			dependency_entry.name = dependency_entry.basename + dependency_entry.ext.replace(":", ".")
		# sort dependencies by their pool offset
		for file_entry in self.files:
			file_entry.dependencies.sort(key=lambda entry: entry.pointers[0].data_offset)

		for aux_entry in self.aux_entries:
			file_entry = self.files[aux_entry.file_index]
			file_entry.aux_entries.append(aux_entry)

		self.static_archive = None
		for archive_entry in self.archives:
			archive_entry.name = self.archive_names.get_str_at(archive_entry.offset)
		self.load_archives()
		# self.debug_unks()
		logging.info(f"Loaded OVL in {time.time() - start_time:.2f} seconds!")

	def update_mimes(self):
		"""Rebuilds the mimes list according to the ovl's current file entries"""
		logging.info("Updating mimes and triplets")
		self.mimes.clear()
		self.triplets.clear()
		# map all files by their extension
		files_by_extension = {}
		for file in self.files:
			if file.ext not in files_by_extension:
				files_by_extension[file.ext] = []
			files_by_extension[file.ext].append(file)

		# now create the mimes
		file_index_offset = 0
		for file_ext, files in sorted(files_by_extension.items()):
			mime_entry = MimeEntry(self.context)
			mime_entry.ext = file_ext
			try:
				mime_entry.update_constants(self)
			except KeyError:
				logging.warning(f"Unsupported extension {file_ext}")
				continue
			mime_entry.file_index_offset = file_index_offset
			mime_entry.file_count = len(files)
			file_index_offset += len(files)
			for file_entry in files:
				file_entry.update_constants(self)
				file_entry.extension = len(self.mimes)
			self.mimes.append(mime_entry)
		self.num_mimes = len(self.mimes)
		self.num_triplets = len(self.triplets)

	def load_archives(self):
		logging.info("Loading archives")
		start_time = time.time()
		self.open_ovs_streams(mode="rb")
		for archive_index, archive_entry in enumerate(self.archives):
			self.print_and_callback(f"Reading archive {archive_entry.name}", value=archive_index,
									max_value=len(self.archives))
			# those point to external ovs archives
			if archive_entry.name == "STATIC":
				read_start = self.eof
			else:
				read_start = archive_entry.read_start
			archive_entry.content = OvsFile(self.context, self, archive_entry)
			try:
				archive_entry.content.unzip(archive_entry, read_start)
			except BaseException as err:
				logging.error(f"Unzipping of {archive_entry.name} from {archive_entry.ovs_path} failed")
				logging.error(err)
				traceback.print_exc()
				print(archive_entry)
				print(archive_entry.content)
				break
		self.close_ovs_streams()
		self.postprocessing()
		logging.info(f"Loaded Archives in {time.time() - start_time:.2f} seconds!")

	def postprocessing(self):
		self.update_ss_dict()
		self.link_streams()
		self.load_flattened_pools()
		self.load_pointers()
		self.load_file_classes()

	def load_flattened_pools(self):
		"""Create flattened list of pools"""
		self.pools = [None for _ in range(self.num_pools)]
		for archive in self.archives:
			if archive.num_pools:
				self.pools[archive.pools_offset: archive.pools_offset + archive.num_pools] = archive.content.pools

	def load_pointers(self):
		"""Handle all pointers of this file, including dependencies, fragments and ss entries"""
		logging.info("Loading pointers")
		# reset pointer map for each header entry
		for pool in self.pools:
			pool.pointer_map = {}
			pool.new = False
			# store fragments per header for faster lookup
			pool.fragments = []
			# pool.dependencies = []
			# pool.ss_entries = []
		logging.debug("Linking pointers to pools")
		for dep in self.dependencies:
			# the index goes into the flattened list of pools
			dep.pointers[0].link_to_pool(self.pools)
		for archive in self.archives:
			ovs = archive.content
			# sort fragments by their first pointer
			ovs.fragments.sort(key=lambda f: (f.pointers[0].pool_index, f.pointers[0].data_offset))
			# attach all pointers to their pool
			# however we no longer break up at fragments' ptr 0
			for entry in ovs.fragments:
				entry.pointers[0].link_to_pool(ovs.pools, is_ref_ptr=False)
				entry.pointers[1].link_to_pool(ovs.pools)
			for entry in ovs.sized_str_entries:
				entry.pointers[0].link_to_pool(ovs.pools)
			for i, frag in enumerate(ovs.fragments):
				# we assign these later when the loader classes run collect()
				frag.done = False
				frag.name = None
				ptr = frag.pointers[0]
				try:
					ptr.pool.fragments.append(frag)
				except:
					logging.warning(f"frag {i} failed")
		logging.debug("Calculating pointer sizes")
		for pool in self.pools:
			pool.calc_pointer_sizes()

	def load_file_classes(self):
		logging.info("Loading file classes")
		for file in self.files:
			file.loader = get_loader(file.ext, self, file)
			if file.loader:
				try:
					file.loader.collect()
				except Exception as err:
					logging.error(err)
					traceback.print_exc()

	def get_sized_str_entry(self, name):
		"""Retrieves the desired ss entry"""
		if name.lower() in self._ss_dict:
			return self._ss_dict[name.lower()][0]
		else:
			for archive_entry in self.archives:
				for file in archive_entry.content.sized_str_entries:
					print(file.name.lower())
			raise KeyError(f"Can't find a sizedstr entry for {name}, not from this archive?")

	def update_ss_dict(self):
		"""Stores a reference to each sizedstring entry in a dict so they can be extracted"""
		logging.info("Updating the entry dict")
		self._ss_dict = {}
		for archive in self.archives:
			for file in archive.content.sized_str_entries:
				self._ss_dict[file.name.lower()] = file, archive

	def link_streams(self):
		"""Attach the data buffers of streamed files to standard files from the first archive"""
		logging.info("Linking streams")

		file_lut = {file.name: file for file in self.files}
		for file in self.files:
			file.streams = []
			if file.ext == ".tex":
				for lod_i in range(3):
					stream_file = file_lut.get(f"{file.basename}_lod{lod_i}.texturestream", None)
					if stream_file:
						file.streams.append(stream_file)
			elif file.ext == ".ms2":
				for lod_i in range(4):
					stream_file = file_lut.get(f"{file.basename[:-1]}{lod_i}.model2stream", None)
					if stream_file:
						file.streams.append(stream_file)

	def get_ovs_path(self, archive_entry):
		if archive_entry.name == "STATIC":
			self.static_archive = archive_entry
			archive_entry.ovs_path = self.filepath
		else:
			# JWE style
			if is_jwe(self) or is_jwe2(self):
				archive_entry.ovs_path = f"{self.file_no_ext}.ovs.{archive_entry.name.lower()}"
			# PZ, PC, ZTUAC Style
			else:
				archive_entry.ovs_path = f"{self.file_no_ext}.ovs"

	def update_hashes(self):
		"""Call this if any file names have changed and hashes or indices have to be recomputed"""
		# rebuild the dependencies list
		self.dependencies.clear()
		self.aux_entries.clear()
		# update file hashes
		for file in self.files:
			file.file_hash = djb(file.basename)
			file.ext_hash = djb(file.ext[1:])
			# logging.debug(f"File: {file.name} {file.file_hash} {file.ext_hash}")
			# update dependency hashes
			for dependency in file.dependencies:
				if dependency.basename == "bad hash":
					logging.warning(f"Bad hash on dependency entry - won't update hash")
				else:
					dependency.file_hash = djb(dependency.basename)
			self.dependencies.extend(file.dependencies)
			self.aux_entries.extend(file.aux_entries)

		# sort the different lists according to the criteria specified
		self.files.sort(key=lambda x: (x.ext, x.file_hash))
		self.dependencies.sort(key=lambda x: x.file_hash)
		self.aux_entries.sort(key=lambda x: x.file_hash)
		self.num_dependencies = len(self.dependencies)
		self.num_aux_entries = len(self.aux_entries)

		# build a lookup table mapping file name to its index
		file_name_lut = {file.name: file_i for file_i, file in enumerate(self.files)}
		# update the file indices
		for file in self.files:
			for entry in file.dependencies + file.aux_entries:
				entry.file_index = file_name_lut[file.name]

		for archive in self.archives:
			# change the hashes / indices of all entries to be valid for the current game version
			archive.content.update_hashes(file_name_lut)

	def sort_pools_and_update_groups(self):
		logging.debug(f"Sorting pools by type and updating pool groups")
		for archive in self.archives:

			logging.debug(f"Sorting pools for {archive.name}")
			ovs = archive.content
			ovs.pools.sort(key=lambda pool: pool.type)

			pools_lut = {pool: pool_i for pool_i, pool in enumerate(ovs.pools)}
			for entry in itertools.chain(ovs.fragments, ovs.sized_str_entries):
				for pointer in entry.pointers:
					# the index goes into the ovs file's pools
					pointer.update_pool_index(pools_lut)

			# map the pool types to pools
			pools_by_type = {}
			for pool in ovs.pools:
				if pool.type not in pools_by_type:
					pools_by_type[pool.type] = []
				pools_by_type[pool.type].append(pool)

			# rebuild pool groups
			ovs.pool_groups.clear()
			for pool_type, pools in pools_by_type.items():
				pool_group = PoolGroup(self.context)
				pool_group.type = pool_type
				pool_group.num_pools = len(pools)
				ovs.pool_groups.append(pool_group)

			# update the counts
			archive.num_pool_groups = len(ovs.pool_groups)
			archive.num_pools = len(ovs.pools)

		# update the flattened list of pools
		self.update_pool_datas()
		self.load_flattened_pools()
		# dependencies index goes into the flattened list of pools
		pools_lut = {pool: pool_i for pool_i, pool in enumerate(self.pools)}
		for dep in self.dependencies:
			dep.pointers[0].update_pool_index(pools_lut)
		# pools are updated, gotta rebuild stream files now
		self.update_stream_files()

	def update_counts(self):
		"""Update counts of this ovl and all of its archives"""
		self.sort_pools_and_update_groups()
		# adjust the counts
		for archive in self.archives:
			archive.content.rebuild_buffer_groups()
			archive.content.update_counts()
			archive.content.rebuild_assets()
		# sum content of individual archives
		self.num_pool_groups = sum(a.num_pool_groups for a in self.archives)
		self.num_pools = sum(a.num_pools for a in self.archives)
		self.num_datas = sum(a.num_datas for a in self.archives)
		self.num_buffers = sum(a.num_buffers for a in self.archives)

		self.num_included_ovls = len(self.included_ovls)
		self.num_files = self.num_files_2 = self.num_files_3 = len(self.files)
		self.num_archives = len(self.archives)

	def open_ovs_streams(self, mode="wb"):
		logging.info("Opening OVS streams")
		self.ovs_dict = {}
		for archive_entry in self.archives:
			# gotta update it here
			self.get_ovs_path(archive_entry)
			if archive_entry.ovs_path not in self.ovs_dict:
				self.ovs_dict[archive_entry.ovs_path] = open(archive_entry.ovs_path, mode)
				# make sure that the ovs exists
				if mode == "rb" and not os.path.exists(archive_entry.ovs_path):
					raise FileNotFoundError("OVS file not found. Make sure is is here: \n" + archive_entry.ovs_path)

	def close_ovs_streams(self):
		logging.info("Closing OVS streams")
		# we don't use context manager so gotta close them
		for ovs_file in self.ovs_dict.values():
			ovs_file.close()

	def update_pool_datas(self):
		pools_byte_offset = 0
		pools_offset = 0
		for archive in self.archives:
			archive.pools_offset = pools_offset
			archive.pools_start = pools_byte_offset
			archive.content.write_pools()
			pools_byte_offset += len(archive.content.pools_data)
			archive.pools_end = pools_byte_offset
			# at least PZ & JWE require 4 additional bytes after each pool region
			pools_byte_offset += 4
			pools_offset += len(archive.content.pools)

	def _get_abs_mem_offset(self, archive, ptr):
		# JWE, JWE2: relative offset for each pool
		if self.user_version.is_jwe:
			return archive.pools_start + ptr.pool.offset + ptr.data_offset
		# PZ, PC: offsets relative to the whole pool block
		else:
			return ptr.pool.offset + ptr.data_offset

	def update_stream_files(self):
		logging.info("Updating stream file memory links")
		self.stream_files.clear()
		# ensure we have an up to date ss dict
		self.update_ss_dict()
		for file in self.files:
			if file.streams:
				file_ss, file_archive = self._ss_dict[file.name.lower()]
				for stream in file.streams:
					stream_ss, stream_archive = self._ss_dict[stream.name.lower()]
					stream_entry = StreamEntry(self.context)
					steam_ptr = stream_ss.pointers[0]
					stream_entry.stream_offset = self._get_abs_mem_offset(stream_archive, steam_ptr)
					file_ptr = file_ss.pointers[0]
					stream_entry.file_offset = self._get_abs_mem_offset(file_archive, file_ptr)
					stream_entry.archive_name = stream_archive.name
					self.stream_files.append(stream_entry)
		# sort stream files by archive and then the file offset in the pool
		self.stream_files.sort(key=lambda s: (s.archive_name, s.file_offset))
		self.num_files_ovs = len(self.stream_files)
		# update the archive entries to point to the stream files
		for archive in self.archives:
			archive.stream_files_offset = 0
			if archive.name != "STATIC":
				files = [f for f in self.stream_files if f.archive_name == archive.name]
				archive.num_files = len(files)
				if not files:
					logging.warning(f"No files in archive {archive.name}")
					continue
				archive.stream_files_offset = self.stream_files.index(files[0])

	def update_files(self):
		logging.info("Updating files")
		for file in self.files:
			if file.loader:
				file.loader.update()

	# def debug_unks(self):
	#     pool_type = set()
	#     set_pool_type = set()
	#     for file in self.files:
	#         pool_type.add(file.pool_type)
	#         set_pool_type.add(file.set_pool_type)
	#         ss = self.get_sized_str_entry(file.name)
	#         ss_ptr = ss.pointers[0]
	#         if not file.set_pool_type:
	#             if file.pool_type != ss_ptr.pool.type:
	#                 raise AttributeError(f"No match: {file.pool_type},  {ss_ptr.pool.type}")
	#             else:
	#                 pass
	#         # logging.debug(f"match: {file.pool_type},  {ss_ptr.pool.type}")
	#         else:
	#             pass
	#     logging.info(f"pool_type {pool_type}")
	#     logging.info(f"set_pool_type {set_pool_type}")
	#     logging.info(self.stream_files)

	def dump_frag_log(self):
		for archive_entry in self.archives:
			try:
				archive_entry.content.assign_frag_names()
				archive_entry.content.dump_frag_log()
				archive_entry.content.dump_buffer_groups_log()
				archive_entry.content.dump_pools()
			except BaseException as err:
				traceback.print_exc()

	def save(self, filepath, dat_path):
		self.store_filepath(filepath)
		logging.info(f"Writing {self.basename}")
		self.update_files()
		self.update_mimes()
		self.update_counts()
		# do this last so we also catch the assets & sets
		self.update_hashes()
		# update the name buffer and offsets
		self.update_names()
		self.update_aux_sizes()
		self.open_ovs_streams()
		ovl_compressed = b""
		# compress data stream
		for i, archive in enumerate(self.archives):
			# write archive into bytes IO stream
			self.progress_callback("Saving archives", value=i, vmax=len(self.archives))
			uncompressed = archive.content.get_bytes(dat_path)
			archive.uncompressed_size, archive.compressed_size, compressed = archive.content.compress(
				uncompressed)
			# update set data size
			archive.set_data_size = archive.content.set_header.io_size
			if archive.name == "STATIC":
				ovl_compressed = compressed
				archive.read_start = 0
			else:
				ovs_stream = self.ovs_dict[archive.ovs_path]
				archive.read_start = ovs_stream.tell()
				ovs_stream.write(compressed)
			# size of the archive entry = 68
			# this is true for jwe2 tylo, but not for jwe2 rex 93 and many others
			self.zlibs[i].zlib_thing_1 = 68 + archive.uncompressed_size
			# this is fairly good, doesn't work for tylo static but all others, all of jwe2 rex 93, jwe1 parrot, pz fallow deer
			self.zlibs[i].zlib_thing_2 = sum([data.size_2 for data in archive.content.data_entries])

		self.close_ovs_streams()
		eof = super().save(filepath)
		with self.writer(filepath) as stream:
			self.write(stream)
			stream.write(ovl_compressed)

	def update_aux_sizes(self):
		logging.debug("Updating AUX sizes in OVL")
		for aux in self.aux_entries:
			name = aux.file.basename
			if aux.extension_index != 0:
				bnkpath = f"{self.file_no_ext}_{name}_bnk_s.aux"
			else:
				bnkpath = f"{self.file_no_ext}_{name}_bnk_b.aux"

			# grab and update size
			if os.path.isfile(bnkpath):
				aux.size = os.path.getsize(bnkpath)


if __name__ == "__main__":
	ovl = OvlFile()
	ovl.load("C:/Users/arnfi/Desktop/Coding/ovl/OVLs/Parrot.ovl")


def rename_entry(entry, name_tups):
	if "bad hash" in entry.name:
		logging.warning(f"Skipping {entry.file_hash} because its hash could not be resolved to a name")
		return
	for old, new in name_tups:
		entry.name = entry.name.replace(old, new)
	entry.basename, entry.ext = os.path.splitext(entry.name)


def replace_bytes(b, name_tups):
	for old, new in name_tups:
		b = b.replace(old, new)
	return b
