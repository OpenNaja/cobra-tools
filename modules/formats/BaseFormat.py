import logging
import os
import struct
import tempfile
from io import BytesIO

from generated.formats.ovl import UNK_HASH
from generated.formats.ovl.compounds.DependencyEntry import DependencyEntry
from generated.formats.ovl.compounds.Fragment import Fragment
from generated.formats.ovl.compounds.BufferEntry import BufferEntry
from generated.formats.ovl.compounds.MemPool import MemPool
from generated.formats.ovl.compounds.RootEntry import RootEntry
from generated.formats.ovl.compounds.DataEntry import DataEntry
from modules.formats.shared import djb2


class BaseFile:
	extension = None
	aliases = ()
	# used to check output for any temporary files that should possibly be deleted
	temp_extensions = ()

	def __init__(self, ovl, file_entry):
		self.ovl = ovl
		# this needs to be figured out by the root_entry
		self.ovs = None
		self.header = None
		self.target_name = ""

		# defined in ovl
		self.file_entry = file_entry
		self.dependencies = []
		self.aux_entries = []
		self.streams = []

		# defined in ovs
		self.root_entry = None
		self.data_entries = {}
		self.children = []
		self.fragments = set()

	@property
	def data_entry(self):
		return self.data_entries.get(self.ovs_name, None)

	@property
	def ovs_name(self):
		return self.ovs.arg.name

	def set_ovs(self, ovs_name):
		"""Assigns or creates suitable ovs"""
		self.ovs = self.ovl.create_archive(ovs_name)

	@property
	def abs_mem_offset(self):
		"""Returns the memory offset of this loader's root_entry"""
		# this is inverted compared to get_pool_offset
		# return self.ovs.get_pool_offset(self.root_ptr.pool.offset + self.root_ptr.data_offset)
		offset = self.root_ptr.pool.offset + self.root_ptr.data_offset
		# JWE, JWE2: relative offset for each pool
		if self.ovl.user_version.use_djb:
			return self.ovs.arg.pools_start + offset
		# PZ, PC: offsets relative to the whole pool block
		else:
			return offset

	def link_streams(self):
		"""Collect other loaders"""
		pass

	def _link_streams(self, names):
		"""Helper that finds and attaches existing loaders for names"""
		for name in names:
			loader = self.ovl.loaders.get(name, None)
			if loader:
				self.streams.append(loader)

	def create(self):
		raise NotImplementedError

	def collect(self):
		pass

	def pack_header(self, fmt_name):
		ovl = self.ovl
		return struct.pack(
			"<4s4BI", fmt_name, ovl.version_flag, ovl.version, ovl.bitswap, ovl.seventh_byte, int(ovl.user_version))

	def attach_frag_to_ptr(self, pointer, pool):
		"""Creates a frag on a MemStruct Pointer; needs to have been written so that io_start is set"""
		pointer.frag = self.create_fragment()
		pointer.frag.link_ptr.data_offset = pointer.io_start
		pointer.frag.link_ptr.pool = pool

	def get_pool(self, pool_type_key):
		assert pool_type_key is not None
		# get one directly editable pool, if it exists
		for pool in self.ovs.pools:
			# todo - add reasonable size condition
			if pool.type == pool_type_key and pool.new:
				return pool
		# nope, means we gotta create pool
		pool = MemPool(self.ovl.context)
		pool.data = BytesIO()
		pool.type = pool_type_key
		# we write to the pool IO directly, so do not reconstruct its data from the pointers' data
		pool.clear_data()
		pool.new = True
		self.ovs.pools.append(pool)
		return pool

	def write_data_to_pool(self, struct_ptr, pool_type_key, data):
		"""Finds or creates a suitable pool in the right ovs and writes data"""
		struct_ptr.pool = self.get_pool(pool_type_key)
		struct_ptr.write_to_pool(data)

	def ptr_relative(self, ptr, other_ptr, rel_offset=0):
		ptr.pool_index = other_ptr.pool_index
		ptr.data_offset = other_ptr.data_offset + rel_offset
		ptr.data_size = other_ptr.data_size
		ptr.pool = other_ptr.pool

	def get_content(self, filepath):
		with open(filepath, 'rb') as f:
			content = f.read()
		return content

	def create_root_entry(self):
		self.root_entry = RootEntry(self.ovl.context)
		self.children = []
		self.data_entries = {}
		self.fragments = set()
		self.ovs.transfer_identity(self.root_entry, self.file_entry)

	def set_dependency_identity(self, dependency, file_name):
		"""Use a standard file name with extension"""
		dependency.name = file_name
		dependency.basename, dependency.ext = os.path.splitext(file_name.lower())
		dependency.ext = dependency.ext.replace(".", ":")
		dependency.file_hash = djb2(dependency.basename)
		logging.debug(f"Dependency: {dependency.basename} | {dependency.ext} | {dependency.file_hash}")

	def create_dependency(self, name):
		dependency = DependencyEntry(self.ovl.context)
		self.set_dependency_identity(dependency, name)
		self.dependencies.append(dependency)
		return dependency

	def create_fragment(self):
		new_frag = Fragment(self.ovl.context)
		self.fragments.add(new_frag)
		return new_frag

	def create_data_entry(self, buffers_bytes):
		data = DataEntry(self.ovl.context)
		# needs to be created in the ovs that this loader has been assigned to use
		# needs additional research to be able to create jwe2 dino manis with stray data_entry
		self.data_entries[self.ovs_name] = data
		data.buffer_count = len(buffers_bytes)
		data.buffers = []
		for i, buffer_bytes in enumerate(buffers_bytes):
			buffer = BufferEntry(self.ovl.context)
			buffer.index = i
			data.buffers.append(buffer)
			self.ovs.transfer_identity(buffer, self.root_entry)
		self.ovs.transfer_identity(data, self.root_entry)
		data.update_data(buffers_bytes)
		return data

	def update(self):
		"""Don't do anything by default, overwrite if needed"""
		pass

	def rename_content(self, name_tuples):
		"""This is the fallback that is used when the loader class itself does not implement custom methods"""
		self.rename_fragments(name_tuples)
		# not all loaders have a header
		if self.header is not None:
			self.header.read_ptrs(self.root_ptr.pool)
		# todo - rename in buffers

	def rename_fragments(self, name_tuples):
		logging.info(f"Renaming inside {self.file_entry.name}")
		byte_name_tups = []
		try:
			# brute force fallback with same length of strings
			for old, new in name_tuples:
				assert len(old) == len(new)
				byte_name_tups.append((old.encode(), new.encode()))
			for fragment in self.fragments:
				fragment.struct_ptr.replace_bytes(byte_name_tups)
		except:
			logging.exception(f"Renaming frags failed for {self.file_entry.name}")

	def rename(self, name_tuples):
		"""Rename all entries controlled by this loader"""
		entries = [self.file_entry, *self.dependencies, *self.aux_entries, self.root_entry, ]
		for data_entry in self.data_entries.values():
			entries.extend((data_entry, *data_entry.buffers))
		for entry in entries:
			if UNK_HASH in entry.name:
				logging.warning(f"Skipping {entry.file_hash} because its hash could not be resolved to a name")
				return
			# update name
			for old, new in name_tuples:
				entry.name = entry.name.replace(old, new)
			entry.basename, entry.ext = os.path.splitext(entry.name)
		# also rename target_name
		for old, new in name_tuples:
			self.target_name = self.target_name.replace(old, new)

	def get_tmp_dir(self):
		temp_dir = tempfile.mkdtemp("-cobra")

		def out_dir_func(n):
			"""Helper function to generate temporary output file name"""
			return os.path.normpath(os.path.join(temp_dir, n))

		return temp_dir, out_dir_func

	@property
	def root_ptr(self):
		"""Shorthand for the root entry's struct_ptr"""
		return self.root_entry.struct_ptr

	def register_entries(self):

		self.ovs.fragments.extend(self.fragments)
		self.ovs.root_entries.append(self.root_entry)

		for ovs_name, data_entry in self.data_entries.items():
			ovs = self.ovl.create_archive(ovs_name)
			ovs.data_entries.append(data_entry)
			ovs.buffer_entries.extend(data_entry.buffers)

	def remove(self, remove_file=True):
		logging.info(f"Removing {self.file_entry.name}")
		self.remove_pointers()

		if remove_file:
			# remove the loader from ovl so it is not saved
			self.ovl.loaders.pop(self.file_entry.name)

		# remove streamed and child files
		for loader in self.streams + self.children:
			loader.remove()

	def remove_pointers(self):
		self.root_entry.struct_ptr.del_struct()
		for frag in self.fragments:
			frag.link_ptr.del_link()
			frag.struct_ptr.del_struct()
		for dep in self.dependencies:
			dep.link_ptr.del_link()

	def register_ptrs(self):
		self.root_entry.struct_ptr.add_struct(self.root_entry)
		for frag in self.fragments:
			frag.link_ptr.add_link(frag)
			frag.struct_ptr.add_struct(frag)
		for dep in self.dependencies:
			dep.link_ptr.add_link(dep)

	def track_ptrs(self):
		logging.debug(f"Tracking {self.file_entry.name}")
		# this is significantly slower if a list is used
		self.fragments = set()
		if self.root_entry.struct_ptr.pool:
			self.check_for_ptrs(self.root_entry.struct_ptr)

	def check_for_ptrs(self, parent_struct_ptr):
		"""Recursively assigns pointers to an entry"""
		# tracking children for each struct adds no detectable overhead for animal ovls
		parent_struct_ptr.children = set()
		# see if any pointers are inside this struct
		for offset, entry in parent_struct_ptr.pool.offset_2_link_entry.items():
			if parent_struct_ptr.data_offset <= offset < parent_struct_ptr.data_offset + parent_struct_ptr.data_size:
				parent_struct_ptr.children.add(entry)
				if isinstance(entry, Fragment):
					# points to a child struct
					struct_ptr = entry.struct_ptr
					if entry not in self.fragments:
						self.fragments.add(entry)
						self.check_for_ptrs(struct_ptr)

	def dump_buffer_infos(self, f):
		debug_str = f"\n\nFILE {self.file_entry.name}"
		f.write(debug_str)

		for ovs_name, data_entry in self.data_entries.items():
			f.write(f"\nData in {ovs_name} with {len(data_entry.buffers)} buffers")
			for buffer in data_entry.buffers:
				f.write(f"\nBuffer {buffer.index}, size {buffer.size}")
		# for loader in self.streams:
		# 	f.write(f"\nSTREAM {loader.file_entry.name}")
		# 	loader.dump_buffer_infos(f)

	def dump_buffers(self, out_dir):
		paths = []
		if self.data_entry:
			for i, b in enumerate(self.data_entry.buffer_datas):
				name = f"{self.file_entry.name}_{i}.dmp"
				out_path = out_dir(name)
				paths.append(out_path)
				with open(out_path, 'wb') as outfile:
					outfile.write(b)
		return paths

	def handle_paths(self, paths, show_temp_files):
		"""Deletes temporary files if asked and returns all valid paths."""
		if self.temp_extensions and not show_temp_files:
			paths_to_remove = [p for p in paths if os.path.splitext(p)[1].lower() in self.temp_extensions]
			for p in paths_to_remove:
				os.remove(p)
			return [p for p in paths if p not in paths_to_remove]
		return paths

	def __eq__(self, other):
		logging.info(f"Comparing {self.file_entry.name}")
		same = True
		# mime version
		if self.file_entry.mime.mime_version != other.file_entry.mime.mime_version:
			logging.warning(f"Mime version does not match")
			same = False
		# data
		if len(self.data_entries) != len(other.data_entries):
			logging.warning(f"Amount of data entries does not match")
			same = False
		for archive_name, data_entry in self.data_entries.items():
			assert archive_name in other.data_entries
			other_data = other.data_entries[archive_name]
			if data_entry != other_data:
				logging.warning(f"this: {data_entry}")
				logging.warning(f"other: {other_data}")
				same = False
		# frags
		if len(self.fragments) != len(other.fragments):
			logging.warning(f"Amount of fragments does not match")
			same = False
		# children
		if len(self.children) != len(other.children):
			logging.warning(f"Amount of children does not match")
			same = False
		# root entry
		this_root = self.root_entry.struct_ptr.data
		other_root = other.root_entry.struct_ptr.data
		if this_root != other_root:
			logging.warning(f"Root entry data does not match - this {len(this_root)} vs other {len(other_root)}")
			min_len = min((len(this_root), len(other_root)))
			this_root = this_root[:min_len]
			other_root = other_root[:min_len]
			if this_root == other_root:
				logging.info(f"Root entry data does actually match, size difference is likely just padding")
			else:
				same = False
		# ovs name
		if self.ovs_name != other.ovs_name:
			logging.warning(f"OVS name does not match")
			same = False
		# streams
		if len(self.streams) != len(other.streams):
			logging.warning(f"Amount of streams does not match self {len(self.streams)} vs other {len(other.streams)}")
			same = False
		for stream, other_stream in zip(self.streams, other.streams):
			if stream != other_stream:
				logging.warning(f"Stream files do not match")
				same = False
		return same

	def log_versions(self):
		logging.info(f"{self.file_entry.ext} {self.file_entry.mime.mime_version}")
		for loader in self.children:
			entry = loader.file_entry
			logging.info(f"{entry.ext} {entry.mime.mime_version}")
		for loader in self.streams:
			entry = loader.file_entry
			logging.info(f"{entry.ext} {entry.mime.mime_version}")


class MemStructLoader(BaseFile):
	target_class: None

	def extract(self, out_dir):
		name = self.root_entry.name
		if self.header:
			out_path = out_dir(name)
			self.header.to_xml_file(self.header, out_path, debug=self.ovl.do_debug)
			return out_path,
		else:
			logging.warning(f"File '{name}' has no header - has the OVL finished loading?")
			return ()

	def collect(self):
		super().collect()
		self.header = self.target_class.from_stream(self.root_ptr.stream, self.ovl.context)
		# print(self.header)
		self.header.read_ptrs(self.root_ptr.pool)

	def create(self):
		self.create_root_entry()
		self.header = self.target_class.from_xml_file(self.file_entry.path, self.ovl.context)
		# print(self.header)
		self.header.write_ptrs(self, self.root_ptr, self.file_entry.pool_type)
