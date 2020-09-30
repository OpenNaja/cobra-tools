# START_GLOBALS
import io

MAX_UINT32 = 4294967295


# END_GLOBALS


class HeaderPointer:

# START_CLASS

	def read_data(self, archive):
		"""Load data from archive header data readers into pointer for modification and io"""

		self.padding = b""
		if self.header_index == MAX_UINT32:
			self.data = None
		else:
			header_reader = archive.header_entries[self.header_index].data
			header_reader.seek(self.data_offset)
			self.data = header_reader.read(self.data_size)


	def write_data(self, archive, update_copies=False):
		"""Write data to header data, update offset, also for copies if told"""

		if self.header_index == MAX_UINT32:
			pass
		else:
			# get header data to write into
			writer = archive.header_entries[self.header_index].data
			# update data offset
			self.data_offset = writer.tell()
			if update_copies:
				for other_pointer in self.copies:
					other_pointer.data_offset = writer.tell()
			# write data to io, adjusting the cursor for that header
			writer.write(self.data + self.padding)


	def strip_zstring_padding(self):
		"""Move surplus padding into the padding attribute"""
		# the actual zstring content + end byte
		data = self.data.split(b"\x00")[0] + b"\x00"
		# do the split itself
		self.split_data_padding(len(data))


	def split_data_padding(self, cut):
		"""Move a fixed surplus padding into the padding attribute"""
		_d = self.data + self.padding
		self.padding = _d[cut:]
		self.data = _d[:cut]


	def link_to_header(self, archive):
		"""Store this pointer in suitable header entry"""

		if self.header_index == MAX_UINT32:
			pass
		else:
			# get header entry
			entry = archive.header_entries[self.header_index]
			if self.data_offset not in entry.pointer_map:
				entry.pointer_map[self.data_offset] = []
			entry.pointer_map[self.data_offset].append(self)


	def update_data(self, data, update_copies=False, pad_to=None, include_old_pad=False):
		"""Update data and size of this pointer"""
		self.data = data
		# only change padding if a new alignment is given
		if pad_to:
			len_d = len(data)
			# consider the old padding for alignment?
			if include_old_pad:
				len_d += len(self.padding)
			moduloed = len_d % pad_to
			if moduloed:
				# create the new blank padding
				new_pad = b"\x00" * (pad_to - moduloed)
			else:
				new_pad = b""
			# append new to the old padding
			if include_old_pad:
				self.padding = self.padding + new_pad
			# overwrite the old padding
			else:
				self.padding = new_pad
		self.data_size = len(self.data + self.padding)
		# update other pointers if asked to by the injector
		if update_copies:
			for other_pointer in self.copies:
				if other_pointer is not self:
					other_pointer.update_data(data, pad_to=pad_to, include_old_pad=include_old_pad)


	def get_reader(self):
		"""Returns a reader of its data"""
		return io.BytesIO(self.data)


	def read_as(self, pyffi_cls, data, num=1):
		"""Return self.data as pyffi cls
		Data must be an object that has version & user_version attributes"""
		reader = self.get_reader()
		insts = []
		for i in range(num):
			inst = pyffi_cls()
			inst.read(reader, data=data)
			insts.append(inst)
		return insts