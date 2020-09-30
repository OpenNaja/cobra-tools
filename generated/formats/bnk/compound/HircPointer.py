from generated.formats.bnk.compound.TypeOther import TypeOther
from generated.formats.bnk.compound.Type2 import Type2
import typing


class HircPointer:

	# length of following data
	id: int
	data: typing.Union[TypeOther, Type2]

	def __init__(self, arg=None, template=None):
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.id = 0
		self.data = Type2()
		self.data = TypeOther()

	def read(self, stream):

		io_start = stream.tell()
		self.id = stream.read_byte()
		if self.id == 2:
			self.data = stream.read_type(Type2)
		if self.id != 2:
			self.data = stream.read_type(TypeOther)

		self.io_size = stream.tell() - io_start

	def write(self, stream):

		io_start = stream.tell()
		stream.write_byte(self.id)
		if self.id == 2:
			stream.write_type(self.data)
		if self.id != 2:
			stream.write_type(self.data)

		self.io_size = stream.tell() - io_start

	def __repr__(self):
		s = 'HircPointer [Size: '+str(self.io_size)+']'
		s += '\n	* id = ' + self.id.__repr__()
		s += '\n	* data = ' + self.data.__repr__()
		s += '\n'
		return s
