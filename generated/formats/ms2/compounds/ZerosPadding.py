from generated.base_struct import BaseStruct
from generated.formats.base.basic import Uint64


class ZerosPadding(BaseStruct):

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.hier_2_padding_0 = 0

		# 128 still has 16 bytes
		self.hier_2_padding_1 = 0

		# 129 is the first with 24 bytes
		self.hier_2_padding_2 = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.hier_2_padding_0 = 0
		if 64 < self.arg:
			self.hier_2_padding_1 = 0
		if 128 < self.arg:
			self.hier_2_padding_2 = 0

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.hier_2_padding_0 = Uint64.from_stream(stream, instance.context, 0, None)
		if 64 < instance.arg:
			instance.hier_2_padding_1 = Uint64.from_stream(stream, instance.context, 0, None)
		if 128 < instance.arg:
			instance.hier_2_padding_2 = Uint64.from_stream(stream, instance.context, 0, None)

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		stream.write_uint64(instance.hier_2_padding_0)
		if 64 < instance.arg:
			stream.write_uint64(instance.hier_2_padding_1)
		if 128 < instance.arg:
			stream.write_uint64(instance.hier_2_padding_2)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'hier_2_padding_0', Uint64, (0, None)
		if 64 < instance.arg:
			yield 'hier_2_padding_1', Uint64, (0, None)
		if 128 < instance.arg:
			yield 'hier_2_padding_2', Uint64, (0, None)

	def get_info_str(self, indent=0):
		return f'ZerosPadding [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* hier_2_padding_0 = {self.fmt_member(self.hier_2_padding_0, indent+1)}'
		s += f'\n	* hier_2_padding_1 = {self.fmt_member(self.hier_2_padding_1, indent+1)}'
		s += f'\n	* hier_2_padding_2 = {self.fmt_member(self.hier_2_padding_2, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
