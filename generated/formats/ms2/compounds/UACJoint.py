import numpy
from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.base.basic import Float
from generated.formats.base.basic import Ushort


class UACJoint(BaseStruct):

	"""
	36 bytes
	"""

	__name__ = 'UACJoint'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# variable
		self.unk = Array((0,), Ushort, self.context, 0, None)

		# some at least
		self.floats = Array((0,), Float, self.context, 0, None)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.unk = numpy.zeros((6,), dtype=numpy.dtype('uint16'))
		self.floats = numpy.zeros((6,), dtype=numpy.dtype('float32'))

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.unk = Array.from_stream(stream, instance.context, 0, None, (6,), Ushort)
		instance.floats = Array.from_stream(stream, instance.context, 0, None, (6,), Float)

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Array.to_stream(stream, instance.unk, (6,), Ushort, instance.context, 0, None)
		Array.to_stream(stream, instance.floats, (6,), Float, instance.context, 0, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'unk', Array, ((6,), Ushort, 0, None), (False, None)
		yield 'floats', Array, ((6,), Float, 0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'UACJoint [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* unk = {self.fmt_member(self.unk, indent+1)}'
		s += f'\n	* floats = {self.fmt_member(self.floats, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
