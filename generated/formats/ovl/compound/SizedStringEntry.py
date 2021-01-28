import typing
from generated.array import Array
from generated.formats.ovl.compound.HeaderPointer import HeaderPointer


class SizedStringEntry:

	"""
	points to a sized string in a header's data block
	"""

	def __init__(self, arg=None, template=None):
		self.name = ''
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# hash of the file that should be read
		self.file_hash = 0

		# matches matching HeaderEntry's Ext Hash
		self.ext_hash = 0

		# points into header datas section
		self.pointers = Array()

	def read(self, stream):

		self.io_start = stream.tell()
		self.file_hash = stream.read_uint()
		if (((stream.user_version == 24724) or (stream.user_version == 25108)) and (stream.version == 19)) or (((stream.user_version == 8340) or (stream.user_version == 8724)) and (stream.version == 19)):
			self.ext_hash = stream.read_uint()
		self.pointers.read(stream, HeaderPointer, 1, None)

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_uint(self.file_hash)
		if (((stream.user_version == 24724) or (stream.user_version == 25108)) and (stream.version == 19)) or (((stream.user_version == 8340) or (stream.user_version == 8724)) and (stream.version == 19)):
			stream.write_uint(self.ext_hash)
		self.pointers.write(stream, HeaderPointer, 1, None)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'SizedStringEntry [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* file_hash = {self.file_hash.__repr__()}'
		s += f'\n	* ext_hash = {self.ext_hash.__repr__()}'
		s += f'\n	* pointers = {self.pointers.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
