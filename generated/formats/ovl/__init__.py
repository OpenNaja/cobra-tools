import os
import itertools
import struct
import io
import time
import traceback
import logging

from generated.io import IoFile, ZipFile, BinaryStream
from generated.formats.ovl.versions import *
from generated.formats.ovl.compound.AssetEntry import AssetEntry
from generated.formats.ovl.compound.Header import Header
from generated.formats.ovl.compound.OvsHeader import OvsHeader
from generated.formats.ovl.compound.SetEntry import SetEntry
from generated.formats.ovl.compound.ArchiveEntry import ArchiveEntry
from generated.formats.ovl.compound.DirEntry import DirEntry
from generated.formats.ovl.compound.FileEntry import FileEntry
from generated.formats.ovl.compound.MimeEntry import MimeEntry
from generated.formats.ovl.compound.ZlibInfo import ZlibInfo

from modules.formats.shared import get_versions, djb, assign_versions, get_padding


lut_mime_version_jwe = {
	".fdb": 1,
	".banis": 5,
	".assetpkg": 2,
	".userinterfaceicondata": 1,
	".lua": 7,
	".txt": 2,
	".tex": 8,
	".ms2": 47,
	".mdl2": 47,
	".fgm": 6,
}

lut_mime_version_pz = {
	".fdb": 1,
	".bani": 5,
	".banis": 5,
	".assetpkg": 2,
	# ".userinterfaceicondata": 1,
	".lua": 7,
	".txt": 3,
	".tex": 9,
	".texturestream": 9,
	".ms2": 50,
	".mdl2": 50,
	".fgm": 6,
}

lut_file_unk_0 = {
	".fdb": 4,
	".assetpkg": 4,
	".userinterfaceicondata": 4,
	".lua": 2,
	".txt": 1,
	".bani": 2,
	".banis": 2,
	".fgm": 2,
	".mdl2": 2,
	".ms2": 2,
	".tex": 3,
}

lut_file_unk_1 = {
	".mdl2": 2,
}

lut_mime_hash_jwe = {
	".assetpkg": 1145776474,
	".banis": 1177957172,
	".fdb": 2545474337,
	".fgm": 861771362,
	".mdl2": 4285397356,
	".ms2": 2893339803,
	".lua": 1779074288,
	".txt": 640591494,
	".tex": 3242366505,
	".userinterfaceicondata": 2127665351,
}

lut_mime_hash_pz = {
	".bani": 1380752341,
	".banis": 1177957172,
	".fgm": 861771362,
	".mdl2": 4285397382,
	".ms2": 2893339829,
	".tex": 3242366506,
	".texturestream": 4096653506,
	".assetpkg": 1145776474,
	".fdb": 2545474337,
	".lua": 1779074288,
	".txt": 640591495,
	# ".userinterfaceicondata": 2127665351,
}


def get_loader(ext):
	from modules.formats.ASSETPKG import AssetpkgLoader
	from modules.formats.MS2 import Ms2Loader
	from modules.formats.LUA import LuaLoader
	from modules.formats.TXT import TxtLoader
	from modules.formats.FDB import FdbLoader
	from modules.formats.USERINTERFACEICONDATA import UserinterfaceicondataLoader
	ext_2_class = {
		".assetpkg": AssetpkgLoader,
		".ms2": Ms2Loader,
		".lua": LuaLoader,
		".txt": TxtLoader,
		".fdb": FdbLoader,
		".userinterfaceicondata": UserinterfaceicondataLoader,
	}
	cls = ext_2_class.get(ext, None)
	if cls:
		return cls()


