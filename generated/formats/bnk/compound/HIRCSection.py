from generated.array import Array
from generated.context import ContextReference
from generated.formats.bnk.compound.HircPointer import HircPointer


class HIRCSection:

	"""
	The HIRC section contains all the Wwise objects, including the events, the containers to group sounds, and the references to the sound files.
	"""

	context = ContextReference()

	def __init__(self, context, arg=None, template=None, set_default=True):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# length of following data
		self.length = 0
		self.count = 0
		self.hirc_pointers = Array((self.count), HircPointer, self.context, None, None)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.length = 0
		self.count = 0
		self.hirc_pointers = Array((self.count), HircPointer, self.context, None, None)

	def read(self, stream):
		self.io_start = stream.tell()
		self.length = stream.read_uint()
		self.count = stream.read_uint()
		self.hirc_pointers.read(stream, HircPointer, self.count, None)

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()
		stream.write_uint(self.length)
		stream.write_uint(self.count)
		self.hirc_pointers.write(stream, HircPointer, self.count, None)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'HIRCSection [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* length = {self.length.__repr__()}'
		s += f'\n	* count = {self.count.__repr__()}'
		s += f'\n	* hirc_pointers = {self.hirc_pointers.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
