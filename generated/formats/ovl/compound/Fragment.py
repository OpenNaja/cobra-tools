import typing
from generated.formats.ovl.compound.HeaderPointer import HeaderPointer


class Fragment:

# often huge amount of tiny files

	# points into header datas section
	pointers: typing.List[HeaderPointer]

	def __init__(self, arg=None, template=None):
		self.arg = arg
		self.template = template
		self.pointers = HeaderPointer()

	def read(self, stream):
		self.pointers = [stream.read_type(HeaderPointer) for _ in range(2)]

	def write(self, stream):
		for item in self.pointers: stream.write_type(item)

	def __repr__(self):
		s = 'Fragment'
		s += '\n	* pointers = ' + self.pointers.__repr__()
		s += '\n'
		return s