class OvsFile(OvsHeader, ZipFile):

	def __init__(self, ovl, archive_entry, archive_index):
		super().__init__()
		self.ovl = ovl
		self.arg = archive_entry
		self.archive_index = archive_index
		# this determines if fragments are written back to header datas
		self.force_update_pools = True

	def update_hashes(self, file_name_lut):
		logging.info("Updating hashes")
		logging.info(f"Game: {get_game(self.ovl)}")
		for entry_list in (
				self.pools,
				self.sized_str_entries,
				self.data_entries,
				self.set_header.sets,
				self.set_header.assets):
			for entry in entry_list:
				file_index = file_name_lut[entry.name]
				file = self.ovl.files[file_index]
				if is_jwe(self.ovl):
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

	def create(self):

		# create loaders for supported files
		for file_entry in self.ovl.files:
			loader = get_loader(file_entry.ext)
			if loader:
				loader.create(self, file_entry)
		# post-process the memory pools
		for pool in self.pools:
			pool.data.write(get_padding(pool.data.tell(), 4))
			self.transfer_identity(pool, self.sized_str_entries[0])

		self.force_update_pools = False
		self.map_buffers()

	def get_sized_str_entry(self, name):
		lower_name = name.lower()
		for sized_str_entry in self.sized_str_entries:
			if lower_name == sized_str_entry.lower_name:
				return sized_str_entry
		# still here - error!
		raise KeyError(f"Can't find a sizedstr entry for {name}, not from this archive?")

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
			pool_index = 0
			for pool_type in self.pool_types:
				for i in range(pool_type.num_pools):
					pool = self.pools[pool_index]
					pool.type = pool_type.type
					self.assign_name(pool)
					# store fragments per header for faster lookup
					pool.fragments = []
					pool_index += 1

			for data_entry in self.data_entries:
				self.assign_name(data_entry)
			for sized_str_entry in self.sized_str_entries:
				self.assign_name(sized_str_entry)
				sized_str_entry.lower_name = sized_str_entry.name.lower()
				sized_str_entry.children = []
				sized_str_entry.fragments = []
				sized_str_entry.model_data_frags = []
				# get data entry for link to buffers, or none
				sized_str_entry.data_entry = self.find_entry(self.data_entries, sized_str_entry)

			for i, fragment in enumerate(self.fragments):
				# we assign these later
				fragment.done = False
				fragment.name = None

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

			# another integrity check
			if self.arg.uncompressed_size and not is_pc(self.ovl) and self.calc_uncompressed_size() != self.arg.uncompressed_size:
				raise AttributeError(
					f"Archive.uncompressed_size ({self.arg.uncompressed_size}) "
					f"does not match calculated size ({self.calc_uncompressed_size()})")

			# add IO object to every pool
			self.read_pools(stream)

			# self.check_pool_size = self.calc_pools_size()
			self.map_pointers()
			self.calc_pointer_addresses()
			self.calc_pointer_sizes()
			self.populate_pointers()
			self.map_frags()
			self.map_buffers()
			self.read_buffer_datas(stream)

	def debug_txt_data(self):
		for ss in self.sized_str_entries:
			if ss.ext == ".txt":
				p = ss.pointers[0]
				b = p.data
				size = struct.unpack("<I", b[:4])[0]
				data = b[4:4 + size]
				padding_size = len(b) - (4 + size)
				print(ss.file_hash, p.pool_index, p.data_offset, p.address, len(b), padding_size, ss.name, data)

	def read_pools(self, stream):
		for pool in self.pools:
			pool.address = stream.tell()
			pool.data = BinaryStream(stream.read(pool.size))
			assign_versions(pool.data, get_versions(self.ovl))

	def calc_pointer_addresses(self):
		logging.info("Calculating pointer addresses")
		# store absolute read addresses from the start of file
		for entry in itertools.chain(self.fragments, self.sized_str_entries):
			# for access from start of file
			for pointer in entry.pointers:
				# some have max_uint as a header value, what do they refer to
				if pointer.pool_index == -1:
					pointer.header = None
					pointer.address = 9999999
				else:
					pointer.header = self.pools[pointer.pool_index]
					pointer.address = self.start_of_pools + pointer.header.offset + pointer.data_offset

	def calc_pointer_sizes(self):
		"""Assign an estimated size to every pointer"""
		logging.info("Calculating pointer sizes")
		# calculate pointer data sizes
		for entry in self.pools:
			# make them unique and sort them
			sorted_items = sorted(entry.pointer_map.items())
			# add the end of the header data block
			sorted_items.append((entry.size, None))
			# get the size of each fragment: find the next entry's address and substract it from address
			for i, (offset, pointers) in enumerate(sorted_items[:-1]):
				# get the offset of the next entry that points into this buffer, substract this offset
				data_size = sorted_items[i + 1][0] - offset
				for pointer in pointers:
					pointer.data_size = data_size

	def map_pointers(self):
		"""Assign list of copies to every pointer so they can be updated with the same data easily"""
		logging.info("Mapping pointers")
		# reset pointer map for each header entry
		for pool in self.pools:
			pool.pointer_map = {}
		logging.debug("Linking pointers to header")
		# append all valid pointers to their respective dicts
		for entry in itertools.chain(self.fragments, self.sized_str_entries):
			for pointer in entry.pointers:
				pointer.link_to_header(self)
		logging.debug("Finding duplicate pointers")
		for pool in self.pools:
			# for every pointer, store any other pointer that points to the same address
			for offset, pointers in pool.pointer_map.items():
				for p in pointers:
					# p.copies = [po for po in pointers if po != p]
					p.copies = pointers

	def populate_pointers(self):
		"""Load data for every pointer"""
		logging.info("Reading data into pointers")
		for entry in itertools.chain(self.fragments, self.sized_str_entries):
			for pointer in entry.pointers:
				pointer.read_data(self.pools)

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
		# source_entry.file_hash = target_entry.file_hash
		# source_entry.ext_hash = target_entry.ext_hash
		source_entry.basename = target_entry.basename
		source_entry.ext = target_entry.ext
		source_entry.name = target_entry.name

	# noinspection PyTypeChecker
	def update_assets(self):
		"""Update archive asset grouping from children list on sized str entries"""
		logging.info("Updating assets")
		self.set_header.sets.clear()
		self.set_header.assets.clear()
		self.set_header.set_count = 0
		self.set_header.asset_count = 0
		start = 0
		ss_index_table = {file.name: i for i, file in enumerate(self.sized_str_entries)}
		for ss_entry in self.sized_str_entries:
			if ss_entry.children:
				set_entry = SetEntry()
				set_entry.start = start
				set_entry.end = start + len(ss_entry.children)
				self.transfer_identity(set_entry, ss_entry)
				self.set_header.sets.append(set_entry)
				for ss_child in ss_entry.children:
					asset_entry = AssetEntry()
					asset_entry.file_index = ss_index_table[ss_child.name]
					self.transfer_identity(asset_entry, ss_child)
					self.set_header.assets.append(asset_entry)
				start += len(ss_entry.children)
				self.set_header.set_count += 1
				self.set_header.asset_count += len(ss_entry.children)
				# set_index is 1-based, so the first set = 1, so we do it after the increment
				ss_entry.data_entry.set_index = self.set_header.set_count

	def frags_accumulate(self, p, d_size, address_0_fragments):
		# get frags whose pointers 0 datas together occupy d_size bytes
		fs = []
		while sum((f.pointers[0].data_size for f in fs)) < d_size:
			# frags = self.frags_for_pointer(p)
			# frags = self.fragments
			# the frag list crosses header borders at Deinonychus_events, so use full frag list
			# -> exceedingly slow
			fs.extend(self.get_frags_after_count(address_0_fragments, p.address, 1))
		return fs

	def frags_from_pointer(self, p, count):
		frags = self.frags_for_pointer(p)
		return self.get_frags_after_count(frags, p.address, count)

	def frags_from_pointer_discon(self, p):
		frags = self.frags_for_pointer(p)
		return self.get_frags_til_discon(frags, p.address, len(p.data))

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

	def prefab_unpack_temp(self, len, data):
		if len % 4 != 0:
			ret = data
		elif len >= 50:
			num = int(len / 4)
			strr = "<" + str(num) + "I"
			ret = struct.unpack(strr, data)
		else:
			num = int(len / 4)
			strr = "<" + str(num) + "I"
			ret = struct.unpack(strr, data)
		return ret

	def prefab_unpack_ss(self, len, data):
		num = int(len)
		strr = "<" + str(num) + "B"
		ret = struct.unpack(strr, data)
		return ret

	def collect_specdef(self, ss_entry):
		print("\nSPECDEF:", ss_entry.name)
		# frags = self.fragments
		ss_data = struct.unpack("<2H4B", ss_entry.pointers[0].data)
		if ss_data[0] == 0:
			print("spec is zero ", ss_data[0])
		ss_entry.fragments = self.frags_from_pointer(ss_entry.pointers[0], 3)
		if ss_data[2] > 0:
			data2_frag = self.frags_from_pointer(ss_entry.pointers[0], 1)
			ss_entry.fragments.extend(data2_frag)
		if ss_data[3] > 0:
			data3_frag = self.frags_from_pointer(ss_entry.pointers[0], 1)
			ss_entry.fragments.extend(data3_frag)
		if ss_data[4] > 0:
			data4_frag = self.frags_from_pointer(ss_entry.pointers[0], 1)
			ss_entry.fragments.extend(data4_frag)
		if ss_data[5] > 0:
			data5_frag = self.frags_from_pointer(ss_entry.pointers[0], 1)
			ss_entry.fragments.extend(data5_frag)

		if ss_data[0] > 0:
			ss_entry.fragments.extend(self.frags_from_pointer(ss_entry.fragments[1].pointers[1], ss_data[0]))
			ss_entry.fragments.extend(self.frags_from_pointer(ss_entry.fragments[2].pointers[1], ss_data[0]))

		if ss_data[2] > 0:
			ss_entry.fragments.extend(self.frags_from_pointer(data2_frag[0].pointers[1], ss_data[2]))
		if ss_data[3] > 0:
			ss_entry.fragments.extend(self.frags_from_pointer(data3_frag[0].pointers[1], ss_data[3]))
		if ss_data[4] > 0:
			ss_entry.fragments.extend(self.frags_from_pointer(data4_frag[0].pointers[1], ss_data[4]))
		if ss_data[5] > 0:
			ss_entry.fragments.extend(self.frags_from_pointer(data5_frag[0].pointers[1], ss_data[5]))

	def collect_prefab(self, ss_entry, ad0_fragments):
		ssdata = self.prefab_unpack_ss(len(ss_entry.pointers[0].data), ss_entry.pointers[0].data)
		# if ss_entry.name in ("dingo_game.prefab"+"cassowary_game.prefab"+"red_kangaroo_game.prefab"+"koala_game.prefab"):
		print("\nPREFAB:", ss_entry.name)
		print(ssdata)
		if (ssdata[4] == 0) and (ssdata[6] == 0):
			ss_entry.fragments = self.frags_from_pointer(ss_entry.pointers[0], 1)
		elif (ssdata[4] != 0) and (ssdata[6] == 0):
			ss_entry.fragments = self.frags_from_pointer(ss_entry.pointers[0], 4)
			f3_d0 = self.prefab_unpack_temp(len(ss_entry.fragments[3].pointers[0].data),
											ss_entry.fragments[3].pointers[0].data)
			f2_d0 = self.prefab_unpack_temp(len(ss_entry.fragments[2].pointers[0].data),
											ss_entry.fragments[2].pointers[0].data)
		elif (ssdata[4] == 0) and (ssdata[6] != 0):
			ss_entry.fragments = self.frags_from_pointer(ss_entry.pointers[0], 3)
			f3_d0 = self.prefab_unpack_temp(len(ss_entry.fragments[2].pointers[0].data),
											ss_entry.fragments[2].pointers[0].data)
			f2_d0 = self.prefab_unpack_temp(len(ss_entry.fragments[2].pointers[0].data),
											ss_entry.fragments[2].pointers[0].data)
		elif (ssdata[4] != 0) and (ssdata[6] != 0):
			ss_entry.fragments = self.frags_from_pointer(ss_entry.pointers[0], 6)
			f5_d0 = self.prefab_unpack_temp(len(ss_entry.fragments[5].pointers[0].data),
											ss_entry.fragments[5].pointers[0].data)
			f2_d0 = self.prefab_unpack_temp(len(ss_entry.fragments[2].pointers[0].data),
											ss_entry.fragments[2].pointers[0].data)
		else:
			ss_entry.fragments = self.frags_from_pointer(ss_entry.pointers[0], 1)
		gub = []
		fug = []

		if (ssdata[4] != 0) and (ssdata[6] == 0):
			if len(f3_d0) == 8:
				gub = self.frags_from_pointer(ss_entry.pointers[0], 1)
				ss_entry.fragments += gub
			ss_entry.fragments += self.frags_from_pointer(ss_entry.fragments[0].pointers[1], ssdata[4])
			if f2_d0[
				2] == 536870911:  # in ("dingo_game.prefab"+"cassowary_game.prefab"+"red_kangaroo_game.prefab"+"koala_game.prefab"):
				ss_entry.fragments += self.frags_from_pointer(ss_entry.fragments[2].pointers[1], 18)
				for x in range(34, 52):
					if x == 34:
						ss_entry.fragments += self.frags_from_pointer_equalsb_counts(ss_entry.fragments[x].pointers[1],
																					 2)
					elif x == 35:
						ss_entry.fragments += self.frags_from_pointer_equalsb_counts(ss_entry.fragments[x].pointers[1],
																					 5)
					elif x == 38:
						ss_entry.fragments += self.frags_from_pointer_equalsb_counts(ss_entry.fragments[x].pointers[1],
																					 3)
					elif x == 41:
						ss_entry.fragments += self.frags_from_pointer_equalsb(ss_entry.fragments[x].pointers[1])
					elif x == 43:
						ss_entry.fragments += self.frags_from_pointer_equalsb_counts(ss_entry.fragments[x].pointers[1],
																					 2)
					elif x == 45:
						ss_entry.fragments += self.frags_from_pointer_equalsb(ss_entry.fragments[x].pointers[1])
					elif x == 47:
						ss_entry.fragments += self.frags_from_pointer_equalsb(ss_entry.fragments[x].pointers[1])
					elif x == 48:
						ss_entry.fragments += self.frags_from_pointer_equalsb(ss_entry.fragments[x].pointers[1])
					elif x == 50:
						ss_entry.fragments += self.frags_from_pointer_equalsb_counts(ss_entry.fragments[x].pointers[1],
																					 2)
					elif x == 51:
						ss_entry.fragments += self.frags_from_pointer_equalsb_counts(ss_entry.fragments[x].pointers[1],
																					 2)
			# elif  f2_d0[2] ==127:
			#	ss_entry.fragments += self.frags_from_pointer(ss_entry.fragments[2].pointers[1], 6)
			# elif  f2_d0[2] ==3:
			#	ss_entry.fragments += self.frags_from_pointer(ss_entry.fragments[2].pointers[1], 1)
			# elif  f2_d0[2] ==63:
			#	ss_entry.fragments += self.frags_from_pointer(ss_entry.fragments[2].pointers[1], 5)
			# elif  f2_d0[2] ==1:
			#	ss_entry.fragments += self.frags_from_pointer(ss_entry.fragments[2].pointers[1], 1)
			# elif  f2_d0[2] ==7:
			#	ss_entry.fragments += self.frags_from_pointer(ss_entry.fragments[2].pointers[1], 4)
			# elif  f2_d0[2] ==15:
			#	ss_entry.fragments += self.frags_from_pointer(ss_entry.fragments[2].pointers[1], 3)
			if len(f3_d0) == 8:
				fug += self.frags_from_pointer_equalsb_counts(ss_entry.fragments[4].pointers[1], 5)
				ss_entry.fragments += fug
				gub_d1 = self.prefab_unpack_temp(len(gub[0].pointers[1].data), gub[0].pointers[1].data)
				fug0_d1 = self.prefab_unpack_temp(len(fug[0].pointers[1].data), fug[0].pointers[1].data)
				fug1_d1 = self.prefab_unpack_temp(len(fug[1].pointers[1].data), fug[1].pointers[1].data)
				fug2_d1 = self.prefab_unpack_temp(len(fug[2].pointers[1].data), fug[2].pointers[1].data)
				fug3_d1 = self.prefab_unpack_temp(len(fug[3].pointers[1].data), fug[3].pointers[1].data)
				fug4_d1 = self.prefab_unpack_temp(len(fug[4].pointers[1].data), fug[4].pointers[1].data)
				print("gub", gub_d1)
				print("fug0", fug0_d1)
				print("fug1", fug1_d1)
				print("fug2", fug2_d1)
				print("fug3", fug3_d1)
				print("fug4", fug4_d1)
				if fug0_d1[len(fug0_d1) - 1] == 0:
					ss_entry.fragments += self.frags_from_pointer_equalsb_counts(fug[1].pointers[1], len(
						fug0_d1) - 1)  # count equal to len(fug[0].pointers[1].data)/4 -1
					ss_entry.fragments += self.frags_from_pointer_equalsb_counts(fug[2].pointers[1], len(
						fug0_d1) - 1)  # count equal to len(fug[0].pointers[1].data)/4 -1
				else:
					ss_entry.fragments += self.frags_from_pointer_equalsb_counts(fug[1].pointers[1], len(
						fug0_d1))  # count equal to len(fug[0].pointers[1].data)/4 -1
					ss_entry.fragments += self.frags_from_pointer_equalsb_counts(fug[2].pointers[1], len(
						fug0_d1))  # count equal to len(fug[0].pointers[1].data)/4 -1
				if gub_d1[0] == 1638405:
					ss_entry.fragments += self.frags_from_pointer_equalsb_counts(fug[4].pointers[1], 8)
				elif gub_d1[0] == 1966113:
					ss_entry.fragments += self.frags_from_pointer_equalsb_counts(fug[4].pointers[1], 13)
				elif gub_d1[0] == 1966113:
					ss_entry.fragments += self.frags_from_pointer_equalsb_counts(fug[4].pointers[1], 13)

		elif (ssdata[4] == 0) and (ssdata[6] != 0):
			if len(f2_d0) == 4:
				gub = self.frags_from_pointer(ss_entry.pointers[0], 1)
				ss_entry.fragments += gub
			ss_entry.fragments += self.frags_from_pointer(ss_entry.fragments[1].pointers[1], ssdata[6])


		elif (ssdata[4] != 0) and (ssdata[6] != 0):
			if len(f5_d0) == 4:
				gub = self.frags_from_pointer(ss_entry.pointers[0], 1)
				ss_entry.fragments += gub
			ss_entry.fragments += self.frags_from_pointer(ss_entry.fragments[0].pointers[1], ssdata[4])
			if f2_d0[
				2] == 536870911:  # in ("dingo_game.prefab"+"cassowary_game.prefab"+"red_kangaroo_game.prefab"+"koala_game.prefab"):
				ss_entry.fragments += self.frags_from_pointer(ss_entry.fragments[2].pointers[1], 18)
				for x in range(34, 52):
					if x == 34:
						ss_entry.fragments += self.frags_from_pointer_equalsb_counts(ss_entry.fragments[x].pointers[1],
																					 2)
					elif x == 35:
						ss_entry.fragments += self.frags_from_pointer_equalsb_counts(ss_entry.fragments[x].pointers[1],
																					 5)
					elif x == 38:
						ss_entry.fragments += self.frags_from_pointer_equalsb_counts(ss_entry.fragments[x].pointers[1],
																					 3)
					elif x == 41:
						ss_entry.fragments += self.frags_from_pointer_equalsb(ss_entry.fragments[x].pointers[1])
					elif x == 43:
						ss_entry.fragments += self.frags_from_pointer_equalsb_counts(ss_entry.fragments[x].pointers[1],
																					 2)
					elif x == 45:
						ss_entry.fragments += self.frags_from_pointer_equalsb(ss_entry.fragments[x].pointers[1])
					elif x == 47:
						ss_entry.fragments += self.frags_from_pointer_equalsb(ss_entry.fragments[x].pointers[1])
					elif x == 48:
						ss_entry.fragments += self.frags_from_pointer_equalsb(ss_entry.fragments[x].pointers[1])
					elif x == 50:
						ss_entry.fragments += self.frags_from_pointer_equalsb_counts(ss_entry.fragments[x].pointers[1],
																					 2)
					elif x == 51:
						ss_entry.fragments += self.frags_from_pointer_equalsb_counts(ss_entry.fragments[x].pointers[1],
																					 2)
			# elif  f2_d0[2] ==127:
			#	ss_entry.fragments += self.frags_from_pointer(ss_entry.fragments[2].pointers[1], 6)
			# elif  f2_d0[2] ==3:
			#	ss_entry.fragments += self.frags_from_pointer(ss_entry.fragments[2].pointers[1], 1)
			# elif  f2_d0[2] ==63:
			#	ss_entry.fragments += self.frags_from_pointer(ss_entry.fragments[2].pointers[1], 5)
			# elif  f2_d0[2] ==1:
			#	ss_entry.fragments += self.frags_from_pointer(ss_entry.fragments[2].pointers[1], 1)
			# elif  f2_d0[2] ==7:
			#	ss_entry.fragments += self.frags_from_pointer(ss_entry.fragments[2].pointers[1], 4)
			# elif  f2_d0[2] ==15:
			#	ss_entry.fragments += self.frags_from_pointer(ss_entry.fragments[2].pointers[1], 3)
			if len(f5_d0) == 4:
				fug += self.frags_from_pointer_equalsb_counts(ss_entry.fragments[6].pointers[1], 5)
				ss_entry.fragments += fug
				gub_d1 = self.prefab_unpack_temp(len(gub[0].pointers[1].data), gub[0].pointers[1].data)
				fug0_d1 = self.prefab_unpack_temp(len(fug[0].pointers[1].data), fug[0].pointers[1].data)
				fug1_d1 = self.prefab_unpack_temp(len(fug[1].pointers[1].data), fug[1].pointers[1].data)
				fug2_d1 = self.prefab_unpack_temp(len(fug[2].pointers[1].data), fug[2].pointers[1].data)
				fug3_d1 = self.prefab_unpack_temp(len(fug[3].pointers[1].data), fug[3].pointers[1].data)
				fug4_d1 = self.prefab_unpack_temp(len(fug[4].pointers[1].data), fug[4].pointers[1].data)
				print("gub", gub_d1)
				print("fug0", fug0_d1)
				print("fug1", fug1_d1)
				print("fug2", fug2_d1)
				print("fug3", fug3_d1)
				print("fug4", fug4_d1)
				if fug0_d1[len(fug0_d1) - 1] == 0:
					ss_entry.fragments += self.frags_from_pointer_equalsb_counts(fug[1].pointers[1], len(
						fug0_d1) - 1)  # count equal to len(fug[0].pointers[1].data)/4 -1
					ss_entry.fragments += self.frags_from_pointer_equalsb_counts(fug[2].pointers[1], len(
						fug0_d1) - 1)  # count equal to len(fug[0].pointers[1].data)/4 -1
				else:
					ss_entry.fragments += self.frags_from_pointer_equalsb_counts(fug[1].pointers[1], len(
						fug0_d1))  # count equal to len(fug[0].pointers[1].data)/4 -1
					ss_entry.fragments += self.frags_from_pointer_equalsb_counts(fug[2].pointers[1], len(
						fug0_d1))  # count equal to len(fug[0].pointers[1].data)/4 -1
				# if gub_d1[0] == 393217:
				# ss_entry.fragments+=  self.frags_from_pointer_equalsb_counts(fug[4].pointers[1], 0) #count equal to len(fug[0].pointers[1].data)/4 -1
				if gub_d1[0] == 1638405:
					ss_entry.fragments += self.frags_from_pointer_equalsb_counts(fug[4].pointers[1], 8)
				elif gub_d1[0] == 1966113:
					ss_entry.fragments += self.frags_from_pointer_equalsb_counts(fug[4].pointers[1], 13)
				elif gub_d1[0] == 1966113:
					ss_entry.fragments += self.frags_from_pointer_equalsb_counts(fug[4].pointers[1], 13)

			ss_entry.fragments += self.frags_from_pointer(ss_entry.fragments[4].pointers[1], ssdata[6])

		zzz = 0
		# if ss_entry.name in "dingo_game.prefab":
		for fragg in ss_entry.fragments:
			if zzz < 6:
				print("frag" + str(zzz))
				print(self.prefab_unpack_temp(len(fragg.pointers[0].data), fragg.pointers[0].data))
				print(self.prefab_unpack_temp(len(fragg.pointers[1].data), fragg.pointers[1].data))
				zzz += 1

	def collect_scaleform(self, ss_entry, frags):
		ss_entry.fragments = self.get_frags_after_count(frags, ss_entry.pointers[0].address, 1)
		f0_d0 = struct.unpack("<8I", ss_entry.fragments[0].pointers[0].data)
		font_declare_count = f0_d0[2]
		ss_entry.fragments += self.get_frags_after_count(frags, ss_entry.fragments[0].pointers[1].address,
														 font_declare_count * 2)

	def collect_enumnamer(self, ss_entry):
		print("\nENUMNAMER / MOTIONGRAPHVARS:", ss_entry.name)
		# Sized string initpos = position of first fragment
		ss_entry.fragments = self.frags_from_pointer(ss_entry.pointers[0], 1)
		count, _ = struct.unpack("<2I", ss_entry.pointers[0].data)
		# print(count)
		ss_entry.vars = self.frags_from_pointer(ss_entry.fragments[0].pointers[1], count)
		# pointers[1].data is the name
		for var in ss_entry.vars:
			var.pointers[1].strip_zstring_padding()
		# The last fragment has padding that may be junk data to pad the size of the name block to multiples of 64
		ss_entry.fragments.extend(ss_entry.vars)

	def collect_wmeta(self, ss_entry, address_0_fragments):
		print("\nwmeta:", ss_entry.name)
		return
		# Sized string initpos = position of first fragment
		ss_entry.fragments = self.frags_from_pointer(ss_entry.pointers[0], 1)
		f = ss_entry.fragments[0]
		# print(f.pointers[0].data, f.pointers[0].address, len(f.pointers[0].data), len(ss_entry.pointers[0].data))
		_, count = struct.unpack("<2Q", ss_entry.pointers[0].data)
		print(count)
		if self.ovl.basename.lower() == "main.ovl":
			print("Debug mode for sound")
			print()
			for frag in self.fragments:
				if 4233228 <= frag.pointers[1].address < 4234772 or 2257932 <= frag.pointers[1].address < 4219472:
					# ss_entry.fragments.append(frag)
					frag.pointers[1].strip_zstring_padding()
					frag.name = frag.pointers[1].data[:-1]  # .decode()

		ss_entry.bnks = []
		# for bnk_index in range(count):
		# ss_entry.bnks = self.frags_from_pointer(ss_entry.fragments[0].pointers[1], 4*count)
		# ss_entry.fragments.extend(ss_entry.bnks)
		# for i in range(count):
		# 	fs = ss_entry.bnks[i*4: i*4+4]
		# 	for f in fs[:3]:
		# 		f.pointers[1].strip_zstring_padding()
		# 	print(fs[0].pointers[1].data)
		# 	print(fs[1].pointers[1].data)
		# 	for f in fs:
		# 		print(f.pointers[0].data)
		for i in range(count):
			print(f"\n\nbnk {i}")
			bnk = self.frags_accumulate(ss_entry.fragments[0].pointers[1], 112, address_0_fragments)
			# if bnk[3].pointers[0].data_size == 64:
			# 	bnk.extend(self.frags_from_pointer(ss_entry.fragments[0].pointers[1], 1))
			for f in bnk[:3]:
				f.pointers[1].strip_zstring_padding()
				print(f.pointers[1].data)
				f.name = f.pointers[1].data[:-1]  # .decode()
			# 	 if it's a media bnk like for the dinos, it has a pointer pointing to the start of the files that belong to this
			if len(bnk) > 3:
				b = bnk[3].pointers[0].data
				# this points to the child data
				ptr = bnk[3].pointers[1]
				if len(b) == 56:
					d = struct.unpack("<6Q2I", b)
					media_count = d[1]
					maybe_hash = d[6]
					print(f.name, media_count, maybe_hash, ptr.address)
					bk_frags = self.frags_from_pointer(ptr, media_count * 3)
					for j in range(media_count):
						z = bk_frags[j*3: j*3+3]
						for f in z:
							f.pointers[1].strip_zstring_padding()
							print(f.pointers[1].data)
			ss_entry.bnks.append(bnk)

	# ss_entry.fragments.extend(bnk)

	# ss_entry.vars = self.frags_from_pointer(ss_entry.fragments[0].pointers[1], count)
	# # pointers[1].data is the name
	# for var in ss_entry.vars:
	# 	var.pointers[1].strip_zstring_padding()
	# # The last fragment has padding that may be junk data to pad the size of the name block to multiples of 64
	# ss_entry.fragments.extend(ss_entry.vars)

	def collect_motiongraph(self, ss_entry):
		print("\nMOTIONGRAPH:", ss_entry.name)
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

	def collect_matcol(self, ss_entry):
		print("\nMATCOL:", ss_entry.name)

		# Sized string initpos = position of first fragment for matcol
		# input_frags = self.frags_for_pointer(ss_entry.pointers[0])
		# ss_entry.fragments = self.get_frag_after(input_frags, ((4,4),), ss_entry.pointers[0].address)
		ss_entry.fragments = self.frags_from_pointer(ss_entry.pointers[0], 1)
		ss_entry.f0 = ss_entry.fragments[0]

		# print(ss_entry.f0)
		# 0,0,collection count,0
		f0_d0 = struct.unpack("<4I", ss_entry.f0.pointers[0].data)
		# flag (3=variant, 2=layered) , 0
		ss_entry.has_texture_list_frag = len(ss_entry.f0.pointers[1].data) == 8
		if ss_entry.has_texture_list_frag:
			f0_d1 = struct.unpack("<2I", ss_entry.f0.pointers[1].data)
		else:
			f0_d1 = struct.unpack("<6I", ss_entry.f0.pointers[1].data)
		# print("f0_d0", f0_d0)
		# print("f0_d1", f0_d1)
		ss_entry.is_variant = f0_d1[0] == 3
		ss_entry.is_layered = f0_d1[0] == 2
		# print("has_texture_list_frag",ss_entry.has_texture_list_frag)
		# print("is_variant",ss_entry.is_variant)
		# print("is_layered",ss_entry.is_layered)
		# print(ss_entry.tex_pointer)
		if ss_entry.has_texture_list_frag:
			# input_frags = self.frags_for_pointer(ss_entry.f0.pointers[1])
			# ss_entry.tex_pointer = self.get_frag_after(input_frags, ((4,4),), ss_entry.f0.pointers[1].address)[0]
			ss_entry.tex_pointer = self.frags_from_pointer(ss_entry.f0.pointers[1], 1)[0]
			tex_pointer_d0 = struct.unpack("<4I", ss_entry.tex_pointer.pointers[0].data)
			# print("tex_pointer_d0", tex_pointer_d0)
			tex_count = tex_pointer_d0[2]
			# print("tex_count",tex_count)
			ss_entry.tex_frags = self.frags_from_pointer(ss_entry.tex_pointer.pointers[1], tex_count * 3)
		# ss_entry.tex_frags = []
		# input_frags = self.frags_for_pointer(ss_entry.tex_pointer.pointers[1])
		# for t in range(tex_count):
		#	 ss_entry.tex_frags += self.get_frag_after(input_frags, ((4,6),(4,6),(4,6)), ss_entry.tex_pointer.pointers[1].address)
		# for tex in ss_entry.tex_frags:
		#	 print(tex.pointers[1].data)
		else:
			ss_entry.tex_pointer = None
		# material pointer frag
		ss_entry.mat_pointer = self.frags_from_pointer(ss_entry.f0.pointers[1], 1)[0]
		# ss_entry.mat_pointer_frag = self.get_frag_after(address_0_fragments, ((4,4),), ss_entry.f0.pointers[1].address)
		# ss_entry.mat_pointer = ss_entry.mat_pointer_frag[0]
		mat_pointer_d0 = struct.unpack("<6I", ss_entry.mat_pointer.pointers[0].data)
		# print("mat_pointer_d0",mat_pointer_d0)
		mat_count = mat_pointer_d0[2]
		# print("mat_count",mat_count)
		ss_entry.mat_frags = []
		for t in range(mat_count):
			if ss_entry.is_variant:
				m0 = self.frags_from_pointer(ss_entry.mat_pointer.pointers[1], 1)[0]
				# m0 = self.get_frag_after(address_0_fragments, ((4,6),), ss_entry.mat_pointer.pointers[1].address)[0]
				# print(m0.pointers[1].data)
				m0.name = ss_entry.name
				ss_entry.mat_frags.append((m0,))
			elif ss_entry.is_layered:
				mat_frags = self.frags_from_pointer(ss_entry.mat_pointer.pointers[1], 3)
				# mat_frags = self.get_frag_after(address_0_fragments, ((4,6),(4,4),(4,4)), ss_entry.mat_pointer.pointers[1].address)

				m0, info, attrib = mat_frags
				m0.pointers[1].strip_zstring_padding()
				# print(m0.pointers[1].data)

				info_d0 = struct.unpack("<8I", info.pointers[0].data)
				info_count = info_d0[2]
				# print("info_count", info_count)
				info.children = self.frags_from_pointer(info.pointers[1], info_count)
				for info_child in info.children:
					# info_child = self.get_frag_after(address_0_fragments, ((4,6),), info.pointers[1].address)[0]
					# 0,0,byte flag,byte flag,byte flag,byte flag,float,float,float,float,0
					# info_child_d0 = struct.unpack("<2I4B4fI", info_child.pointers[0].data)
					info_child.pointers[1].strip_zstring_padding()
				# print(info_child.pointers[1].data, info_d0)

				attrib.children = []
				attrib.pointers[0].split_data_padding(16)
				attrib_d0 = struct.unpack("<4I", attrib.pointers[0].data)
				attrib_count = attrib_d0[2]
				# print("attrib_count",attrib_count)
				attrib.children = self.frags_from_pointer(attrib.pointers[1], attrib_count)
				for attr_child in attrib.children:
					# attr_child = self.get_frag_after(address_0_fragments, ((4,6),), attrib.pointers[1].address)[0]
					# attrib.children.append(attr_child)
					# attr_child_d0 = struct.unpack("<2I4BI", attr_child.pointers[0].data)
					attr_child.pointers[1].strip_zstring_padding()
				# print(attr_child.pointers[1].data, attr_child_d0)

				# store names for frag log
				for frag in mat_frags + info.children + attrib.children:
					frag.name = ss_entry.name
				# store frags
				ss_entry.mat_frags.append(mat_frags)
		if ss_entry.has_texture_list_frag:
			for frag in ss_entry.tex_frags + [ss_entry.tex_pointer, ]:
				frag.name = ss_entry.name
		all_frags = [ss_entry.f0, ss_entry.mat_pointer]
		for frag in all_frags:
			frag.name = ss_entry.name

	def map_frags(self):
		if not self.fragments:
			return
		print(f"\nMapping SizedStrs to {len(self.fragments)} Fragments")

		# we go from the start
		address_0_fragments = list(sorted(self.fragments, key=lambda f: f.pointers[0].address))

		# just reverse is good enough, no longer need to sort them
		sorted_sized_str_entries = list(reversed(self.sized_str_entries))
		for frag in address_0_fragments:
			# fragments always have a valid pool_index
			self.pools[frag.pointers[0].pool_index].fragments.append(frag)

		# todo: document more of these type requirements
		dic = {".bani": 1,
			   ".tex": 2,
			   ".xmlconfig": 1,
			   # ".hier": ( (4,6) for x in range(19) ),
			   ".spl": 1,
			   # ".world": will be a variable length one with a 4,4; 4,6; then another variable length 4,6 set : set world before assetpkg in order
			   }
		# include formats that are known to have no fragments
		no_frags = (".txt", ".mani", ".manis",)
		ss_max = len(sorted_sized_str_entries)
		try:
			for ss_index, sized_str_entry in enumerate(sorted_sized_str_entries):
				self.ovl.print_and_callback("Collecting fragments", value=ss_index, max_value=ss_max)
				if sized_str_entry.ext in no_frags:
					continue
				print(f"Collecting fragments for {sized_str_entry.name} at {sized_str_entry.pointers[0].address}")
				pool_index = sized_str_entry.pointers[0].pool_index
				if pool_index == -1:
					frags = address_0_fragments
				else:
					frags = self.pools[pool_index].fragments
				if sized_str_entry.ext == ".tex" and (is_pc(self.ovl) or is_ztuac(self.ovl)):
					sized_str_entry.fragments = self.get_frags_after_count(frags, sized_str_entry.pointers[0].address,
																		   1)
				# get fixed fragments
				elif sized_str_entry.ext in dic:

					t = dic[sized_str_entry.ext]
					# get and set fragments
					try:
						sized_str_entry.fragments = self.get_frags_after_count(frags,
																			   sized_str_entry.pointers[0].address, t)
					except:
						print("bug")
						pass
				elif sized_str_entry.ext == ".fgm":
					sized_str_entry.fragments = self.get_frag_after_terminator(frags,
																			   sized_str_entry.pointers[0].address)

				elif sized_str_entry.ext == ".materialcollection":
					self.collect_matcol(sized_str_entry)
				elif sized_str_entry.ext in (".enumnamer", ".motiongraphvars"):
					self.collect_enumnamer(sized_str_entry)
				elif sized_str_entry.ext in (".wmetasb",):  # ".wmetarp", ".wmetasf"):
					self.collect_wmeta(sized_str_entry, address_0_fragments)
				elif sized_str_entry.ext == ".motiongraph":
					self.collect_motiongraph(sized_str_entry)
				elif sized_str_entry.ext == ".specdef":
					self.collect_specdef(sized_str_entry)
				elif sized_str_entry.ext == ".scaleformlanguagedata":
					if not is_pc(self.ovl):
						# todo - this is different for PC
						self.collect_scaleform(sized_str_entry, frags)
			# elif sized_str_entry.ext == ".prefab":
			# self.collect_prefab(sized_str_entry, address_0_fragments)
			# print("sizedstr",sized_str_entry.pointers[0].pool_index)
			# print("frags",tuple((f.pointers[0].pool_index, f.pointers[1].pool_index) for f in sized_str_entry.fragments))
			# for f in sized_str_entry.fragments:
			#	 assert(f.pointers[0].pool_index == sized_str_entry.pointers[0].pool_index)
		except Exception as err:
			print(err)

	def assign_frag_names(self):
		# for debugging only:
		for sized_str_entry in self.sized_str_entries:
			for frag in sized_str_entry.model_data_frags + sized_str_entry.fragments:
				frag.name = sized_str_entry.name

	def map_buffers(self):
		"""Map buffers to data entries"""
		print("\nMapping buffers")
		# sequentially attach buffers to data entries by each entry's buffer count
		buff_ind = 0
		for i, data in enumerate(self.data_entries):
			data.buffers = []
			for j in range(data.buffer_count):
				# print("data",i,"buffer",j, "buff_ind",buff_ind)
				buffer = self.buffer_entries[buff_ind]
				# also give each buffer a reference to data so we can access it later
				buffer.data_entry = data
				data.buffers.append(buffer)
				buff_ind += 1
			data.streams = list(data.buffers)

	@property
	def buffers_io_order(self):
		"""sort buffers into load order"""
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
		print("\nReading from buffers")
		# stream.seek(self.start_of_pools + self.check_pool_size)
		for buffer in self.buffers_io_order:
			# read buffer data and store it in buffer object
			buffer.read_data(stream)

	@staticmethod
	def get_ptr_debug_str(entry, ind):
		# return f"{' '.join((f'[{p.address} {p.data_size}]' for p in entry.pointers))} {ind} {entry.name}"
		return f"{' '.join((f'[{p.pool_index} {p.data_offset} | {p.address} {p.data_size}]' for p in entry.pointers))} ({ind}) {entry.name}"

	def write_frag_log(self, ):
		"""for development; collect info about fragment types"""
		frag_log_path = os.path.join(self.ovl.dir, f"{self.ovl.basename}_frag{self.archive_index}.log")
		print(f"Writing Fragment log to {frag_log_path}")
		with open(frag_log_path, "w") as f:
			for i, pool in enumerate(self.pools):
				f.write(f"\n\nHeader[{i}] at {pool.address} with {len(pool.fragments)} fragments\n")
				entries = pool.fragments + [ss for ss in self.sized_str_entries if ss.pointers[0].pool_index == i]
				entries.sort(key=lambda entry: entry.pointers[0].data_offset)
				lines = [self.get_ptr_debug_str(frag, j) for j, frag in enumerate(entries)]
				f.write("\n".join(lines))
			f.write("\n\n\nself.fragments > sizedstr\nfragments in file order\n")
			lines = [self.get_ptr_debug_str(frag, j) for j, frag in enumerate(self.fragments)]
			f.write("\n".join(lines))

	@staticmethod
	def get_frag_after_terminator(l, initpos, terminator=24):
		"""Returns entries of l matching h_types that have not been processed until it reaches a frag of terminator size."""
		out = []
		# print("looking for",h_types)
		for f in l:
			# can't add fragments that have already been added elsewhere
			if f.done:
				continue
			if f.pointers[0].address >= initpos:
				# print(f.data_offset_0,"  ",initpos)
				f.done = True
				out.append(f)
				if f.pointers[0].data_size == terminator:
					break
		else:
			raise AttributeError(
				f"Could not find a terminator fragment matching initpos {initpos} and pointer[0].size {terminator}")
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
			if f.pointers[0].address >= initpos:
				f.done = True
				out.append(f)
		else:
			if len(out) != count:
				raise AttributeError(
					f"Could not find {count} fragments after initpos {initpos}, only found {len(out)}!")
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
				if (f.pointers[0].address == initpos):
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
	def get_frags_til_discon(frags, initpos, datalength):
		"""Returns entries of frags that have not been processed and until discontinuity."""
		out = []
		lastpos = initpos
		length = 0
		firstgrab = 1
		for f in frags:
			if firstgrab == 1:
				if f.done:
					continue
				if (f.pointers[0].address == initpos) or (f.pointers[0].address == initpos + datalength):
					f.done = True
					out.append(f)
					firstgrab = 0
					length = len(f.pointers[0].data)
					lastpos = f.pointers[0].address
					print("first ", initpos, length, lastpos)
			else:
				if f.pointers[0].address - length == lastpos:
					if f.done:
						continue
					if f.pointers[0].address >= initpos:
						f.done = True
						out.append(f)
						length = len(f.pointers[0].data)
						lastpos = f.pointers[0].address
				else:
					break
		return out

	def find_entry(self, entries, src_entry):
		""" returns entry from list l whose file hash matches hash, or none"""
		for entry in entries:
			if entry.name == src_entry.name:
				return entry

	def assign_name(self, entry):
		"""Fetch a filename for an entry"""
		n = "NONAME"
		e = ".UNK"
		# JWE style
		if self.ovl.user_version.is_jwe:
			try:
				n = self.ovl.hash_table_local[entry.file_hash]
				e = self.ovl.hash_table_local[entry.ext_hash]
			except KeyError:
				raise KeyError(
					f"No match for entry!\n{entry}")
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
		return self.start_of_pools + self.calc_pools_size() + self.calc_buffers_size()

	def calc_pools_size(self, ):
		"""Calculate the size of the whole memory pool region that sizedstr, fragment and ovl dependency entries point into"""
		return sum(pool.size for pool in self.pools)

	def calc_buffers_size(self, ):
		"""Calculate the size of the buffer region that data entries use"""
		return sum(buffer.size for buffer in self.buffer_entries)

	def write_pointers_to_pools(self, ignore_unaccounted_bytes=False):
		"""Pre-writing step to convert all edits that were done on individual points back into the consolidated header data io blocks"""
		for i, pool in enumerate(self.pools):
			# maintain sorting order
			# grab the first pointer for each address
			# it is assumed that subsequent pointers to that address share the same data
			sorted_first_pointers = [pointers[0] for offset, pointers in sorted(pool.pointer_map.items())]
			if sorted_first_pointers:
				# only known from indominus
				first_offset = sorted_first_pointers[0].data_offset
				if first_offset != 0 and not ignore_unaccounted_bytes:
					print(f"Found {first_offset} unaccounted bytes at start of header data {i}")
					unaccounted_bytes = pool.data.getvalue()[:first_offset]
				else:
					unaccounted_bytes = b""

				# clear io objects
				pool.data = io.BytesIO()
				pool.data.write(unaccounted_bytes)
				# write updated strings
				for pointer in sorted_first_pointers:
					pointer.write_data(self, update_copies=True)
			else:
				print(f"No pointers into header entry {i} - keeping its stock data!")

	def write_pools(self):
		logging.debug(f"Writing pools for {self.arg.name}")
		if self.force_update_pools:
			self.write_pointers_to_pools()
		# do this first so pools can be updated
		pools_data_writer = io.BytesIO()
		# the ugly stuff with all fragments and sizedstr entries
		for pool in self.pools:
			pool_bytes = pool.data.getvalue()
			# JWE style stores relative offset for each pool
			if is_jwe(self.ovl):
				pool.offset = pools_data_writer.tell()
			# PZ, PC Style has offsets relative to the whole pool block
			else:
				pool.offset = self.arg.pools_start + pools_data_writer.tell()
			logging.debug(f"header.offset {pool.offset}, pools_start {self.arg.pools_start}")
			pool.size = len(pool_bytes)
			pools_data_writer.write(pool_bytes)
		self.pools_data = pools_data_writer.getvalue()

	def write_archive(self, stream):
		logging.debug(f"Writing archive {self.arg.name}")
		# write out all entries
		super().write(stream)
		# write the header data containing all the pointers' datas
		stream.write(self.pools_data)
		# write buffer data
		for b in self.buffers_io_order:
			stream.write(b.data)


