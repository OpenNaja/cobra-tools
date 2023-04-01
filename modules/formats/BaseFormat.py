import contextlib
import logging
import os
import struct
import tempfile
from io import BytesIO
import shutil

from generated.formats.ovl import UNK_HASH
from generated.formats.ovl.compounds.DependencyEntry import DependencyEntry
from generated.formats.ovl.compounds.Fragment import Fragment
from generated.formats.ovl.compounds.BufferEntry import BufferEntry
from generated.formats.ovl.compounds.MemPool import MemPool
from generated.formats.ovl.compounds.RootEntry import RootEntry
from generated.formats.ovl.compounds.DataEntry import DataEntry
from modules.formats.shared import djb2

TAB = '  '


class BaseFile:
	extension = None
	aliases = ()
	# used to check output for any temporary files that should possibly be deleted
	temp_extensions = ()
	can_extract = True
	target_class: None

	def __init__(self, ovl, file_name):
		self.ovl = ovl
		self.context = ovl.context
		self.name = file_name
		# this needs to be figured out by the root_entry
		self.ovs = None
		self.header = None
		self.target_name = ""

		# defined in ovl
		self.dependencies = {}
		self.aux_entries = []
		self.streams = []

		# defined in ovs
		self.data_entries = {}
		self.children = []
		self.fragments = set()
		self.stack = {}
		self.root_ptr = (None, 0)

		self.same = False

	@property
	def name(self):
		return self._name

	@name.setter
	def name(self, n):
		self._name = n.lower()
		self.basename, self.ext = os.path.splitext(self._name)
		self.file_hash = djb2(self.basename)
		self.ext_hash = djb2(self.ext[1:])

	@property
	def data_entry(self):
		return self.data_entries.get(self.ovs_name, None)

	def get_constants_entry(self):
		# logging.info(f"Getting contants for {self.name}")
		self.pool_type = self.ovl.get_mime(self.ext, "pool")
		self.set_pool_type = self.ovl.get_mime(self.ext, "set_pool")
		self.mime_version = self.ovl.get_mime(self.ext, "version")

	@property
	def ovs_name(self):
		if self.ovs:
			return self.ovs.arg.name

	def set_ovs(self, ovs_name):
		"""Assigns or creates suitable ovs"""
		self.ovs = self.ovl.create_archive(ovs_name)

	@property
	def abs_mem_offset(self):
		"""Returns the memory offset of this loader's root_entry"""
		# this is inverted compared to get_pool_offset
		pool, data_offset = self.root_ptr
		offset = pool.offset + data_offset
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

	def create(self, file_path):
		raise NotImplementedError

	def collect(self):
		pass

	def pack_header(self, fmt_name):
		ovl = self.ovl
		return struct.pack(
			"<4s4BI", fmt_name, ovl.version_flag, ovl.version, ovl.bitswap, ovl.seventh_byte, int(ovl.user_version))

	def delete_frag(self, l_pool, l_offset, s_pool, s_offset):
		if l_offset in l_pool.offset_2_link:
			l_pool.offset_2_link.pop(l_offset)
		if (s_pool, s_offset) in self.stack:
			self.stack.pop((s_pool, s_offset))
		for f in tuple(self.fragments):
			if f[0] == (l_pool, l_offset):
				self.fragments.remove(f)
				logging.info(f"Deleted frag {f}")

	def attach_frag_to_ptr(self, l_pool, l_offset, s_pool, s_offset):
		"""Creates a frag on a MemStruct Pointer; needs to have been written so that io_start is set"""
		# todo - doesn't add struct to list of children of an extisting struct in stack
		l_pool.offset_2_link[l_offset] = (s_pool, s_offset)
		self.stack[(s_pool, s_offset)] = {}
		self.fragments.add(((l_pool, l_offset), (s_pool, s_offset)))

	def get_pool(self, pool_type_key):
		assert pool_type_key is not None
		# get one directly editable pool, if it exists
		for pool in self.ovs.pools:
			if pool.type == pool_type_key and pool.new:
				# seems like a reasonable size condition - seen stock with 17608 bytes
				if pool.get_size() < 16000:
					return pool
		# nope, means we gotta create pool
		pool = MemPool(self.ovl.context)
		pool.data = BytesIO()
		pool.type = pool_type_key
		pool.clear_data()
		pool.new = True
		self.ovs.pools.append(pool)
		return pool

	def write_root_bytes(self, data):
		"""Finds or creates a suitable pool in the right ovs and writes data"""
		pool = self.get_pool(self.pool_type)
		stream, offset = pool.align_write(data)
		stream.write(data)
		self.root_ptr = (pool, offset)
		pool.offsets.add(offset)
		pool.size_map[offset] = len(data)
		self.stack[(pool, offset)] = {}

	def get_content(self, filepath):
		with open(filepath, 'rb') as f:
			content = f.read()
		return content

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
			self.ovs.transfer_identity(buffer, self)
		self.ovs.transfer_identity(data, self)
		data.update_data(buffers_bytes)
		return data

	def update(self):
		"""Don't do anything by default, overwrite if needed"""
		pass

	def validate(self):
		"""Don't do anything by default, overwrite if needed"""
		pass

	def rename_content(self, name_tuples):
		"""This is the fallback that is used when the loader class itself does not implement custom methods"""
		try:
			self.rename_stack(name_tuples)
			# not all loaders have a header
			if self.header is not None:
				pool, offset = self.root_ptr
				stream = pool.stream_at(offset)
				self.header = self.target_class.from_stream(stream, self.context)
				self.header.read_ptrs(pool)
		except:
			logging.exception(f"Renaming contents failed for {self.name}")
		# todo - rename in buffers

	def rename_stack(self, name_tuples):
		# todo - rewrite to collect all zstring pointers (incl. obfuscated)
		logging.info(f"Renaming inside {self.name}")
		byte_name_tups = []
		try:
			# brute force fallback with same length of strings
			for old, new in name_tuples:
				assert len(old) == len(new)
				byte_name_tups.append((old.encode(), new.encode()))
			for (p_pool, p_offset) in self.stack:
				p_pool.replace_bytes_at(p_offset, byte_name_tups)
		except:
			logging.exception(f"Renaming frags failed for {self.name}")

	def rename(self, name_tuples):
		"""Rename all entries controlled by this loader"""
		def _rename(s):
			for old, new in name_tuples:
				s = s.replace(old, new)
			return s
		entries = []
		for data_entry in self.data_entries.values():
			entries.extend((data_entry, *data_entry.buffers))
		for entry in entries:
			if UNK_HASH in entry.name:
				logging.warning(f"Skipping {entry.file_hash} because its hash could not be resolved to a name")
				return
			entry.name = _rename(entry.name)

		self.target_name = _rename(self.target_name)
		self.name = _rename(self.name)
		self.aux_entries = [_rename(aux) for aux in self.aux_entries]
		self.dependencies = {_rename(dep): ptr for dep, ptr in self.dependencies.items()}

	@contextlib.contextmanager
	def get_tmp_dir(self):
		temp_dir = tempfile.mkdtemp("-cobra")

		def out_dir_func(n):
			"""Helper function to generate temporary output file name"""
			return os.path.normpath(os.path.join(temp_dir, n))

		yield out_dir_func
		# delete temp dir again
		shutil.rmtree(temp_dir)

	def register_entries(self):
		for ovs_name, data_entry in self.data_entries.items():
			ovs = self.ovl.create_archive(ovs_name)
			ovs.data_entries.append(data_entry)
			ovs.buffer_entries.extend(data_entry.buffers)

	def remove(self):
		logging.info(f"Removing {self.name}")
		for pool, offset in self.stack.keys():
			if pool is not None:
				pool.offsets.remove(offset)
		# remove the loader from ovl so it is not saved
		self.ovl.loaders.pop(self.name)
		# remove streamed and child files
		for loader in self.streams + self.children:
			loader.remove()

	def track_ptrs(self):
		# logging.debug(f"Tracking {self.name}")
		self.stack = {}
		self.fragments = set()
		pool, offset = self.root_ptr
		if pool:
			self.check_for_ptrs(pool, offset)

	def check_for_ptrs(self, p_pool, p_offset):
		"""Recursively assigns pointers to an entry"""
		# tracking children for each struct adds no detectable overhead for animal ovls
		# slight slowdown in JWE2 Content0 main.ovl with vectorized search for linked child pointers
		children = {}
		self.stack[(p_pool, p_offset)] = children
		p_size = p_pool.size_map[p_offset]
		k = p_pool.link_offsets
		# find all link offsets that are within the parent struct using a boolean mask
		for l_offset in k[(p_offset <= k) * (k < p_offset+p_size)]:
			entry = p_pool.offset_2_link[l_offset]
			rel_offset = l_offset - p_offset
			# store frag and deps
			children[rel_offset] = entry
			if isinstance(entry, tuple):
				s_pool, s_offset = entry
				frag = ((p_pool, l_offset), (s_pool, s_offset))
				# points to a child struct
				if frag not in self.fragments:
					self.fragments.add(frag)
					# don't track empty pointers to the end of a pool
					if s_offset is not None:
						self.check_for_ptrs(s_pool, s_offset)

	def dump_ptr_stack(self, f, parent_struct_ptr, rec_check, pools_lut, indent=1):
		"""Recursively writes parent_struct_ptr.children to f"""
		children = self.stack.get(parent_struct_ptr, {})
		# sort by offset
		for rel_offset, target in sorted(children.items()):
			# get the relative offset of this pointer to its struct
			if isinstance(target, tuple):
				# points to a child struct
				s_pool, s_offset = target
				s_pool_i = pools_lut[s_pool]
				data_size = s_pool.size_map.get(s_offset, -1)
				if target in rec_check:
					# pointer refers to a known entry - stop here to avoid recursion
					f.write(f"\n{indent * TAB}PTR @ {rel_offset: <4} -> REF {s_pool_i} | {s_offset} ({data_size: 4})")
				else:
					rec_check.add(target)
					f.write(f"\n{indent * TAB}PTR @ {rel_offset: <4} -> SUB {s_pool_i} | {s_offset} ({data_size: 4})")
					self.dump_ptr_stack(f, target, rec_check, pools_lut, indent=indent + 1)
			# dependency
			else:
				f.write(f"\n{indent * TAB}DEP @ {rel_offset: <4} -> {target}")

	def dump_buffer_infos(self, f):
		debug_str = f"\n\nFILE {self.name}"
		f.write(debug_str)

		for ovs_name, data_entry in self.data_entries.items():
			f.write(f"\nData in {ovs_name} with {len(data_entry.buffers)} buffers")
			for buffer in data_entry.buffers:
				f.write(f"\nBuffer {buffer.index}, size {buffer.size}")
		# for loader in self.streams:
		# 	f.write(f"\nSTREAM {loader.name}")
		# 	loader.dump_buffer_infos(f)

	def dump_buffers(self, out_dir):
		paths = []
		if self.data_entry:
			for i, b in enumerate(self.data_entry.buffer_datas):
				name = f"{self.name}_{i}.dmp"
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

	def check(self, a, b, s):
		if a != b:
			logging.warning(f"{s} does not match - this: {a} vs other: {b}")
			self.same = False

	def __eq__(self, other):
		logging.info(f"Comparing {self.name}")
		self.same = True
		self.check(self.mime_version, other.mime_version, "Mime version")
		self.check(len(self.data_entries), len(other.data_entries), "Amount of data entries")
		# data
		for archive_name, data_entry in self.data_entries.items():
			assert archive_name in other.data_entries
			other_data = other.data_entries[archive_name]
			self.check(data_entry, other_data, "Data entry")
		self.check(len(self.fragments), len(other.fragments), "Amount of fragments")
		self.check(len(self.children), len(other.children), "Amount of children")
		# recursive check of pointers
		self.compare_pointer(other, *self.root_ptr, *other.root_ptr)
		self.check(self.ovs_name, other.ovs_name, "OVS name")
		self.check(len(self.streams), len(other.streams), "Amount of streams")
		for stream, other_stream in zip(self.streams, other.streams):
			self.check(stream, other_stream, "Stream entry")
		return self.same

	def compare_pointer(self, other, t_p, t_o, o_p, o_o):
		# logging.debug(f"compare_pointer {t_o} vs {o_o}")
		this_struct = t_p.get_data_at(t_o)
		other_struct = o_p.get_data_at(o_o)
		if this_struct != other_struct:
			logging.warning(f"Struct does not match - this {len(this_struct)} vs other {len(other_struct)}")
			min_len = min((len(this_struct), len(other_struct)))
			this_struct = this_struct[:min_len]
			other_struct = other_struct[:min_len]
			if this_struct == other_struct:
				logging.info(f"...but it's likely just padding")
			else:
				self.same = False
		this_children = self.stack.get((t_p, t_o), {})
		other_children = other.stack.get((o_p, o_o), {})
		all_offsets = set(this_children.keys())
		all_offsets.update(other_children.keys())
		# sort by offset
		for rel_offset in sorted(all_offsets):
			# logging.debug(f"rel_offset {rel_offset}")
			if rel_offset in this_children:
				this_target_ptr = this_children[rel_offset]
			else:
				logging.warning(f"Pointer at relative offset {rel_offset} missing in this: {t_p.i} | {t_o} vs {o_p.i} | {o_o}")
				self.same = False
				continue
			if rel_offset in other_children:
				other_target_ptr = other_children[rel_offset]
			else:
				logging.warning(f"Pointer at relative offset {rel_offset} missing in other: {t_p.i} | {t_o} vs {o_p.i} | {o_o}")
				self.same = False
				continue
			# dependency?
			if isinstance(this_target_ptr, str):
				if this_target_ptr != other_target_ptr:
					logging.warning(f"Dependency at {rel_offset} does not match {this_target_ptr} vs {other_target_ptr}")
					self.same = False
			else:
				# traverse down the tree of pointers
				self.compare_pointer(other, *this_target_ptr, *other_target_ptr)

	def log_versions(self):
		logging.info(f"{self.ext} {self.mime_version}")
		for loader in self.children:
			logging.info(f"{loader.ext} {loader.mime_version}")
		for loader in self.streams:
			logging.info(f"{loader.ext} {loader.mime_version}")

	def write_memory_data(self):
		pool = self.get_pool(self.pool_type)
		stream, offset = pool.align_write(self)
		self.root_ptr = (pool, offset)
		self.target_class.to_stream(self.header, stream, self.context)
		self.header.write_ptrs(self, pool)


class MemStructLoader(BaseFile):

	def __init__(self, ovl, file_name):
		super().__init__(ovl, file_name)
		self.context = self.ovl.context

	def extract(self, out_dir):
		if self.header:
			out_path = out_dir(self.name)
			self.header.to_xml_file(self.header, out_path, debug=self.ovl.do_debug)
			return out_path,
		else:
			logging.warning(f"File '{self.name}' has no header - has the OVL finished loading?")
			return ()

	def collect(self):
		super().collect()
		pool, offset = self.root_ptr
		stream = pool.stream_at(offset)
		self.header = self.target_class.from_stream(stream, self.context)
		# print(self.header)
		self.header.read_ptrs(pool)

	def create(self, file_path):
		self.header = self.target_class.from_xml_file(file_path, self.context)
		self.write_memory_data()

# class MimeContext:
# 	def __init__(self, v):
# 		self.version = v
#
#
# class MimeVersionedLoader(MemStructLoader):
#
# 	def __init__(self, ovl, file_name):
# 		super().__init__(ovl, file_name)
# 		self.context = MimeContext(self.mime_version)
