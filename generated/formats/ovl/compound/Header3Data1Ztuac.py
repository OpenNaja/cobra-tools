import typing
from generated.array import Array
from generated.formats.ovl.compound.Header3Data1ZTUACEntry import Header3Data1ZTUACEntry


class Header3Data1Ztuac:

	"""
	Data struct for headers of type 7
	"""

	def __init__(self, arg=None, template=None):
		self.name = ''
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.lods = Array()

		# ?not sure if this isn't just junk data
		self.data_size = 0

	def read(self, stream):

		self.io_start = stream.tell()
		self.lods.read(stream, Header3Data1ZTUACEntry, self.arg, None)
		self.data_size = stream.read_ushort()

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		self.lods.write(stream, Header3Data1ZTUACEntry, self.arg, None)
		stream.write_ushort(self.data_size)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'Header3Data1Ztuac [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* lods = {self.lods.__repr__()}'
		s += f'\n	* data_size = {self.data_size.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
