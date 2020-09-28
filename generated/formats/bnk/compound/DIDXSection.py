import typing
from generated.formats.bnk.compound.DataPointer import DataPointer


class DIDXSection:

# second Section of a soundback aux

	# length of following data
	length: int
	data_pointers: typing.List[DataPointer]

	def __init__(self, arg=None, template=None):
		self.arg = arg
		self.template = template
		self.length = 0
		self.data_pointers = DataPointer()

	def read(self, stream):
		self.length = stream.read_uint()
		self.data_pointers = [stream.read_type(DataPointer) for _ in range(int(self.length / 12))]

	def write(self, stream):
		stream.write_uint(self.length)
		for item in self.data_pointers: stream.write_type(item)

	def __repr__(self):
		s = 'DIDXSection'
		s += '\n	* length = ' + self.length.__repr__()
		s += '\n	* data_pointers = ' + self.data_pointers.__repr__()
		s += '\n'
		return s