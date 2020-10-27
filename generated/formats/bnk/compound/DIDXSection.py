import typing
from generated.array import Array
from generated.formats.bnk.compound.DataPointer import DataPointer


class DIDXSection:

	"""
	second Section of a soundback aux
	"""

	def __init__(self, arg=None, template=None):
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# length of following data
		self.length = 0
		self.data_pointers = Array()

	def read(self, stream):

		self.io_start = stream.tell()
		self.length = stream.read_uint()
		self.data_pointers.read(stream, DataPointer, int(self.length / 12), None)

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_uint(self.length)
		self.data_pointers.write(stream, DataPointer, int(self.length / 12), None)

		self.io_size = stream.tell() - self.io_start

	def __repr__(self):
		s = 'DIDXSection [Size: '+str(self.io_size)+', Address:'+str(self.io_start)+']'
		s += '\n	* length = ' + self.length.__repr__()
		s += '\n	* data_pointers = ' + self.data_pointers.__repr__()
		s += '\n'
		return s
