import logging
import os
import struct
import time
import zlib
from contextlib import contextmanager
from io import BytesIO

from generated.formats.ovl.compounds.ArchiveEntry import ArchiveEntry
from generated.formats.ovl.compounds.AssetEntry import AssetEntry
from generated.formats.ovl.compounds.BufferGroup import BufferGroup
from generated.formats.ovl.compounds.FileEntry import FileEntry
from generated.formats.ovl.compounds.Fragment import Fragment
from generated.formats.ovl.compounds.Header import Header
from generated.formats.ovl.compounds.OvsHeader import OvsHeader
from generated.formats.ovl.compounds.SetEntry import SetEntry
from generated.formats.ovl.compounds.StreamEntry import StreamEntry
from generated.formats.ovl.compounds.ZlibInfo import ZlibInfo
from generated.formats.ovl.versions import *
from generated.formats.ovl_base.enums.Compression import Compression
from generated.io import IoFile
from modules.formats.formats_dict import FormatDict
from modules.formats.shared import djb2
from ovl_util.oodle.oodle import OodleDecompressEnum, oodle_compressor
from root_path import root_dir

UNK_HASH = "Unknown Hash"
OODLE_MAGIC = (b'\x8c', b'\xcc')
TAB = '  '


class DummySignal:

	def emit(self, val):
		logging.debug(f"Emitted {val}")

	def connect(self, func):
		pass


