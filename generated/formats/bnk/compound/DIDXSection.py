import numpy
import typing
from generated.array import Array
from generated.context import ContextReference
from generated.formats.bnk.compound.DataPointer import DataPointer


class DIDXSection:

	"""
	second Section of a soundback aux
	"""

	context = ContextReference()

	def __init__(self, context, arg=None, template=None):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# length of following data
		self.length = 0
		self.data_pointers = Array(self.context)
		self.set_defaults()

	def set_defaults(self):
		self.length = 0
		self.data_pointers = Array(self.context)

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

	def get_info_str(self):
		return f'DIDXSection [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* length = {self.length.__repr__()}'
		s += f'\n	* data_pointers = {self.data_pointers.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
