import contextlib
import io
import logging
import os
import struct
import tempfile
from copy import copy
from io import BytesIO
import shutil

from generated.formats.ovl import UNK_HASH, is_jwe2
from generated.formats.ovl.compounds.BufferEntry import BufferEntry
from generated.formats.ovl.compounds.MemPool import MemPool
from generated.formats.ovl.compounds.DataEntry import DataEntry
from modules.formats.shared import djb2
from ovl_util.shared import hex_dump

TAB = '  '


class BaseFile:
	extension = None
	aliases = ()
	# used to check output for any temporary files that should possibly be deleted
	temp_extensions = ()
	can_extract = True
	target_class: None

	def __init__(self, ovl, file_name, mime_version):
		self.ovl = ovl
		self.context = ovl.context
		self.name = file_name
		self.mime_version = mime_version
		# this needs to be figured out by the root_entry
		self.ovs = None
		self.header = None
		self.target_name = ""

		# defined in ovl
		self.dependencies = []
		self.streams = []
		self.extra_loaders = []

		# defined in ovs
		self.data_entries = {}
		self.children = []
		self.fragments = set()
		self.stack = {}
		self.root_ptr = (None, 0)

		self.same = False
		self.aux_data = {}

	def flush_to_aux(self):
		pass

	def close_aux_handles(self):
		"""Close existing aux readers / writers, then clear aux_data"""
		for aux_suffix, aux_handle in self.aux_data.items():
			aux_handle.close()
		self.aux_data.clear()

	def get_aux_handle(self, aux_suffix, aux_size, mode):
		"""init reader if it doesn't exist"""
		if aux_suffix not in self.aux_data:
			aux_path = self.get_aux_path(aux_suffix, aux_size)
			try:
				self.aux_data[aux_suffix] = open(aux_path, mode)
			except FileNotFoundError:
				logging.exception(f"Couldn't find {aux_path}")
				self.aux_data[aux_suffix] = io.BytesIO()
		return self.aux_data[aux_suffix]

	def open_aux_readers(self, aux_suffix: str, aux_size: int = 0):
		"""Store aux bytes in loader's aux_data dict"""
		self.get_aux_handle(aux_suffix, aux_size, "rb")

	def write_aux_data(self, aux_suffix: str, data):
		"""Write data to aux_data, return offset and size"""
		aux_writer = self.get_aux_handle(aux_suffix, len(data), "wb")
		offset = aux_writer.tell()
		aux_writer.write(data)
		return offset, len(data)

	def get_aux_data(self, aux_suffix: str, offset: int, size: int = -1):
		"""Get aux data from storage"""
		aux_reader = self.aux_data[aux_suffix]
		aux_reader.seek(offset)
		data = aux_reader.read(size)
		if size >= 0:
			assert len(data) == size
		return data

	def get_aux_path(self, aux_suffix, aux_size=0):
		"""Get path of aux file on disk"""
		return os.path.join(self.ovl.dir, self.get_aux_name(aux_suffix, aux_size))

	def get_aux_name(self, aux_suffix, aux_size=0):
		"""Get name of aux file from aux file of matching size"""
		logging.debug(f"Picking .aux file for type '{aux_suffix}' ({aux_size} bytes)")
		for file_name in os.listdir(self.ovl.dir):
			if file_name.endswith(".aux"):
				aux_path = os.path.join(self.ovl.dir, file_name)
				if os.path.getsize(aux_path) == aux_size:
					return file_name
		else:
			raise LookupError(f"Found no matching .aux file for {self.name}!")

	def get_aux_size(self, aux_suffix):
		"""Return aux file size from aux_data"""
		# aux_handle = self.aux_data[aux_suffix]
		# return aux_handle.tell()
		# this is independent of flushing the aux
		return os.path.getsize(self.get_aux_path(aux_suffix))

	@property
	def controlled_loaders(self):
		for stream in self.streams + self.children + self.extra_loaders:
			if stream:
				yield stream

	def check_controlled_conflicts(self):
		"""check if there is a name conflict in the controlled loaders"""
		possible_conflicts = [loader for loader in self.ovl.loaders.values() if loader.ext == self.ext]
		used_names = {stream.name for stream in self.controlled_loaders}
		for old_container in possible_conflicts:
			for child in old_container.controlled_loaders:
				if child.name in used_names and old_container.name != self.name:
					raise AttributeError(
						f"Injected file '{self.name}' conflicts with '{old_container.name}' from the OVL, "
						f"as it defines files with the same name, such as '{child.name}'.")

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
		# logging.info(f"Getting constants for {self.name}")
		self.pool_type = self.ovl.get_mime(self.ext, "pool")
		self.set_pool_type = self.ovl.get_mime(self.ext, "set_pool")
		self.mime_version = self.ovl.get_mime(self.ext, "version")

	@property
	def ovs_name(self):
		"""Returns the name of the main ovs archive that holds this loader's root entry"""
		if self.ovs:
			return self.ovs.arg.name

	@property
	def ovs_names(self):
		"""Returns the names of all ovs archives containing this loader's root entry and data"""
		out = []
		if self.ovs:
			out.append(self.ovs.arg.name)
		for data_ovs_name in self.data_entries.keys():
			out.append(data_ovs_name)
		return out

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
				logging.info(f"Deleted frag {l_pool.i} | {l_offset} -> {s_pool.i} | {s_offset}")

	def attach_frag_to_ptr(self, l_pool, l_offset, s_pool, s_offset):
		"""Creates a frag on a MemStruct Pointer; needs to have been written so that io_start is set"""
		# todo - doesn't add struct to list of children of an existing struct in stack
		l_pool.offset_2_link[l_offset] = (s_pool, s_offset)
		self.stack[(s_pool, s_offset)] = {}
		self.fragments.add(((l_pool, l_offset), (s_pool, s_offset)))

	def get_pool(self, pool_type_key):
		assert pool_type_key is not None
		# get one directly editable pool, if it exists
		for pool in self.ovs.pools:
			if pool.type == pool_type_key and pool.new:
				# while a condition on size would be nice to replicate stock, it would have to check after writing a whole struct
				# only checking here could break in the middle of an array, so disable for now
				# seems like a reasonable size condition - seen stock with 17608 bytes
				# if pool.get_size() < 16000:
				return pool
		# nope, have to create pool
		pool = MemPool(self.ovl.context)
		pool.i = None
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

	def delete_unused(self):
		pass

	def create_data_entry(self, buffers_bytes, ovs_name=None):
		data = DataEntry(self.ovl.context)
		# needs to be created in the ovs that this loader has been assigned to use
		# needs additional research to be able to create jwe2 dino manis with stray data_entry
		if not ovs_name:
			ovs_name = self.ovs_name
		self.data_entries[ovs_name] = data

		valid_datas = [b for b in buffers_bytes if b is not None]
		data.buffer_count = len(valid_datas)
		data.buffers = []
		for i, buffer_bytes in enumerate(buffers_bytes):
			if buffer_bytes is not None:
				buffer = BufferEntry(self.ovl.context)
				buffer.index = i
				data.buffers.append(buffer)
				self.ovs.transfer_identity(buffer, self)
		self.ovs.transfer_identity(data, self)
		data.update_data(valid_datas)
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
			self.collect()
		except:
			logging.exception(f"Renaming contents failed for {self.name}")

	# todo - rename in buffers?

	def rename_stack(self, name_tuples):
		"""Brute force implementation of byte-based renaming directly on pools"""
		logging.info(f"Renaming inside {self.name} (brute force)")
		byte_name_tups = []
		if not self.fragments:
			return
		try:
			for old, new in name_tuples:
				byte_name_tups.append((old.encode(), new.encode()))
			# make a copy, we might have to edit the stack dict
			for (p_pool, p_offset), children in list(self.stack.items()):
				for rel_offset, entry in children.items():
					# frags only
					if isinstance(entry, tuple):
						l_offset = p_offset + rel_offset
						# points to a child struct
						s_pool, s_offset = entry
						# check if it contains any of the target string
						if s_pool.contains_at(s_offset, byte_name_tups):
							frag = ((p_pool, l_offset), (s_pool, s_offset))
							if frag in self.fragments:
								self.fragments.remove(frag)
							self.remove_ptr_from_pool(s_pool, s_offset)
							# get the new string
							new_bytes = s_pool.get_data_at(s_offset)
							for old, new in byte_name_tups:
								new_bytes = new_bytes.replace(old, new)
							# actually write the ptr
							target_pool = self.get_pool(s_pool.type)
							# seek to end, set data_offset, write
							stream, target_offset = target_pool.align_write(new_bytes)
							stream.write(new_bytes)
							# only store these if the pointer had valid data
							target_pool.offsets.add(target_offset)
							# store size in size_map
							target_pool.size_map[target_offset] = target_pool.data.tell() - target_offset
							# assign children to new offset
							self.attach_frag_to_ptr(p_pool, l_offset, target_pool, target_offset)
		except:
			logging.exception(f"Renaming frags failed for {self.name}")

	def remove_ptr_from_pool(self, s_pool, s_offset):
		if s_pool is not None:
			# different files may have a struct at this offset
			if s_offset in s_pool.offsets:
				s_pool.offsets.remove(s_offset)

	def increment_buffers(self, buffer_i):
		"""Linearly increments buffer indices for games that need it"""
		# create increasing buffer indices for PZ (still needed 22-05-10), JWE
		if not is_jwe2(self.ovl):
			for buff in self.data_entry.buffers:
				buff.index = buffer_i
				buffer_i += 1
		return buffer_i

	@staticmethod
	def _rename(name_tuples, s):
		for old, new in name_tuples:
			s = s.replace(old, new)
		return s

	def rename_check(self, name_tuples):
		"""Returns str if name changed, none if it stayed the same"""
		new_name = self._rename(name_tuples, self.name)
		if new_name != self.name:
			return new_name

	def rename(self, name_tuples):
		"""Rename all entries controlled by this loader"""
		entries = []
		for data_entry in self.data_entries.values():
			entries.extend((data_entry, *data_entry.buffers))
		for entry in entries:
			if UNK_HASH in entry.name:
				logging.warning(f"Skipping {entry.file_hash} because its hash could not be resolved to a name")
				return
			entry.name = self._rename(name_tuples, entry.name)
		self.target_name = self._rename(name_tuples, self.target_name)
		self.name = self._rename(name_tuples, self.name)
		self.dependencies = [(self._rename(name_tuples, dep), ptr) for dep, ptr in self.dependencies]
		# dependencies in stack & pools' link tables
		for (p_pool, p_offset), children in self.stack.items():
			for rel_offset, entry in children.items():
				if isinstance(entry, str):
					children[rel_offset] = self._rename(name_tuples, entry)
					p_pool.offset_2_link[p_offset + rel_offset] = self._rename(name_tuples, entry)
		# for direct rename: remove extensions to be able to rename child loaders in the same run
		for_children = set(name_tuples)
		for old, new in name_tuples:
			if old.endswith(self.ext):
				for_children.add((old.replace(self.ext, ""), new.replace(self.ext, "")))
		# force an update to get the memstruct up to date
		if self.dependencies:
			self.collect()

	@contextlib.contextmanager
	def get_tmp_dir_func(self):
		temp_dir = tempfile.mkdtemp("-cobra")

		def out_dir_func(n):
			"""Helper function to generate temporary output file name"""
			return os.path.normpath(os.path.join(temp_dir, n))

		yield out_dir_func
		# delete temp dir again
		shutil.rmtree(temp_dir)

	@contextlib.contextmanager
	def get_tmp_dir(self):
		temp_dir = tempfile.mkdtemp("-cobra")

		yield temp_dir
		# delete temp dir again
		shutil.rmtree(temp_dir)

	def register_entries(self):
		for ovs_name, data_entry in self.data_entries.items():
			ovs = self.ovl.create_archive(ovs_name)
			ovs.data_entries.append(data_entry)
			ovs.buffer_entries.extend(data_entry.buffers)

	def remove(self):
		logging.info(f"Removing {self.name}")
		self.clear_stack()
		# remove the loader from ovl so it is not saved
		self.ovl.loaders.pop(self.name)
		# remove streamed and child files
		for loader in self.controlled_loaders:
			loader.remove()

	def clear_stack(self):
		"""Safely clear the stack by removing pointers from pools so that pools' names are still reliably detected"""
		for pool, offset in self.stack.keys():
			self.remove_ptr_from_pool(pool, offset)
		self.stack.clear()

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
		for l_offset, rel_offset, entry in p_pool.get_ptrs_in_struct(p_offset, p_size):
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

	def get_hex_dump(self, pool, offset, size, indent=1):
		dump_hex = False
		# TODO: Test if dump_stack or dump_ptr_stack was the None crash here
		if offset is not None:
			dump_hex = True
		# TODO: Configurable max size?
		if size > int(16 * 1024 * 1024):
			dump_hex = False
		if dump_hex:
			pool_data = pool.debug_dump[offset: offset + size]
			return f"\n{hex_dump(pool_data, size > 1024, True, indent=indent, line_width=min(size, 16))}"
		return ""

	def dump_ptr_stack(self, f, parent_struct_ptr, rec_check, indent=1):
		"""Recursively writes parent_struct_ptr.children to f"""
		children = self.stack.get(parent_struct_ptr, {})

		# sort by offset
		for rel_offset, target in sorted(children.items()):
			# get the relative offset of this pointer to its struct
			if isinstance(target, tuple):
				# points to a child struct
				s_pool, s_offset = target
				data_size = s_pool.size_map.get(s_offset, -1)

				hex_string = self.get_hex_dump(s_pool, s_offset, data_size, indent=indent + 1)

				f.write("\n\n")
				if target in rec_check:
					# pointer refers to a known entry - stop here to avoid recursion
					f.write(f"{indent * TAB}PTR @ {rel_offset: <4} -> REF {s_pool.i} | {s_offset} ({data_size: 4})")
					f.write(hex_string)
				else:
					rec_check.add(target)
					f.write(f"{indent * TAB}PTR @ {rel_offset: <4} -> SUB {s_pool.i} | {s_offset} ({data_size: 4})")
					f.write(hex_string)
					self.dump_ptr_stack(f, target, rec_check, indent=indent + 1)
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
				# ui files eg. uigameface/img/workshop/workshopmap_artworkmask.png.tex
				if "/" in name:
					# create subfolder for dump
					os.makedirs(os.path.dirname(out_path), exist_ok=True)
				paths.append(out_path)
				with open(out_path, 'wb') as outfile:
					outfile.write(b)
		return paths

	@property
	def show_temp_files(self):
		return self.ovl.do_debug

	def handle_paths(self, paths):
		"""Deletes temporary files if asked and returns all valid paths."""
		if self.temp_extensions and not self.show_temp_files:
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
		self.check(len(self.extra_loaders), len(other.extra_loaders), "Amount of extra loaders")
		for stream, other_stream in zip(self.streams, other.streams):
			self.check(stream, other_stream, "Stream entry")
		self.check(len(self.aux_data), len(other.aux_data), "Amount of aux entries")
		for aux_suffix in self.aux_data:
			own_aux = self.get_aux_data(aux_suffix, 0, size=-1)
			other_aux = other.get_aux_data(aux_suffix, 0, size=-1)
			self.check(own_aux, other_aux, "Aux entry")
		return self.same

	def compare_pointer(self, other, t_p, t_o, o_p, o_o):
		# logging.debug(f"compare_pointer {t_o} vs {o_o}")
		if not t_p and not o_p:
			return
		if not t_p or not o_p:
			self.same = False
			return
		this_struct = t_p.get_data_at(t_o)
		other_struct = o_p.get_data_at(o_o)
		if not (this_struct and other_struct):
			logging.warning(f"No valid offset for this {t_o} vs other {o_o}")
			self.same = False
			return
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
				logging.warning(
					f"Pointer at relative offset {rel_offset} missing in this: {t_p.i} | {t_o} vs {o_p.i} | {o_o}")
				self.same = False
				continue
			if rel_offset in other_children:
				other_target_ptr = other_children[rel_offset]
			else:
				logging.warning(
					f"Pointer at relative offset {rel_offset} missing in other: {t_p.i} | {t_o} vs {o_p.i} | {o_o}")
				self.same = False
				continue
			# dependency?
			if isinstance(this_target_ptr, str):
				if this_target_ptr != other_target_ptr:
					logging.warning(
						f"Dependency at {rel_offset} does not match {this_target_ptr} vs {other_target_ptr}")
					self.same = False
			else:
				# traverse down the tree of pointers
				self.compare_pointer(other, *this_target_ptr, *other_target_ptr)

	def write_memory_data(self):
		pool = self.get_pool(self.pool_type)
		stream, offset = pool.align_write(self)
		# logging.debug(f"Writing to {pool} at {offset}")
		self.root_ptr = (pool, offset)
		self.stack[self.root_ptr] = {}
		self.target_class.to_stream(self.header, stream, self.context)
		self.header.write_ptrs(self, pool)


