import typing
from generated.formats.manis.compound.Repeat import Repeat


class ManiBlock:
	indices_0: typing.List[int]
	indices_1: typing.List[int]
	indices_2: typing.List[int]
	p_indices_0: typing.List[int]
	p_indices_1: typing.List[int]
	p_indices_2: typing.List[int]
	c_indices_0: typing.List[int]
	c_indices_1: typing.List[int]
	c_indices_2: typing.List[int]
	zero: int

	# likely
	frame_count: int
	c: int
	e: int

	# fixed
	zeros: typing.List[int]
	count: int

	# usually / always 420
	four_and_twenty: int
	pad_to_8: typing.List[int]

	# these are likely a scale reference or factor
	floats: typing.List[float]
	repeats: typing.List[Repeat]

	def __init__(self, arg=None, template=None):
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.indices_0 = []
		self.indices_1 = []
		self.indices_2 = []
		self.indices_0 = []
		self.indices_1 = []
		self.indices_2 = []
		self.p_indices_0 = []
		self.p_indices_1 = []
		self.p_indices_2 = []
		self.c_indices_0 = []
		self.c_indices_1 = []
		self.c_indices_2 = []
		self.zero = 0
		self.frame_count = 0
		self.c = 0
		self.e = 0
		self.zeros = []
		self.count = 0
		self.four_and_twenty = 0
		self.zeros = []
		self.pad_to_8 = []
		self.floats = []
		self.repeats = []

	def read(self, stream):

		self.io_start = stream.tell()
		if stream.version == 18:
			self.indices_0 = [stream.read_ushort() for _ in range(self.arg.c)]
			self.indices_1 = [stream.read_ushort() for _ in range(self.arg.name_count)]
			self.indices_2 = [stream.read_ushort() for _ in range(self.arg.e)]
		if not (stream.version == 18):
			self.indices_0 = [stream.read_uint() for _ in range(self.arg.c)]
			self.indices_1 = [stream.read_uint() for _ in range(self.arg.name_count)]
			self.indices_2 = [stream.read_uint() for _ in range(self.arg.e)]
		self.p_indices_0 = [stream.read_ubyte() for _ in range(self.arg.c)]
		self.p_indices_1 = [stream.read_ubyte() for _ in range(self.arg.name_count)]
		self.p_indices_2 = [stream.read_ubyte() for _ in range(self.arg.e)]
		if stream.version == 18:
			self.c_indices_0 = [stream.read_ubyte() for _ in range(self.arg.c)]
			self.c_indices_1 = [stream.read_ubyte() for _ in range(self.arg.name_count)]
			self.c_indices_2 = [stream.read_ubyte() for _ in range(self.arg.e)]
		self.zero = stream.read_uint64()
		self.frame_count = stream.read_uint()
		self.c = stream.read_uint()
		self.e = stream.read_uint()
		self.zeros = [stream.read_uint() for _ in range(19)]
		self.count = stream.read_ushort()
		self.four_and_twenty = stream.read_ushort()
		self.zeros = [stream.read_ubyte() for _ in range(self.count)]
		self.pad_to_8 = [stream.read_ubyte() for _ in range((8 - (self.count % 8)) % 8)]
		self.floats = [stream.read_float() for _ in range(6)]
		self.repeats = [stream.read_type(Repeat) for _ in range(self.count)]

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		if stream.version == 18:
			for item in self.indices_0: stream.write_ushort(item)
			for item in self.indices_1: stream.write_ushort(item)
			for item in self.indices_2: stream.write_ushort(item)
		if not (stream.version == 18):
			for item in self.indices_0: stream.write_uint(item)
			for item in self.indices_1: stream.write_uint(item)
			for item in self.indices_2: stream.write_uint(item)
		for item in self.p_indices_0: stream.write_ubyte(item)
		for item in self.p_indices_1: stream.write_ubyte(item)
		for item in self.p_indices_2: stream.write_ubyte(item)
		if stream.version == 18:
			for item in self.c_indices_0: stream.write_ubyte(item)
			for item in self.c_indices_1: stream.write_ubyte(item)
			for item in self.c_indices_2: stream.write_ubyte(item)
		stream.write_uint64(self.zero)
		stream.write_uint(self.frame_count)
		stream.write_uint(self.c)
		stream.write_uint(self.e)
		for item in self.zeros: stream.write_uint(item)
		stream.write_ushort(self.count)
		stream.write_ushort(self.four_and_twenty)
		for item in self.zeros: stream.write_ubyte(item)
		for item in self.pad_to_8: stream.write_ubyte(item)
		for item in self.floats: stream.write_float(item)
		for item in self.repeats: stream.write_type(item)

		self.io_size = stream.tell() - self.io_start

	def __repr__(self):
		s = 'ManiBlock [Size: '+str(self.io_size)+', Address:'+str(self.io_start)+']'
		s += '\n	* indices_0 = ' + self.indices_0.__repr__()
		s += '\n	* indices_1 = ' + self.indices_1.__repr__()
		s += '\n	* indices_2 = ' + self.indices_2.__repr__()
		s += '\n	* p_indices_0 = ' + self.p_indices_0.__repr__()
		s += '\n	* p_indices_1 = ' + self.p_indices_1.__repr__()
		s += '\n	* p_indices_2 = ' + self.p_indices_2.__repr__()
		s += '\n	* c_indices_0 = ' + self.c_indices_0.__repr__()
		s += '\n	* c_indices_1 = ' + self.c_indices_1.__repr__()
		s += '\n	* c_indices_2 = ' + self.c_indices_2.__repr__()
		s += '\n	* zero = ' + self.zero.__repr__()
		s += '\n	* frame_count = ' + self.frame_count.__repr__()
		s += '\n	* c = ' + self.c.__repr__()
		s += '\n	* e = ' + self.e.__repr__()
		s += '\n	* zeros = ' + self.zeros.__repr__()
		s += '\n	* count = ' + self.count.__repr__()
		s += '\n	* four_and_twenty = ' + self.four_and_twenty.__repr__()
		s += '\n	* pad_to_8 = ' + self.pad_to_8.__repr__()
		s += '\n	* floats = ' + self.floats.__repr__()
		s += '\n	* repeats = ' + self.repeats.__repr__()
		s += '\n'
		return s
