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

	def validate_child(self, file_path):
		return False

	def create(self):
		raise NotImplementedError

	def collect(self):
		raise NotImplementedError

	def pack_header(self, fmt_name):
		ovl = self.ovl
		return struct.pack(
			"<4s4BI", fmt_name, ovl.version_flag, ovl.version, ovl.bitswap, ovl.seventh_byte, int(ovl.user_version))

	def assign_root_entry(self):
		self.root_entry, archive = self.ovl.get_root_entry(self.file_entry.name)
		self.ovs = archive.content

	def get_streams(self):
		logging.debug(f"Num streams: {len(self.file_entry.streams)}")
		all_buffers = [*self.root_entry.data_entry.buffers]
		logging.debug(f"Static buffers: {all_buffers}")
		for stream_file in self.file_entry.streams:
			stream_ss, archive = self.ovl.get_root_entry(stream_file.name)
			all_buffers.extend(stream_ss.data_entry.buffers)
			logging.debug(f"Stream buffers: {stream_ss.data_entry.buffers} {stream_file.name}")
		return all_buffers

	def get_pool(self, pool_type_key, ovs="STATIC"):
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

	def write_to_pool(self, ptr, pool_type_key, data, ovs="STATIC"):
		ptr.pool = self.get_pool(pool_type_key, ovs=ovs)
		ptr.write_to_pool(data)

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
		self.ovl.files.append(file_entry)
		return file_entry

	def create_root_entry(self, file_entry, ovs="STATIC"):
		root_entry = RootEntry(self.ovl.context)
		root_entry.children = []
		root_entry.fragments = set()
		ovs_file = self.ovl.create_archive(ovs)
		ovs_file.transfer_identity(root_entry, file_entry)
		ovs_file.root_entries.append(root_entry)
		return root_entry

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

	def create_fragment(self, root_entry):
		new_frag = Fragment(self.ovl.context)
		root_entry.fragments.add(new_frag)
		return new_frag

	def create_data_entry(self, root_entry, buffers_bytes, ovs="STATIC"):
		ovs_file = self.ovl.create_archive(ovs)
		data = DataEntry(self.ovl.context)
		root_entry.data_entry = data
		data.buffer_count = len(buffers_bytes)
		data.buffers = []
		for i, buffer_bytes in enumerate(buffers_bytes):
			buffer = BufferEntry(self.ovl.context)
			buffer.index = i
			data.buffers.append(buffer)
			ovs_file.transfer_identity(buffer, root_entry)
			ovs_file.buffer_entries.append(buffer)
		ovs_file.transfer_identity(data, root_entry)
		ovs_file.data_entries.append(data)
		data.update_data(buffers_bytes)
		return data

	def update(self):
		"""Don't do anything by default, overwrite if needed"""
		pass

	def rename_content(self, name_tuple_bytes):
		# try:
		# 	# hash the internal buffers
		# 	for archive_entry in ovl.archives:
		# 		ovs = archive_entry.content
		# 		for fragment in ovs.fragments:
		# 			for pointer in fragment.pointers:
		# 				pointer.data = replace_bytes(pointer.data, name_tups_new)
		# except Exception as err:
		# 	showdialog(str(err))
		# logging.info("Done!")
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
		for frag in self.root_entry.fragments:
			frag.struct_ptr.remove()
		self.root_entry.struct_ptr.remove()

	def remove(self):
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

		# remove entries in ovl
		# self.ovl.files.pop(i)
		self.ovl.files.remove(self.file_entry)

		# todo children files
		# remove streamed and child files
		for stream_file in self.file_entry.streams:
			if stream_file.loader:
				stream_file.loader.remove()
			else:
				logging.warning(f"Could not remove {stream_file.name} as it has no loader")


class MemStructLoader(BaseFile):
	target_class: None

	def extract(self, out_dir, show_temp_files, progress_callback):
		name = self.root_entry.name
		out_path = out_dir(name)
		self.header.to_xml_file(out_path)
		return out_path,

	def collect(self):
		self.assign_root_entry()
		self.header = self.target_class.from_stream(self.root_ptr.stream, self.ovl.context)
		self.header.read_ptrs(self.root_ptr.pool)
		# print(self.header)

	def create(self):
		self.root_entry = self.create_root_entry(self.file_entry)
		self.header = self.target_class.from_xml_file(self.file_entry.path, self.ovl.context)
		# print(self.header)
		self.header.write_ptrs(self, self.ovs, self.root_ptr, self.file_entry.pool_type)

	def load(self, file_path):
		# todo - fix removal etc
		# self.remove_pointers()
		self.header = self.target_class.from_xml_file(file_path, self.ovl.context)
		# print(self.header)
		self.header.write_ptrs(self, self.ovs, self.root_ptr, self.file_entry.pool_type)
