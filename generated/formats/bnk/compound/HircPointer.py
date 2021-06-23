import typing
from generated.formats.bnk.compound.Type2 import Type2
from generated.formats.bnk.compound.TypeOther import TypeOther


class HircPointer:

	def __init__(self, arg=None, template=None):
		self.name = ''
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# length of following data
		self.id = 0
		self.data = Type2(None, None)
		self.data = TypeOther(None, None)

	def read(self, stream):

		self.io_start = stream.tell()
		self.id = stream.read_byte()
		if self.id == 2:
			self.data = stream.read_type(Type2)
		if self.id != 2:
			self.data = stream.read_type(TypeOther)

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_byte(self.id)
		if self.id == 2:
			stream.write_type(self.data)
		if self.id != 2:
			stream.write_type(self.data)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'HircPointer [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* id = {self.id.__repr__()}'
		s += f'\n	* data = {self.data.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
