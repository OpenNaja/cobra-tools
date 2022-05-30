import logging
import os
import struct
import tempfile

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
		self.ovs = ovl.create_archive()
		self.file_entry = file_entry
		self.root_entry = None
		self.streams = []
		self.children = []
		self.header = None
		self.fragments = set()

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

	def create(self, ovs_name=""):
		raise NotImplementedError

	def collect(self):
		pass

	def pack_header(self, fmt_name):
		ovl = self.ovl
		return struct.pack(
			"<4s4BI", fmt_name, ovl.version_flag, ovl.version, ovl.bitswap, ovl.seventh_byte, int(ovl.user_version))

	def assign_root_entry(self):
		self.root_entry, archive = self.ovl.get_root_entry(self.file_entry.name)
		self.ovs = archive.content

	def attach_frag_to_ptr(self, pointer, pool):
		"""Creates a frag on a MemStruct Pointer; needs to have been written so that io_start is set"""
		pointer.frag = self.create_fragment()
		pointer.frag.link_ptr.data_offset = pointer.io_start
		pointer.frag.link_ptr.pool = pool

	def get_pool(self, pool_type_key, ovs="STATIC"):
		assert pool_type_key is not None
		ovs_file = self.ovl.create_archive(ovs)
		# get one directly editable pool, if it exists
		for pool in ovs_file.pools:
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
		ovs_file.pools.append(pool)
		return pool

	def write_data_to_pool(self, struct_ptr, pool_type_key, data, ovs="STATIC"):
		"""Finds or creates a suitable pool in the right ovs and writes data"""
		struct_ptr.pool = self.get_pool(pool_type_key, ovs=ovs)
		struct_ptr.write_to_pool(data)

	def ptr_relative(self, ptr, other_ptr, rel_offset=0):
		ptr.pool_index = other_ptr.pool_index
		ptr.data_offset = other_ptr.data_offset + rel_offset
		ptr.pool = other_ptr.pool

	def get_content(self, filepath):
		with open(filepath, 'rb') as f:
			content = f.read()
		return content

	def get_file_entry(self, file_path):
		file_name = os.path.basename(file_path)
		for file_entry in self.ovl.files:
			if file_entry.name == file_name:
				return file_entry
		file_entry = self.ovl.create_file_entry(file_path)
		file_entry.loader = self.ovl.get_loader(file_entry)
		self.ovl.loaders[file_entry.name] = file_entry.loader
		self.ovl.files.append(file_entry)
		return file_entry

	def create_root_entry(self, ovs="STATIC"):
		self.root_entry = RootEntry(self.ovl.context)
		self.root_entry.children = []
		self.root_entry.data_entry = None
		self.fragments = set()
		self.ovs = self.ovl.create_archive(ovs)
		self.ovs.transfer_identity(self.root_entry, self.file_entry)
		self.ovs.root_entries.append(self.root_entry)

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
		self.file_entry.dependencies.append(dependency)
		return dependency

	def create_fragment(self):
		new_frag = Fragment(self.ovl.context)
		self.fragments.add(new_frag)
		return new_frag

	def create_data_entry(self, buffers_bytes, ovs="STATIC"):
		ovs_file = self.ovl.create_archive(ovs)
		data = DataEntry(self.ovl.context)
		self.root_entry.data_entry = data
		data.buffer_count = len(buffers_bytes)
		data.buffers = []
		for i, buffer_bytes in enumerate(buffers_bytes):
			buffer = BufferEntry(self.ovl.context)
			buffer.index = i
			data.buffers.append(buffer)
			ovs_file.transfer_identity(buffer, self.root_entry)
			ovs_file.buffer_entries.append(buffer)
		ovs_file.transfer_identity(data, self.root_entry)
		ovs_file.data_entries.append(data)
		data.update_data(buffers_bytes)
		return data

	def update(self):
		"""Don't do anything by default, overwrite if needed"""
		pass

	def rename_content(self, name_tuple_bytes):
		pass

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

	def remove_pointers(self):
		# remove any pointers
		for frag in self.fragments:
			frag.struct_ptr.remove()
		self.root_entry.struct_ptr.remove()

	def remove(self, remove_file=True):
		logging.info(f"Removing {self.file_entry.name}")
		self.remove_pointers()

		# remove entries in ovs
		self.ovs.root_entries.remove(self.root_entry)
		data = self.root_entry.data_entry
		if data:
			for buffer in data.buffers:
				buffer.update_data(b"")
				self.ovs.buffer_entries.remove(buffer)
			self.ovs.data_entries.remove(data)

		if remove_file:
			# remove entries in ovl
			# self.ovl.files.pop(i)
			self.ovl.files.remove(self.file_entry)

		# clear dependencies, they are automatically regenerated for the ovl on saving
		self.file_entry.dependencies.clear()
		# remove children files
		for file_entry in self.ovl.files:
			for child_root in self.root_entry.children:
				if file_entry.name == child_root.name:
					if file_entry.loader:
						file_entry.loader.remove()
						break
					else:
						logging.warning(f"Could not remove {file_entry.name} as it has no loader")
		# remove streamed and child files
		for loader in self.streams:
			loader.remove()

	def load(self, file_path):
		logging.info(f"Injecting {file_path} with new workflow")
		self.remove(remove_file=False)
		self.file_entry.path = file_path
		self.create()

	def register_created_ptrs(self):
		if self.root_entry.struct_ptr.pool:
			self.root_entry.struct_ptr.pool.add_struct(self.root_entry)
		for frag in self.fragments:
			frag.link_ptr.pool.add_link(frag)
			frag.struct_ptr.pool.add_struct(frag)
		for dep in self.file_entry.dependencies:
			dep.link_ptr.pool.add_link(dep)

	def track_ptrs(self):
		logging.info(f"Tracking {self.file_entry.name}")
		self.assign_root_entry()
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
		self.header.write_ptrs(self, self.ovs, self.root_ptr, self.file_entry.pool_type)
