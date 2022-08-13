import numpy
from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.base.basic import Float
from generated.formats.base.basic import Uint
from generated.formats.ms2.compound.Vector3 import Vector3


class ListCEntry(BaseStruct):

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# 1 for carch and nasuto
		self.one = 0

		# center of the collider
		self.loc = 0

		# -1 for PZ, 80 for JWE
		self.constant = 0

		# ?
		self.a = 0

		# ?
		self.floats = 0

		# sometimes repeat of a
		self.a_2 = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		print(f'set_defaults {self.__class__.__name__}')
		self.one = 0
		self.loc = Vector3(self.context, 0, None)
		self.constant = 0.0
		self.a = 0.0
		self.floats = numpy.zeros((4,), dtype=numpy.dtype('float32'))
		self.a_2 = 0.0

	def read(self, stream):
		self.io_start = stream.tell()
		self.read_fields(stream, self)
		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()
		self.write_fields(stream, self)
		self.io_size = stream.tell() - self.io_start

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.one = stream.read_uint()
		instance.loc = Vector3.from_stream(stream, instance.context, 0, None)
		instance.constant = stream.read_float()
		instance.a = stream.read_float()
		instance.floats = stream.read_floats((4,))
		instance.a_2 = stream.read_float()

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		stream.write_uint(instance.one)
		Vector3.to_stream(stream, instance.loc)
		stream.write_float(instance.constant)
		stream.write_float(instance.a)
		stream.write_floats(instance.floats)
		stream.write_float(instance.a_2)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		super()._get_filtered_attribute_list(instance)
		yield ('one', Uint, (0, None))
		yield ('loc', Vector3, (0, None))
		yield ('constant', Float, (0, None))
		yield ('a', Float, (0, None))
		yield ('floats', Array, ((4,), Float, 0, None))
		yield ('a_2', Float, (0, None))

	def get_info_str(self, indent=0):
		return f'ListCEntry [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* one = {self.fmt_member(self.one, indent+1)}'
		s += f'\n	* loc = {self.fmt_member(self.loc, indent+1)}'
		s += f'\n	* constant = {self.fmt_member(self.constant, indent+1)}'
		s += f'\n	* a = {self.fmt_member(self.a, indent+1)}'
		s += f'\n	* floats = {self.fmt_member(self.floats, indent+1)}'
		s += f'\n	* a_2 = {self.fmt_member(self.a_2, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
