import numpy
from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.base.basic import Ubyte
from generated.formats.base.basic import Uint


class BKHDSection(BaseStruct):

	"""
	First Section of a soundbank aux
	"""

	__name__ = BKHDSection

	def set_defaults(self):
		super().set_defaults()
		self.length = 0
		self.version = 0
		self.id_a = 0
		self.id_b = 0
		self.constant_a = 0
		self.constant_b = 0
		self.unk = 0
		self.zeroes = numpy.zeros((self.length - 24,), dtype=numpy.dtype('uint8'))

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.length = Uint.from_stream(stream, instance.context, 0, None)
		instance.version = Uint.from_stream(stream, instance.context, 0, None)
		instance.context.version = instance.version
		instance.id_a = Uint.from_stream(stream, instance.context, 0, None)
		instance.id_b = Uint.from_stream(stream, instance.context, 0, None)
		instance.constant_a = Uint.from_stream(stream, instance.context, 0, None)
		instance.constant_b = Uint.from_stream(stream, instance.context, 0, None)
		instance.unk = Uint.from_stream(stream, instance.context, 0, None)
		instance.zeroes = Array.from_stream(stream, instance.context, 0, None, (instance.length - 24,), Ubyte)

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Uint.to_stream(stream, instance.length)
		Uint.to_stream(stream, instance.version)
		Uint.to_stream(stream, instance.id_a)
		Uint.to_stream(stream, instance.id_b)
		Uint.to_stream(stream, instance.constant_a)
		Uint.to_stream(stream, instance.constant_b)
		Uint.to_stream(stream, instance.unk)
		Array.to_stream(stream, instance.zeroes, (instance.length - 24,), Ubyte, instance.context, 0, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'length', Uint, (0, None), (False, None)
		yield 'version', Uint, (0, None), (False, None)
		yield 'id_a', Uint, (0, None), (False, None)
		yield 'id_b', Uint, (0, None), (False, None)
		yield 'constant_a', Uint, (0, None), (False, None)
		yield 'constant_b', Uint, (0, None), (False, None)
		yield 'unk', Uint, (0, None), (False, None)
		yield 'zeroes', Array, ((instance.length - 24,), Ubyte, 0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'BKHDSection [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* length = {self.fmt_member(self.length, indent+1)}'
		s += f'\n	* version = {self.fmt_member(self.version, indent+1)}'
		s += f'\n	* id_a = {self.fmt_member(self.id_a, indent+1)}'
		s += f'\n	* id_b = {self.fmt_member(self.id_b, indent+1)}'
		s += f'\n	* constant_a = {self.fmt_member(self.constant_a, indent+1)}'
		s += f'\n	* constant_b = {self.fmt_member(self.constant_b, indent+1)}'
		s += f'\n	* unk = {self.fmt_member(self.unk, indent+1)}'
		s += f'\n	* zeroes = {self.fmt_member(self.zeroes, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# length of following data
		self.length = 0
		self.version = 0
		self.id_a = 0
		self.id_b = 0
		self.constant_a = 0
		self.constant_b = 0
		self.unk = 0

		# sometimes present
		# self.zeroes = numpy.zeros((self.length - 24,), dtype=numpy.dtype('uint8'))


