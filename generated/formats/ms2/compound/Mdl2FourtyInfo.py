import typing
from generated.array import Array


class Mdl2FourtyInfo:

	def __init__(self, arg=None, template=None):
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# 0, 1, 0, 0, 0
		self.unknowns = Array()

	def read(self, stream):

		self.io_start = stream.tell()
		self.unknowns.read(stream, 'Uint64', 5, None)

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		self.unknowns.write(stream, 'Uint64', 5, None)

		self.io_size = stream.tell() - self.io_start

	def __repr__(self):
		s = 'Mdl2FourtyInfo [Size: '+str(self.io_size)+', Address:'+str(self.io_start)+']'
		s += '\n	* unknowns = ' + self.unknowns.__repr__()
		s += '\n'
		return s
