import typing
from generated.formats.ovl.compound.HeaderPointer import HeaderPointer


class SizedStringEntry:

	"""
	points to a sized string in a header's data block
	"""

	# hash of the file that should be read
	file_hash: int

	# matches matching HeaderEntry's Ext Hash
	ext_hash: int

	# points into header datas section
	pointers: typing.List[HeaderPointer]

	def __init__(self, arg=None, template=None):
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.file_hash = 0
		self.ext_hash = 0
		self.pointers = []

	def read(self, stream):

		self.io_start = stream.tell()
		self.file_hash = stream.read_uint()
		if ((stream.user_version == 24724) and (stream.version == 19)) or ((stream.user_version == 8340) and (stream.version == 19)):
			self.ext_hash = stream.read_uint()
		self.pointers = [stream.read_type(HeaderPointer) for _ in range(1)]

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_uint(self.file_hash)
		if ((stream.user_version == 24724) and (stream.version == 19)) or ((stream.user_version == 8340) and (stream.version == 19)):
			stream.write_uint(self.ext_hash)
		for item in self.pointers: stream.write_type(item)

		self.io_size = stream.tell() - self.io_start

	def __repr__(self):
		s = 'SizedStringEntry [Size: '+str(self.io_size)+', Address:'+str(self.io_start)+']'
		s += '\n	* file_hash = ' + self.file_hash.__repr__()
		s += '\n	* ext_hash = ' + self.ext_hash.__repr__()
		s += '\n	* pointers = ' + self.pointers.__repr__()
		s += '\n'
		return s
