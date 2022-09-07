import numpy
from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.base.basic import Uint
from generated.formats.base.basic import ZString
from generated.formats.base.compounds.PadAlign import PadAlign


class Buffer1(BaseStruct):

	__name__ = 'Buffer1'

	_import_path = 'generated.formats.manis.compounds.Buffer1'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.bone_hashes = Array(self.context, 0, None, (0,), Uint)
		self.bone_names = Array(self.context, 0, None, (0,), ZString)

		# ?
		self.bone_pad = PadAlign(self.context, 4, self.bone_names)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.bone_hashes = numpy.zeros((self.arg,), dtype=numpy.dtype('uint32'))
		self.bone_names = Array(self.context, 0, None, (self.arg,), ZString)
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
		Array.to_stream(stream, instance.bone_hashes, Uint)
		Array.to_stream(stream, instance.bone_names, ZString)
		PadAlign.to_stream(stream, instance.bone_pad)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'bone_hashes', Array, (0, None, (instance.arg,), Uint), (False, None)
		yield 'bone_names', Array, (0, None, (instance.arg,), ZString), (False, None)
		yield 'bone_pad', PadAlign, (4, instance.bone_names), (False, None)

	def get_info_str(self, indent=0):
		return f'Buffer1 [Size: {self.io_size}, Address: {self.io_start}] {self.name}'
