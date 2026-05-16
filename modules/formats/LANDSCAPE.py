import io
import os
import struct
import logging

from generated.formats.landscape.structs.LandscapeRoot import LandscapeRoot
from generated.formats.landscape.structs.Buffer0 import Buffer0


from generated.formats.base.structs.PadAlign import get_padding
from modules.formats.BaseFormat import BaseFile, MemStructLoader, MimeVersionedLoader
from modules.helpers import as_bytes


class LandscapeStreamLoader(BaseFile):
	extension = ".landscapestream"
	can_extract = False

	# def create(self, file_path):
	# 	self.header = self.target_class(self.context)
	# 	# JWE2, PC2
	# 	if self.context.version >= 52:
	# 		self.header.lod_index = int(self.basename[-1])
	# 	self.write_memory_data()
	#
	# def create_data(self, buffer_data):
	# 	self.create_data_entry((buffer_data,))
	# 	for buffer in self.data_entry.buffers:
	# 		buffer.index = 2
	# 	self.data_entry.size_1 = 0
	# 	self.data_entry.size_2 = len(buffer_data)


class LandscapeLoader(MemStructLoader):
	extension = ".landscape"
	target_class = LandscapeRoot

	def link_streams(self):
		"""Collect other loaders"""
		# if the landscape name ends in a trailing underscore, remove it
		bare_name = self.basename.rstrip("_")
		self._link_streams(f"{bare_name}{lod_i}.landscapestream" for lod_i in range(4))

	def collect(self):
		pool, offset = self.root_ptr
		stream = pool.stream_at(offset)
		self.header = LandscapeRoot.from_stream(stream, self.context)
		try:
			self.header.read_ptrs(pool, debug=self.ovl.do_debug)
			if self.header.buffer_pointers.data:
				for i, buffer_presence in enumerate(self.header.buffer_pointers.data):
					d = buffer_presence.dependency_name
					if d.pool_index != -1 and not d.data:
						logging.warning(f"Streamed mesh buffer {i} for {self.name} has no dependency to a .landscapestream file")
		except:
			logging.exception(f"MS2 collecting failed")
		print(self.header)
		buffer_0_stream = io.BytesIO(self.data_entry.buffer_datas[0])
		names_buffer = Buffer0.from_stream(buffer_0_stream, self.context, self.header)
		print(names_buffer)

	def extract(self, out_dir):
		all_buffer_bytes = self.data_entry.buffer_datas
		out_path = out_dir(self.name)
		context = self.header.context
		with open(out_path, 'wb') as stream:
			self.header.to_stream(self.header, stream, context)
			if self.header.buffer_pointers.data is not None:
				self.header.buffer_pointers.data.to_stream(self.header.buffer_pointers.data, stream, context)
			for loader in self.streams:
				stream.write(as_bytes(loader.basename))
			for b in all_buffer_bytes:
				stream.write(b)
			for loader in self.streams:
				# logging.debug(f"Writing {loader.name} at {stream.tell()}")
				logging.debug(f"Stream {loader.name} is in {loader.ovs.arg.name}")
				stream.write(loader.data_entry.buffer_datas[0])
				
		return [out_path, ]

