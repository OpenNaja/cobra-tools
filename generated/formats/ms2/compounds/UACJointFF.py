import numpy
from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.base.basic import Int
from generated.formats.base.basic import Uint


class UACJointFF(BaseStruct):

	__name__ = 'UACJointFF'

	_import_path = 'generated.formats.ms2.compounds.UACJointFF'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# must be 11
		self.eleven = 0

		# bunch of -1's, and constants
		self.f_fs = Array(self.context, 0, None, (0,), Int)
		self.name_offset = 0
		self.hitcheck_count = 0

		# 12 bytes of zeros
		self.zeros = Array(self.context, 0, None, (0,), Uint)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.eleven = 0
		self.f_fs = numpy.zeros((4,), dtype=numpy.dtype('int32'))
		self.name_offset = 0
		self.hitcheck_count = 0
		self.zeros = numpy.zeros((3,), dtype=numpy.dtype('uint32'))

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.eleven = Uint.from_stream(stream, instance.context, 0, None)
		instance.f_fs = Array.from_stream(stream, instance.context, 0, None, (4,), Int)
		instance.name_offset = Uint.from_stream(stream, instance.context, 0, None)
		instance.hitcheck_count = Uint.from_stream(stream, instance.context, 0, None)
		instance.zeros = Array.from_stream(stream, instance.context, 0, None, (3,), Uint)

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Uint.to_stream(stream, instance.eleven)
		Array.to_stream(stream, instance.f_fs, instance.context, 0, None, (4,), Int)
		Uint.to_stream(stream, instance.name_offset)
		Uint.to_stream(stream, instance.hitcheck_count)
		Array.to_stream(stream, instance.zeros, instance.context, 0, None, (3,), Uint)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'eleven', Uint, (0, None), (False, None)
		yield 'f_fs', Array, (0, None, (4,), Int), (False, None)
		yield 'name_offset', Uint, (0, None), (False, None)
		yield 'hitcheck_count', Uint, (0, None), (False, None)
		yield 'zeros', Array, (0, None, (3,), Uint), (False, None)

	def get_info_str(self, indent=0):
		return f'UACJointFF [Size: {self.io_size}, Address: {self.io_start}] {self.name}'
