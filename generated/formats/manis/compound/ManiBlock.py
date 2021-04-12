import numpy
import typing
from generated.array import Array
from generated.formats.manis.compound.Repeat import Repeat


class ManiBlock:

	def __init__(self, arg=None, template=None):
		self.name = ''
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.indices_0 = numpy.zeros((), dtype='ushort')
		self.indices_0 = numpy.zeros((), dtype='uint')
		self.indices_1 = numpy.zeros((), dtype='ushort')
		self.indices_1 = numpy.zeros((), dtype='uint')
		self.indices_2 = numpy.zeros((), dtype='ushort')
		self.indices_2 = numpy.zeros((), dtype='uint')
		self.p_indices_0 = numpy.zeros((), dtype='ubyte')
		self.p_indices_1 = numpy.zeros((), dtype='ubyte')
		self.p_indices_2 = numpy.zeros((), dtype='ubyte')
		self.c_indices_0 = numpy.zeros((), dtype='ubyte')
		self.c_indices_1 = numpy.zeros((), dtype='ubyte')
		self.c_indices_2 = numpy.zeros((), dtype='ubyte')
		self.padding = numpy.zeros((), dtype='ubyte')

		# likely
		self.frame_count = 0
		self.c = 0
		self.e = 0

		# fixed
		self.zeros_19 = numpy.zeros((19), dtype='uint')
		self.count = 0

		# usually / always 420
		self.four_and_twenty = 0
		self.zeros = numpy.zeros((self.count), dtype='ubyte')
		self.pad_to_8 = numpy.zeros(((8 - (self.count % 8)) % 8), dtype='ubyte')

		# these are likely a scale reference or factor
		self.floats = numpy.zeros((6), dtype='float')
		self.repeats = Array()

	def read(self, stream):

		self.io_start = stream.tell()
		if stream.version == 18:
			self.indices_0 = stream.read_ushorts((self.arg.c))
		if not (stream.version == 18):
			self.indices_0 = stream.read_uints((self.arg.c))
		if stream.version == 18:
			self.indices_1 = stream.read_ushorts((self.arg.name_count))
		if not (stream.version == 18):
			self.indices_1 = stream.read_uints((self.arg.name_count))
		if stream.version == 18:
			self.indices_2 = stream.read_ushorts((self.arg.e))
		if not (stream.version == 18):
			self.indices_2 = stream.read_uints((self.arg.e))
		self.p_indices_0 = stream.read_ubytes((self.arg.c))
		self.p_indices_1 = stream.read_ubytes((self.arg.name_count))
		self.p_indices_2 = stream.read_ubytes((self.arg.e))
		if stream.version == 18:
			self.c_indices_0 = stream.read_ubytes((self.arg.c))
			self.c_indices_1 = stream.read_ubytes((self.arg.name_count))
			self.c_indices_2 = stream.read_ubytes((self.arg.e))
		self.padding = stream.read_ubytes(((16 - (((self.arg.c + (self.arg.name_count + self.arg.e)) * 4) % 16)) % 16))
		self.frame_count = stream.read_uint()
		self.c = stream.read_uint()
		self.e = stream.read_uint()
		self.zeros_19 = stream.read_uints((19))
		self.count = stream.read_ushort()
		self.four_and_twenty = stream.read_ushort()
		self.zeros = stream.read_ubytes((self.count))
		self.pad_to_8 = stream.read_ubytes(((8 - (self.count % 8)) % 8))
		self.floats = stream.read_floats((6))
		self.repeats.read(stream, Repeat, self.count, None)

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		if stream.version == 18:
			stream.write_ushorts(self.indices_0)
		if not (stream.version == 18):
			stream.write_uints(self.indices_0)
		if stream.version == 18:
			stream.write_ushorts(self.indices_1)
		if not (stream.version == 18):
			stream.write_uints(self.indices_1)
		if stream.version == 18:
			stream.write_ushorts(self.indices_2)
		if not (stream.version == 18):
			stream.write_uints(self.indices_2)
		stream.write_ubytes(self.p_indices_0)
		stream.write_ubytes(self.p_indices_1)
		stream.write_ubytes(self.p_indices_2)
		if stream.version == 18:
			stream.write_ubytes(self.c_indices_0)
			stream.write_ubytes(self.c_indices_1)
			stream.write_ubytes(self.c_indices_2)
		stream.write_ubytes(self.padding)
		stream.write_uint(self.frame_count)
		stream.write_uint(self.c)
		stream.write_uint(self.e)
		stream.write_uints(self.zeros_19)
		stream.write_ushort(self.count)
		stream.write_ushort(self.four_and_twenty)
		stream.write_ubytes(self.zeros)
		stream.write_ubytes(self.pad_to_8)
		stream.write_floats(self.floats)
		self.repeats.write(stream, Repeat, self.count, None)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'ManiBlock [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* indices_0 = {self.indices_0.__repr__()}'
		s += f'\n	* indices_1 = {self.indices_1.__repr__()}'
		s += f'\n	* indices_2 = {self.indices_2.__repr__()}'
		s += f'\n	* p_indices_0 = {self.p_indices_0.__repr__()}'
		s += f'\n	* p_indices_1 = {self.p_indices_1.__repr__()}'
		s += f'\n	* p_indices_2 = {self.p_indices_2.__repr__()}'
		s += f'\n	* c_indices_0 = {self.c_indices_0.__repr__()}'
		s += f'\n	* c_indices_1 = {self.c_indices_1.__repr__()}'
		s += f'\n	* c_indices_2 = {self.c_indices_2.__repr__()}'
		s += f'\n	* padding = {self.padding.__repr__()}'
		s += f'\n	* frame_count = {self.frame_count.__repr__()}'
		s += f'\n	* c = {self.c.__repr__()}'
		s += f'\n	* e = {self.e.__repr__()}'
		s += f'\n	* zeros_19 = {self.zeros_19.__repr__()}'
		s += f'\n	* count = {self.count.__repr__()}'
		s += f'\n	* four_and_twenty = {self.four_and_twenty.__repr__()}'
		s += f'\n	* zeros = {self.zeros.__repr__()}'
		s += f'\n	* pad_to_8 = {self.pad_to_8.__repr__()}'
		s += f'\n	* floats = {self.floats.__repr__()}'
		s += f'\n	* repeats = {self.repeats.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
