import numpy
from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.base.basic import Float
from generated.formats.base.basic import Uint
from generated.formats.ms2.compounds.Vector3 import Vector3


class ListCEntry(BaseStruct):

	__name__ = ListCEntry

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# 1 for carch and nasuto
		self.one = 0

		# center of the collider
		self.loc = Vector3(self.context, 0, None)

		# -1 for PZ, 80 for JWE
		self.constant = 0.0

		# ?
		self.a = 0.0

		# ?
		self.floats = Array((0,), Float, self.context, 0, None)

		# sometimes repeat of a
		self.a_2 = 0.0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.one = 0
		self.loc = Vector3(self.context, 0, None)
		self.constant = 0.0
		self.a = 0.0
		self.floats = numpy.zeros((4,), dtype=numpy.dtype('float32'))
		self.a_2 = 0.0

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.one = Uint.from_stream(stream, instance.context, 0, None)
		instance.loc = Vector3.from_stream(stream, instance.context, 0, None)
		instance.constant = Float.from_stream(stream, instance.context, 0, None)
		instance.a = Float.from_stream(stream, instance.context, 0, None)
		instance.floats = Array.from_stream(stream, instance.context, 0, None, (4,), Float)
		instance.a_2 = Float.from_stream(stream, instance.context, 0, None)

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Uint.to_stream(stream, instance.one)
		Vector3.to_stream(stream, instance.loc)
		Float.to_stream(stream, instance.constant)
		Float.to_stream(stream, instance.a)
		Array.to_stream(stream, instance.floats, (4,), Float, instance.context, 0, None)
		Float.to_stream(stream, instance.a_2)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'one', Uint, (0, None), (False, None)
		yield 'loc', Vector3, (0, None), (False, None)
		yield 'constant', Float, (0, None), (False, None)
		yield 'a', Float, (0, None), (False, None)
		yield 'floats', Array, ((4,), Float, 0, None), (False, None)
		yield 'a_2', Float, (0, None), (False, None)

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
