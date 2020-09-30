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
	zerosa: int

	# ?
	zerosb: int

	# ?
	some_id: int

	# ?
	const_c: int

	# ?
	const_d: int

	# ?
	const_e: int

	# ?
	float_a: float

	# four unknown bytes
	zeros_c: typing.List[int]

	# ?
	flag: int

	# ?
	zerosd: int

	# ?
	zerose: int

	# ?

	# ?
	extra: typing.List[int]

	def __init__(self, arg=None, template=None):
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.length = 0
		self.sfx_id = 0
		self.const_a = 0
		self.const_b = 0
		self.didx_id = 0
		self.wem_length = 0
		self.zerosa = 0
		self.zerosb = 0
		self.some_id = 0
		self.const_c = 0
		self.const_d = 0
		self.const_e = 0
		self.float_a = 0
		self.zeros_c = 0
		self.flag = 0
		self.zerosd = 0
		self.zerose = 0
		self.extra = 0
		self.extra = 0

	def read(self, stream):

		io_start = stream.tell()
		self.length = stream.read_uint()
		self.sfx_id = stream.read_uint()
		self.const_a = stream.read_uint()
		self.const_b = stream.read_byte()
		self.didx_id = stream.read_uint()
		self.wem_length = stream.read_uint()
		self.zerosa = stream.read_uint()
		self.zerosb = stream.read_uint()
		self.some_id = stream.read_uint()
		self.const_c = stream.read_byte()
		self.const_d = stream.read_byte()
		if self.const_d != 0:
			self.const_e = stream.read_byte()
			self.float_a = stream.read_float()
		self.zeros_c = [stream.read_byte() for _ in range(4)]
		self.flag = stream.read_byte()
		self.zerosd = stream.read_uint()
		self.zerose = stream.read_uint()
		if (self.const_d != 0) and ((self.length - 49) > 0):
			self.extra = [stream.read_byte() for _ in range(self.length - 49)]
		if (self.const_d == 0) and ((self.length - 44) > 0):
			self.extra = [stream.read_byte() for _ in range(self.length - 44)]

		self.io_size = stream.tell() - io_start

	def write(self, stream):

		io_start = stream.tell()
		stream.write_uint(self.length)
		stream.write_uint(self.sfx_id)
		stream.write_uint(self.const_a)
		stream.write_byte(self.const_b)
		stream.write_uint(self.didx_id)
		stream.write_uint(self.wem_length)
		stream.write_uint(self.zerosa)
		stream.write_uint(self.zerosb)
		stream.write_uint(self.some_id)
		stream.write_byte(self.const_c)
		stream.write_byte(self.const_d)
		if self.const_d != 0:
			stream.write_byte(self.const_e)
			stream.write_float(self.float_a)
		for item in self.zeros_c: stream.write_byte(item)
		stream.write_byte(self.flag)
		stream.write_uint(self.zerosd)
		stream.write_uint(self.zerose)
		if (self.const_d != 0) and ((self.length - 49) > 0):
			for item in self.extra: stream.write_byte(item)
		if (self.const_d == 0) and ((self.length - 44) > 0):
			for item in self.extra: stream.write_byte(item)

		self.io_size = stream.tell() - io_start

	def __repr__(self):
		s = 'Type2 [Size: '+str(self.io_size)+']'
		s += '\n	* length = ' + self.length.__repr__()
		s += '\n	* sfx_id = ' + self.sfx_id.__repr__()
		s += '\n	* const_a = ' + self.const_a.__repr__()
		s += '\n	* const_b = ' + self.const_b.__repr__()
		s += '\n	* didx_id = ' + self.didx_id.__repr__()
		s += '\n	* wem_length = ' + self.wem_length.__repr__()
		s += '\n	* zerosa = ' + self.zerosa.__repr__()
		s += '\n	* zerosb = ' + self.zerosb.__repr__()
		s += '\n	* some_id = ' + self.some_id.__repr__()
		s += '\n	* const_c = ' + self.const_c.__repr__()
		s += '\n	* const_d = ' + self.const_d.__repr__()
		s += '\n	* const_e = ' + self.const_e.__repr__()
		s += '\n	* float_a = ' + self.float_a.__repr__()
		s += '\n	* zeros_c = ' + self.zeros_c.__repr__()
		s += '\n	* flag = ' + self.flag.__repr__()
		s += '\n	* zerosd = ' + self.zerosd.__repr__()
		s += '\n	* zerose = ' + self.zerose.__repr__()
		s += '\n	* extra = ' + self.extra.__repr__()
		s += '\n'
		return s
