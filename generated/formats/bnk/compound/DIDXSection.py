import typing
from generated.formats.bnk.compound.DataPointer import DataPointer


class DIDXSection:

	"""
	second Section of a soundback aux
	"""

	# length of following data
	length: int
	data_pointers: typing.List[DataPointer]

	def __init__(self, arg=None, template=None):
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.length = 0
		self.data_pointers = []

	def read(self, stream):

		io_start = stream.tell()
		self.length = stream.read_uint()
		self.data_pointers = [stream.read_type(DataPointer) for _ in range(int(self.length / 12))]

		self.io_size = stream.tell() - io_start

	def write(self, stream):

		io_start = stream.tell()
		stream.write_uint(self.length)
		for item in self.data_pointers: stream.write_type(item)

		self.io_size = stream.tell() - io_start

	def __repr__(self):
		s = 'DIDXSection [Size: '+str(self.io_size)+']'
		s += '\n	* length = ' + self.length.__repr__()
		s += '\n	* data_pointers = ' + self.data_pointers.__repr__()
		s += '\n'
		return s
