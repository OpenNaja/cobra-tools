import typing
from generated.array import Array
from generated.formats.ms2.compound.StreamInfo import StreamInfo


class Ms2BufferInfoZT:

	"""
	Data describing a MS2 buffer giving the size of the whole vertex and tri buffer.
	266 bytes
	very end of buffer 0 after the names list
	"""

	def __init__(self, arg=None, template=None):
		self.name = ''
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.unk = 0
		self.stream_count = 0
		self.unks = Array()
		self.streams = Array()

	def read(self, stream):

		self.io_start = stream.tell()
		self.unk = stream.read_ushort()
		self.stream_count = stream.read_ushort()
		self.unks = stream.read_ushorts((3))
		self.streams.read(stream, StreamInfo, self.stream_count, None)

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_ushort(self.unk)
		stream.write_ushort(self.stream_count)
		stream.write_ushorts(self.unks)
		self.streams.write(stream, StreamInfo, self.stream_count, None)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'Ms2BufferInfoZT [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* unk = {self.unk.__repr__()}'
		s += f'\n	* stream_count = {self.stream_count.__repr__()}'
		s += f'\n	* unks = {self.unks.__repr__()}'
		s += f'\n	* streams = {self.streams.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
