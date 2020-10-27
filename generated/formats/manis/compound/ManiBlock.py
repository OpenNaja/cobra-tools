import typing
from generated.array import Array
from generated.formats.manis.compound.Repeat import Repeat


class ManiBlock:

	def __init__(self, arg=None, template=None):
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.indices_0 = Array()
		self.indices_0 = Array()
		self.indices_1 = Array()
		self.indices_1 = Array()
		self.indices_2 = Array()
		self.indices_2 = Array()
		self.p_indices_0 = Array()
		self.p_indices_1 = Array()
		self.p_indices_2 = Array()
		self.c_indices_0 = Array()
		self.c_indices_1 = Array()
		self.c_indices_2 = Array()
		self.zero = 0

		# likely
		self.frame_count = 0
		self.c = 0
		self.e = 0

		# fixed
		self.zeros = Array()
		self.zeros = Array()
		self.count = 0

		# usually / always 420
		self.four_and_twenty = 0
		self.pad_to_8 = Array()

		# these are likely a scale reference or factor
		self.floats = Array()
		self.repeats = Array()

	def read(self, stream):

		self.io_start = stream.tell()
		if stream.version == 18:
			self.indices_0.read(stream, 'Ushort', self.arg.c, None)
		if not (stream.version == 18):
			self.indices_0.read(stream, 'Uint', self.arg.c, None)
		if stream.version == 18:
			self.indices_1.read(stream, 'Ushort', self.arg.name_count, None)
		if not (stream.version == 18):
			self.indices_1.read(stream, 'Uint', self.arg.name_count, None)
		if stream.version == 18:
			self.indices_2.read(stream, 'Ushort', self.arg.e, None)
		if not (stream.version == 18):
			self.indices_2.read(stream, 'Uint', self.arg.e, None)
		self.p_indices_0.read(stream, 'Ubyte', self.arg.c, None)
		self.p_indices_1.read(stream, 'Ubyte', self.arg.name_count, None)
		self.p_indices_2.read(stream, 'Ubyte', self.arg.e, None)
		if stream.version == 18:
			self.c_indices_0.read(stream, 'Ubyte', self.arg.c, None)
			self.c_indices_1.read(stream, 'Ubyte', self.arg.name_count, None)
			self.c_indices_2.read(stream, 'Ubyte', self.arg.e, None)
		self.zero = stream.read_uint64()
		self.frame_count = stream.read_uint()
		self.c = stream.read_uint()
		self.e = stream.read_uint()
		self.zeros.read(stream, 'Uint', 19, None)
		self.zeros.read(stream, 'Ubyte', self.count, None)
		self.count = stream.read_ushort()
		self.four_and_twenty = stream.read_ushort()
		self.pad_to_8.read(stream, 'Ubyte', (8 - (self.count % 8)) % 8, None)
		self.floats.read(stream, 'Float', 6, None)
		self.repeats.read(stream, Repeat, self.count, None)

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		if stream.version == 18:
			self.indices_0.write(stream, 'Ushort', self.arg.c, None)
		if not (stream.version == 18):
			self.indices_0.write(stream, 'Uint', self.arg.c, None)
		if stream.version == 18:
			self.indices_1.write(stream, 'Ushort', self.arg.name_count, None)
		if not (stream.version == 18):
			self.indices_1.write(stream, 'Uint', self.arg.name_count, None)
		if stream.version == 18:
			self.indices_2.write(stream, 'Ushort', self.arg.e, None)
		if not (stream.version == 18):
			self.indices_2.write(stream, 'Uint', self.arg.e, None)
		self.p_indices_0.write(stream, 'Ubyte', self.arg.c, None)
		self.p_indices_1.write(stream, 'Ubyte', self.arg.name_count, None)
		self.p_indices_2.write(stream, 'Ubyte', self.arg.e, None)
		if stream.version == 18:
			self.c_indices_0.write(stream, 'Ubyte', self.arg.c, None)
			self.c_indices_1.write(stream, 'Ubyte', self.arg.name_count, None)
			self.c_indices_2.write(stream, 'Ubyte', self.arg.e, None)
		stream.write_uint64(self.zero)
		stream.write_uint(self.frame_count)
		stream.write_uint(self.c)
		stream.write_uint(self.e)
		self.zeros.write(stream, 'Uint', 19, None)
		self.zeros.write(stream, 'Ubyte', self.count, None)
		stream.write_ushort(self.count)
		stream.write_ushort(self.four_and_twenty)
		self.pad_to_8.write(stream, 'Ubyte', (8 - (self.count % 8)) % 8, None)
		self.floats.write(stream, 'Float', 6, None)
		self.repeats.write(stream, Repeat, self.count, None)

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
