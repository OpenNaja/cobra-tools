from generated.formats.bnk.compound.Type2 import Type2
import typing
from generated.formats.bnk.compound.TypeOther import TypeOther


class HircPointer:

	# length of following data
	id: int
	data: typing.Union[Type2, TypeOther]

	def __init__(self, arg=None, template=None):
		self.arg = arg
		self.template = template
		self.id = 0
		self.data = Type2()
		self.data = TypeOther()

	def read(self, stream):
		self.id = stream.read_byte()
		if self.id == 2:
			self.data = stream.read_type(Type2)
		if self.id != 2:
			self.data = stream.read_type(TypeOther)

	def write(self, stream):
		stream.write_byte(self.id)
		if self.id == 2:
			stream.write_type(self.data)
		if self.id != 2:
			stream.write_type(self.data)

	def __repr__(self):
		s = 'HircPointer'
		s += '\n	* id = ' + self.id.__repr__()
		s += '\n	* data = ' + self.data.__repr__()
		s += '\n	* data = ' + self.data.__repr__()
		s += '\n'
		return s