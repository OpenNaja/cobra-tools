import typing


class Type2:

	"""
	Sound SFX/Sound Voice
	02 -- identifier for Sound SFX section
	"""

	# length of this section
	length: int

	# id of this Sound SFX object
	sfx_id: int

	# ?
	const_a: int

	# ?
	const_b: int

	# ?
	didx_id: int

	# ?
	wem_length: int

	# ?
	extra: typing.List[int]

	def __init__(self, arg=None, template=None):
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.length = 0
		self.sfx_id = 0
		self.const_a = 0
		self.const_b = 0
		self.didx_id = 0
		self.wem_length = 0
		self.extra = []

	def read(self, stream):

		self.io_start = stream.tell()
		self.length = stream.read_uint()
		self.sfx_id = stream.read_uint()
		self.const_a = stream.read_uint()
		self.const_b = stream.read_byte()
		self.didx_id = stream.read_uint()
		self.wem_length = stream.read_uint()
		self.extra = [stream.read_byte() for _ in range(self.length - 17)]

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_uint(self.length)
		stream.write_uint(self.sfx_id)
		stream.write_uint(self.const_a)
		stream.write_byte(self.const_b)
		stream.write_uint(self.didx_id)
		stream.write_uint(self.wem_length)
		for item in self.extra: stream.write_byte(item)

		self.io_size = stream.tell() - self.io_start

	def __repr__(self):
		s = 'Type2 [Size: '+str(self.io_size)+', Address:'+str(self.io_start)+']'
		s += '\n	* length = ' + self.length.__repr__()
		s += '\n	* sfx_id = ' + self.sfx_id.__repr__()
		s += '\n	* const_a = ' + self.const_a.__repr__()
		s += '\n	* const_b = ' + self.const_b.__repr__()
		s += '\n	* didx_id = ' + self.didx_id.__repr__()
		s += '\n	* wem_length = ' + self.wem_length.__repr__()
		s += '\n	* extra = ' + self.extra.__repr__()
		s += '\n'
		return s
