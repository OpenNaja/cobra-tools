import numpy
from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.base.basic import Byte


class NodeBaseParams(BaseStruct):

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.raw = numpy.zeros((30,), dtype=numpy.dtype('int8'))
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.raw = numpy.zeros((30,), dtype=numpy.dtype('int8'))

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.raw = Array.from_stream(stream, instance.context, 0, None, (30,), Byte)

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		stream.write_bytes(instance.raw)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'raw', Array, ((30,), Byte, 0, None)

	def get_info_str(self, indent=0):
		return f'NodeBaseParams [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* raw = {self.fmt_member(self.raw, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
