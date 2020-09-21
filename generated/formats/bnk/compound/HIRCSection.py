import typing
from generated.formats.bnk.compound.HircPointer import HircPointer

class HIRCSection:

# First Section of a soundback aux

	# length of following data
    
	length: int
	count: int
	hirc_pointers: typing.List[HircPointer]
    

	# filler zeroes
	data: typing.List[int]

	def __init__(self, arg=None, template=None):
		self.arg = arg
		self.template = template

	def read(self, stream):
		self.length = stream.read_uint()
		self.count = stream.read_uint()
		self.hirc_pointers = [stream.read_type(HircPointer) for _ in range(self.count)]

	def write(self, stream):
		stream.write_uint(self.length)
		stream.write_uint(self.count)
		for item in self.hirc_pointers: stream.write_type(item)

	def __repr__(self):
		s = 'HIRCSection'
		s += '\nlength ' + self.length.__repr__()
		s += '\ncount ' + self.length.__repr__()
		s += '\nhirc_pointers ' + self.hirc_pointers.__repr__()
		s += '\n'
		return s
