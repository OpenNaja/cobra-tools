from generated.formats.ovl.imports import name_type_map
import contextlib
import itertools
import logging
import os
import struct
import time
import zlib
from contextlib import contextmanager
from io import BytesIO

from constants import ConstantsProvider
from generated.formats.ovl.compounds.ArchiveEntry import ArchiveEntry
from generated.formats.ovl.compounds.BufferGroup import BufferGroup
from generated.formats.ovl.compounds.Header import Header
from generated.formats.ovl.compounds.OvsHeader import OvsHeader
from generated.formats.ovl.versions import *
from generated.formats.ovl_base.enums.Compression import Compression
from modules.formats.formats_dict import FormatDict
from modules.formats.shared import djb2, DummySignal
from ovl_util.oodle.oodle import OodleDecompressEnum, oodle_compressor

UNK_HASH = "UnknownHash"
OODLE_MAGIC = (b'\x8c', b'\xcc')


def pairwise(iterable):
	# pairwise('ABCDEFG') --> AB BC CD DE EF FG
	a, b = itertools.tee(iterable)
	next(b, None)
	return zip(a, b)


class OvsFile(OvsHeader):

	def __init__(self, context, ovl_inst, archive_entry):
		# init with a dummy default archive
		dummy_archive = ArchiveEntry(context, None, None)
		super().__init__(context, dummy_archive, None)
		self.ovl = ovl_inst
		# set arg later to avoid initializing huge arrays with default data
		self.arg = archive_entry

	def clear_ovs_arrays(self):
		self.arg.num_datas = self.arg.num_buffers = self.arg.num_buffer_groups = 0
		self.reset_field("data_entries")
		self.reset_field("buffer_entries")
		self.reset_field("buffer_groups")

	@contextmanager
	def unzipper(self, compressed_bytes, uncompressed_size):
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

	def update_hashes(self):
		logging.info(f"Updating hashes for {self.arg.name}")
		entry_lists = (
			self.pools,
			self.data_entries,
			# self.buffer_entries
		)
		# update references to ovl files
		for entry_list in entry_lists:
			for entry in entry_list:
				if not entry.name:
					logging.warning(f"{entry} has no name assigned to it, cannot assign proper ID")
					continue
				loader = self.ovl.loaders[entry.name]
				if self.ovl.user_version.use_djb:
					entry.file_hash = loader.file_hash
				else:
					entry.file_hash = loader.file_index
				entry.ext_hash = loader.ext_hash

	def load(self, archive_entry, start):
		filepath = archive_entry.ovs_path
		stream = self.ovl.ovs_dict[filepath]
		stream.seek(start)
		logging.info(
			f"Loading archive {archive_entry.name}")
		logging.debug(
			f"Compressed stream {archive_entry.name} in {os.path.basename(filepath)} starts at {stream.tell()}")
		compressed_bytes = stream.read(archive_entry.compressed_size)
		with self.unzipper(compressed_bytes, archive_entry.uncompressed_size) as stream:
			# start_time = time.time()
			super().read_fields(stream, self)
			# logging.info(f"Read decompressed stream in {time.time() - start_time:.2f} seconds")
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

			self.root_entries_name = self.get_names_list(self.root_entries)

			if not (self.set_header.sig_a == 1065336831 and self.set_header.sig_b == 16909320):
				raise AttributeError("Set header signature check failed!")
			if self.set_header.io_size != self.arg.set_data_size:
				raise AttributeError(
					f"Set data size incorrect (got {self.set_header.io_size}, expected {self.arg.set_data_size})!")
			# for set_entry in self.set_header.sets:
			# 	self.assign_name(set_entry)
			# for asset_entry in self.set_header.assets:
			# 	self.assign_name(asset_entry)
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
		set_entries_name = self.get_names_list(self.set_header.sets)
		set_entries_offsets = list(self.set_header.sets["start"])
		# add end value
		set_entries_offsets.append(self.set_header.asset_count)
		# use itertools.pairwise from 3.10
		for name, (start, end) in zip(set_entries_name, pairwise(set_entries_offsets)):
			# map assets to entry
			assets = self.set_header.assets[start: end]
			assets_root_index = assets["root_index"]
			# store the references on the corresponding loader
			loader = self.ovl.loaders[name]
			loader.children = [self.ovl.loaders[self.root_entries_name[i]] for i in assets_root_index]

	@staticmethod
	def transfer_identity(source_entry, target_entry):
		source_entry.basename, source_entry.ext = os.path.splitext(target_entry.name)
		source_entry.name = target_entry.name
		source_entry.file_hash = target_entry.file_hash
		source_entry.ext_hash = target_entry.ext_hash

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
					# logging.debug(f"Buffer {i}, last: {last_ext} this: {buffer.ext}")
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
			if pool.offsets:
				# store pool in pool_groups map
				if pool.type not in pools_by_type:
					pools_by_type[pool.type] = []
				pools_by_type[pool.type].append(pool)
				# try to get a name for the pool
				logging.debug(f"Pool[{pool_index}]: {len(pool.offsets)} structs")
				first_offset = pool.get_first_offset()
				ptr = (pool, first_offset)
				for loader in self.ovl.loaders.values():
					if ptr in loader.stack:
						break
				else:
					logging.warning(f"Could not find loader to get name for Pool[{pool_index}] type {pool.type} at offset {first_offset}")
					continue
				logging.debug(f"Pool[{pool_index}]: {pool.name} -> '{loader.name}'")
				self.transfer_identity(pool, loader)
				# make sure that all pools are padded already before writing
				pool.pad()
			else:
				logging.debug(
					f"Pool[{pool_index}]: deleting '{pool.name}' from archive '{self.arg.name}' as it has no pointers")
				# logging.debug(
				# 	f"Pool[{pool_index}]: data '{pool.data.getvalue()}'")
		self.pools.clear()
		# rebuild pool groups
		self.arg.num_pool_groups = len(pools_by_type)
		self.reset_field("pool_groups")
		# print(pools_by_type)
		for pool_group, (pool_type, pools) in zip(self.pool_groups, sorted(pools_by_type.items())):
			pool_group.type = pool_type
			pool_group.num_pools = len(pools)
			self.pools.extend(pools)
		self.arg.num_pools = len(self.pools)

	def map_buffers(self):
		"""Map buffers to data entries"""
		logging.debug("Mapping buffers")
		if self.ovl.version >= 20:
			for data in self.data_entries:
				data.buffers = []
			logging.debug("Assigning buffer indices")
			for b_group in self.buffer_groups:
				b_group.ext = f".{self.ovl.mimes_ext[b_group.ext_index]}"
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
				for offset, entry in pool.offset_2_link.items():
					f.seek(offset)
					if isinstance(entry, tuple):
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

	def dump_stack(self, fp):
		"""for development; collect info about fragment types"""
		with open(f"{fp}.stack", "w") as f:
			for i, pool in enumerate(self.pools):
				f.write(f"\nPool {i} (type: {pool.type})")
			pools_lut = {pool: i for i, pool in enumerate(self.pools)}
			for loader in self.ovl.loaders.values():
				if loader.ovs == self:
					pool, offset = loader.root_ptr
					s_pool_i = pools_lut.get(pool, None)
					if pool:
						size = pool.size_map[offset]
						debug_str = f"\n\nFILE {s_pool_i} | {offset} ({size: 4}) {loader.name}"
						f.write(debug_str)
						try:
							loader.dump_ptr_stack(f, loader.root_ptr, set(), pools_lut)
						except AttributeError:
							logging.exception(f"Dumping {loader.name} failed")
							f.write("\n!FAILED!")

	def assign_name(self, entry):
		"""Fetch a filename for an entry"""
		# JWE style
		if self.ovl.user_version.use_djb:
			try:
				n = self.ovl.hash_table_local[entry.file_hash]
				e = f".{self.ovl.hash_table_local[entry.ext_hash]}"
			except KeyError:
				raise KeyError(
					f"No match for entry {entry.file_hash} [{entry.__class__.__name__}] from archive {self.arg.name}")
		# PZ Style and PC Style
		else:
			# file_hash is an index into ovl files
			try:
				file_name = self.ovl.files_name[entry.file_hash]
				loader = self.ovl.loaders[file_name]
				n = loader.basename
				e = loader.ext
			except IndexError:
				logging.warning(
					f"Entry ID {entry.file_hash} [{entry.__class__.__name__}] does not index into ovl file table of length {len(self.ovl.files)}")
				n = "none"
				e = ".ext"
		entry.ext = e
		entry.basename = n
		entry.name = f"{n}{e}"

	def get_names_list(self, array):
		"""Fetch list of file names for an array"""
		# JWE style
		if self.ovl.user_version.use_djb:
			# look up the hashes
			return [f"{n}.{e}" for n, e in zip(
					[self.ovl.hash_table_local[h] for h in array["file_hash"]],
					[self.ovl.hash_table_local[h] for h in array["ext_hash"]])]
		# PZ Style and PC Style
		else:
			# file_hash is an index into ovl files
			return [self.ovl.files_name[i] for i in array["file_hash"]]

	def assign_ids(self, array, loaders, with_ext_hash=True):
		"""Assign ids to an array"""
		if loaders:
			# JWE style
			if self.ovl.user_version.use_djb:
				# look up the hashes
				array["file_hash"] = [loader.file_hash for loader in loaders]
			# PZ Style and PC Style
			else:
				# file_hash is an index into ovl files
				array["file_hash"] = [loader.file_index for loader in loaders]
			if with_ext_hash:
				# PZ does not consistently store ext_hash, eg. it is no longer used on pools
				try:
					array["ext_hash"] = [loader.ext_hash for loader in loaders]
				except:
					pass

	def write_pools(self):
		logging.debug(f"Writing pools for {self.arg.name}")
		# do this first so pools can be updated
		pools_data_writer = BytesIO()
		for pool in self.pools:
			pool_bytes = pool.data.getvalue()
			pool.offset = self.get_pool_offset(pools_data_writer.tell())
			logging.debug(f"pool.offset {pool.offset}, pools_start {self.arg.pools_start}")
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


