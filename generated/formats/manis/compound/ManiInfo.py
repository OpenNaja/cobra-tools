import typing
from generated.array import Array


class ManiInfo:

	"""
	288 bytes for JWE / PZ
	312 bytes for PC
	"""

	def __init__(self, arg=None, template=None):
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.zeros_start = Array()
		self.duration = 0

		# likely
		self.frame_count = 0
		self.b = 0

		# rest
		self.zeros_0 = Array()
		self.c = 0
		self.name_count = 0

		# rest
		self.zeros_1 = Array()
		self.e = 0
		self.extra_pc = Array()

		# always FF FF
		self.ffff = 0
		self.g = 0

		# rest 228 bytes
		self.zeros_2 = Array()

		# rest 14 bytes
		self.extra_zeros_pc = Array()
		self.i = 0
		self.j = 0

		# always FF
		self.ff = 0

	def read(self, stream):

		self.io_start = stream.tell()
		self.zeros_start.read(stream, 'Ushort', 5, None)
		self.duration = stream.read_float()
		self.frame_count = stream.read_uint()
		self.b = stream.read_uint()
		self.zeros_0.read(stream, 'Ushort', 7, None)
		self.c = stream.read_ushort()
		self.name_count = stream.read_ushort()
		self.zeros_1.read(stream, 'Ushort', 4, None)
		self.e = stream.read_ushort()
		if stream.version == 18:
			self.extra_pc.read(stream, 'Ushort', 5, None)
		self.ffff = stream.read_ushort()
		self.g = stream.read_ushort()
		self.zeros_2.read(stream, 'Uint', 57, None)
		if stream.version == 18:
			self.extra_zeros_pc.read(stream, 'Ushort', 7, None)
		self.i = stream.read_ushort()
		self.j = stream.read_ushort()
		self.ff = stream.read_ushort()

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		self.zeros_start.write(stream, 'Ushort', 5, None)
		stream.write_float(self.duration)
		stream.write_uint(self.frame_count)
		stream.write_uint(self.b)
		self.zeros_0.write(stream, 'Ushort', 7, None)
		stream.write_ushort(self.c)
		stream.write_ushort(self.name_count)
		self.zeros_1.write(stream, 'Ushort', 4, None)
		stream.write_ushort(self.e)
		if stream.version == 18:
			self.extra_pc.write(stream, 'Ushort', 5, None)
		stream.write_ushort(self.ffff)
		stream.write_ushort(self.g)
		self.zeros_2.write(stream, 'Uint', 57, None)
		if stream.version == 18:
			self.extra_zeros_pc.write(stream, 'Ushort', 7, None)
		stream.write_ushort(self.i)
		stream.write_ushort(self.j)
		stream.write_ushort(self.ff)

		self.io_size = stream.tell() - self.io_start

	def __repr__(self):
		s = 'ManiInfo [Size: '+str(self.io_size)+', Address:'+str(self.io_start)+']'
		s += '\n	* zeros_start = ' + self.zeros_start.__repr__()
		s += '\n	* duration = ' + self.duration.__repr__()
		s += '\n	* frame_count = ' + self.frame_count.__repr__()
		s += '\n	* b = ' + self.b.__repr__()
		s += '\n	* zeros_0 = ' + self.zeros_0.__repr__()
		s += '\n	* c = ' + self.c.__repr__()
		s += '\n	* name_count = ' + self.name_count.__repr__()
		s += '\n	* zeros_1 = ' + self.zeros_1.__repr__()
		s += '\n	* e = ' + self.e.__repr__()
		s += '\n	* extra_pc = ' + self.extra_pc.__repr__()
		s += '\n	* ffff = ' + self.ffff.__repr__()
		s += '\n	* g = ' + self.g.__repr__()
		s += '\n	* zeros_2 = ' + self.zeros_2.__repr__()
		s += '\n	* extra_zeros_pc = ' + self.extra_zeros_pc.__repr__()
		s += '\n	* i = ' + self.i.__repr__()
		s += '\n	* j = ' + self.j.__repr__()
		s += '\n	* ff = ' + self.ff.__repr__()
		s += '\n'
		return s
