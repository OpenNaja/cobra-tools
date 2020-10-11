import typing


class FFCounter:

	"""
	count is nonzero in PZ broken birch model
	"""
	count: int
	f_fs: typing.List[int]

	def __init__(self, arg=None, template=None):
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.count = 0
		self.f_fs = []

	def read(self, stream):

		self.io_start = stream.tell()
		self.count = stream.read_uint()
		self.f_fs = [stream.read_int() for _ in range(self.count)]

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_uint(self.count)
		for item in self.f_fs: stream.write_int(item)

		self.io_size = stream.tell() - self.io_start

	def __repr__(self):
		s = 'FFCounter [Size: '+str(self.io_size)+', Address:'+str(self.io_start)+']'
		s += '\n	* count = ' + self.count.__repr__()
		s += '\n	* f_fs = ' + self.f_fs.__repr__()
		s += '\n'
		return s
