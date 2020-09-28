import typing
from generated.formats.ovl.compound.HeaderPointer import HeaderPointer


class SizedStringEntry:

# points to a sized string in a header's data block

	# hash of the file that should be read
	file_hash: int

	# matches matching HeaderEntry's Ext Hash
	ext_hash: int

	# points into header datas section
	pointers: typing.List[HeaderPointer]

	def __init__(self, arg=None, template=None):
		self.arg = arg
		self.template = template
		self.file_hash = 0
		self.ext_hash = 0
		self.pointers = HeaderPointer()

	def read(self, stream):
		self.file_hash = stream.read_uint()
		if ((stream.user_version == 24724) and (stream.version == 19)) or ((stream.user_version == 8340) and (stream.version == 19)):
			self.ext_hash = stream.read_uint()
		self.pointers = [stream.read_type(HeaderPointer) for _ in range(1)]

	def write(self, stream):
		stream.write_uint(self.file_hash)
		if ((stream.user_version == 24724) and (stream.version == 19)) or ((stream.user_version == 8340) and (stream.version == 19)):
			stream.write_uint(self.ext_hash)
		for item in self.pointers: stream.write_type(item)

	def __repr__(self):
		s = 'SizedStringEntry'
		s += '\n	* file_hash = ' + self.file_hash.__repr__()
		s += '\n	* ext_hash = ' + self.ext_hash.__repr__()
		s += '\n	* pointers = ' + self.pointers.__repr__()
		s += '\n'
		return s