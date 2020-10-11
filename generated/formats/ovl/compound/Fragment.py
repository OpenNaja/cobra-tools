import typing
from generated.formats.ovl.compound.HeaderPointer import HeaderPointer


class Fragment:

	"""
	often huge amount of tiny files
	"""

	# points into header datas section
	pointers: typing.List[HeaderPointer]

	def __init__(self, arg=None, template=None):
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.pointers = []

	def read(self, stream):

		self.io_start = stream.tell()
		self.pointers = [stream.read_type(HeaderPointer) for _ in range(2)]

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		for item in self.pointers: stream.write_type(item)

		self.io_size = stream.tell() - self.io_start

	def __repr__(self):
		s = 'Fragment [Size: '+str(self.io_size)+', Address:'+str(self.io_start)+']'
		s += '\n	* pointers = ' + self.pointers.__repr__()
		s += '\n'
		return s
