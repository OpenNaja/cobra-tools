import numpy
import typing
from generated.array import Array
from generated.context import ContextReference
from generated.formats.ms2.compound.StreamInfo import StreamInfo


class Ms2BufferInfoZT:

	"""
	Data describing a MS2 buffer giving the size of the whole vertex and tri buffer.
	from here on, it's buffer 1
	"""

	context = ContextReference()

	def __init__(self, context, arg=None, template=None):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.streams = Array(self.context)
		self.set_defaults()

	def set_defaults(self):
		self.streams = Array(self.context)

	def read(self, stream):
		self.io_start = stream.tell()
		self.streams.read(stream, StreamInfo, self.arg.general_info.vertex_buffer_count, None)

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()
		self.streams.write(stream, StreamInfo, self.arg.general_info.vertex_buffer_count, None)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'Ms2BufferInfoZT [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* streams = {self.streams.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
