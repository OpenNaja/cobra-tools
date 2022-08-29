import numpy
from generated.array import Array
from generated.formats.base.basic import Float
from generated.formats.ovl_base.compounds.GenericHeader import GenericHeader
from generated.formats.wsm.compounds.WsmHeader import WsmHeader


class Wsm(GenericHeader):

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.header = WsmHeader(self.context, 0, None)

		# xyz
		self.locs = Array((0,), Float, self.context, 0, None)

		# xyzw
		self.quats = Array((0,), Float, self.context, 0, None)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.header = WsmHeader(self.context, 0, None)
		self.locs = numpy.zeros((self.header.frame_count, 3,), dtype=numpy.dtype('float32'))
		self.quats = numpy.zeros((self.header.frame_count, 4,), dtype=numpy.dtype('float32'))

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.header = WsmHeader.from_stream(stream, instance.context, 0, None)
		instance.locs = Array.from_stream(stream, instance.context, 0, None, (instance.header.frame_count, 3,), Float)
		instance.quats = Array.from_stream(stream, instance.context, 0, None, (instance.header.frame_count, 4,), Float)

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		WsmHeader.to_stream(stream, instance.header)
		Array.to_stream(stream, instance.locs, (instance.header.frame_count, 3,), Float, instance.context, 0, None)
		Array.to_stream(stream, instance.quats, (instance.header.frame_count, 4,), Float, instance.context, 0, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'header', WsmHeader, (0, None), (False, None)
		yield 'locs', Array, ((instance.header.frame_count, 3,), Float, 0, None), (False, None)
		yield 'quats', Array, ((instance.header.frame_count, 4,), Float, 0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'Wsm [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* header = {self.fmt_member(self.header, indent+1)}'
		s += f'\n	* locs = {self.fmt_member(self.locs, indent+1)}'
		s += f'\n	* quats = {self.fmt_member(self.quats, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
