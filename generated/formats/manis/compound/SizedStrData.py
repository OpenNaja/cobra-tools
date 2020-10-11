import typing


class SizedStrData:
	a: int
	hash_block_size: int
	zeros: typing.List[int]
	c: int

	def __init__(self, arg=None, template=None):
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.a = 0
		self.hash_block_size = 0
		self.zeros = []
		self.c = 0

	def read(self, stream):

		self.io_start = stream.tell()
		self.a = stream.read_ushort()
		self.hash_block_size = stream.read_ushort()
		self.zeros = [stream.read_int() for _ in range(2)]
		self.c = stream.read_ushort()

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_ushort(self.a)
		stream.write_ushort(self.hash_block_size)
		for item in self.zeros: stream.write_int(item)
		stream.write_ushort(self.c)

		self.io_size = stream.tell() - self.io_start

	def __repr__(self):
		s = 'SizedStrData [Size: '+str(self.io_size)+', Address:'+str(self.io_start)+']'
		s += '\n	* a = ' + self.a.__repr__()
		s += '\n	* hash_block_size = ' + self.hash_block_size.__repr__()
		s += '\n	* zeros = ' + self.zeros.__repr__()
		s += '\n	* c = ' + self.c.__repr__()
		s += '\n'
		return s
