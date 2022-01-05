import logging
import os
import struct
import tempfile

from generated.formats.ovl.compound.DependencyEntry import DependencyEntry
from generated.formats.ovl.compound.Fragment import Fragment
from generated.formats.ovl.compound.BufferEntry import BufferEntry
from generated.formats.ovl.compound.MemPool import MemPool
from generated.formats.ovl.compound.PoolGroup import PoolGroup
from generated.formats.ovl.compound.SizedStringEntry import SizedStringEntry
from generated.formats.ovl.compound.HeaderPointer import HeaderPointer
from generated.formats.ovl.compound.DataEntry import DataEntry
from generated.io import BinaryStream
from modules.formats.shared import djb
import xml.etree.ElementTree as ET # prob move this to a custom modules.helpers or utils?


class BaseFile:

	def __init__(self, ovl, file_entry):
		self.ovl = ovl
		self.ovs = ovl.create_archive()
		self.file_entry = file_entry
		self.sized_str_entry = None

	def create(self):
		raise NotImplementedError

	def collect(self):
		raise NotImplementedError

	def pack_header(self, fmt_name):
		ovl = self.ovl
		return struct.pack(
			"<4s4BI", fmt_name, ovl.version_flag, ovl.version, ovl.bitswap, ovl.seventh_byte, int(ovl.user_version))

	def collect_array(self, ptr, count, entry_size):
		logging.debug(f"Collecting array {count} {entry_size}")
		array_size = count * entry_size
		array_data = ptr.read_from_pool(array_size)
		frags = self.ovs.frags_for_pointer(ptr)
		logging.debug(f"frags {len(frags)}")
		offset_start = ptr.data_offset
		offset_end = offset_start + array_size
		out_frags = self.get_frags_between(frags, offset_start, offset_end)
		return out_frags, array_data

	# def collect_array_elements(self, ptr, count, entry_size):
	# 	logging.debug(f"Collecting array {count} {entry_size}")
	# 	offset_start = ptr.data_offset
	# 	data_frags = []
	# 	array_size = count * entry_size
	# 	array_data = ptr.read_from_pool(array_size)
	# 	for i in range(count):
	# 		offset_start += entry_size
	# 	frags = self.ovs.frags_for_pointer(ptr)
	# 	logging.debug(f"frags {len(frags)}")
	# 	offset_end = offset_start + array_size
	# 	out_frags = self.get_frags_between(frags, offset_start, offset_end)
	# 	return out_frags, array_data

	def get_frags_between(self, frags, offset_start, offset_end):
		out_frags = []
		for frag in frags:
			o = frag.pointers[0].data_offset
			if offset_start <= o < offset_end:
				out_frags.append(frag)
		logging.debug(f"found {len(out_frags)} frags between {offset_start} and {offset_end}")
		return out_frags

	def assign_ss_entry(self):
		self.sized_str_entry = self.ovl.get_sized_str_entry(self.file_entry.name)

	def assign_fixed_frags(self, count):
		self.assign_ss_entry()
		ss_pointer = self.sized_str_entry.pointers[0]
		self.sized_str_entry.fragments = self.ovs.frags_from_pointer(ss_pointer, count)

	def get_streams(self):
		logging.debug(f"Num streams: {len(self.file_entry.streams)}")
		all_buffers = [*self.sized_str_entry.data_entry.buffers]
		logging.debug(f"Static buffers: {all_buffers}")
		for stream_file in self.file_entry.streams:
			stream_ss = self.ovl.get_sized_str_entry(stream_file.name)
			all_buffers.extend(stream_ss.data_entry.buffers)
			logging.debug(f"Stream buffers: {stream_ss.data_entry.buffers} {stream_file.name}")
		return all_buffers

	def get_pool(self, pool_type_key, ovs="STATIC"):
		ovs_file = self.ovl.create_archive(ovs)
		# get one directly editable pool, if it exists
		for pool_index, pool in enumerate(ovs_file.pools):
			if pool.type == pool_type_key and not pool.update_from_ptrs:
				return pool_index, pool
		# nope, means we gotta create pool
		pool = MemPool(self.ovl.context)
		pool.data = BinaryStream()
		# the real address isn't known until it is written, but declare it anyway
		pool.address = 0
		# assign_versions(pool.data, get_versions(self.ovl))
		pool.type = pool_type_key
		# we write to the pool IO directly, so do not reconstruct its data from the pointers' data
		pool.update_from_ptrs = False
		ovs_file.pools.append(pool)
		return len(ovs_file.pools)-1, pool

	def write_to_pool(self, ptr, pool_type_key, data, ovs="STATIC"):
		ptr.pool_index, ptr.pool = self.get_pool(pool_type_key, ovs=ovs)
		ptr.data = data
		ptr.write_data()

	def ptr_relative(self, ptr, other_ptr, rel_offset=0):
		ptr.pool_index = other_ptr.pool_index
		ptr.data_offset = other_ptr.data_offset + rel_offset
		# hack
		ptr.data = other_ptr.data
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

	def create_ss_entry(self, file_entry, ovs="STATIC"):
		ss_entry = SizedStringEntry(self.ovl.context)
		ss_entry.children = []
		ss_entry.fragments = []
		ss_entry.pointers.append(HeaderPointer(self.ovl.context))
		ovs_file = self.ovl.create_archive(ovs)
		ovs_file.transfer_identity(ss_entry, file_entry)
		ovs_file.sized_str_entries.append(ss_entry)
		return ss_entry

	def set_dependency_identity(self, dependency, file_name):
		"""Use a standard file name with extension"""
		dependency.name = file_name
		dependency.basename, dependency.ext = os.path.splitext(file_name)
		dependency.ext = dependency.ext.replace(".", ":")
		dependency.file_hash = djb(dependency.basename.lower())

	def create_dependency(self, name):
		dependency = DependencyEntry(self.ovl.context)
		self.set_dependency_identity(dependency, name)
		dependency.pointers.append(HeaderPointer(self.ovl.context))
		self.file_entry.dependencies.append(dependency)
		return dependency

	def create_fragments(self, ss, count):
		frags = [self.create_fragment() for i in range(count)]
		ss.fragments.extend(frags)
		return frags

	def create_fragment(self):
		new_frag = Fragment(self.ovl.context)
		new_frag.pointers.append(HeaderPointer(self.ovl.context))
		new_frag.pointers.append(HeaderPointer(self.ovl.context))
		self.ovs.fragments.append(new_frag)
		return new_frag

	def create_data_entry(self, ss_entry, buffers_bytes, ovs="STATIC"):
		ovs_file = self.ovl.create_archive(ovs)
		data = DataEntry(self.ovl.context)
		ss_entry.data_entry = data
		data.buffer_count = len(buffers_bytes)
		data.buffers = []
		for i, buffer_bytes in enumerate(buffers_bytes):
			buffer = BufferEntry(self.ovl.context)
			buffer.index = i
			data.buffers.append(buffer)
			ovs_file.transfer_identity(buffer, ss_entry)
			ovs_file.buffer_entries.append(buffer)
		ovs_file.transfer_identity(data, ss_entry)
		ovs_file.data_entries.append(data)
		data.update_data(buffers_bytes)
		return data

	def update(self):
		"""Don't do anything by default, overwrite if needed"""
		pass

	def indent(self, e, level=0):
		i = "\n" + level*"	"
		if len(e):
			if not e.text or not e.text.strip():
				e.text = i + "	"
			if not e.tail or not e.tail.strip():
				e.tail = i
			for e in e:
				self.indent(e, level+1)
			if not e.tail or not e.tail.strip():
				e.tail = i
		else:
			if level and (not e.tail or not e.tail.strip()):
				e.tail = i

	def load_xml(self, xml_path):
		tree = ET.parse(xml_path)
		return tree.getroot()

	def write_xml(self, out_path, xml_data):
		self.indent(xml_data)
		xml_text = ET.tostring(xml_data)
		with open(out_path, 'wb') as outfile:
			outfile.write(xml_text)

	def p1_ztsr(self, frag):
		ptr = frag.pointers[1]
		# not needed here, but for good measure
		ptr.strip_zstring_padding()
		return self.get_zstr(ptr.data)

	def get_zstr(self, d):
		end = d.find(b'\x00')
		return d[:end].decode()

	def rename_content(self, name_tuple_bytes):
		# try:
		# 	# hash the internal buffers
		# 	for archive_entry in ovl.archives:
		# 		ovs = archive_entry.content
		# 		for fragment in ovs.fragments:
		# 			for ptr in fragment.pointers:
		# 				ptr.data = replace_bytes(ptr.data, name_tups_new)
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