class MemStructLoader(BaseFile):

	def __init__(self, ovl, file_name, mime_version):
		super().__init__(ovl, file_name, mime_version)
		self.context = copy(self.ovl.context)
		self.context.mime_version = self.mime_version

	def accept_string(self, in_str):
		"""Return True if string should receive replacement"""
		return True

	def rename_stack(self, name_tuples):
		"""Collect all zstring pointers (incl. obfuscated) and rename them"""
		if not self.header:
			# fallback for files that haven't been collected
			super().rename_stack(name_tuples)
			return
		logging.info(f"Renaming structs for {self.name}")
		try:
			for zstr_ptr in self.header.get_all_str_pointers(self.header):
				zstr = zstr_ptr.data
				if not zstr:
					continue
				# check if this string should be replaced
				if not self.accept_string(zstr):
					continue
				# replace the strings
				for old, new in name_tuples:
					zstr = zstr.replace(old, new)
				# if it's still the same, don't write new string
				if zstr == zstr_ptr.data:
					continue
				# delete existing frag, write_ptr will create the new one
				frag = ((zstr_ptr.src_pool, zstr_ptr.io_start), (zstr_ptr.target_pool, zstr_ptr.target_offset))
				if frag in self.fragments:
					self.fragments.remove(frag)
				self.remove_ptr_from_pool(zstr_ptr.target_pool, zstr_ptr.target_offset)
				# set and write the ptr to a suitable pool
				zstr_ptr.data = zstr
				zstr_ptr.write_ptr(self, zstr_ptr.src_pool)
		except:
			logging.exception(f"Renaming struct failed for {self.name}")

	def extract(self, out_dir):
		if self.header:
			out_path = out_dir(self.name)
			with self.header.to_xml_file(self.header, out_path, debug=self.ovl.do_debug) as xml_root:
				if self.ovl.do_debug:
					pool, offset = self.root_ptr
					xml_root.set("_address", f"{pool.i} | {offset}")
					xml_root.set("_size", f"{pool.size_map.get(offset, -1)}")
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
		self.header.read_ptrs(pool, debug=self.ovl.do_debug)

	def create(self, file_path):
		self.header = self.target_class.from_xml_file(file_path, self.context)
		self.write_memory_data()


class MimeContext:
	def __init__(self, v):
		self.version = v

	def __repr__(self):
		return f"MimeContext v={self.version}"


class MimeVersionedLoader(MemStructLoader):

	def __init__(self, ovl, file_name, mime_version):
		super().__init__(ovl, file_name, mime_version)
		# self.get_constants_entry()
		self.context = MimeContext(self.mime_version)
	# logging.debug(self.context)
