import logging
import os
import struct
import tempfile

from generated.formats.ovl.compound.DependencyEntry import DependencyEntry
from generated.formats.ovl.compound.Fragment import Fragment
from generated.formats.ovl.compound.BufferEntry import BufferEntry
from generated.formats.ovl.compound.MemPool import MemPool
from generated.formats.ovl.compound.SizedStringEntry import SizedStringEntry
from generated.formats.ovl.compound.DataEntry import DataEntry
from generated.formats.ovl_base.basic import ConvStream
from modules.formats.shared import djb
import xml.etree.ElementTree as ET # prob move this to a custom modules.helpers or utils?

from modules.helpers import as_bytes


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

	def collect_array_elements(self, ptr, count, entry_size):
		out_frags, array_data = self.collect_array(ptr, count, entry_size)
		frag_data_pairs = []
		for i in range(count):
			x = i * entry_size
			abs_offset = ptr.data_offset + x
			frags_entry = self.get_frags_between(out_frags, abs_offset, abs_offset+entry_size)
			rel_offsets = [f.pointers[0].data_offset-abs_offset for f in frags_entry]
			# frag_data_pairs.append((frags_entry, array_data[x:x+entry_size], rel_offsets))
			frag_data_pairs.append((frags_entry, array_data[x:x+entry_size]))
		return frag_data_pairs

	def get_frags_between(self, frags, offset_start, offset_end):
		out_frags = []
		for frag in frags:
			o = frag.pointers[0].data_offset
			if offset_start <= o < offset_end:
				out_frags.append(frag)
		logging.debug(f"found {len(out_frags)} frags between {offset_start} and {offset_end}")
		return out_frags

	def get_str_list_at_offset(self, count, offset):
		"""Gets list of strings pointed to at offset from ss ptr"""
		output = []
		if count:
			link_frag = self.ovs.frag_at_pointer(self.sized_str_entry.pointers[0], offset=offset)
			tmp_fragments = self.ovs.frags_from_pointer(link_frag.pointers[1], count)
			for frag in tmp_fragments:
				output.append(self.p1_ztsr(frag))
			# log the frags
			self.sized_str_entry.fragments.append(link_frag)
			self.sized_str_entry.fragments.extend(tmp_fragments)
		return output

	def get_int_list_at_offset(self, count, offset):
		"""Gets list of ints pointed to at offset from ss ptr"""
		if count:
			link_frag = self.ovs.frag_at_pointer(self.sized_str_entry.pointers[0], offset=offset)
			# log the frag
			self.sized_str_entry.fragments.append(link_frag)
			return list(struct.unpack(f"<{count}I", link_frag.pointers[1].read_from_pool(4 * count)))
		return []

	def get_str_at_offset(self, offset):
		"""Gets string pointed to at offset from ss ptr"""
		f = self.ovs.frag_at_pointer(self.sized_str_entry.pointers[0], offset=offset)
		if f:
			# log the frag
			self.sized_str_entry.fragments.append(f)
			return self.p1_ztsr(f)

	def write_str_list_at_rel_offset(self, ref_ptr, rel_offset, items_list, bytes_func=None):
		"""Writes a list of pointers and items, and reference it from a ptr at rel_offset from the ref_ptr"""
		if items_list:
			if not bytes_func:
				def bytes_func(s):
					return b"\x00" * 8
			# for each line, add the frag ptr space and create the frag ptr
			item_frags = self.create_fragments(self.sized_str_entry, len(items_list))
			for item, frag in zip(items_list, item_frags):
				self.write_to_pool(frag.pointers[0], 2, bytes_func(item))
			for item, frag in zip(items_list, item_frags):
				self.write_to_pool(frag.pointers[1], 2, as_bytes(item))
			# point the list frag to the end of the data now.
			new_frag1 = self.create_fragments(self.sized_str_entry, 1)[0]
			self.ptr_relative(new_frag1.pointers[0], ref_ptr, rel_offset)
			self.ptr_relative(new_frag1.pointers[1], item_frags[0].pointers[0])

	def write_int_list_at_rel_offset(self, ref_ptr, rel_offset, items_list):
		"""Writes a list of ints, and reference it from a ptr at rel_offset from the ref_ptr"""
		if items_list:
			new_frag1 = self.create_fragments(self.sized_str_entry, 1)[0]
			self.ptr_relative(new_frag1.pointers[0], ref_ptr, rel_offset)

			itembytes = b''
			for item in items_list:
				itembytes += struct.pack("<I", int(item))
			if len(items_list) < 4:
				padding = 4 * (4 - len(items_list))
				itembytes += struct.pack(f"<{padding}s", b'')
			self.write_to_pool(new_frag1.pointers[1], 2, itembytes)

	def write_str_at_rel_offset(self, ref_ptr, rel_offset, s):
		"""Writes a string, and reference it from a ptr at rel_offset from the ref_ptr"""
		if s:
			new_frag1 = self.create_fragments(self.sized_str_entry, 1)[0]
			self.ptr_relative(new_frag1.pointers[0], ref_ptr, rel_offset)
			self.write_to_pool(new_frag1.pointers[1], 2, as_bytes(s))

	def assign_ss_entry(self):
		self.sized_str_entry = self.ovl.get_sized_str_entry(self.file_entry.name)

	def assign_fixed_frags(self, count):
		self.assign_ss_entry()
		ss_ptr = self.sized_str_entry.pointers[0]
		self.sized_str_entry.fragments = self.ovs.frags_from_pointer(ss_ptr, count)

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
		# todo - remove pool index throughout all formats
		for pool_index, pool in enumerate(ovs_file.pools):
			# todo - reasonable add size condition
			if pool.type == pool_type_key and pool.new:
				return pool
		# nope, means we gotta create pool
		pool = MemPool(self.ovl.context)
		pool.data = ConvStream()
		# the real address isn't known until it is written, but declare it anyway
		pool.address = 0
		# assign_versions(pool.data, get_versions(self.ovl))
		pool.type = pool_type_key
		# we write to the pool IO directly, so do not reconstruct its data from the pointers' data
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

	def create_ss_entry(self, file_entry, ovs="STATIC"):
		ss_entry = SizedStringEntry(self.ovl.context)
		ss_entry.children = []
		ss_entry.fragments = []
		# ss_entry.pointers.append(HeaderPointer(self.ovl.context))
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
		# dependency.pointers.append(HeaderPointer(self.ovl.context))
		self.file_entry.dependencies.append(dependency)
		return dependency

	def create_fragments(self, ss, count):
		frags = [self.create_fragment() for i in range(count)]
		ss.fragments.extend(frags)
		return frags

	def create_fragment(self):
		new_frag = Fragment(self.ovl.context)
		# new_frag.pointers.append(HeaderPointer(self.ovl.context))
		# new_frag.pointers.append(HeaderPointer(self.ovl.context))
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


class MemStructLoader(BaseFile):

	target_class: None

	def extract(self, out_dir, show_temp_files, progress_callback):
		name = self.sized_str_entry.name
		out_path = out_dir(name)
		self.header.to_xml_file(out_path)
		return out_path,

	def collect(self):
		self.assign_ss_entry()
		ss_ptr = self.sized_str_entry.pointers[0]
		self.header = self.target_class.from_stream(ss_ptr.stream, self.ovl.context)
		self.header.read_ptrs(ss_ptr.pool, self.sized_str_entry)
		# print(self.header)

	def create(self):
		self.sized_str_entry = self.create_ss_entry(self.file_entry)
		ss_ptr = self.sized_str_entry.pointers[0]

		self.header = self.target_class.from_xml_file(self.file_entry.path, self.ovl.context)
		# print(self.header)
		self.header.write_ptrs(self, self.ovs, ss_ptr)
		# todo - may use wrong pools !
		# todo - may need padding here

	def load(self, file_path):
		self.header = self.target_class.from_xml_file(file_path, self.ovl.context)
		# print(self.header)
		# todo
