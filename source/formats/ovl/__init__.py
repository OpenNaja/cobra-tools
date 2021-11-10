import os
import itertools
import struct
import zlib
import io
import time
import traceback
import logging
from contextlib import contextmanager

from hashes import constants_pz
from ovl_util.oodle.oodle import OodleDecompressEnum, oodle_compressor

from generated.io import IoFile, BinaryStream
from generated.formats.ovl_base.bitfield.VersionInfo import VersionInfo
from generated.formats.ovl.versions import *
from generated.formats.ovl.compound.AssetEntry import AssetEntry
from generated.formats.ovl.compound.Header import Header
from generated.formats.ovl.compound.OvsHeader import OvsHeader
from generated.formats.ovl.compound.SetEntry import SetEntry
from generated.formats.ovl.compound.ArchiveEntry import ArchiveEntry
from generated.formats.ovl.compound.DirEntry import DirEntry
from generated.formats.ovl.compound.FileEntry import FileEntry
from generated.formats.ovl.compound.MimeEntry import MimeEntry
from generated.formats.ovl.compound.BufferGroup import BufferGroup
from generated.formats.ovl.compound.Triplet import Triplet
from generated.formats.ovl.compound.ZlibInfo import ZlibInfo

from modules.formats.shared import get_versions, djb, assign_versions, get_padding

OODLE_MAGIC = (b'\x8c', b'\xcc')
REVERSED_TYPES = (
	".tex", ".texturestream", ".mdl2", ".ms2", ".lua", ".fdb", ".xmlconfig", ".fgm", ".assetpkg", ".materialcollection", ".txt")


def get_loader(ext, ovl):
	from modules.formats.ASSETPKG import AssetpkgLoader
	from modules.formats.MS2 import Ms2Loader
	from modules.formats.LUA import LuaLoader
	from modules.formats.TXT import TxtLoader
	from modules.formats.FDB import FdbLoader
	from modules.formats.USERINTERFACEICONDATA import UserinterfaceicondataLoader
	from modules.formats.ANIMALRESEARCHUNLOCKSSETTINGS import AnimalresearchunlockssettingsLoader
	from modules.formats.SPECDEF import SpecdefLoader
	from modules.formats.MATCOL import MatcolLoader
	from modules.formats.MATLAYERS import MatlayersLoader
	from modules.formats.SCALEFORMLANGUAGEDATA import ScaleformLoader
	ext_2_class = {
		".assetpkg": AssetpkgLoader,
		".ms2": Ms2Loader,
		".lua": LuaLoader,
		".txt": TxtLoader,
		".fdb": FdbLoader,
		".userinterfaceicondata": UserinterfaceicondataLoader,
		".animalresearchunlockssettings": AnimalresearchunlockssettingsLoader,
		".specdef": SpecdefLoader,
		".materialcollection": MatcolLoader,
		".dinosaurmateriallayers": MatlayersLoader,
		".scaleformlanguagedata": ScaleformLoader,
	}
	cls = ext_2_class.get(ext, None)
	if cls:
		return cls(ovl)


class OvlContext(object):
	def __init__(self):
		self.version = 0
		self.user_version = VersionInfo()

	def __repr__(self):
		return f"{self.version} | {self.user_version}"