class OvsFile(OvsHeader):

	def __init__(self, context, ovl_inst, archive_entry):
		# init with a dummy default archive
		dummy_archive = ArchiveEntry(context, None, None)
		super().__init__(context, dummy_archive, None)
		self.ovl = ovl_inst
		# set arg later to avoid initializing huge arrays with default data
		self.arg = archive_entry

	def clear_ovs_arrays(self):
		self.pool_groups.clear()
		self.fragments.clear()
		self.root_entries.clear()
		self.data_entries.clear()
		self.buffer_entries.clear()
		self.buffer_groups.clear()

	@contextmanager
	def unzipper(self, compressed_bytes, uncompressed_size):
		start_time = time.time()
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
		# not relevant for user info since it is usually 0.00 sec
		# logging.info(f"Decompressed in {time.time() - start_time:.2f} seconds")
		with BytesIO(decompressed) as stream:
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
		entry_lists = (
			self.pools,
			self.root_entries,
			self.data_entries,
			# self.set_header.sets,
			# self.set_header.assets,
			# self.buffer_entries
		)
		# update references to ovl files
		for entry_list in entry_lists:
			for entry in entry_list:
				if not entry.name:
					logging.warning(f"{entry} has no name assigned to it, cannot assign proper ID")
					continue
				if entry.name in file_name_lut:
					file_index = file_name_lut[entry.name]
				else:
					logging.debug(file_name_lut)
					# raise KeyError
					logging.warning(
						f"Can't find '{entry.name}' [{entry.__class__.__name__}] in name LUT, cannot update hash")
					continue
				file = self.ovl.files[file_index]
				if self.ovl.user_version.use_djb:
					entry.file_hash = file.file_hash
				else:
					entry.file_hash = file_index
				entry.ext_hash = file.ext_hash

	def unzip(self, archive_entry, start):
		filepath = archive_entry.ovs_path
		stream = self.ovl.ovs_dict[filepath]
		stream.seek(start)
		logging.info(
			f"Compressed stream {archive_entry.name} in {os.path.basename(filepath)} starts at {stream.tell()}")
		compressed_bytes = stream.read(archive_entry.compressed_size)
		with self.unzipper(compressed_bytes, archive_entry.uncompressed_size) as stream:
			start_time = time.time()
			super().read_fields(stream, self)
			logging.info(f"Read decompressed stream in {time.time() - start_time:.2f} seconds")
			# print(self)
			pool_index = 0
			for pool_type in self.pool_groups:
				for i in range(pool_type.num_pools):
					pool = self.pools[pool_index]
					pool.type = pool_type.type
					self.assign_name(pool)
					pool_index += 1

			for data_entry in self.data_entries:
				self.assign_name(data_entry)
				loader = self.ovl.loaders[data_entry.name]
				loader.data_entries[archive_entry.name] = data_entry
			for root_entry in self.root_entries:
				self.assign_name(root_entry)
				# store ovs and root_entry on loader
				loader = self.ovl.loaders[root_entry.name]
				loader.root_entry = root_entry
				loader.ovs = self

			if not (self.set_header.sig_a == 1065336831 and self.set_header.sig_b == 16909320):
				raise AttributeError("Set header signature check failed!")
			if self.set_header.io_size != self.arg.set_data_size:
				raise AttributeError(
					f"Set data size incorrect (got {self.set_header.io_size}, expected {self.arg.set_data_size})!")
			for set_entry in self.set_header.sets:
				self.assign_name(set_entry)
			for asset_entry in self.set_header.assets:
				self.assign_name(asset_entry)
			self.map_assets()
			# add IO object to every pool
			self.read_pools(stream)
			self.map_buffers()
			for buffer in self.buffers_io_order:
				# read buffer data and store it in buffer object
				buffer.read_data(stream)

	def read_pools(self, stream):
		for pool in self.pools:
			pool.data = BytesIO(stream.read(pool.size))

	def map_assets(self):
		"""Parse set and asset entries, and store children on loaders"""
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
			logging.debug(f"Set {set_entry.name} with {len(assets)} assets")
			# store the references on the corresponding loader
			loader = self.ovl.loaders[set_entry.name]
			loader.children = [self.ovl.loaders[self.root_entries[a.file_index].name] for a in assets]

	@staticmethod
	def transfer_identity(source_entry, target_entry):
		source_entry.basename, source_entry.ext = os.path.splitext(target_entry.name)
		source_entry.name = target_entry.name
		source_entry.file_hash = target_entry.file_hash
		source_entry.ext_hash = target_entry.ext_hash

	def rebuild_assets(self):
		"""Update archive asset grouping from children list on root_entries"""
		logging.info(f"Updating assets for {self.arg.name}")
		self.set_header.sets.clear()
		self.set_header.assets.clear()
		self.set_header.set_count = 0
		self.set_header.asset_count = 0
		start = 0
		root_entry_lut = {file.name: i for i, file in enumerate(self.root_entries)}
		for loader in self.ovl.loaders.values():
			if loader.ovs == self:
				if loader.children:
					set_entry = SetEntry(self.context)
					set_entry.start = start
					set_entry.end = start + len(loader.children)
					self.transfer_identity(set_entry, loader.root_entry)
					self.set_header.sets.append(set_entry)
					for child_loader in loader.children:
						asset_entry = AssetEntry(self.context)
						asset_entry.file_index = root_entry_lut[child_loader.root_entry.name]
						self.transfer_identity(asset_entry, child_loader.root_entry)
						self.set_header.assets.append(asset_entry)
					start += len(loader.children)
					self.set_header.set_count += 1
					self.set_header.asset_count += len(loader.children)
					# set_index is 1-based, so the first set = 1, so we do it after the increment
					loader.data_entry.set_index = self.set_header.set_count

	def rebuild_buffer_groups(self, mime_lut):
		logging.info(f"Updating buffer groups for {self.arg.name}")
		if self.data_entries:
			for data_entry in self.data_entries:
				for buffer in data_entry.buffers:
					self.transfer_identity(buffer, data_entry)
				# to ensure that the io order matches, sort buffers per data too, as that will influence the order
				if self.ovl.version < 20:
					data_entry.buffers.sort(key=lambda b: b.index)
			# sort buffers
			if self.ovl.version < 20:
				# rely on the data_entry's hashes for sorting for JWE1
				# sorting by index is not enforced in JWE1 stock
				self.buffer_entries.sort(key=lambda b: (b.ext, b.file_hash, b.index))
			else:
				# cobra < 20 used buffer index per data entry
				self.buffer_entries.sort(key=lambda b: (b.ext, b.index, b.file_hash))

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
		# update buffer groups
		for buffer_group in self.buffer_groups:
			buffer_group.ext_index = mime_lut.get(buffer_group.ext)

	def rebuild_pools(self):
		logging.info("Updating pool names, deleting unused pools")
		# map the pool types to pools
		pools_by_type = {}
		for pool_index, pool in enumerate(self.pools):
			if pool.offset_2_struct_entries:
				# store pool in pool_groups map
				if pool.type not in pools_by_type:
					pools_by_type[pool.type] = []
				pools_by_type[pool.type].append(pool)
				# try to get a name for the pool
				logging.debug(f"Pool[{pool_index}]: {len(pool.offset_2_struct_entries)} structs")
				first_entry = pool.get_first_entry()
				assert first_entry
				type_str = first_entry.__class__.__name__
				# map fragment to containing root entry
				if isinstance(first_entry, Fragment):
					for loader in self.ovl.loaders.values():
						if first_entry in loader.fragments:
							first_entry = loader.root_entry
							break
					else:
						logging.warning(f"Could not find root entry to get name for {first_entry}")
						continue
				logging.debug(f"Pool[{pool_index}]: {pool.name} -> '{first_entry.name}' ({type_str})")
				self.transfer_identity(pool, first_entry)
			else:
				logging.debug(
					f"Pool[{pool_index}]: deleting '{pool.name}' from archive '{self.arg.name}' as it has no pointers")
		self.pools.clear()
		# rebuild pool groups
		self.arg.num_pool_groups = len(pools_by_type)
		self.reset_field("pool_groups")
		for pool_group, (pool_type, pools) in zip(self.pool_groups, sorted(pools_by_type.items())):
			pool_group.type = pool_type
			pool_group.num_pools = len(pools)
			self.pools.extend(pools)
		self.arg.num_pools = len(self.pools)

	def map_buffers(self):
		"""Map buffers to data entries"""
		logging.info("Mapping buffers")
		if self.ovl.version >= 20:
			for data in self.data_entries:
				data.buffers = []
			logging.debug("Assigning buffer indices")
			for b_group in self.buffer_groups:
				b_group.ext = self.ovl.mimes[b_group.ext_index].ext
				# note that datas can be bigger than buffers
				buffers = self.buffer_entries[b_group.buffer_offset: b_group.buffer_offset + b_group.buffer_count]
				datas = self.data_entries[b_group.data_offset: b_group.data_offset + b_group.data_count]
				for buffer in buffers:
					buffer.index = b_group.buffer_index
					for data in datas:
						if buffer.file_hash == data.file_hash:
							self.transfer_identity(buffer, data)
							data.buffers.append(buffer)
							break
					else:
						raise BufferError(
							f"Buffer group {b_group.ext}, index {b_group.buffer_index} did not find a data entry for buffer {buffer.file_hash}")
		else:
			# sequentially attach buffers to data entries by each entry's buffer count
			i = 0
			for data in self.data_entries:
				data.buffers = self.buffer_entries[i: i+data.buffer_count]
				for buffer in data.buffers:
					self.transfer_identity(buffer, data)
				i += data.buffer_count

	@property
	def buffers_io_order(self):
		"""sort buffers into the order in which they are read from the file"""
		if self.ovl.version >= 20:
			return self.buffer_entries
		else:
			# sorting depends on order of data entries, and order of buffers therein (not necessarily sorted by index)
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

	def dump_pools(self, fp):
		"""for debugging"""
		for i, pool in enumerate(self.pools):
			with open(f"{fp}_pool[{i}].dmp", "wb") as f:
				f.write(pool.data.getvalue())
				# write a pointer marker at each offset
				for offset, entry in pool.offset_2_link_entry.items():
					f.seek(offset)
					if isinstance(entry, Fragment):
						f.write(b"@POINTER")
					else:
						f.write(b"@DEPENDS")

	def dump_buffer_groups_log(self, fp):
		with open(f"{fp}_buffers.log", "w") as f:
			f.write("\nBuffers IO order")
			for x, buffer in enumerate(self.buffers_io_order):
				f.write(f"\n{buffer.name} index: {buffer.index}| {buffer.size}")
			f.write("\n\nBuffers")
			for x, buffer in enumerate(self.buffer_entries):
				f.write(f"\n{buffer.name} index: {buffer.index}| {buffer.size}")
			f.write("\n\n")
			for x, buffer_group in enumerate(self.buffer_groups):
				f.write(
					f"\n{buffer_group.ext} {buffer_group.buffer_offset} {buffer_group.buffer_count} {buffer_group.buffer_index} | {buffer_group.size} {buffer_group.data_offset} {buffer_group.data_count} ")

	def _dump_ptr_stack(self, f, parent_struct_ptr, rec_check, indent=1):
		"""Recursively writes parent_struct_ptr.children to f"""
		for entry in sorted(parent_struct_ptr.children, key=lambda e: e.link_ptr.data_offset):
			# get the relative offset of this pointer to its struct
			rel_offset = entry.link_ptr.data_offset - parent_struct_ptr.data_offset
			if isinstance(entry, Fragment):
				# points to a child struct
				struct_ptr = entry.struct_ptr
				if entry in rec_check:
					# pointer refers to a known entry - stop here to avoid recursion
					f.write(f"\n{indent * TAB}PTR @ {rel_offset: <4} -> REF {struct_ptr} ({struct_ptr.data_size: 4})")
				else:
					rec_check.add(entry)
					f.write(f"\n{indent * TAB}PTR @ {rel_offset: <4} -> SUB {struct_ptr} ({struct_ptr.data_size: 4})")
					self._dump_ptr_stack(f, struct_ptr, rec_check, indent=indent + 1)
			else:
				f.write(f"\n{indent * TAB}DEP @ {rel_offset: <4} -> {entry.name}")

	def dump_stack(self, fp):
		"""for development; collect info about fragment types"""
		with open(f"{fp}.stack", "w") as f:
			for i, pool in enumerate(self.pools):
				f.write(f"\nPool {i} (type: {pool.type})")

			for root_entry in self.root_entries:
				ptr = root_entry.struct_ptr
				if ptr.pool:
					debug_str = f"\n\nFILE {ptr} ({ptr.data_size: 4}) {root_entry.name}"
					f.write(debug_str)
					try:
						self._dump_ptr_stack(f, ptr, set())
					except AttributeError:
						logging.exception(f"Dumping {root_entry.name} failed")
						f.write("\n!FAILED!")

	def assign_name(self, entry):
		"""Fetch a filename for an entry"""
		# JWE style
		if self.ovl.user_version.use_djb:
			try:
				n = self.ovl.hash_table_local[entry.file_hash]
				e = self.ovl.hash_table_local[entry.ext_hash]
			except KeyError:
				raise KeyError(
					f"No match for entry {entry.file_hash} [{entry.__class__.__name__}] from archive {self.arg.name}")
		# PZ Style and PC Style
		else:
			# file_hash is an index into ovl files
			try:
				file = self.ovl.files[entry.file_hash]
				n = file.basename
				e = file.ext
			except IndexError:
				logging.warning(
					f"Entry ID {entry.file_hash} [{entry.__class__.__name__}] does not index into ovl file table of length {len(self.ovl.files)}")
				n = "none"
				e = ".ext"
		# fix for island.island, force extension to start with .
		if e[0] != ".":
			e = f".{e}"
		entry.ext = e
		entry.basename = n
		entry.name = f"{n}{e}"

	def write_pools(self):
		logging.debug(f"Writing pools for {self.arg.name}")
		# do this first so pools can be updated
		pools_data_writer = BytesIO()
		for pool in self.pools:
			# make sure that all pools are padded before writing
			pool.pad()
			pool.move_empty_pointers_to_end()
			pool_bytes = pool.data.getvalue()
			pool.offset = self.get_pool_offset(pools_data_writer.tell())
			logging.debug(f"pool.offset {pool.offset}, pools_start {self.arg.pools_start}")
			pool.size = len(pool_bytes)
			pools_data_writer.write(pool_bytes)
		self.pools_data = pools_data_writer.getvalue()

	def get_pool_offset(self, in_offset):
		# JWE, JWE2: relative offset for each pool
		if self.ovl.user_version.use_djb:
			return in_offset
		# PZ, PC: offsets relative to the whole pool block
		else:
			return self.arg.pools_start + in_offset

	def write_archive(self):
		logging.info(f"Writing archive {self.arg.name}")
		with BytesIO() as stream:
			# write out all entries
			super().write_fields(stream, self)
			# write the pools data containing all the pointers' datas
			stream.write(self.pools_data)
			# write buffer data
			for b in self.buffers_io_order:
				stream.write(b.data)
			return stream.getvalue()


