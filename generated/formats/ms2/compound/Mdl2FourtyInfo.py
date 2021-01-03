import typing
from generated.array import Array


class Mdl2FourtyInfo:

	def __init__(self, arg=None, template=None):
		self.name = ''
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# 0, 1 or 0, 0, 0, 0
		self.unknowns = Array()

	def read(self, stream):

		self.io_start = stream.tell()
		self.unknowns = stream.read_uint64s((5))

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_uint64s(self.unknowns)

		self.io_size = stream.tell() - self.io_start

	def __repr__(self):
		s = 'Mdl2FourtyInfo [Size: '+str(self.io_size)+', Address: '+str(self.io_start)+'] ' + self.name
		s += '\n	* unknowns = ' + self.unknowns.__repr__()
		s += '\n'
		return s
