import numpy
import typing
from generated.array import Array


class ManiBlock:

	def __init__(self, arg=None, template=None):
		self.name = ''
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.indices_c_2 = numpy.zeros((), dtype='ushort')
		self.indices_c_2 = numpy.zeros((), dtype='uint')
		self.indices_0 = numpy.zeros((), dtype='ushort')
		self.indices_0 = numpy.zeros((), dtype='uint')
		self.indices_1 = numpy.zeros((), dtype='ushort')
		self.indices_1 = numpy.zeros((), dtype='uint')
		self.indices_e_2 = numpy.zeros((), dtype='ushort')
		self.indices_e_2 = numpy.zeros((), dtype='uint')
		self.p_indices_00 = numpy.zeros((), dtype='ubyte')
		self.p_indices_00 = numpy.zeros((), dtype='ubyte')
		self.p_indices_0 = numpy.zeros((), dtype='ubyte')
		self.p_indices_0 = numpy.zeros((), dtype='ubyte')
		self.p_indices_1 = numpy.zeros((), dtype='ubyte')
		self.p_indices_1 = numpy.zeros((), dtype='ubyte')
		self.p_indices_2 = numpy.zeros((), dtype='ubyte')
		self.p_indices_2 = numpy.zeros((), dtype='ubyte')

	def read(self, stream):

		self.io_start = stream.tell()
		if stream.version == 18:
			self.indices_c_2 = stream.read_ushorts((self.arg.c_2))
		if not (stream.version == 18):
			self.indices_c_2 = stream.read_uints((self.arg.c_2))
		if stream.version == 18:
			self.indices_0 = stream.read_ushorts((self.arg.c))
		if not (stream.version == 18):
			self.indices_0 = stream.read_uints((self.arg.c))
		if stream.version == 18:
			self.indices_1 = stream.read_ushorts((self.arg.name_count))
		if not (stream.version == 18):
			self.indices_1 = stream.read_uints((self.arg.name_count))
		if stream.version == 18:
			self.indices_e_2 = stream.read_ushorts((self.arg.e_2))
		if not (stream.version == 18):
			self.indices_e_2 = stream.read_uints((self.arg.e_2))
		self.p_indices_00 = stream.read_ubytes((self.arg.c_2))
		if stream.version == 18:
			self.p_indices_00 = stream.read_ubytes((self.arg.c_2))
		self.p_indices_0 = stream.read_ubytes((self.arg.c))
		if stream.version == 18:
			self.p_indices_0 = stream.read_ubytes((self.arg.c))
		self.p_indices_1 = stream.read_ubytes((self.arg.name_count))
		if stream.version == 18:
			self.p_indices_1 = stream.read_ubytes((self.arg.name_count))
		self.p_indices_2 = stream.read_ubytes((self.arg.e))
		if stream.version == 18:
			self.p_indices_2 = stream.read_ubytes((self.arg.e))

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		if stream.version == 18:
			stream.write_ushorts(self.indices_c_2)
		if not (stream.version == 18):
			stream.write_uints(self.indices_c_2)
		if stream.version == 18:
			stream.write_ushorts(self.indices_0)
		if not (stream.version == 18):
			stream.write_uints(self.indices_0)
		if stream.version == 18:
			stream.write_ushorts(self.indices_1)
		if not (stream.version == 18):
			stream.write_uints(self.indices_1)
		if stream.version == 18:
			stream.write_ushorts(self.indices_e_2)
		if not (stream.version == 18):
			stream.write_uints(self.indices_e_2)
		stream.write_ubytes(self.p_indices_00)
		if stream.version == 18:
			stream.write_ubytes(self.p_indices_00)
		stream.write_ubytes(self.p_indices_0)
		if stream.version == 18:
			stream.write_ubytes(self.p_indices_0)
		stream.write_ubytes(self.p_indices_1)
		if stream.version == 18:
			stream.write_ubytes(self.p_indices_1)
		stream.write_ubytes(self.p_indices_2)
		if stream.version == 18:
			stream.write_ubytes(self.p_indices_2)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'ManiBlock [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* indices_c_2 = {self.indices_c_2.__repr__()}'
		s += f'\n	* indices_0 = {self.indices_0.__repr__()}'
		s += f'\n	* indices_1 = {self.indices_1.__repr__()}'
		s += f'\n	* indices_e_2 = {self.indices_e_2.__repr__()}'
		s += f'\n	* p_indices_00 = {self.p_indices_00.__repr__()}'
		s += f'\n	* p_indices_0 = {self.p_indices_0.__repr__()}'
		s += f'\n	* p_indices_1 = {self.p_indices_1.__repr__()}'
		s += f'\n	* p_indices_2 = {self.p_indices_2.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