class OvlFile(Header, IoFile):

	def __init__(self, progress_callback=None):
		super().__init__()

		self.last_print = None
		if progress_callback:
			self.progress_callback = progress_callback
		else:
			self.progress_callback = self.dummy_callback

	def extract(self, out_dir, only_names=(), only_types=(), show_temp_files=False):
		"""Extract the files, after all archives have been read"""
		# create output dir
		print(f"Extracting from {len(self.files)} files...")
		from modules.extract import IGNORE_TYPES, extract_kernel
		os.makedirs(out_dir, exist_ok=True)

		def out_dir_func(n):
			"""Helper function to generate temporary output file name"""
			return os.path.normpath(os.path.join(out_dir, n))

		# the actual export, per file type
		error_files = []
		skip_files = []
		out_paths = []
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
			if file.ext in IGNORE_TYPES:
				continue
			extract_files.append(file)
		for ss_index, file in enumerate(extract_files):
			self.progress_callback("Extracting...", value=ss_index, vmax=len(extract_files))
			sized_str_entry = self.ss_dict[file.name]
			try:
				out_paths.extend(
					extract_kernel(self, sized_str_entry, out_dir_func, show_temp_files, self.progress_callback))

			except BaseException as error:
				print(f"\nAn exception occurred while extracting {sized_str_entry.name}")
				print(error)
				traceback.print_exc()
				error_files.append(sized_str_entry.name)
		self.progress_callback("Extraction completed!", value=1, vmax=1)

		return out_paths, error_files, skip_files

	def create(self, ovl_dir, mime_names_dict):
		print(f"Creating OVL from {ovl_dir}")
		print(f"Game: {get_game(self)}")
		# map all files in ovl_dir by their extension
		files_by_extension = {}
		for file_name in os.listdir(ovl_dir):
			file_name_bare, file_ext = os.path.splitext(file_name)
			file_path = os.path.join(ovl_dir, file_name)
			if file_ext not in files_by_extension:
				files_by_extension[file_ext] = []
			files_by_extension[file_ext].append(file_path)

		file_index_offset = 0
		for file_ext, file_paths in sorted(files_by_extension.items()):
			if file_ext not in mime_names_dict:
				logging.warning(f"Ignoring extension {file_ext}")
				continue
			mime_entry = MimeEntry()
			mime_entry.name = mime_names_dict[file_ext]
			mime_entry.ext = file_ext
			# update offset using the name buffer
			if is_jwe(self):
				mime_entry.mime_hash = lut_mime_hash_jwe.get(file_ext)
				mime_entry.version = lut_mime_version_jwe.get(file_ext)
			elif is_pz(self):
				mime_entry.mime_hash = lut_mime_hash_pz.get(file_ext)
				mime_entry.version = lut_mime_version_pz.get(file_ext)
			else:
				raise ValueError(f"Unsupported game {get_game(self)}")
			mime_entry.file_index_offset = file_index_offset
			mime_entry.file_count = len(file_paths)
			file_index_offset += len(file_paths)

			for file_path in file_paths:
				file_entry = FileEntry()
				filename = os.path.basename(file_path)
				file_entry.path = file_path
				file_entry.name = filename
				file_entry.basename, file_entry.ext = os.path.splitext(filename)
				file_entry.unkn_0 = lut_file_unk_0[file_ext]
				file_entry.unkn_1 = lut_file_unk_1.get(file_ext, 0)
				file_entry.extension = len(self.mimes)
				self.files.append(file_entry)
			self.mimes.append(mime_entry)

		# update ovl stuff
		self.fres.data = b"FRES"
		self.archive_names.data = b'STATIC\x00\x00'

		self.update_hashes()
		# sort the different lists according to the criteria specified
		self.files.sort(key=lambda x: (x.ext, x.file_hash))
		# nope they are not sorted by hash
		# self.dependencies.sort(key=lambda x: x.file_hash)

		archive_entry = ArchiveEntry()
		self.archives.append(archive_entry)

		content = OvsFile(self, archive_entry, 0)
		content.create()
		archive_entry.content = content
		archive_entry.name = "STATIC"
		archive_entry.offset = 0
		archive_entry.pools_offset = 0
		archive_entry.ovs_file_offset = 0
		archive_entry.ovs_offset = 0

		new_zlib = ZlibInfo()
		self.zlibs.append(new_zlib)

		self.update_ss_dict()
		self.update_hashes()

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
		if not self.mute:
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
		new_directory = DirEntry()
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
		self.names.update_with((
			(self.dependencies, "ext"),
			(self.dirs, "basename"),
			(self.mimes, "name"),
			(self.files, "basename")
		))
		self.len_names = len(self.names.data)
		self.len_archive_names = len(self.archive_names.data)

		# catching ovl files without entries, default len_type_names is 0
		if len(self.files) > 0:
			self.len_type_names = min(file.offset for file in self.files)

	def load(self, filepath, verbose=0, commands=(), mute=False, hash_table={}):
		start_time = time.time()
		self.eof = super().load(filepath)
		logging.info(f"Game: {get_game(self)}")

		# store commands
		self.commands = commands
		self.mute = mute
		self.store_filepath(filepath)

		# maps OVL hash to final filename + extension
		self.hash_table_local = {}
		self.hash_table_global = hash_table

		# add extensions to hash dict
		hm_max = len(self.mimes)
		for hm_index, mime_entry in enumerate(self.mimes):
			self.print_and_callback("Adding extensions to hash dict", value=hm_index, max_value=hm_max)
			# get the whole mime type string
			mime_entry.name = self.names.get_str_at(mime_entry.offset)
			# only get the extension
			mime_entry.ext = f".{mime_entry.name.split(':')[-1]}"
			logging.debug(f'"{mime_entry.ext}": {mime_entry.mime_hash},')
			logging.debug(f'"{mime_entry.ext}": {mime_entry.version},')
			# the stored mime hash is not used anywhere
			# self.hash_table_local[mime_entry.mime_hash] = mime_type
			# instead we must calculate the DJB hash of the extension and store that
			# because this is how we find the extension from inside the archive
			self.hash_table_local[djb(mime_entry.ext[1:])] = mime_entry.ext

		# add file name to hash dict; ignoring the extension pointer
		hf_max = len(self.files)
		for hf_index, file_entry in enumerate(self.files):
			self.print_and_callback("Adding file names to hash dict", value=hf_index, max_value=hf_max)
			# get file name from name table
			file_name = self.names.get_str_at(file_entry.offset)
			file_entry.ext = self.mimes[file_entry.extension].ext
			logging.debug(f'"{file_entry.ext}": {file_entry.unkn_0},')
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
				logging.debug(f"LOCAL: {h} -> {dependency_entry.basename}")
			elif h in self.hash_table_global:
				dependency_entry.basename = self.hash_table_global[h]
				logging.debug(f"GLOBAL: {h} -> {dependency_entry.basename}")
			else:
				logging.debug(f"UNRESOLVED DEPENDENCY: {h} -> ?")
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
		logging.info(f"Loaded OVL in {time.time() - start_time:.2f} seconds!")

	def load_headers(self):
		self.pools = [None for _ in range(self.num_pools)]
		for archive_entry in self.archives:
			if archive_entry.num_pools:
				self.pools[archive_entry.pools_offset: archive_entry.pools_offset + archive_entry.num_pools] = archive_entry.content.pools

	def load_archives(self):
		logging.info("Loading archives...")
		start_time = time.time()
		self.open_ovs_streams(mode="rb")
		for archive_index, archive_entry in enumerate(self.archives):
			self.print_and_callback(f"Reading archive {archive_entry.name}", value=archive_index, max_value=len(self.archives))
			# those point to external ovs archives
			if archive_entry.name == "STATIC":
				read_start = self.eof
			else:
				read_start = archive_entry.read_start
			archive_entry.content = OvsFile(self, archive_entry, archive_index)
			try:
				archive_entry.content.unzip(archive_entry, read_start)
			except BaseException as err:
				logging.error(f"Unzipping of {archive_entry.name} from {archive_entry.ovs_path} failed")
				logging.error(err)
				traceback.print_exc()
		self.close_ovs_streams()
		self.update_ss_dict()
		self.link_streams()
		self.load_headers()
		self.load_file_classes()

		if "write_frag_log" in self.commands:
			for archive_entry in self.archives:
				archive_entry.content.assign_frag_names()
				archive_entry.content.write_frag_log()
				archive_entry.content.debug_txt_data()
		logging.info(f"Loaded Archives in {time.time() - start_time:.2f} seconds!")

	def load_file_classes(self):
		logging.info("Loading file classes...")
		for file in self.files:
			loader = get_loader(file.ext)
			if loader:
				try:
					loader.collect(self, file)
				except Exception as err:
					logging.error(err)

	def update_ss_dict(self):
		"""Stores a reference to each sizedstring entry in a dict so they can be extracted"""
		logging.info("Updating the entry dict...")
		self.ss_dict = {}
		for archive_index, archive_entry in enumerate(self.archives):
			for file in archive_entry.content.sized_str_entries:
				self.ss_dict[file.name] = file

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
			if is_jwe(self):
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
		# adjust the counts
		for archive in self.archives:
			archive.content.update_counts()
			archive.content.update_assets()

		# sum content of individual archives
		self.num_pool_types = sum(a.num_pool_types for a in self.archives)
		self.num_pools = sum(a.num_pools for a in self.archives)
		self.num_datas = sum(a.num_datas for a in self.archives)
		self.num_buffers = sum(a.num_buffers for a in self.archives)

		self.num_dirs = len(self.dirs)
		self.num_files = self.num_files_2 = self.num_files_3 = len(self.files)
		self.num_dependencies = len(self.dependencies)
		self.num_mimes = len(self.mimes)
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

	def save(self, filepath, dat_path):
		logging.info("Writing OVL")
		self.store_filepath(filepath)
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
			archive_entry.uncompressed_size, archive_entry.compressed_size, compressed = archive_entry.content.zipper(i, dat_path)
			# update set data size
			archive_entry.set_data_size = archive_entry.content.set_header.io_size
			if i == 0:
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
			name = self.files[aux.file_index].basename
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
