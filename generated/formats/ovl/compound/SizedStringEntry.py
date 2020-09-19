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

	def read(self, stream):
		self.file_hash = stream.read_uint()
		self.ext_hash = stream.read_uint()
		self.pointers = [stream.read_type(HeaderPointer) for _ in range(1)]

	def write(self, stream):
		stream.write_uint(self.file_hash)
		stream.write_uint(self.ext_hash)
		for item in self.pointers: stream.write_type(item)

	def __repr__(self):
		s = 'SizedStringEntry'
		s += '\nfile_hash ' + self.file_hash.__repr__()
		s += '\next_hash ' + self.ext_hash.__repr__()
		s += '\npointers ' + self.pointers.__repr__()
		s += '\n'
		return s