class OvlFile(Header):

	warning_msg = DummySignal()
	files_list = DummySignal()
	included_ovls_list = DummySignal()
	progress_percentage = DummySignal()
	current_action = DummySignal()

	def __init__(self):
		# pass self as context
		super().__init__(self)
		self.magic.data = b'FRES'

		self.is_biosyn = None
		self.do_debug = False

		self.formats_dict = FormatDict()
		self.constants = {}
		self.loaders = {}
		self.included_ovl_names = []

	@classmethod
	def context_to_xml(cls, elem, prop, instance, arg, template, debug):
		from generated.formats.ovl.versions import get_game
		elem.attrib[prop] = str(get_game(instance)[0])

	def clear(self):
		self.num_archives = 0
		self.reset_field("archives")
		self.loaders = {}

	def init_loader(self, filename, ext):
		# fall back to BaseFile loader, but only for collecting, not creating
		from modules.formats.BaseFormat import BaseFile
		loader_cls = self.formats_dict.get(ext, BaseFile)
		return loader_cls(self, filename)

	def remove(self, filenames):
		"""
		Removes files from an ovl file
		:param filenames: list of file names (eg. "example.ext") that should be removed from ovl
		:return:
		"""
		logging.info(f"Removing files for {filenames}")
		for filename in filenames:
			self.loaders[filename].remove()

	def rename(self, name_tups, mesh_mode=False):
		logging.info(f"Renaming for {name_tups}, mesh mode = {mesh_mode}")
		# todo - support renaming included_ovls?
		# make a temporary copy
		temp_loaders = list(self.loaders.values())
		for loader in temp_loaders:
			if mesh_mode and loader.ext not in (".ms2", ".mdl2", ".motiongraph", ".motiongraphvars"):
				continue
			loader.rename(name_tups)
		# recreate the loaders dict
		self.loaders = {loader.name: loader for loader in temp_loaders}
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
		out_paths = []
		loaders_for_extract = []
		_only_types = [s.lower() for s in only_types]
		_only_names = [s.lower() for s in only_names]
		for loader in self.loaders.values():
			# for batch operations, only export those that we need
			if _only_types and loader.ext not in _only_types:
				continue
			if _only_names and loader.name not in _only_names:
				continue
			# ignore types in the count that we export from inside other type exporters
			if loader.ext in self.formats_dict.ignore_types:
				continue
			loaders_for_extract.append(loader)
		with self.report_error_files("Extracting") as error_files:
			for loader in self.iter_progress(loaders_for_extract, "Extracting"):
				try:
					ret_paths = loader.extract(out_dir_func)
					ret_paths = loader.handle_paths(ret_paths, show_temp_files)
					out_paths.extend(ret_paths)
				except:
					logging.exception(f"An exception occurred while extracting {loader.name}")
					error_files.append(loader.name)
		return out_paths

	@contextlib.contextmanager
	def report_error_files(self, operation):
		error_files = []
		yield error_files
		if error_files:
			self.warning_msg.emit(
				(f"{operation} {len(error_files)} files failed - please check 'Show Details' or the log.", "\n".join(error_files)))

	def create_file(self, file_path, ovs_name="STATIC"):
		"""Create a loader from a file path"""
		filename = os.path.basename(file_path)
		_, ext = os.path.splitext(filename)
		logging.info(f"Creating {filename} in {ovs_name}")
		try:
			loader = self.init_loader(filename, ext, )
			loader.get_constants_entry()
			loader.set_ovs(ovs_name)
			loader.create(file_path)
			return loader
		except NotImplementedError:
			logging.warning(f"Creation not implemented for {filename}")
			raise
		except BaseException:
			logging.exception(f"Could not create: {filename}")
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
		with self.report_error_files("Adding") as error_files:
			for file_path in self.iter_progress(file_paths, "Adding files"):
				# ilo: ignore file extensions in the IGNORE list
				bare_path, ext = os.path.splitext(file_path)
				# ignore dirs, links etc.
				if not os.path.isfile(file_path):
					continue
				if ext in self.formats_dict.ignore_types:
					logging.info(f"Ignoring {file_path}")
					continue
				elif ext in (".png", ".dds"):
					if f"{bare_path}.tex" in file_paths:
						logging.info(f"Ignoring {file_path} as matching .tex file is also selected")
					else:
						logging.error(f"Inject the corresponding .tex file for {file_path}")
						error_files.append(file_path)
					continue
				try:
					loader = self.create_file(file_path)
					self.register_loader(loader)
				except:
					logging.exception(f"Adding '{file_path}' failed")
					error_files.append(file_path)
			for loader in self.iter_progress(self.loaders.values(), "Validating files"):
				loader.validate()
		self.files_list.emit([[loader.name, loader.ext] for loader in self.loaders.values()])

	def register_loader(self, loader):
		"""register the loader, and delete any existing loader if needed"""
		if loader:
			# check if this file exists in this ovl, if so, first delete old loader
			if loader.name in self.loaders:
				old_loader = self.loaders[loader.name]
				old_loader.remove()
			# only store loader in self.loaders after successful create
			self.loaders[loader.name] = loader
			# also store any streams created by loader
			for stream in loader.streams + loader.children:
				if stream:
					self.loaders[stream.name] = stream

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

	def load_included_ovls(self, path):
		self.included_ovl_names.clear()
		if os.path.isfile(path):
			with open(path) as f:
				self.included_ovl_names = [line.strip() for line in f.readlines() if line.strip()]
		self.included_ovls_list.emit(self.included_ovl_names)

	def save_included_ovls(self, path):
		with open(path, "w") as f:
			for ovl_name in self.included_ovl_names:
				f.write(f"{ovl_name}\n")

	def load_hash_table(self):
		logging.info("Loading hash table...")
		start_time = time.time()
		self.constants = ConstantsProvider()
		logging.info(f"Loaded constants in {time.time() - start_time:.2f} seconds")

	def get_mime(self, ext, key):
		game = get_game(self)[0].value
		if game in self.constants:
			game_lut = self.constants[game]
			if ext in game_lut["mimes"]:
				mime = game_lut["mimes"][ext]
				return getattr(mime, key)
			else:
				raise NotImplementedError(f"Unsupported extension {ext} in game {game}")
		else:
			raise NotImplementedError(f"Unsupported game {game}")

	def get_hash(self, h):
		game = get_game(self)[0].value
		if game in self.constants:
			game_lut = self.constants[game]
			if h in game_lut["hashes"]:
				return game_lut["hashes"][h]
			else:
				logging.warning(f"Unresolved dependency [{h}]")
		else:
			logging.warning(f"Unsupported game {game}")
		return f"{UNK_HASH}_{h}"

	def load(self, filepath, commands={}):
		start_time = time.time()
		self.is_biosyn = None
		# store commands
		self.commands = commands
		self.store_filepath(filepath)
		logging.info(f"Loading {self.name}")
		with open(filepath, "rb") as stream:
			self.read_fields(stream, self)
			self.eof = stream.tell()
		logging.debug(f"Loaded {self.name} structs in {time.time()-start_time:.2f} seconds")
		logging.info(f"Game: {get_game(self)[0].value}")

		self.loaders = {}
		# maps djb2 hash to string
		self.hash_table_local = {}
		# add extensions to hash dict
		self.mimes_name = [self.names.get_str_at(i) for i in self.mimes["name"]]
		# without leading . to avoid collisions on cases like JWE island.island
		self.mimes_ext = [name.split(':')[-1] for name in self.mimes_name]
		# store mime extension hash so we can use it
		self.hash_table_local = {djb2(ext): ext for ext in self.mimes_ext}

		if "triplet_offset" in self.mimes.dtype.fields:
			self.mimes_triplets = [self.triplets[o: o+c] for o, c in zip(
				self.mimes["triplet_offset"], self.mimes["triplet_count"])]
		else:
			self.mimes_triplets = []
		# add file name to hash dict; ignoring the extension pointer
		self.files_basename = [self.names.get_str_at(i) for i in self.files["basename"]]
		self.files_ext = [f".{self.mimes_ext[i]}" for i in self.files["extension"]]
		self.files_name = [f"{b}{e}" for b, e in zip(self.files_basename, self.files_ext)]
		self.dependencies_ext = [self.names.get_str_at(i).replace(":", ".") for i in self.dependencies["ext_raw"]]
		self.hash_table_local.update({h: b for b, h in zip(self.files_basename, self.files["file_hash"])})

		if "generate_hash_table" in self.commands:
			deps_exts = self.commands["generate_hash_table"]
			filtered_hash_table = {h: basename for h, basename, ext in zip(
				self.files["file_hash"], self.files_basename, self.files_ext) if ext in deps_exts}
			return filtered_hash_table, set(self.dependencies_ext)
		else:
			self.files_list.emit([[f, e] for f, e in zip(self.files_name, self.files_ext)])
			self.mimes_version = self.mimes["mime_version"]
			files_version = [self.mimes_version[i] for i in self.files["extension"]]
			# initialize the loaders right here
			for filename, ext, version, pt, set_pt in zip(self.files_name, self.files_ext, files_version, self.files["pool_type"], self.files["set_pool_type"]):
				loader = self.init_loader(filename, ext)
				loader.mime_version = version
				loader.pool_type = pt
				loader.set_pool_type = set_pt
				self.loaders[filename] = loader

		# get included ovls
		self.included_ovl_names = [self.names.get_str_at(i) for i in self.included_ovls["basename"]]
		self.included_ovls_list.emit(self.included_ovl_names)

		self.dependencies_basename = [self.get_dep_name(h) for h in self.dependencies["file_hash"]]
		self.dependencies_name = [b+e for b, e in zip(self.dependencies_basename, self.dependencies_ext)]

		self.aux_entries_names = [self.names.get_str_at(i) for i in self.aux_entries["basename"]]
		for f_i, aux_name in zip(self.aux_entries["file_index"], self.aux_entries_names):
			file_name = self.files_name[f_i]
			self.loaders[file_name].aux_entries.append(aux_name)
		self.load_archives()
		logging.info(f"Loaded OVL in {time.time() - start_time:.2f} seconds")

	def get_dep_name(self, h):
		if h in self.hash_table_local:
			return self.hash_table_local[h]
		else:
			return self.get_hash(h)

	def load_archives(self):
		logging.info("Loading archives")
		start_time = time.time()
		self.open_ovs_streams(mode="rb")
		with self.report_error_files("Reading") as error_files:
			for archive_entry in self.iter_progress(self.archives, "Reading archives"):
				# those point to external ovs archives
				if archive_entry.name == "STATIC":
					read_start = self.eof
				else:
					read_start = archive_entry.read_start
				# start_time = time.time()
				archive_entry.content = OvsFile(self.context, self, archive_entry)
				# logging.info(f"Initialized OVS in {time.time() - start_time:.2f} seconds")
				try:
					archive_entry.content.load(archive_entry, read_start)
				except:
					error_files.append(archive_entry.name)
					logging.exception(f"Loading {archive_entry.name} from {archive_entry.ovs_path} failed: {archive_entry}")
					logging.warning(archive_entry.content)
					continue
				# logging.info(f"Loading {archive_entry.name} from {archive_entry.ovs_path} worked: {archive_entry}\n{archive_entry.content}")
		# logging.info(self.archives_meta)
		self.close_ovs_streams()
		self.load_flattened_pools()
		self.load_pointers()
		logging.info(f"Loaded archives in {time.time() - start_time:.2f} seconds")

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
		for i, pool in enumerate(self.pools):
			pool.clear_data()
			pool.i = i
		logging.debug("Linking pointers to pools")
		for n, f_i, l_i, l_o in zip(
					self.dependencies_name,
					self.dependencies["file_index"],
					self.dependencies["link_ptr"]["pool_index"],
					self.dependencies["link_ptr"]["data_offset"]):
			file_name = self.files_name[f_i]
			pool = self.pools[l_i]
			self.loaders[file_name].dependencies[n] = (pool, l_o)
			# the index goes into the flattened list of ovl pools
			pool.offset_2_link[l_o] = n
		# this loop is extremely costly in JWE2 c0 main.ovl, about 145 s
		for archive in self.archives:
			try:
				ovs = archive.content
				# attach all pointers to their pool
				for n, s_i, s_o, in zip(
						ovs.root_entries_name,
						ovs.root_entries["struct_ptr"]["pool_index"],
						ovs.root_entries["struct_ptr"]["data_offset"]):
					loader = self.loaders[n]
					loader.ovs = ovs
					# may not have a pool
					if s_i != -1:
						s_pool = ovs.pools[s_i]
						s_pool.offsets.add(s_o)
						loader.root_ptr = (s_pool, s_o)
				# vectorized like this, it takes virtually no time
				for l_i, l_o, s_i, s_o, in zip(
						ovs.fragments["link_ptr"]["pool_index"],
						ovs.fragments["link_ptr"]["data_offset"],
						ovs.fragments["struct_ptr"]["pool_index"],
						ovs.fragments["struct_ptr"]["data_offset"]):
					s_pool = ovs.pools[s_i]
					# replace offsets pointing to end of pool with None
					if s_pool.size != s_o:
						s_pool.offsets.add(s_o)
					else:
						s_o = None
					ovs.pools[l_i].offset_2_link[l_o] = (s_pool, s_o)
			except:
				logging.exception(f"Could not load pointers for {archive.name} - something went wrong before")
		logging.debug("Calculating pointer sizes")
		for pool in self.pools:
			pool.calc_size_map()
		logging.info(f"Prepared pointers in {time.time() - start_time:.2f} seconds")

		logging.info("Loading file classes")
		start_time = time.time()

		loaders = self.loaders.values()
		if "only_types" in self.commands:
			only_types = self.commands['only_types']
			logging.info(f"Loading only {only_types}")
			loaders = [loader for loader in loaders if loader.ext in only_types]
		with self.report_error_files("Collecting") as error_files:
			for loader in self.iter_progress(loaders, "Mapping files"):
				loader.track_ptrs()
				try:
					loader.collect()
				except:
					logging.exception(f"Collecting {loader.name} errored")
					error_files.append(loader.name)
					# we can keep collecting
				loader.link_streams()
			for loader in self.iter_progress(loaders, "Validating files"):
				loader.validate()
		logging.info(f"Loaded file classes in {time.time() - start_time:.2f} seconds")

	def get_ovs_path(self, archive_entry):
		if archive_entry.name == "STATIC":
			archive_entry.ovs_path = self.filepath
		else:
			# JWE style
			if is_jwe(self) or is_jwe2(self):
				archive_entry.ovs_path = f"{self.path_no_ext}.ovs.{archive_entry.name.lower()}"
			# DLA, PZ, PC, ZTUAC Style
			else:
				archive_entry.ovs_path = f"{self.path_no_ext}.ovs"

	@staticmethod
	def get_dep_hash(name):
		if UNK_HASH in name:
			logging.warning(f"Won't update hash {name}")
			return int(name.replace(f"{UNK_HASH}_", ""))
		return djb2(name)

	def rebuild_ovl_arrays(self):
		"""Call this if any file names have changed and hashes or indices have to be recomputed"""

		# update file hashes and extend entries per loader
		# self.files.sort(key=lambda x: (x.ext, x.file_hash))
		# sorted_loaders = sorted(self.loaders, key=lambda x: (x.ext, x.file_hash))
		# map all files by their extension
		loaders_by_extension = {}
		for loader in self.loaders.values():
			if loader.ext not in loaders_by_extension:
				loaders_by_extension[loader.ext] = []
			loaders_by_extension[loader.ext].append(loader)
		mimes_ext = sorted(loaders_by_extension)
		mimes_triplets = [self.get_mime(ext, "triplets") for ext in mimes_ext]
		mimes_name = [self.get_mime(ext, "name") for ext in mimes_ext]
		# clear ovl lists
		loaders_with_deps = [loader for loader in self.loaders.values() if loader.dependencies]
		loaders_with_aux = [loader for loader in self.loaders.values() if loader.aux_entries]
		# flat list of all dependencies
		loaders_and_deps = [(dep, loader) for loader in loaders_with_deps for dep in loader.dependencies]
		loaders_and_aux = [(dep, loader) for loader in loaders_with_aux for dep in loader.aux_entries]
		ovl_includes = sorted(set(self.included_ovl_names))
		ovl_includes = [ovl_path.replace(".ovl", "") for ovl_path in ovl_includes]

		self.num_dependencies = len(loaders_and_deps)
		self.num_files = self.num_files_2 = self.num_files_3 = len(self.loaders.values())
		self.num_mimes = len(loaders_by_extension)
		self.num_triplets = sum(len(trip) for trip in mimes_triplets)
		self.num_included_ovls = len(ovl_includes)
		self.num_aux_entries = len(loaders_and_aux)
		self.reset_field("mimes")
		self.reset_field("dependencies")
		self.reset_field("files")
		self.reset_field("triplets")
		self.reset_field("included_ovls")
		self.reset_field("aux_entries")
		# print(loaders_and_deps)
		if loaders_and_deps:
			deps_basename, deps_ext = zip(*[os.path.splitext(dep) for dep, loader in loaders_and_deps])
		else:
			deps_basename = deps_ext = ()
		deps_ext = [ext.replace(".", ":") for ext in deps_ext]
		aux_names = [aux for aux, loader in loaders_and_aux]
		names_list = [
			*sorted(set(deps_ext)),
			*ovl_includes,
			*mimes_name,
			*aux_names,
			*sorted(loader.basename for loader in self.loaders.values())]
		self.names.update_strings(names_list)
		# create the mimes
		file_offset = 0
		triplet_offset = 0
		self.mimes["name"] = [self.names.offset_dic[name] for name in mimes_name]
		self.mimes["mime_version"] = [self.get_mime(ext, "version") for ext in mimes_ext]
		self.mimes["mime_hash"] = [self.get_mime(ext, "hash") for ext in mimes_ext]
		for i, (mime, name, ext, triplets,) in enumerate(
				zip(self.mimes, mimes_name, mimes_ext, mimes_triplets)):
			mime.name = self.names.offset_dic[name]
			try:
				mime.triplet_offset = triplet_offset
				mime.triplet_count = len(triplets)
			except:
				pass
			self.triplets[triplet_offset: triplet_offset+len(triplets)] = triplets
			# get the loaders using this ext
			loaders = loaders_by_extension[ext]
			mime.file_index_offset = file_offset
			mime.file_count = len(loaders)
			# take all files for this mime
			files = self.files[file_offset: file_offset+len(loaders)]
			# sort this mime's loaders by hash
			loaders.sort(key=lambda x: x.file_hash)
			# variable per loader
			files["basename"] = [self.names.offset_dic[loader.basename] for loader in loaders]
			files["file_hash"] = [loader.file_hash for loader in loaders]
			# shared by all loaders using this mime
			files["extension"] = i
			files["pool_type"] = loaders[0].pool_type
			files["set_pool_type"] = loaders[0].set_pool_type
			file_offset += len(loaders)
			triplet_offset += len(triplets)
		self.len_names = len(self.names.data)
		# catching ovl files without entries, default len_type_names is 0
		if self.loaders:
			self.len_type_names = min(self.files["basename"])
		else:
			self.len_type_names = 0

		flat_sorted_loaders = []
		for ext in mimes_ext:
			flat_sorted_loaders.extend(loaders_by_extension[ext])
		for i, loader in enumerate(flat_sorted_loaders):
			loader.file_index = i
		ext_lut = {ext: i for i, ext in enumerate(mimes_ext)}

		# self.dependencies.sort(key=lambda x: x.file_hash)
		self.dependencies["file_hash"] = [self.get_dep_hash(name) for name in deps_basename]
		self.dependencies["ext_raw"] = [self.names.offset_dic[name] for name in deps_ext]
		self.dependencies["file_index"] = [loader.file_index for dep, loader in loaders_and_deps]
		ptrs = [loader.dependencies[dep] for dep, loader in loaders_and_deps]

		# update all pools before indexing anything that points into pools
		pools_offset = 0
		for archive in self.archives:
			ovs = archive.content
			ovs.clear_ovs_arrays()
			ovs.rebuild_pools()
			archive.pools_offset = pools_offset
			pools_offset += archive.num_pools
		self.num_pools = sum(a.num_pools for a in self.archives)
		self.num_pool_groups = sum(a.num_pool_groups for a in self.archives)
		# apply the new pools to the ovl
		self.load_flattened_pools()

		pools_lut = {pool: i for i, pool in enumerate(self.pools)}
		self.dependencies["link_ptr"] = [(pools_lut[pool], offset) for pool, offset in ptrs]

		self.included_ovls["basename"] = [self.names.offset_dic[name] for name in ovl_includes]

		# self.aux_entries.sort(key=lambda x: x.file_index)
		self.aux_entries["file_index"] = [loader.file_index for aux, loader in loaders_and_aux]
		self.aux_entries["basename"] = [self.names.offset_dic[name] for name in aux_names]
		self.aux_entries["size"] = [loader.get_aux_size(aux) for aux, loader in loaders_and_aux]

		self.rebuild_ovs_arrays(flat_sorted_loaders, ext_lut)

	def rebuild_ovs_arrays(self, flat_sorted_loaders, ext_lut):
		"""Produces valid ovl.pools and ovs.pools and valid links for everything that points to them"""
		try:
			logging.debug(f"Sorting pools by type and updating pool groups")
			self.archives.sort(key=lambda a: a.name)

			archive_name_to_loaders = {archive.name: [] for archive in self.archives}
			for loader in flat_sorted_loaders:
				try:
					archive_name_to_loaders[loader.ovs_name].append(loader)
				except:
					logging.exception(f"Couldn't map loader {loader.name} to ovs {loader.ovs_name}")
					raise
			# remove all entries to rebuild them from the loaders
			for archive in self.archives:
				ovs = archive.content
				loaders = archive_name_to_loaders[archive.name]
				archive.num_root_entries = len(loaders)
				all_frags = set()
				for i, loader in enumerate(loaders):
					all_frags.update(loader.fragments)
					loader.root_index = i
				archive.num_fragments = len(all_frags)
				ovs.reset_field("root_entries")
				ovs.reset_field("fragments")
				# create lut for pool indices
				pools_lut = {pool: i for i, pool in enumerate(ovs.pools)}

				def resolve(pool, offset):
					# pools are already padded, and pool.size is set
					# pool is either None or part of pools_lut
					# offset is either None or an int
					if offset is None:
						assert pool
						offset = pool.size
					return pools_lut.get(pool, -1), offset

				if all_frags:
					ovs.fragments["link_ptr"]["pool_index"], \
					ovs.fragments["link_ptr"]["data_offset"], \
					ovs.fragments["struct_ptr"]["pool_index"], \
					ovs.fragments["struct_ptr"]["data_offset"] = zip(*[(*resolve(p_pool, l_o), *resolve(s_pool, s_o)) for (p_pool, l_o), (s_pool, s_o) in all_frags])
					# not needed but nice to have to keep saves consistent for easier debugging
					ovs.fragments.sort()
				# get root entries; not all ovs have root entries - some JWE2 ovs just have data
				if loaders:
					root_ptrs = [loader.root_ptr for loader in loaders]
					ovs.root_entries["struct_ptr"]["pool_index"], \
					ovs.root_entries["struct_ptr"]["data_offset"] = zip(*[resolve(s_pool, s_o) for s_pool, s_o in root_ptrs])
					ovs.assign_ids(ovs.root_entries, loaders)
				# print(ovs.fragments, ovs.root_entries)

				logging.info(f"Updating assets for {archive.name}")
				loaders_with_children = [loader for loader in loaders if loader.children]
				child_loaders = list(itertools.chain.from_iterable([loader.children for loader in loaders_with_children]))
				ovs.set_header.set_count = len(loaders_with_children)
				ovs.set_header.asset_count = len(child_loaders)
				ovs.set_header.reset_field("sets")
				ovs.set_header.reset_field("assets")
				ovs.assign_ids(ovs.set_header.sets, loaders_with_children)
				ovs.assign_ids(ovs.set_header.assets, child_loaders)
				ovs.set_header.assets["root_index"] = [loader.root_index for loader in child_loaders]
				start = 0
				for i, (set_entry, loader) in enumerate(zip(ovs.set_header.sets, loaders_with_children)):
					set_entry.start = start
					start += len(loader.children)
					# set_index is 1-based, so the first set = 1
					loader.data_entry.set_index = i + 1
			# add entries to correct ovs
			for loader in self.loaders.values():
				# attach the entries used by this loader to the ovs lists
				loader.register_entries()
				# force an update on the loader's data for older versions' data
				# and link entries like bani to banis
				loader.update()

			pools_byte_offset = 0
			# make a temporary copy so we can delete archive if needed
			for archive in tuple(self.archives):

				logging.debug(f"Sorting pools for {archive.name}")
				ovs = archive.content

				# needs to happen after loader.register_entries
				# change the hashes / indices of all entries to be valid for the current game version
				ovs.update_hashes()
				ovs.data_entries.sort(key=lambda b: (b.ext, b.file_hash))

				# depends on correct hashes applied to buffers and datas
				ovs.rebuild_buffer_groups(ext_lut)

				# update the ovs counts
				archive.num_datas = len(ovs.data_entries)
				archive.num_buffers = len(ovs.buffer_entries)
				archive.num_buffer_groups = len(ovs.buffer_groups)

				# remove stream archive if it has no pools and no roots and no datas
				if archive.name != "STATIC" and not (archive.num_pools or archive.num_root_entries or archive.num_datas):
					logging.info(f"Removed stream archive {archive.name} as it was empty")
					self.archives.remove(archive)
					continue

				archive.pools_start = pools_byte_offset
				archive.content.write_pools()
				pools_byte_offset += len(archive.content.pools_data)
				archive.pools_end = pools_byte_offset
				# at least PZ & JWE require 4 additional bytes after each pool region
				pools_byte_offset += 4
				logging.debug(
					f"Archive {archive.name} has {archive.num_pools} pools in {archive.num_pool_groups} pool_groups")

			# update archive names
			self.archive_names.update_with((
				(self.archives, "name"),
			))
			self.len_archive_names = len(self.archive_names.data)
			# update the ovl counts
			self.num_archives = len(self.archives)
			# sum counts of individual archives
			self.num_datas = sum(a.num_datas for a in self.archives)
			self.num_buffers = sum(a.num_buffers for a in self.archives)
		except:
			logging.exception("Rebuilding ovl arrays failed")

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
		stream_loaders = [(loader, stream_loader) for loader in self.loaders.values() for stream_loader in loader.streams]
		stream_loaders.sort(key=lambda x: (x[1].ovs.arg.name, x[0].abs_mem_offset))
		self.num_stream_files = len(stream_loaders)
		self.reset_field("stream_files")
		if stream_loaders:
			self.stream_files["file_offset"], self.stream_files["stream_offset"] = zip(*[
				(loader.abs_mem_offset, stream_loader.abs_mem_offset) for loader, stream_loader in stream_loaders])
		# update the archive entries to point to the stream files
		stream_files_offset = 0
		for archive in self.archives:
			archive.stream_files_offset = stream_files_offset
			archive_streams = [stream_loader for (loader, stream_loader) in stream_loaders if stream_loader.ovs.arg == archive]
			# some JWE2 dino archives have no stream_files, just extra data_entries
			stream_files_offset += len(archive_streams)

	def dump_debug_data(self):
		"""Dumps various logs needed to reverse engineer and debug the ovl format"""
		out_dir = os.path.join(self.dir, f"{self.basename}_dump")
		logging.info(f"Dumping debug data to {self.dir}")
		os.makedirs(out_dir, exist_ok=True)
		for archive_entry in self.archives:
			fp = os.path.join(out_dir, f"{self.name}_{archive_entry.name}")
			try:
				archive_entry.content.dump_stack(fp)
				archive_entry.content.dump_buffer_groups_log(fp)
				archive_entry.content.dump_pools(fp)
			except:
				logging.exception("Dumping failed")
		try:
			self.dump_buffer_info(out_dir)
		except:
			logging.exception("Dumping failed")

	@property
	def sorted_loaders(self):
		return sorted(self.loaders.values(), key=lambda l: l.name)

	def dump_buffer_info(self, out_dir):
		"""for development; collect info about fragment types"""
		def out_dir_func(n):
			"""Helper function to generate temporary output file name"""
			return os.path.normpath(os.path.join(out_dir, n))
		log_path = out_dir_func(f"{self.name}_buffer_info.log")
		with open(log_path, "w") as f:
			for loader in self.sorted_loaders:
				loader.dump_buffer_infos(f)
		for loader in self.sorted_loaders:
			loader.dump_buffers(out_dir_func)

	def save(self, filepath):
		start_time = time.time()
		logging.info(f"Writing {self.name}")
		# do this last so we also catch the assets & sets
		self.rebuild_ovl_arrays()
		# these need to be done after the rest
		self.update_stream_files()
		self.store_filepath(filepath)
		self.open_ovs_streams()
		ovl_compressed = b""
		self.reset_field("archives_meta")
		# print(self)
		# compress data stream
		for archive, meta in zip(self.iter_progress(self.archives, "Saving archives"), self.archives_meta):
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
			# size of the archive entry = 68
			# this is true for jwe2 tylo, but not for jwe2 rex 93 and many others
			meta.unk_0 = 68 + archive.uncompressed_size
			# this is fairly good, doesn't work for tylo static but all others, all of jwe2 rex 93, jwe1 parrot, pz fallow deer
			meta.unk_1 = sum([data.size_2 for data in archive.content.data_entries])

		self.close_ovs_streams()
		with open(filepath, "wb") as stream:
			self.write_fields(stream, self)
			stream.write(ovl_compressed)
		logging.info(f"Saved OVL in {time.time() - start_time:.2f} seconds")


if __name__ == "__main__":
	ovl = OvlFile()
	# ovl = Header()
	# ovl.load("C:/Users/arnfi/Desktop/Coding/ovl/OVLs/Parrot.ovl")
	# ovl.load("C:/Users/arnfi/Desktop/Coding/Frontier/Disneyland/SpatialDatabaseTest.ovl")
	# print(ovl.mimes)
