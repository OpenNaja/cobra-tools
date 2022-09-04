import numpy
from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.base.basic import Byte
from generated.formats.base.basic import Uint


class TypeOther(BaseStruct):

	"""
	generic
	"""

	__name__ = 'TypeOther'

	_import_path = 'generated.formats.bnk.compounds.TypeOther'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# length of this section
		self.length = 0

		# id of this Sound SFX object
		self.raw = Array(self.context, 0, None, (0,), Byte)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.length = 0
		self.raw = numpy.zeros((self.length,), dtype=numpy.dtype('int8'))

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.length = Uint.from_stream(stream, instance.context, 0, None)
		instance.raw = Array.from_stream(stream, instance.context, 0, None, (instance.length,), Byte)

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Uint.to_stream(stream, instance.length)
		Array.to_stream(stream, instance.raw, instance.context, 0, None, (instance.length,), Byte)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'length', Uint, (0, None), (False, None)
		yield 'raw', Array, (0, None, (instance.length,), Byte), (False, None)

	def get_info_str(self, indent=0):
		return f'TypeOther [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* length = {self.fmt_member(self.length, indent+1)}'
		s += f'\n	* raw = {self.fmt_member(self.raw, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
