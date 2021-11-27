import logging
import os
import struct

from generated.formats.ovl.compound.DependencyEntry import DependencyEntry
from generated.formats.ovl.compound.Fragment import Fragment
from generated.formats.ovl.compound.BufferEntry import BufferEntry
from generated.formats.ovl.compound.MemPool import MemPool
from generated.formats.ovl.compound.PoolType import PoolType
from generated.formats.ovl.compound.SizedStringEntry import SizedStringEntry
from generated.formats.ovl.compound.HeaderPointer import HeaderPointer
from generated.formats.ovl.compound.DataEntry import DataEntry
from generated.io import BinaryStream
from modules.formats.shared import djb
import xml.etree.ElementTree as ET # prob move this to a custom modules.helpers or utils?


class BaseFile:

	def __init__(self, ovl, file_entry):
		self.ovl = ovl
		self.ovs = ovl.static_archive.content
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
		logging.debug(f"out_frags {len(out_frags)}")
		return out_frags

	def assign_ss_entry(self):
		self.sized_str_entry = self.ovl.get_sized_str_entry(self.file_entry.name)

	def assign_fixed_frags(self, count):
		self.assign_ss_entry()
		ss_pointer = self.sized_str_entry.pointers[0]
		self.sized_str_entry.fragments = self.ovs.frags_from_pointer(ss_pointer, count)

	def get_pool(self, pool_type_key):
		# get one if it exists
		for pool_index, pool in enumerate(self.ovs.pools):
			if pool.type == pool_type_key:
				return pool_index, pool
		# nope, means we gotta create pool type and pool
		pool_type = PoolType(self.ovl.context)
		pool_type.type = pool_type_key
		pool_type.num_pools = 1

		pool = MemPool(self.ovl.context)
		pool.data = BinaryStream()
		# the real address isn't known until it is written, but declare it anyway
		pool.address = 0
		# assign_versions(pool.data, get_versions(self.ovl))
		pool.type = pool_type_key
		self.ovs.pool_types.append(pool_type)
		self.ovs.pools.append(pool)
		return len(self.ovs.pools)-1, pool

	def write_to_pool(self, ptr, pool_type_key, data):
		ptr.pool_index, ptr.pool = self.get_pool(pool_type_key)
		ptr.data = data
		ptr.write_data()

	def get_content(self, filepath):
		with open(filepath, 'rb') as f:
			content = f.read()
		return content

	def get_file_entry(self, file_name):
		for file_entry in self.ovl.files:
			if file_entry.name == file_name:
				return file_entry

	def create_ss_entry(self, file_entry):
		ss_entry = SizedStringEntry(self.ovl.context)
		ss_entry.children = []
		ss_entry.fragments = []
		self.ovs.transfer_identity(ss_entry, file_entry)
		ss_entry.pointers.append(HeaderPointer(self.ovl.context))
		self.ovs.sized_str_entries.append(ss_entry)
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

	def create_data_entry(self, ss_entry, buffer_bytes):
		new_data = DataEntry(self.ovl.context)
		self.ovs.transfer_identity(new_data, ss_entry)
		ss_entry.data_entry = new_data
		new_data.buffer_count = len(buffer_bytes)
		new_data.buffers = []
		for i, b in enumerate(buffer_bytes):
			new_buff = BufferEntry(self.ovl.context)
			self.ovs.transfer_identity(new_buff, ss_entry)
			new_buff.index = i
			new_data.buffers.append(new_buff)
			self.ovs.buffer_entries.append(new_buff)
		self.ovs.data_entries.append(new_data)
		new_data.update_data(buffer_bytes)
		return new_data

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

	def get_zstr(self, d):
		end = d.find(b'\x00')
		return d[:end].decode()
