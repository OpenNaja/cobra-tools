import typing
from generated.formats.bnk.compound.Type2 import Type2
from generated.formats.bnk.compound.TypeOther import TypeOther


class HircPointer:

	# length of following data
	id: int
	data: typing.Union[Type2, TypeOther]

	def __init__(self, arg=None, template=None):
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.id = 0
		self.data = Type2()
		self.data = TypeOther()

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

	def __repr__(self):
		s = 'HircPointer [Size: '+str(self.io_size)+', Address:'+str(self.io_start)+']'
		s += '\n	* id = ' + self.id.__repr__()
		s += '\n	* data = ' + self.data.__repr__()
		s += '\n'
		return s