class OvsFile(OvsHeader):

	def __init__(self, context, ovl_inst, archive_entry):
		super().__init__(context)
		# print(self.context)
		self.ovl = ovl_inst
		self.arg = archive_entry
		# this determines if fragments are written back to header datas
		self.force_update_pools = True

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
				logging.debug(f"Keeping header name {pool.name} as it has not been reverse engineered!")
				continue
			ss_map = pointers_to_ss[pool_index]
			results = tuple(sorted(ss_map.items()))
			if not results:
				logging.debug("No ss pointer found, checking frag pointers!")
				ss_map = pointers_to_ss_frag[pool_index]
				results = tuple(sorted(ss_map.items()))
				if not results:
					logging.error(f"No pointer found for header {pool_index}, error!")
					continue
			ss = results[0][1]
			logging.debug(f"Header[{pool_index}]: {pool.name} -> {ss.name}")
			self.transfer_identity(pool, ss)

	def get_bytes(self, archive_index, external_path):
		# load external uncompressed data
		if external_path and archive_index == 0:
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
		if self.ovl.user_version.use_oodle:
			logging.debug("Oodle compression")
			decompressed = oodle_compressor.decompress(compressed_bytes, len(compressed_bytes), uncompressed_size)
		elif self.ovl.user_version.use_zlib:
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
		# change to zipped format for saving of uncompressed or oodled ovls
		if not self.ovl.user_version.use_zlib:
			logging.info("HACK: setting compression to zlib")
			self.ovl.user_version.use_oodle = False
			self.ovl.user_version.use_zlib = True
		# pc/pz zlib			8340	00100000 10010100
		# pc/pz uncompressed	8212	00100000 00010100
		# pc/pz oodle			8724	00100010 00010100
		# JWE zlib				24724	01100000 10010100
		# JWE oodle (switch)	25108	01100010 00010100
		# vs = (8340, 8212, 8724, 24724, 25108)
		# for v in vs:
		# 	print(v)
		# 	print(bin(v))
		# 	print()
		if self.ovl.user_version.use_oodle:
			assert self.compression_header.startswith(OODLE_MAGIC)
			a, raw_algo = struct.unpack("BB", self.compression_header)
			algo = OodleDecompressEnum(raw_algo)
			logging.debug(f"Oodle compression {a} {raw_algo} {algo.name}")
			compressed = oodle_compressor.compress(bytes(uncompressed_bytes), algo.name)
		elif self.ovl.user_version.use_zlib:
			compressed = zlib.compress(uncompressed_bytes)
		else:
			compressed = uncompressed_bytes
		return len(uncompressed_bytes), len(compressed), compressed

	def update_hashes(self, file_name_lut):
		logging.info(f"Updating hashes for {self.arg.name}")
		logging.debug(f"Game: {get_game(self.ovl)}")
		self.header_name_finder()
		entry_lists = [
					self.pools,
					self.sized_str_entries,
					self.data_entries,
					self.set_header.sets,
					self.set_header.assets]
		if is_pz16(self.ovl) or is_jwe2(self.ovl):
			entry_lists.append(self.buffer_entries)
		for entry_list in entry_lists:
			for entry in entry_list:
				file_index = file_name_lut[entry.name]
				file = self.ovl.files[file_index]
				if self.ovl.user_version.is_jwe:
					entry.file_hash = file.file_hash
				else:
					entry.file_hash = file_index
				entry.ext_hash = file.ext_hash

	# these seem to be sorted, but they are indexed into by other lists so gotta be careful when sorting them
	# self.sized_str_entries.sort(key=lambda x: x.file_hash)

	def update_counts(self):
		"""Update counts of this archive"""
		# adjust the counts
		self.arg.num_pools = len(self.pools)
		self.arg.num_datas = len(self.data_entries)
		self.arg.num_pool_types = len(self.pool_types)
		self.arg.num_buffers = len(self.buffer_entries)
		self.arg.num_fragments = len(self.fragments)
		self.arg.num_files = len(self.sized_str_entries)
		self.arg.num_new = len(self.new_entries)

	def unzip(self, archive_entry, start):
		filepath = archive_entry.ovs_path
		save_temp_dat = f"{filepath}_{self.arg.name}.dat" if "write_dat" in self.ovl.commands else ""
		stream = self.ovl.ovs_dict[filepath]
		stream.seek(start)
		logging.debug(f"Compressed stream in {os.path.basename(filepath)} starts at {stream.tell()}")
		compressed_bytes = stream.read(archive_entry.compressed_size)
		with self.unzipper(compressed_bytes, archive_entry.uncompressed_size, save_temp_dat=save_temp_dat) as stream:
			logging.debug("Reading unzipped stream...")
			assign_versions(stream, get_versions(self.ovl))
			super().read(stream)
			# print(self)
			# print(self.new_entries)
			pool_index = 0
			for pool_type in self.pool_types:
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
				sized_str_entry.model_data_frags = []
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

	def link_ptrs_to_pools(self):
		logging.debug("Linking pointers to pools")
		# append all valid pointers to their respective dicts
		for entry in itertools.chain(self.fragments, self.sized_str_entries):
			for pointer in entry.pointers:
				pointer.link_to_pool(self.pools)

	def resolve_pointers(self):
		"""Handle all of the pointer logic that goes beyond loading the pools"""
		self.build_frag_lut()
		self.map_frags()

	def read_pools(self, stream):
		for pool in self.pools:
			pool.address = stream.tell()
			pool.data = BinaryStream(stream.read(pool.size))
			assign_versions(pool.data, get_versions(self.ovl))

	def build_frag_lut(self):
		"""Create a lookup table for fragments"""
		logging.info("Building frag lookup table")

		# first sort fragments by their first pointer
		self.fragments.sort(key=lambda f: (f.pointers[0].pool_index, f.pointers[0].data_offset))
		# create a lut per pool
		for pool in self.pools:
			pool.frag_lut = {}
			# store fragments per header for faster lookup
			pool.fragments = []
		# link into flattened list of fragments
		for frag_i, frag in enumerate(self.fragments):
			# we assign these later during map_frags or when the loader classes run collect()
			frag.done = False
			frag.name = None
			ptr = frag.pointers[0]
			pool = self.pools[ptr.pool_index]
			pool.fragments.append(frag)
			pool.frag_lut[ptr.data_offset] = frag_i

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
		self.new_entries.clear()
		if (is_pz16(self.ovl) or is_jwe2(self.ovl)) and len(self.data_entries) > 0:
			# sort the buffers to be what 1.6 needs
			for data_entry in self.data_entries:
				for buffer in data_entry.buffers:
					self.transfer_identity(buffer, data_entry)
			# cobra < 20 used buffer index per data entry
			self.buffer_entries.sort(key=lambda b: (b.ext, b.index))

			# print("AYAYA\n", self.data_entries, "AYAYA\n", self.buffer_entries)
			# generate a mime lut to know the index of the mimes
			mime_lut = {mime.ext: i for i, mime in enumerate(self.ovl.mimes)}
			# generate the buffergroup entries

			last_ext = None
			last_index = None
			new_entry = None
			buffer_offset = 0
			data_offset = 0
			for i, buffer in enumerate(self.buffer_entries):
				logging.debug(f"Buffer {i}, last: {last_ext} this: {buffer.ext}")
				# we have to create a new group
				if buffer.ext != last_ext or buffer.index != last_index:
					# if we already have a new_entry declared, update offsets for the next one
					# if new_entry:
					# 	logging.debug(f"Updating offsets {buffer_offset}, {data_offset}")
					# 	buffer_offset += new_entry.buffer_count
					# 	# only change data offset if ext changes
					# 	if buffer.ext != last_ext:
					# 		data_offset += new_entry.data_count
					# now create the new new_entry and update its initial data
					new_entry = BufferGroup(self.context)
					new_entry.ext = buffer.ext
					new_entry.ext_index = mime_lut.get(buffer.ext)
					new_entry.buffer_index = buffer.index
					new_entry.buffer_offset = buffer_offset
					new_entry.data_offset = data_offset
					self.new_entries.append(new_entry)
				# gotta add this buffer to the current group
				new_entry.buffer_count += 1
				new_entry.size += buffer.size
				new_entry.data_count += 1
				# change buffer identity for next loop
				last_ext = buffer.ext
				last_index = buffer.index

			# fix the offsets of the buffergroups
			for x, new_entry in enumerate(self.new_entries):
				if x > 0:
					new_entry.buffer_offset = self.new_entries[x - 1].buffer_offset + self.new_entries[
						x - 1].buffer_count
					if new_entry.ext != self.new_entries[x - 1].ext:
						new_entry.data_offset = self.new_entries[x - 1].data_offset + self.new_entries[x - 1].data_count
					else:
						new_entry.data_offset = self.new_entries[x - 1].data_offset
						if new_entry.data_count < self.new_entries[x - 1].data_count:
							new_entry.data_count = self.new_entries[x - 1].data_count
			# tex buffergroups sometimes are 0,1 instead of 1,2 so the offsets need additional correction
			tex_fixa = 0
			tex_fixb = 0
			tex_fixc = 0
			for new_entry in self.new_entries:
				if ".tex" == new_entry.ext:
					if new_entry.buffer_count > tex_fixb:
						tex_fixb = new_entry.buffer_count
					if new_entry.data_offset > tex_fixa:
						tex_fixa = new_entry.data_offset
				elif ".texturestream" == new_entry.ext:
					tex_fixc += new_entry.buffer_count
			for new_entry in self.new_entries:
				if ".tex" == new_entry.ext:
					new_entry.data_offset = tex_fixa
					new_entry.data_count = tex_fixb
				elif ".texturestream" == new_entry.ext:
					new_entry.data_count = tex_fixc

			if (self.new_entries[-1].data_count + self.new_entries[-1].data_offset) < len(self.data_entries):
				for x in range(self.new_entries[-1].buffer_index + 1):
					self.new_entries[-1 - x].data_count = len(self.data_entries) - self.new_entries[-1 - x].data_offset

	def frags_accumulate(self, p, d_size):
		# get frags whose pointers 0 datas together occupy d_size bytes
		fs = []
		while sum((f.pointers[0].data_size for f in fs)) < d_size:
			# frags = self.frags_for_pointer(p)
			# frags = self.fragments
			# the frag list crosses header borders at Deinonychus_events, so use full frag list
			# -> exceedingly slow
			fs.extend(self.get_frags_after_count(self.fragments, p.data_offset, 1))
		return fs

	def frags_from_pointer(self, ptr, count):
		# print(ptr)
		frags = self.frags_for_pointer(ptr)
		return self.get_frags_after_count(frags, ptr.data_offset, count)

	def get_frags_from_ptr_lut(self, ptr, count):
		"""Use the fragment lookup table to retrieve count fragments starting at a given pointer"""
		pool = self.pools[ptr.pool_index]
		try:
			frag_i = pool.frag_lut[ptr.data_offset]
		except:
			print("error", ptr.data_offset, pool.frag_lut)
		return self.fragments[frag_i:frag_i + count]

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

	def collect_enumnamer(self, ss_entry):
		# Sized string initpos = position of first fragment
		ss_entry.fragments = self.frags_from_pointer(ss_entry.pointers[0], 1)
		count, _ = struct.unpack("<2I", ss_entry.pointers[0].data)
		ss_entry.vars = self.frags_from_pointer(ss_entry.fragments[0].pointers[1], count)
		# pointers[1].data is the name
		for var in ss_entry.vars:
			var.pointers[1].strip_zstring_padding()
		# The last fragment has padding that may be junk data to pad the size of the name block to multiples of 64
		ss_entry.fragments.extend(ss_entry.vars)

	def collect_motiongraph(self, ss_entry):
		# Sized string initpos = position of first fragment
		print(ss_entry.pointers[0].address, len(ss_entry.pointers[0].data))
		if self.ovl.basename.lower() == "driver.ovl":
			print("Debug mode for driver motiongraph!")
			print()
			for frag in self.fragments:
				if 10036 <= frag.pointers[1].address < 10700:
					# ss_entry.fragments.append(frag)
					frag.pointers[1].strip_zstring_padding()
					frag.name = frag.pointers[1].data[:-1]  # .decode()

			f = self.frags_from_pointer(ss_entry.pointers[0], 4)
			u0, u1, counts, name_ptr = f
			d2 = struct.unpack("<4I", counts.pointers[0].data)
			print("counts", d2)
			_, _, unk_count, name_count_1 = d2
			ss_entry.names_1 = self.frags_from_pointer(name_ptr.pointers[1], name_count_1)
			for n in ss_entry.names_1:
				print(n.pointers[1].data)
			d3 = struct.unpack("<3Q", counts.pointers[1].data)
			_, two, one = d3
			print(d3)
			k = self.frags_from_pointer(counts.pointers[1], 9)
			for i in k:
				z = struct.unpack("<3Q", i.pointers[0].data)
				print(z)

	# count, _ = struct.unpack("<2I", ss_entry.pointers[0].data)
	# # print(count)
	# ss_entry.vars = self.frags_from_pointer(ss_entry.fragments[0].pointers[1], count)
	# # pointers[1].data is the name
	# for var in ss_entry.vars:
	# 	var.pointers[1].strip_zstring_padding()
	# # The last fragment has padding that may be junk data to pad the size of the name block to multiples of 64
	# ss_entry.fragments.extend(ss_entry.vars)

	def map_frags(self):
		if not self.fragments:
			return
		logging.info(f"Mapping SizedStrs to {len(self.fragments)} Fragments")

		dic = {
			".bani": 1,
			".tex": 2,
			".xmlconfig": 1,
			# ".hier": ( (4,6) for x in range(19) ),
			".spl": 1,
			# ".world": will be a variable length one with a 4,4; 4,6; then another variable length 4,6 set : set world before assetpkg in order
		}
		# include formats that are known to have no fragments
		no_frags = (".txt", ".mani", ".manis",)
		ss_max = len(self.sized_str_entries)
		for ss_index, sized_str_entry in enumerate(self.sized_str_entries):
			if sized_str_entry.ext in no_frags:
				continue
			self.ovl.print_and_callback("Collecting fragments", value=ss_index, max_value=ss_max)
			logging.debug(f"Collecting fragments for {sized_str_entry.name}")
			try:
				if sized_str_entry.ext == ".tex" and (is_pc(self.ovl) or is_ztuac(self.ovl)):
					sized_str_entry.fragments = self.frags_from_pointer(sized_str_entry.pointers[0], 1)
				# get fixed fragments
				elif sized_str_entry.ext in dic:
					t = dic[sized_str_entry.ext]
					# get and set fragments
					try:
						sized_str_entry.fragments = self.frags_from_pointer(sized_str_entry.pointers[0], t)
					except:
						logging.error("fragment bug")
				elif sized_str_entry.ext == ".fgm":
					sized_str_entry.fragments = self.get_frag_after_terminator(sized_str_entry.pointers[0], (24, 32))
				elif sized_str_entry.ext in (".enumnamer", ".motiongraphvars"):
					self.collect_enumnamer(sized_str_entry)
				elif sized_str_entry.ext == ".motiongraph":
					self.collect_motiongraph(sized_str_entry)
			except Exception as err:
				logging.error(err)

	def assign_frag_names(self):
		# for debugging only:
		for sized_str_entry in self.sized_str_entries:
			for frag in sized_str_entry.model_data_frags + sized_str_entry.fragments:
				frag.name = sized_str_entry.name

	def map_buffers(self):
		"""Map buffers to data entries"""
		logging.info("Mapping buffers")
		# print(self.data_entries)
		# print(self.buffer_entries)
		# print(self.new_entries)
		if is_pz16(self.ovl) or is_jwe2(self.ovl):
			for data in self.data_entries:
				data.buffers = []
			logging.debug("Assigning buffer indices")
			for b_group in self.new_entries:
				b_group.ext = self.ovl.mimes[b_group.ext_index].ext
				# print(b_group.ext)
				# print(b_group)
				# print(b_group.buffer_count, b_group.data_count)
				# note that datas can be bigger than buffers
				buffers = self.buffer_entries[b_group.buffer_offset: b_group.buffer_offset + b_group.buffer_count]
				datas = self.data_entries[b_group.data_offset: b_group.data_offset + b_group.data_count]
				for buffer in buffers:
					buffer.index = b_group.buffer_index
					for data in datas:
						if buffer.file_hash == data.file_hash:
							buffer.name = data.name
							buffer.ext = data.ext
							data.buffers.append(buffer)
							break
			# for buffer, data in zip(buffers, datas):
			# 	buffer.index = b_group.buffer_index
			# 	data.buffers.append(buffer)
			# print(self.buffer_entries)
			# print(self.new_entries)
			for data in self.data_entries:
				data.streams = list(data.buffers)
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
				data.streams = list(data.buffers)
		# print(self.buffer_entries)

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

	@staticmethod
	def get_ptr_debug_str(entry, ind):
		return f"{' '.join((f'[{p.pool_index} {p.data_offset} | {p.address} {p.data_size}]' for p in entry.pointers))} ({ind}) {entry.name}"
	
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
			for x, new_entry in enumerate(self.new_entries):
				f.write(f"\n{new_entry.ext} {new_entry.buffer_offset} {new_entry.buffer_count} {new_entry.buffer_index} | {new_entry.size} {new_entry.data_offset} {new_entry.data_count} ")

	def dump_frag_log(self):
		"""for development; collect info about fragment types"""
		frag_log_path = os.path.join(self.ovl.dir, f"{self.ovl.basename}_{self.arg.name}.log")
		logging.info(f"Dumping fragment log to {frag_log_path}")
		with open(frag_log_path, "w") as f:
			for i, pool in enumerate(self.pools):
				f.write(f"\n\nHeader[{i}] at {pool.address} with {len(pool.fragments)} fragments\n")
				entries = pool.fragments + [ss for ss in self.sized_str_entries if ss.pointers[0].pool_index == i]
				entries.sort(key=lambda entry: entry.pointers[0].data_offset)
				lines = [self.get_ptr_debug_str(frag, j) for j, frag in enumerate(entries)]
				f.write("\n".join(lines))

	def get_frag_after_terminator(self, ptr, terminator=(24,)):
		"""Returns entries of l matching h_types that have not been processed until it reaches a frag of terminator size."""
		frags = self.frags_for_pointer(ptr)
		out = []
		for f in frags:
			# can't add fragments that have already been added elsewhere
			if f.done:
				continue
			if f.pointers[0].data_offset >= ptr.data_offset:
				f.done = True
				out.append(f)
				if f.pointers[0].data_size in terminator:
					break
		else:
			raise AttributeError(
				f"Could not find a terminator fragment matching initpos {ptr.data_offset} and pointer[0].size {terminator}")
		return out

	@staticmethod
	def get_frags_after_count(frags, initpos, count):
		"""Returns count entries of frags that have not been processed and occur after initpos."""
		out = []
		for f in frags:
			# check length of fragment, grab good ones
			if len(out) == count:
				break
			# can't add fragments that have already been added elsewhere
			if f.done:
				continue
			if f.pointers[0].data_offset >= initpos:
				f.done = True
				out.append(f)
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

	def find_entry(self, entries, src_entry):
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
		entry.ext = e
		entry.basename = n
		entry.name = f"{n}{e}"

	def calc_uncompressed_size(self, ):
		"""Calculate the size of the whole decompressed stream for this archive"""
		return self.start_of_pools + sum(pool.size for pool in self.pools) + sum(
			buffer.size for buffer in self.buffer_entries)

	def write_pointers_to_pools(self, ignore_unaccounted_bytes=False):
		"""Pre-writing step to convert all edits that were done on individual points back into the consolidated header
		data io blocks"""
		for i, pool in enumerate(self.pools):
			# maintain sorting order
			# grab the first pointer for each address
			# it is assumed that subsequent pointers to that address share the same data
			sorted_first_pointers = [pointers[0] for offset, pointers in sorted(pool.pointer_map.items())]
			if sorted_first_pointers:
				# only known from indominus
				first_offset = sorted_first_pointers[0].data_offset
				if first_offset != 0 and not ignore_unaccounted_bytes:
					logging.debug(f"Found {first_offset} unaccounted bytes at start of header data {i}")
					unaccounted_bytes = pool.data.getvalue()[:first_offset]
				else:
					unaccounted_bytes = b""

				# clear io objects
				pool.data = io.BytesIO()
				pool.data.write(unaccounted_bytes)
				# write updated strings
				for pointer in sorted_first_pointers:
					pointer.write_data(update_copies=True)
			else:
				# todo - shouldn't we delete the header entry in that case?
				logging.debug(f"No pointers into header entry {i} - keeping its stock data!")

	def write_pools(self):
		logging.debug(f"Writing pools for {self.arg.name}")
		if self.force_update_pools:
			self.write_pointers_to_pools()
		# do this first so pools can be updated
		pools_data_writer = io.BytesIO()
		# the ugly stuff with all fragments and sizedstr entries
		for pool in self.pools:
			pool_bytes = pool.data.getvalue()
			# JWE, JWE2: relative offset for each pool
			if self.ovl.user_version.is_jwe:
				pool.offset = pools_data_writer.tell()
			# PZ, PC: offsets relative to the whole pool block
			else:
				pool.offset = self.arg.pools_start + pools_data_writer.tell()
			logging.debug(f"header.offset {pool.offset}, pools_start {self.arg.pools_start}")
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

		self.last_print = None
		if progress_callback:
			self.progress_callback = progress_callback
		else:
			self.progress_callback = self.dummy_callback

	def extract(self, out_dir, only_names=(), only_types=(), show_temp_files=False):
		"""Extract the files, after all archives have been read"""
		# create output dir
		logging.info(f"Extracting from {len(self.files)} files...")
		os.makedirs(out_dir, exist_ok=True)

		def out_dir_func(n):
			"""Helper function to generate temporary output file name"""
			return os.path.normpath(os.path.join(out_dir, n))

		# the actual export, per file type
		error_files = []
		skip_files = []
		out_paths = []
		from modules.extract import extract_kernel, get_files
		extract_files = get_files(self, only_names, only_types, skip_files)
		for ss_index, file in enumerate(extract_files):
			self.progress_callback("Extracting...", value=ss_index, vmax=len(extract_files))
			sized_str_entry = self.get_sized_str_entry(file.name)
			try:
				out_paths.extend(
					extract_kernel(self, sized_str_entry, out_dir_func, show_temp_files, self.progress_callback))

			except BaseException as error:
				logging.error(f"An exception occurred while extracting {sized_str_entry.name}")
				logging.error(error)
				traceback.print_exc()
				error_files.append(sized_str_entry.name)
		self.progress_callback("Extraction completed!", value=1, vmax=1)

		return out_paths, error_files, skip_files

	def create_file(self, file_path):
		"""Create a file entry from a file path"""
		filename = os.path.basename(file_path)
		logging.debug(f"Creating {filename}")
		file_entry = FileEntry(self.context)
		file_entry.path = file_path
		file_entry.name = filename
		file_entry.basename, file_entry.ext = os.path.splitext(filename)
		try:
			file_entry.update_constants(self)
		except KeyError:
			logging.warning(f"Unsupported extension {filename}")
			return
		file_entry.dependencies = []
		self.files.append(file_entry)

	def create(self, ovl_dir):
		logging.info(f"Creating OVL from {ovl_dir}")
		logging.info(f"Game: {get_game(self)}")
		for file_name in os.listdir(ovl_dir):
			file_path = os.path.join(ovl_dir, file_name)
			self.create_file(file_path)
		# generate hashes so we can sort the files
		self.update_hashes()
		self.files.sort(key=lambda x: (x.ext, x.file_hash))

		archive_entry = ArchiveEntry(self.context)
		self.archives.append(archive_entry)
		self.static_archive = archive_entry

		content = OvsFile(self.context, self, archive_entry)
		archive_entry.content = content
		archive_entry.name = "STATIC"
		archive_entry.offset = 0
		archive_entry.pools_offset = 0
		archive_entry.ovs_file_offset = 0
		archive_entry.ovs_offset = 0

		new_zlib = ZlibInfo(self.context)
		self.zlibs.append(new_zlib)

		# create loaders for supported files
		for file_entry in self.files:
			file_entry.loader = get_loader(file_entry.ext, self)
			if file_entry.loader:
				file_entry.loader.create(content, file_entry)
		# ensure that each pool data is padded to 4
		for pool in content.pools:
			pool.data.write(get_padding(pool.data.tell(), 4))
		content.force_update_pools = False
		content.map_buffers()

		self.update_hashes()
		self.update_counts()
		self.postprocessing()

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

	@property
	def dir_names(self):
		return [dir_entry.basename for dir_entry in self.dirs]

	def store_filepath(self, filepath):
		# store file name for later
		self.filepath = filepath
		self.dir, self.basename = os.path.split(filepath)
		self.file_no_ext = os.path.splitext(self.filepath)[0]

	def inject_dir(self, directory_name):
		# validate can't insert same directory twice
		for dir_entry in self.dirs:
			if dir_entry.name == directory_name:
				return

		# store file name for later
		new_directory = DirEntry(self.context)
		new_directory.name = directory_name
		new_directory.basename = directory_name
		self.dirs.append(new_directory)

	def remove_dir(self, directory_name):
		for dir_entry in self.dirs:
			if dir_entry.name == directory_name:
				self.dirs.remove(dir_entry)

	def rename_dir(self, directory_name, directory_new_name):
		# find an existing entry in the list
		for idx, dir_entry in enumerate(self.dirs):
			if dir_entry.name == directory_name:
				dir_entry.name = directory_new_name
				dir_entry.basename = directory_new_name

	def update_names(self):
		"""Update the name buffers with names from list entries, and update the name offsets on those entries"""
		# update ext dependencies with : prefix instead of .
		for dependency in self.dependencies:
			dependency.ext = dependency.ext.replace(".", ":")
		# regenerate the name buffer
		self.names.update_with((
			(self.dependencies, "ext"),
			(self.dirs, "basename"),
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

	def load(self, filepath, verbose=0, commands=(), hash_table={}):
		start_time = time.time()
		# store commands
		self.commands = commands
		self.store_filepath(filepath)
		logging.info(f"Loading {self.basename}")
		self.eof = super().load(filepath)
		logging.info(f"Game: {get_game(self)}")

		# maps OVL hash to final filename + extension
		self.hash_table_local = {}
		self.hash_table_global = hash_table
		# print(self)
		# add extensions to hash dict
		hm_max = len(self.mimes)
		for hm_index, mime_entry in enumerate(self.mimes):
			self.print_and_callback("Adding extensions to hash dict", value=hm_index, max_value=hm_max)
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
			self.print_and_callback("Adding file names to hash dict", value=hf_index, max_value=hf_max)
			# get file name from name table
			file_name = self.names.get_str_at(file_entry.offset)
			file_entry.ext = self.mimes[file_entry.extension].ext
			# store this so we can use it
			file_entry.ext_hash = djb(file_entry.ext[1:])
			file_entry.basename = file_name
			file_entry.name = file_name + file_entry.ext
			file_entry.dependencies = []
			self.hash_table_local[file_entry.file_hash] = file_name
		if "generate_hash_table" in self.commands:
			return self.hash_table_local

		# get directories
		hd_max = len(self.dirs)
		for hd_index, dir_entry in enumerate(self.dirs):
			self.print_and_callback("Creating directories", value=hd_index, max_value=hd_max)
			# get dir name from name table
			dir_entry.basename = self.names.get_str_at(dir_entry.offset)
			dir_entry.ext = ""
			dir_entry.name = dir_entry.basename + dir_entry.ext

		# get names of all dependencies
		ht_max = len(self.dependencies)
		for ht_index, dependency_entry in enumerate(self.dependencies):
			self.print_and_callback("Getting dependency names", value=ht_index, max_value=ht_max)
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
				logging.warning(f"UNRESOLVED DEPENDENCY: {h} -> ?")
				dependency_entry.basename = "bad hash"

			dependency_entry.name = dependency_entry.basename + dependency_entry.ext.replace(":", ".")
			try:
				file_entry = self.files[dependency_entry.file_index]
				file_entry.dependencies.append(dependency_entry)
				dependency_entry.file = file_entry
			# funky bug due to some PC ovls using a different DependencyEntry struct
			except IndexError as err:
				logging.error(err)
		# sort dependencies by their pool offset
		for file_entry in self.files:
			file_entry.dependencies.sort(key=lambda entry: entry.pointers[0].data_offset)

		for aux_entry in self.aux_entries:
			aux_entry.file = self.files[aux_entry.file_index]

		self.static_archive = None
		for archive_entry in self.archives:
			archive_entry.name = self.archive_names.get_str_at(archive_entry.offset)
		self.load_archives()
		logging.info(f"Loaded OVL in {time.time() - start_time:.2f} seconds!")

	def update_mimes(self):
		"""Rebuilds the mimes list according to the ovl's current file entries"""
		logging.info("Updating mimes")
		self.mimes.clear()
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

	def update_triplets(self):
		logging.info("Updating triplets")
		self.triplets.clear()
		if is_pz16(self) or is_jwe2(self):
			triplet_offset = 0
			for mime in self.mimes:
				mime.triplet_offset = triplet_offset
				if mime.ext in constants_pz.mimes_triplets:
					triplet_grab = constants_pz.mimes_triplets[mime.ext]
					mime.triplet_count = len(triplet_grab)
					triplet_offset += len(triplet_grab)
					for triplet in triplet_grab:
						trip = Triplet(self.context)
						trip.a, trip.b, trip.c = triplet
						self.triplets.append(trip)

	def load_headers(self):
		"""Create flattened list of pools"""
		self.pools = [None for _ in range(self.num_pools)]
		for archive_entry in self.archives:
			if archive_entry.num_pools:
				self.pools[
				archive_entry.pools_offset: archive_entry.pools_offset + archive_entry.num_pools] = archive_entry.content.pools

	def link_ptrs_to_pools(self):
		""""Link all pointers to their respective pools"""
		for dep in self.dependencies:
			# the index goes into the flattened list of pools
			dep.pointers[0].link_to_pool(self.pools)
		for archive_entry in self.archives:
			ovs = archive_entry.content
			ovs.link_ptrs_to_pools()

	def load_archives(self):
		logging.info("Loading archives...")
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
		self.load_headers()
		self.load_pointers()
		self.load_file_classes()

	def load_pointers(self):
		"""Handle all pointers of this file, including dependencies, fragments and ss entries"""
		logging.info("Loading pointers")
		# reset pointer map for each header entry
		for pool in self.pools:
			pool.pointer_map = {}
		self.link_ptrs_to_pools()
		self.calc_pointer_sizes()
		self.resolve_pointers()

	def resolve_pointers(self):
		# apparently JWE has 16 bytes, PZ seems to have either?
		valid_dep_ptrs = (b'\x00' * 8, b'\x00' * 16)
		for dep in self.dependencies:
			if dep.pointers[0].data not in valid_dep_ptrs:
				logging.warning(f"Unexpected data for dependency ptr {dep.name}: {dep.pointers[0].data}")
		for archive_entry in self.archives:
			ovs = archive_entry.content
			ovs.resolve_pointers()

	def calc_pointer_sizes(self):
		"""Assign an estimated size to every pointer"""
		logging.info("Calculating pointer sizes, addresses, copies & reading data")
		# calculate pointer data sizes
		for pool in self.pools:
			# make them unique and sort them
			sorted_items = sorted(pool.pointer_map.items())
			# add the end of the header data block
			sorted_items.append((pool.size, None))
			# get the size of each pointer
			for i, (offset, pointers) in enumerate(sorted_items[:-1]):
				# get the offset of the next pointer, substract this offset
				data_size = sorted_items[i + 1][0] - offset
				# also calculate address of pointer
				address = pool.address + offset
				for pointer in pointers:
					pointer.data_size = data_size
					pointer.address = address
					pointer.copies = pointers
					pointer.read_data()

	def dump_frag_log(self):
		for archive_entry in self.archives:
			try:
				archive_entry.content.assign_frag_names()
				archive_entry.content.dump_frag_log()
				archive_entry.content.dump_buffer_groups_log()
				archive_entry.content.dump_pools()
			except BaseException as err:
				print(err)

	def load_file_classes(self):
		logging.info("Loading file classes...")
		for file in self.files:
			file.loader = get_loader(file.ext, self)
			if file.loader:
				try:
					file.loader.collect(self, file)
				except Exception as err:
					logging.error(err)
					traceback.print_exc()

	def get_sized_str_entry(self, name):
		"""Retrieves the desired ss entry"""
		# logging.debug(f"Getting {name.lower()}")
		if name.lower() in self.ss_dict:
			return self.ss_dict[name.lower()]
		else:
			raise KeyError(f"Can't find a sizedstr entry for {name}, not from this archive?")

	def update_ss_dict(self):
		"""Stores a reference to each sizedstring entry in a dict so they can be extracted"""
		logging.info("Updating the entry dict...")
		self.ss_dict = {}
		for archive_index, archive_entry in enumerate(self.archives):
			for file in archive_entry.content.sized_str_entries:
				self.ss_dict[file.name.lower()] = file

	def link_streams(self):
		"""Attach the data buffers of streamed filed to standard files from the first archive"""
		if not self.archives:
			return
		logging.info("Linking streams...")
		# find texstream buffers
		for tb_index, sized_str_entry in enumerate(self.static_archive.content.sized_str_entries):
			# self.print_and_callback("Finding texstream buffers", value=tb_index, max_value=tb_max)
			if sized_str_entry.ext == ".tex":
				for lod_i in range(3):
					for archive in self.archives:
						if archive == self.static_archive:
							continue
						for other_sizedstr in archive.content.sized_str_entries:
							if f"{sized_str_entry.basename}_lod{lod_i}" in other_sizedstr.name:
								sized_str_entry.data_entry.streams.extend(other_sizedstr.data_entry.buffers)
						# sized_str_entry.streams.append(other_sizedstr)
			if sized_str_entry.ext == ".ms2":
				for lod_i in range(4):
					for archive in self.archives:
						if archive == self.static_archive:
							continue
						for other_sizedstr in archive.content.sized_str_entries:
							if f"{sized_str_entry.basename[:-1]}{lod_i}.model2stream" in other_sizedstr.name:
								# print("model2stream")
								sized_str_entry.data_entry.streams.extend(other_sizedstr.data_entry.buffers)
						# sized_str_entry.streams.append(other_sizedstr)
		# print(sized_str_entry.data_entry.buffers)

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
		# update file hashes
		for file in self.files:
			file.file_hash = djb(file.basename)
			file.ext_hash = djb(file.ext[1:])
		# update dependency hashes
		for dependency in self.dependencies:
			if dependency.basename == "bad hash":
				logging.warning(f"Bad hash on dependency entry - cannot resolve this")
			else:
				dependency.file_hash = djb(dependency.basename)

		# sort the different lists according to the criteria specified
		self.files.sort(key=lambda x: (x.ext, x.file_hash))
		self.dependencies.sort(key=lambda x: x.file_hash)

		# build a lookup table mapping file name to its index
		file_name_lut = {file.name: file_i for file_i, file in enumerate(self.files)}
		# update the file indices
		for entry in self.dependencies + self.aux_entries:
			entry.file_index = file_name_lut[entry.file.name]

		for archive in self.archives:
			# change the hashes / indices of all entries to be valid for the current game version
			archive.content.update_hashes(file_name_lut)

	def update_counts(self):
		"""Update counts of this ovl and all of its archives"""
		self.update_mimes()
		self.update_triplets()
		# adjust the counts
		for archive in self.archives:
			archive.content.rebuild_buffer_groups()
			archive.content.update_counts()
			archive.content.rebuild_assets()
		# sum content of individual archives
		self.num_pool_types = sum(a.num_pool_types for a in self.archives)
		self.num_pools = sum(a.num_pools for a in self.archives)
		self.num_datas = sum(a.num_datas for a in self.archives)
		self.num_buffers = sum(a.num_buffers for a in self.archives)

		self.num_dirs = len(self.dirs)
		self.num_files = self.num_files_2 = self.num_files_3 = len(self.files)
		self.num_dependencies = len(self.dependencies)
		self.num_mimes = len(self.mimes)
		self.num_triplets = len(self.triplets)
		self.num_archives = len(self.archives)

	def open_ovs_streams(self, mode="wb"):
		logging.info("Opening OVS streams...")
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
		logging.info("Closing OVS streams...")
		# we don't use context manager so gotta close them
		for ovs_file in self.ovs_dict.values():
			ovs_file.close()

	def update_pool_datas(self):
		pools_offset = 0
		for i, archive_entry in enumerate(self.archives):
			archive_entry.pools_start = pools_offset
			archive_entry.content.write_pools()
			pools_offset += len(archive_entry.content.pools_data)
			archive_entry.pools_end = pools_offset
			# at least PZ & JWE require 4 additional bytes after each pool
			pools_offset += 4

	def update_files(self):
		logging.info("Updating files...")
		for file in self.files:
			if file.loader:
				file.loader.update()

	def save(self, filepath, dat_path):
		logging.info("Writing OVL")
		self.store_filepath(filepath)
		self.update_files()
		self.update_counts()
		# do this last so we also catch the assets & sets
		self.update_hashes()
		# update the name buffer and offsets
		self.update_names()
		self.update_pool_datas()
		self.update_aux_sizes()
		self.open_ovs_streams()
		ovl_compressed = b""
		# compress data stream
		for i, archive_entry in enumerate(self.archives):
			# write archive into bytes IO stream
			self.progress_callback("Saving archives...", value=i, vmax=len(self.archives))
			uncompressed = archive_entry.content.get_bytes(i, dat_path)
			archive_entry.uncompressed_size, archive_entry.compressed_size, compressed = archive_entry.content.compress(
				uncompressed)
			# update set data size
			archive_entry.set_data_size = archive_entry.content.set_header.io_size
			if archive_entry.name == "STATIC":
				ovl_compressed = compressed
				archive_entry.read_start = 0
			else:
				ovs_stream = self.ovs_dict[archive_entry.ovs_path]
				archive_entry.read_start = ovs_stream.tell()
				ovs_stream.write(compressed)
			self.zlibs[i].zlib_thing_1 = 68 + archive_entry.uncompressed_size

		self.close_ovs_streams()
		eof = super().save(filepath)
		with self.writer(filepath) as stream:
			# first header
			self.write(stream)
			# write zlib block
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
# print(aux.size)


if __name__ == "__main__":
	ovl = OvlFile()
	ovl.load("C:/Users/arnfi/Desktop/Coding/ovl/OVLs/Parrot.ovl")