class OvlFile(Header, IoFile):

	warning_msg = DummySignal()
	files_list = DummySignal()
	included_ovls_list = DummySignal()
	progress_percentage = DummySignal()
	current_action = DummySignal()

	def __init__(self):
		# pass self as context
		super().__init__(self)
		self.magic.data = b'FRES'
		self.hash_table_global = {}

		self.is_biosyn = None
		self.do_debug = False

		self.formats_dict = FormatDict()
		self.loaders = {}

	@classmethod
	def context_to_xml(cls, elem, prop, instance, arg, template, debug):
		from generated.formats.ovl.versions import get_game
		elem.attrib[prop] = str(get_game(instance)[0])

	def clear(self):
		self.archives.clear()
		self.files.clear()
		self.mimes.clear()
		self.loaders = {}

	def init_loader(self, file_entry):
		# fall back to BaseFile loader
		from modules.formats.BaseFormat import BaseFile
		cls = self.formats_dict.get(file_entry.ext, BaseFile)
		loader = cls(self, file_entry)
		return loader

	def remove(self, filenames):
		"""
		Removes files from an ovl file
		:param filenames: list of file names (eg. "example.ext") that should be removed from ovl
		:return:
		"""
		logging.info(f"Removing files for {filenames}")
		# prevent RuntimeError: dictionary changed size during iteration
		for loader in tuple(self.loaders.values()):
			if loader.file_entry.name in filenames:
				loader.remove()

	def rename(self, name_tups, mesh_mode=False):
		logging.info(f"Renaming for {name_tups}, mesh mode = {mesh_mode}")
		# todo - support renaming included_ovls?
		# make a temporary copy
		temp_loaders = list(self.loaders.values())
		for loader in temp_loaders:
			if mesh_mode and loader.file_entry.ext not in (".ms2", ".mdl2", ".motiongraph", ".motiongraphvars"):
				continue
			loader.rename(name_tups)
		# recreate the loaders dict
		self.loaders = {loader.file_entry.name: loader for loader in temp_loaders}
		logging.info("Finished renaming!")

	def rename_contents(self, name_tups, only_files):
		if not only_files:
			only_files = list(self.loaders.keys())
		logging.info(f"Renaming contents for {name_tups} for {len(only_files)} selected files")
		for file_name in only_files:
			self.loaders[file_name].rename_content(name_tups)
		logging.info("Finished renaming contents!")

	def extract(self, out_dir, only_names=(), only_types=(), show_temp_files=False):
		"""Extract the files, after all archives have been read"""
		# create output dir
		logging.info(f"Extracting from {len(self.files)} files")
		os.makedirs(out_dir, exist_ok=True)

		def out_dir_func(n):
			"""Helper function to generate temporary output file name"""
			return os.path.normpath(os.path.join(out_dir, n))

		self.do_debug = show_temp_files
		error_files = []
		out_paths = []
		loaders_for_extract = []
		_only_types = [s.lower() for s in only_types]
		_only_names = [s.lower() for s in only_names]
		for loader in self.loaders.values():
			# for batch operations, only export those that we need
			if _only_types and loader.file_entry.ext not in _only_types:
				continue
			if _only_names and loader.file_entry.name not in _only_names:
				continue
			# ignore types in the count that we export from inside other type exporters
			if loader.file_entry.ext in self.formats_dict.ignore_types:
				continue
			loaders_for_extract.append(loader)
		for loader in self.iter_progress(loaders_for_extract, "Extracting"):
			try:
				ret_paths = loader.extract(out_dir_func)
				ret_paths = loader.handle_paths(ret_paths, show_temp_files)
				out_paths.extend(ret_paths)
			except:
				logging.exception(f"An exception occurred while extracting {loader.file_entry.name}")
				error_files.append(loader.file_entry.name)
		return out_paths, error_files

	def create_file_entry(self, file_path):
		"""Create a file entry from a file path"""
		# capital letters in the name buffer crash JWE2, apparently
		file_path = file_path.lower()
		filename = os.path.basename(file_path)
		file_entry = FileEntry(self.context)
		file_entry.path = file_path
		file_entry.name = filename
		# just init it here
		file_entry.ext_hash = 0
		file_entry.basename, file_entry.ext = os.path.splitext(filename)
		try:
			file_entry.update_constants(self)
			return file_entry
		except KeyError:
			logging.warning(f"Unsupported file type {file_entry.ext} for game {get_game(self.context)[0].value}")
			return

	def create_file(self, file_path, ovs_name="STATIC"):
		"""Register a file entry from a file path, add a loader"""
		file_entry = self.create_file_entry(file_path)
		if not file_entry:
			return
		logging.info(f"Creating {file_entry.name} in {ovs_name}")
		loader = self.init_loader(file_entry)
		try:
			loader.set_ovs(ovs_name)
			loader.create()
			loader.register_ptrs()
			return loader
		except NotImplementedError:
			logging.warning(f"Creation not implemented for {loader.file_entry.ext}")
		except BaseException:
			logging.exception(f"Could not create: {loader.file_entry.name}")
			raise

	def create(self, ovl_dir):
		logging.info(f"Creating OVL from {ovl_dir}")
		self.store_filepath(f"{ovl_dir}.ovl")
		file_paths = [os.path.join(ovl_dir, file_name) for file_name in os.listdir(ovl_dir)]
		self.loaders = {}
		self.add_files(file_paths)
		self.load_included_ovls(os.path.join(ovl_dir, "ovls.include"))

	def add_files(self, file_paths):
		logging.info(f"Adding {len(file_paths)} files to OVL")
		logging.info(f"Game: {get_game(self)[0].name}")
		error_files = []
		for file_path in self.iter_progress(file_paths, "Adding files"):
			# ilo: ignore file extensions in the IGNORE list
			bare_path, ext = os.path.splitext(file_path)
			if ext in self.formats_dict.ignore_types:
				logging.info(f"Ignoring {file_path}")
				continue
			try:
				loader = self.create_file(file_path)
				self.register_loader(loader)
			except:
				error_files.append(file_path)
		if error_files:
			self.warning_msg.emit(f"Adding the following files failed - please check the console log:\n"+"\n".join(error_files))
		self.files_list.emit([[loader.file_entry.name, loader.file_entry.ext] for loader in self.loaders.values()])

	def register_loader(self, loader):
		"""register the loader, and delete any existing loader if needed"""
		if loader:
			# check if this file exists in this ovl, if so, first delete old loader
			if loader.file_entry.name in self.loaders:
				loader = self.loaders[loader.file_entry.name]
				loader.remove()
			# only store loader in self.loaders after successful create
			self.loaders[loader.file_entry.name] = loader
			# also store any streams created by loader
			for stream in loader.streams + loader.children:
				if stream:
					self.loaders[stream.file_entry.name] = stream

	def create_archive(self, name="STATIC"):
		# see if it exists
		for archive in self.archives:
			if archive.name == name:
				return archive.content
		# nope, gotta create it
		logging.debug(f"Creating archive '{name}'")
		archive = ArchiveEntry(self.context)
		archive.name = name
		self.archives.append(archive)
		content = OvsFile(self.context, self, archive)
		archive.content = content
		return content

	# dummy (black hole) callback for if we decide we don't want one
	def dummy_callback(self, *args, **kwargs):
		return

	def iter_progress(self, iterable, message):
		if hasattr(self,  'current_action'):
			self.current_action.emit(message)
		self._percentage = 0
		v_max = len(iterable) - 1
		for i, item in enumerate(iterable):
			yield item
			if i and v_max:
				p = round(i / v_max * 100)
				if p != self._percentage:
					self.progress_percentage.emit(p)
					self._percentage = p
		if hasattr(self,  'current_action'):
			self.current_action.emit(f"Finished {message}")

	def store_filepath(self, filepath):
		# store file name for later
		self.filepath = filepath
		self.dir, self.name = os.path.split(filepath)
		self.basename, self.ext = os.path.splitext(self.name)
		self.path_no_ext = os.path.splitext(self.filepath)[0]

	@property
	def included_ovl_names(self):
		return [included_ovl.name for included_ovl in self.included_ovls]

	@included_ovl_names.setter
	def included_ovl_names(self, ovl_names):
		# remove duplicates
		ovl_names = set(ovl_names)
		logging.debug(f"Setting {len(ovl_names)} included OVLs")
		self.num_included_ovls = len(ovl_names)
		self.reset_field("included_ovls")
		for incl, ovl_name in zip(self.included_ovls, ovl_names):
			ovl_name = ovl_name.strip()
			if not ovl_name.lower().endswith(".ovl"):
				ovl_name += ".ovl"
			incl.name = ovl_name
			logging.debug(f"Including {incl.name}")

	def load_included_ovls(self, path):
		if os.path.isfile(path):
			with open(path) as f:
				self.included_ovl_names = f.readlines()

	def save_included_ovls(self, path):
		with open(path, "w") as f:
			for ovl_name in self.included_ovl_names:
				f.write(f"{ovl_name}\n")

	def update_names(self):
		"""Update the name buffers with names from list entries, and update the name offsets on those entries"""
		# regenerate the name buffer
		self.names.update_with((
			(self.dependencies, "ext_raw"),
			(self.included_ovls, "basename"),
			(self.mimes, "name"),
			(self.aux_entries, "basename"),
			(self.files, "basename")
		))
		self.archive_names.update_with((
			(self.archives, "name"),
		))
		self.len_names = len(self.names.data)
		self.len_archive_names = len(self.archive_names.data)

		# catching ovl files without entries, default len_type_names is 0
		if self.files:
			self.len_type_names = min(self.names.offset_dic.get(file.basename, -1) for file in self.files)
			# self.len_type_names = min(file.offset for file in self.files)
		else:
			self.len_type_names = 0

	def load_hash_table(self):
		logging.info("Loading hash table...")
		start_time = time.time()
		self.hash_table_global = {}
		hashes_dir = os.path.join(root_dir, "hashes")
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
			f"Loaded {len(self.hash_table_global)} hash - name pairs in {time.time() - start_time:.2f} seconds")

	def load(self, filepath, commands={}):
		start_time = time.time()
		self.is_biosyn = None
		# store commands
		self.commands = commands
		self.store_filepath(filepath)
		logging.info(f"Loading {self.name}")
		self.eof = super().load(filepath)
		logging.info(f"Game: {get_game(self)[0].name}")

		self.loaders = {}
		# maps djb2 hash to string
		self.hash_table_local = {}
		# add extensions to hash dict
		for mime_entry in self.iter_progress(self.mimes, "Loading extensions"):
			# get the bare extension from the mime string
			mime_entry.ext = f".{mime_entry.name.split(':')[-1]}"
			# we must calculate the djb2 hash of the extension to find it from the ovs
			self.hash_table_local[djb2(mime_entry.ext[1:].lower())] = mime_entry.ext
			mime_entry.triplets = self.triplets[
								  mime_entry.triplet_offset: mime_entry.triplet_offset + mime_entry.triplet_count]

		# add file name to hash dict; ignoring the extension pointer
		for file_entry in self.iter_progress(self.files, "Loading files"):
			file_entry.mime = self.mimes[file_entry.extension]
			file_entry.ext = file_entry.mime.ext
			# store this so we can use it
			file_entry.ext_hash = djb2(file_entry.ext[1:])
			self.hash_table_local[file_entry.file_hash] = file_entry.basename

		if "generate_hash_table" in self.commands:
			deps_exts = self.commands["generate_hash_table"]
			filtered_hash_table = {f.file_hash: f.basename for f in self.files if f.ext in deps_exts}
			return filtered_hash_table, set(d.ext for d in self.dependencies)
		else:
			self.files_list.emit([[file.name, file.ext] for file in self.files])
			# initialize the loaders right here
			for file_entry in self.files:
				self.loaders[file_entry.name] = self.init_loader(file_entry)

		# get included ovls
		for included_ovl in self.iter_progress(self.included_ovls, "Loading includes"):
			included_ovl.ext = ".ovl"
		self.included_ovls_list.emit(self.included_ovl_names)

		# get names of all dependencies
		for dependency_entry in self.iter_progress(self.dependencies, "Loading Dependencies"):
			file_entry = self.files[dependency_entry.file_index]

			self.loaders[file_entry.name].dependencies.append(dependency_entry)
			h = dependency_entry.file_hash
			if h in self.hash_table_local:
				dependency_entry.basename = self.hash_table_local[h]
			# logging.debug(f"LOCAL: {h} -> {dependency_entry.basename}")
			elif h in self.hash_table_global:
				dependency_entry.basename = self.hash_table_global[h]
			# logging.debug(f"GLOBAL: {h} -> {dependency_entry.basename}")
			else:
				logging.warning(f"Unresolved dependency [{h}] for {file_entry.name}")
				dependency_entry.basename = UNK_HASH

		for aux_entry in self.aux_entries:
			file_entry = self.files[aux_entry.file_index]
			self.loaders[file_entry.name].aux_entries.append(aux_entry)

		self.load_archives()
		# self.debug_unks()
		logging.info(f"Loaded OVL in {time.time() - start_time:.2f} seconds")

	def load_archives(self):
		logging.info("Loading archives")
		start_time = time.time()
		self.open_ovs_streams(mode="rb")
		for archive_entry in self.iter_progress(self.archives, "Reading archives"):
			# those point to external ovs archives
			if archive_entry.name == "STATIC":
				read_start = self.eof
			else:
				read_start = archive_entry.read_start
			start_time = time.time()
			archive_entry.content = OvsFile(self.context, self, archive_entry)
			logging.info(f"Initialized OVS in {time.time() - start_time:.2f} seconds")
			try:
				archive_entry.content.unzip(archive_entry, read_start)
			except BaseException as err:
				logging.exception(f"Decompressing {archive_entry.name} from {archive_entry.ovs_path} failed")
				# print(archive_entry)
				# print(archive_entry.content)
				continue
		self.close_ovs_streams()
		self.postprocessing()
		logging.info(f"Loaded archives in {time.time() - start_time:.2f} seconds")

	def postprocessing(self):
		self.load_flattened_pools()
		self.load_pointers()

	def load_flattened_pools(self):
		"""Create flattened list of ovl.pools from all ovs.pools"""
		self.pools = [None for _ in range(self.num_pools)]
		for archive in self.archives:
			assert len(archive.content.pools) == archive.num_pools
			self.pools[archive.pools_offset: archive.pools_offset + archive.num_pools] = archive.content.pools

	def load_pointers(self):
		"""Handle all pointers of this file, including dependencies, fragments and root_entry entries"""
		logging.info("Loading pointers")
		start_time = time.time()
		# reset pointer map for each pool
		for pool in self.pools:
			pool.clear_data()
		logging.debug("Linking pointers to pools")
		for dep in self.dependencies:
			# the index goes into the flattened list of ovl pools
			dep.link_ptr.assign_pool(self.pools)
			dep.link_ptr.add_link(dep)
		for archive in self.archives:
			ovs = archive.content
			# attach all pointers to their pool
			for root_entry in ovs.root_entries:
				root_entry.struct_ptr.assign_pool(ovs.pools)
				# may not have a pool
				root_entry.struct_ptr.add_struct(root_entry)
			for i, frag in enumerate(ovs.fragments):
				frag.link_ptr.assign_pool(ovs.pools)
				frag.struct_ptr.assign_pool(ovs.pools)
				try:
					frag.struct_ptr.add_struct(frag)
					frag.link_ptr.add_link(frag)
				except:
					logging.exception(f"linking frag {i} failed")
		logging.debug("Calculating pointer sizes")
		for pool in self.pools:
			pool.calc_struct_ptr_sizes()
		logging.info(f"Prepared pointers in {time.time() - start_time:.2f} seconds")

		logging.info("Loading file classes")
		start_time = time.time()

		loaders = self.loaders.values()
		if "only_types" in self.commands:
			only_types = self.commands['only_types']
			logging.info(f"Loading only {only_types}")
			loaders = [loader for loader in loaders if loader.file_entry.ext in only_types]
		for loader in self.iter_progress(loaders, "Mapping files"):
			loader.track_ptrs()
			try:
				loader.collect()
			except:
				logging.exception(f"Collecting {loader.file_entry.name} errored")
			loader.link_streams()
		logging.info(f"Loaded file classes in {time.time() - start_time:.2f} seconds")

	def get_ovs_path(self, archive_entry):
		if archive_entry.name == "STATIC":
			archive_entry.ovs_path = self.filepath
		else:
			# JWE style
			if is_jwe(self) or is_jwe2(self):
				archive_entry.ovs_path = f"{self.path_no_ext}.ovs.{archive_entry.name.lower()}"
			# PZ, PC, ZTUAC Style
			else:
				archive_entry.ovs_path = f"{self.path_no_ext}.ovs"

	def rebuild_ovl_arrays(self):
		"""Call this if any file names have changed and hashes or indices have to be recomputed"""
		# clear ovl lists
		self.dependencies.clear()
		self.aux_entries.clear()
		self.files.clear()
		self.mimes.clear()
		self.triplets.clear()

		# update file hashes and extend entries per loader
		for loader in self.loaders.values():
			# ensure lowercase, at the risk of being redundant
			loader.file_entry.file_hash = djb2(loader.file_entry.basename.lower())
			loader.file_entry.ext_hash = djb2(loader.file_entry.ext[1:].lower())
			# logging.debug(f"File: {file.name} {file.file_hash} {file.ext_hash}")
			# update dependency hashes
			for dependency in loader.dependencies:
				if UNK_HASH in dependency.basename:
					logging.warning(f"{UNK_HASH} on dependency entry - won't update hash")
				else:
					dependency.file_hash = djb2(dependency.basename.lower())
			self.files.append(loader.file_entry)
			self.dependencies.extend(loader.dependencies)
			self.aux_entries.extend(loader.aux_entries)

		# sort the different lists according to the criteria specified
		self.files.sort(key=lambda x: (x.ext, x.file_hash))
		self.dependencies.sort(key=lambda x: x.file_hash)

		# build a lookup table mapping file name to its index
		file_name_lut = {file.name: file_i for file_i, file in enumerate(self.files)}
		# update indices into ovl.files
		for loader in self.loaders.values():
			for entry in loader.dependencies + loader.aux_entries:
				entry.file_index = file_name_lut[loader.file_entry.name]
		self.aux_entries.sort(key=lambda x: x.file_index)

		# map all files by their extension
		files_by_extension = {}
		for file in self.files:
			if file.ext not in files_by_extension:
				files_by_extension[file.ext] = []
			files_by_extension[file.ext].append(file)
		# create the mimes
		file_index_offset = 0
		self.num_mimes = len(files_by_extension)
		self.reset_field("mimes")
		for i, ((file_ext, files), mime_entry) in enumerate(zip(sorted(files_by_extension.items()), self.mimes)):
			mime_entry.ext = file_ext
			try:
				mime_entry.update_constants(self)
			except KeyError:
				raise KeyError(f"Extension {file_ext} missing from hash constants, regenerate hash table!")
			mime_entry.file_index_offset = file_index_offset
			mime_entry.file_count = len(files)
			file_index_offset += len(files)
			for file_entry in files:
				file_entry.update_constants(self)
				file_entry.extension = i
		# update ovl counts
		self.num_dependencies = len(self.dependencies)
		self.num_aux_entries = len(self.aux_entries)
		self.num_triplets = len(self.triplets)
		self.num_files = self.num_files_2 = self.num_files_3 = len(self.files)

	def rebuild_ovs_arrays(self):
		"""Produces valid ovl.pools and ovs.pools and valid links for everything that points to them"""
		try:
			logging.debug(f"Sorting pools by type and updating pool groups")
			self.archives.sort(key=lambda a: a.name)

			# generate a mime lut for the index of the mimes
			mime_lut = {mime.ext: i for i, mime in enumerate(self.mimes)}

			# remove all entries to rebuild them from the loaders
			for archive in self.archives:
				archive.content.clear_ovs_arrays()

			# add entries to correct ovs
			for loader in self.loaders.values():
				# attach the entries used by this loader to the ovs lists
				loader.register_entries()
				# force an update on the loader's data for older versions' data
				# and link entries like bani to banis
				loader.update()

			# todo - maybe reuse the lut?
			# build a lookup table mapping file name to its index
			file_name_lut = {file.name: file_i for file_i, file in enumerate(self.files)}
			pools_byte_offset = 0
			pools_offset = 0
			# make a temporary copy so we can delete archive if needed
			for archive in tuple(self.archives):

				logging.debug(f"Sorting pools for {archive.name}")
				ovs = archive.content

				ovs.rebuild_pools()
				# needs to happen after loader.register_entries
				# change the hashes / indices of all entries to be valid for the current game version
				ovs.update_hashes(file_name_lut)
				# sort fragments by their first pointer just to keep saves consistent for easier debugging
				ovs.fragments.sort(key=lambda f: (f.struct_ptr.pool_index, f.struct_ptr.data_offset))
				ovs.root_entries.sort(key=lambda b: (b.ext, b.file_hash))
				ovs.data_entries.sort(key=lambda b: (b.ext, b.file_hash))

				# depends on correct hashes applied to buffers and datas
				ovs.rebuild_buffer_groups(mime_lut)
				# depends on sorted root_entries
				ovs.rebuild_assets()

				# update the ovs counts
				archive.num_datas = len(ovs.data_entries)
				archive.num_buffers = len(ovs.buffer_entries)
				archive.num_fragments = len(ovs.fragments)
				archive.num_root_entries = len(ovs.root_entries)
				archive.num_buffer_groups = len(ovs.buffer_groups)

				# remove stream archive if it has no pools and no roots and no datas
				if archive.name != "STATIC" and not (archive.num_pools or archive.num_root_entries or archive.num_datas):
					logging.info(f"Removed stream archive {archive.name} as it was empty")
					self.archives.remove(archive)
					continue

				archive.pools_offset = pools_offset
				archive.pools_start = pools_byte_offset
				archive.content.write_pools()
				pools_byte_offset += len(archive.content.pools_data)
				archive.pools_end = pools_byte_offset
				# at least PZ & JWE require 4 additional bytes after each pool region
				pools_byte_offset += 4
				pools_offset += len(archive.content.pools)
				logging.debug(
					f"Archive {archive.name} has {archive.num_pools} pools in {archive.num_pool_groups} pool_groups")

			# update the ovl counts
			self.num_archives = len(self.archives)
			# sum counts of individual archives
			self.num_pool_groups = sum(a.num_pool_groups for a in self.archives)
			self.num_pools = sum(a.num_pools for a in self.archives)
			self.num_datas = sum(a.num_datas for a in self.archives)
			self.num_buffers = sum(a.num_buffers for a in self.archives)

			# apply the new pools to the ovl
			self.load_flattened_pools()
		except:
			logging.exception("Rebuilding ovl arrays failed")

	def update_pool_indices(self):
		"""Updates pool_index for all entries"""
		logging.info(f"Updating pool indices")
		# nb. this relies on dependencies being updated already
		for archive in self.archives:
			# we have the final list of pools now
			ovs = archive.content
			pools_lut = {pool: pool_i for pool_i, pool in enumerate(ovs.pools)}
			for loader in self.loaders.values():
				if loader.ovs == ovs:
					loader.root_entry.struct_ptr.update_pool_index(pools_lut)
					for frag in loader.fragments:
						frag.link_ptr.update_pool_index(pools_lut)
						frag.struct_ptr.update_pool_index(pools_lut)
		# dependencies index goes into the flattened list of pools
		pools_lut = {pool: pool_i for pool_i, pool in enumerate(self.pools)}
		for dep in self.dependencies:
			dep.link_ptr.update_pool_index(pools_lut)

	def open_ovs_streams(self, mode="wb"):
		logging.info("Opening OVS streams")
		self.ovs_dict = {}
		for archive_entry in self.archives:
			# gotta update it here
			self.get_ovs_path(archive_entry)
			logging.debug(f"Loading {archive_entry.ovs_path}")
			if archive_entry.ovs_path not in self.ovs_dict:
				# make sure that the ovs exists
				if mode == "rb" and not os.path.exists(archive_entry.ovs_path):
					raise FileNotFoundError(f"OVS file not found. Make sure it is here: {archive_entry.ovs_path}")
				# open file in desired mode
				self.ovs_dict[archive_entry.ovs_path] = open(archive_entry.ovs_path, mode)

	def close_ovs_streams(self):
		logging.info("Closing OVS streams")
		# we don't use context manager so gotta close them
		for ovs_file in self.ovs_dict.values():
			ovs_file.close()

	def update_stream_files(self):
		logging.info("Updating stream file memory links")
		self.stream_files.clear()
		for loader in self.loaders.values():
			for stream_loader in loader.streams:
				stream_entry = StreamEntry(self.context)
				stream_entry.file_offset = loader.abs_mem_offset
				stream_entry.stream_offset = stream_loader.abs_mem_offset
				stream_entry.archive_name = stream_loader.ovs.arg.name
				self.stream_files.append(stream_entry)
		# sort stream files by archive and then the file offset in the pool
		self.stream_files.sort(key=lambda s: (s.archive_name, s.file_offset))
		self.num_stream_files = len(self.stream_files)
		# update the archive entries to point to the stream files
		stream_files_offset = 0
		for archive in self.archives:
			archive.stream_files_offset = stream_files_offset
			stream_files = [f for f in self.stream_files if f.archive_name == archive.name]
			# some JWE2 dino archives have no stream_files, just extra data_entries
			stream_files_offset += len(stream_files)

	def dump_debug_data(self):
		"""Dumps various logs needed to reverse engineer and debug the ovl format"""
		logging.info(f"Dumping debug data to {self.dir}")

		for archive_entry in self.archives:
			fp = os.path.join(self.dir, f"{self.name}_{archive_entry.name}")
			try:
				archive_entry.content.dump_stack(fp)
				archive_entry.content.dump_buffer_groups_log(fp)
				archive_entry.content.dump_pools(fp)
			except:
				logging.exception("Dumping failed")
		self.dump_buffer_info()

	@property
	def sorted_loaders(self):
		return sorted(self.loaders.values(), key=lambda l: l.file_entry.name)

	def dump_buffer_info(self):
		"""for development; collect info about fragment types"""
		def out_dir_func(n):
			"""Helper function to generate temporary output file name"""
			return os.path.normpath(os.path.join(self.dir, n))
		log_path = out_dir_func(f"{self.name}_buffer_info.log")
		with open(log_path, "w") as f:
			for loader in self.sorted_loaders:
				loader.dump_buffer_infos(f)
		for loader in self.sorted_loaders:
			loader.dump_buffers(out_dir_func)

	def save(self, filepath):
		start_time = time.time()
		self.store_filepath(filepath)
		logging.info(f"Writing {self.name}")
		# do this last so we also catch the assets & sets
		self.rebuild_ovl_arrays()
		self.rebuild_ovs_arrays()
		# these need to be done after the rest
		self.update_pool_indices()
		self.update_stream_files()
		# update the name buffer and offsets
		self.update_names()
		self.open_ovs_streams()
		ovl_compressed = b""
		self.zlibs.clear()
		# compress data stream
		for archive in self.iter_progress(self.archives, "Saving archives"):
			# write archive into bytes IO stream
			uncompressed = archive.content.write_archive()
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
			new_zlib = ZlibInfo(self.context)
			# size of the archive entry = 68
			# this is true for jwe2 tylo, but not for jwe2 rex 93 and many others
			new_zlib.zlib_thing_1 = 68 + archive.uncompressed_size
			# this is fairly good, doesn't work for tylo static but all others, all of jwe2 rex 93, jwe1 parrot, pz fallow deer
			new_zlib.zlib_thing_2 = sum([data.size_2 for data in archive.content.data_entries])
			self.zlibs.append(new_zlib)

		self.close_ovs_streams()
		with open(filepath, "wb") as stream:
			self.write_fields(stream, self)
			stream.write(ovl_compressed)
		logging.info(f"Saved OVL in {time.time() - start_time:.2f} seconds")


if __name__ == "__main__":
	ovl = OvlFile()
	# ovl.load("C:/Users/arnfi/Desktop/Coding/ovl/OVLs/Parrot.ovl")
	ovl.load("C:/Users/arnfi/Desktop/Coding/Frontier/Disneyland/SpatialDatabaseTest.ovl")
	print(ovl.mimes)
