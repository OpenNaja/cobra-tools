import typing
from generated.array import Array


class PcFFCounter:

	"""
	count is nonzero in PZ broken birch model
	"""

	def __init__(self, arg=None, template=None):
		self.name = ''
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.count = 0
		self.f_fs = Array()

	def read(self, stream):

		self.io_start = stream.tell()
		self.count = stream.read_uint()
		self.f_fs = stream.read_bytes((self.count))

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_uint(self.count)
		stream.write_bytes(self.f_fs)

		self.io_size = stream.tell() - self.io_start

	def __repr__(self):
		s = 'PcFFCounter [Size: '+str(self.io_size)+', Address: '+str(self.io_start)+'] ' + self.name
		s += '\n	* count = ' + self.count.__repr__()
		s += '\n	* f_fs = ' + self.f_fs.__repr__()
		s += '\n'
		return s
