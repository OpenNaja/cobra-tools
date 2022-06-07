import logging
import os
import struct
import tempfile

from generated.formats.ovl import UNK_HASH
from generated.formats.ovl.compound.DependencyEntry import DependencyEntry
from generated.formats.ovl.compound.Fragment import Fragment
from generated.formats.ovl.compound.BufferEntry import BufferEntry
from generated.formats.ovl.compound.MemPool import MemPool
from generated.formats.ovl.compound.RootEntry import RootEntry
from generated.formats.ovl.compound.DataEntry import DataEntry
from generated.formats.ovl_base.basic import ConvStream
from modules.formats.shared import djb


class BaseFile:
	extension = None
	child_extensions = ()

	def __init__(self, ovl, file_entry):
		self.ovl = ovl
		# this needs to be figured out by the root_entry
		self.ovs = None
		self.header = None

		# defined in ovl
		self.file_entry = file_entry
		self.dependencies = []
		self.aux_entries = []
		self.streams = []

		# defined in ovs
		self.root_entry = None
		self.data_entry = None
		self.children = []
		self.fragments = set()

	def set_ovs(self, ovs_name):
		"""Assigns or creates suitable ovs"""
		self.ovs = self.ovl.create_archive(ovs_name)

	@property
	def abs_mem_offset(self):
		"""Returns the memory offset of this loader's root_entry"""
		offset = self.root_ptr.pool.offset + self.root_ptr.data_offset
		# JWE, JWE2: relative offset for each pool
		if self.ovl.user_version.is_jwe:
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

	def validate_child(self, file_path):
		return False

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
		pool.data = ConvStream()
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
		ptr.pool = other_ptr.pool

	def get_content(self, filepath):
		with open(filepath, 'rb') as f:
			content = f.read()
		return content

	def create_root_entry(self):
		self.root_entry = RootEntry(self.ovl.context)
		self.children = []
		self.data_entry = None
		self.fragments = set()
		self.ovs.transfer_identity(self.root_entry, self.file_entry)
		# self.ovs.root_entries.append(self.root_entry)

	def set_dependency_identity(self, dependency, file_name):
		"""Use a standard file name with extension"""
		dependency.name = file_name
		dependency.basename, dependency.ext = os.path.splitext(file_name.lower())
		dependency.ext = dependency.ext.replace(".", ":")
		dependency.file_hash = djb(dependency.basename)
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
		self.data_entry = data
		data.buffer_count = len(buffers_bytes)
		data.buffers = []
		for i, buffer_bytes in enumerate(buffers_bytes):
			buffer = BufferEntry(self.ovl.context)
			buffer.index = i
			data.buffers.append(buffer)
			self.ovs.transfer_identity(buffer, self.root_entry)
			# self.ovs.buffer_entries.append(buffer)
		self.ovs.transfer_identity(data, self.root_entry)
		# self.ovs.data_entries.append(data)
		data.update_data(buffers_bytes)
		return data

	def update(self):
		"""Don't do anything by default, overwrite if needed"""
		pass

	def rename_content(self, name_tuples):
		# this needs to be implemented per file format to actually do something
		pass

	def rename(self, name_tuples):
		"""Rename all entries controlled by this loader"""
		entries = [self.file_entry, *self.dependencies, *self.aux_entries, self.root_entry, ]
		if self.data_entry:
			entries.extend((self.data_entry, *self.data_entry.buffers))
		for entry in entries:
			if UNK_HASH in entry.name:
				logging.warning(f"Skipping {entry.file_hash} because its hash could not be resolved to a name")
				return
			# update name
			for old, new in name_tuples:
				entry.name = entry.name.replace(old, new)
			entry.basename, entry.ext = os.path.splitext(entry.name)

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
		if self.data_entry:
			self.ovs.data_entries.append(self.data_entry)
			self.ovs.buffer_entries.extend(self.data_entry.buffers)

	def remove(self, remove_file=True):
		logging.info(f"Removing {self.file_entry.name}")
		self.remove_pointers()

		if remove_file:
			# remove the loader from ovl so it is not saved
			self.ovl.loaders.pop(self.file_entry.name)

		# remove streamed and child files
		for loader in self.streams + self.children:
			loader.remove()

	def load(self, file_path):
		logging.info(f"Injecting {file_path} with new workflow")
		self.remove(remove_file=False)
		self.file_entry.path = file_path
		self.create()

	def remove_pointers(self):
		# in theory, this should handle the removal of all other pointers
		# remove any struct pointers - the link ptrs are removed as well
		self.root_entry.struct_ptr.remove()
		for frag in self.fragments:
			frag.struct_ptr.remove()

	# def get_pools(self):
	# 	# todo - can't do this here as frags need to be assigned to loaders first
	# 	for dep in self.dependencies:
	# 		# the index goes into the flattened list of ovl pools
	# 		dep.link_ptr.assign_pool(self.ovl.pools)
	# 	# attach all pointers to their pool
	# 	self.root_entry.assign_pool(self.ovs.pools)
	# 	for frag in self.ovs.fragments:
	# 		frag.link_ptr.assign_pool(self.ovs.pools)
	# 		frag.struct_ptr.assign_pool(self.ovs.pools)

	def register_ptrs(self):
		if self.root_entry.struct_ptr.pool:
			self.root_entry.struct_ptr.pool.add_struct(self.root_entry)
		for frag in self.fragments:
			frag.link_ptr.pool.add_link(frag)
			frag.struct_ptr.pool.add_struct(frag)
		for dep in self.dependencies:
			dep.link_ptr.pool.add_link(dep)

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


class MemStructLoader(BaseFile):
	target_class: None

	def extract(self, out_dir, show_temp_files, progress_callback):
		name = self.root_entry.name
		out_path = out_dir(name)
		self.header.to_xml_file(out_path)
		return out_path,

	def collect(self):
		super().collect()
		self.header = self.target_class.from_stream(self.root_ptr.stream, self.ovl.context)
		self.header.read_ptrs(self.root_ptr.pool)
		# print(self.header)

	def create(self):
		self.create_root_entry()
		self.header = self.target_class.from_xml_file(self.file_entry.path, self.ovl.context)
		# print(self.header)
		self.header.write_ptrs(self, self.root_ptr, self.file_entry.pool_type)
