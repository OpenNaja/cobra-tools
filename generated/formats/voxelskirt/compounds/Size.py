from generated.base_struct import BaseStruct
from generated.formats.base.basic import Uint64


class Size(BaseStruct):

	__name__ = 'Size'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# index into name list
		self.id = 0
		self.width_1 = 0
		self.height_1 = 0
		self.width_2 = 0
		self.height_2 = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.id = 0
		self.width_1 = 0
		self.height_1 = 0
		self.width_2 = 0
		self.height_2 = 0

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.id = Uint64.from_stream(stream, instance.context, 0, None)
		instance.width_1 = Uint64.from_stream(stream, instance.context, 0, None)
		instance.height_1 = Uint64.from_stream(stream, instance.context, 0, None)
		instance.width_2 = Uint64.from_stream(stream, instance.context, 0, None)
		instance.height_2 = Uint64.from_stream(stream, instance.context, 0, None)

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Uint64.to_stream(stream, instance.id)
		Uint64.to_stream(stream, instance.width_1)
		Uint64.to_stream(stream, instance.height_1)
		Uint64.to_stream(stream, instance.width_2)
		Uint64.to_stream(stream, instance.height_2)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'id', Uint64, (0, None), (False, None)
		yield 'width_1', Uint64, (0, None), (False, None)
		yield 'height_1', Uint64, (0, None), (False, None)
		yield 'width_2', Uint64, (0, None), (False, None)
		yield 'height_2', Uint64, (0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'Size [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* id = {self.fmt_member(self.id, indent+1)}'
		s += f'\n	* width_1 = {self.fmt_member(self.width_1, indent+1)}'
		s += f'\n	* height_1 = {self.fmt_member(self.height_1, indent+1)}'
		s += f'\n	* width_2 = {self.fmt_member(self.width_2, indent+1)}'
		s += f'\n	* height_2 = {self.fmt_member(self.height_2, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
