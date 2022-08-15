import numpy
from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.base.basic import Uint
from generated.formats.base.basic import ZString
from generated.formats.base.compounds.PadAlign import PadAlign


class Buffer1(BaseStruct):

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.bone_hashes = numpy.zeros((self.arg,), dtype=numpy.dtype('uint32'))
		self.bone_names = Array((self.arg,), ZString, self.context, 0, None)

		# ?
		self.bone_pad = PadAlign(self.context, 4, self.bone_names)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.bone_hashes = numpy.zeros((self.arg,), dtype=numpy.dtype('uint32'))
		self.bone_names = Array((self.arg,), ZString, self.context, 0, None)
		self.bone_pad = PadAlign(self.context, 4, self.bone_names)

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.bone_hashes = Array.from_stream(stream, instance.context, 0, None, (instance.arg,), Uint)
		instance.bone_names = Array.from_stream(stream, instance.context, 0, None, (instance.arg,), ZString)
		instance.bone_pad = PadAlign.from_stream(stream, instance.context, 4, instance.bone_names)

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Array.to_stream(stream, instance.bone_hashes, (instance.arg,), Uint, instance.context, 0, None)
		Array.to_stream(stream, instance.bone_names, (instance.arg,), ZString, instance.context, 0, None)
		PadAlign.to_stream(stream, instance.bone_pad)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'bone_hashes', Array, ((instance.arg,), Uint, 0, None), (False, None)
		yield 'bone_names', Array, ((instance.arg,), ZString, 0, None), (False, None)
		yield 'bone_pad', PadAlign, (4, instance.bone_names), (False, None)

	def get_info_str(self, indent=0):
		return f'Buffer1 [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* bone_hashes = {self.fmt_member(self.bone_hashes, indent+1)}'
		s += f'\n	* bone_names = {self.fmt_member(self.bone_names, indent+1)}'
		s += f'\n	* bone_pad = {self.fmt_member(self.bone_pad, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
