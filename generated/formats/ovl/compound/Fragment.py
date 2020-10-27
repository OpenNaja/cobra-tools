import typing
from generated.array import Array
from generated.formats.ovl.compound.HeaderPointer import HeaderPointer


class Fragment:

	"""
	often huge amount of tiny files
	"""

	def __init__(self, arg=None, template=None):
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# points into header datas section
		self.pointers = Array()

	def read(self, stream):

		self.io_start = stream.tell()
		self.pointers.read(stream, HeaderPointer, 2, None)

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		self.pointers.write(stream, HeaderPointer, 2, None)

		self.io_size = stream.tell() - self.io_start

	def __repr__(self):
		s = 'Fragment [Size: '+str(self.io_size)+', Address:'+str(self.io_start)+']'
		s += '\n	* pointers = ' + self.pointers.__repr__()
		s += '\n'
		return s
