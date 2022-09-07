from generated.base_struct import BaseStruct
from generated.formats.base.basic import Uint64
from generated.formats.voxelskirt.compounds.Empty import Empty


class Material(BaseStruct):

	__name__ = 'Material'

	_import_path = 'generated.formats.voxelskirt.compounds.Material'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# address of child data
		self.offset = 0

		# repeat count of child structs (4 floats)
		self.count = 0

		# index into name list
		self.id = 0
		self.data = Empty(self.context, 0, None)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.offset = 0
		self.count = 0
		self.id = 0
		self.data = Empty(self.context, 0, None)

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.offset = Uint64.from_stream(stream, instance.context, 0, None)
		instance.count = Uint64.from_stream(stream, instance.context, 0, None)
		instance.id = Uint64.from_stream(stream, instance.context, 0, None)
		instance.data = Empty.from_stream(stream, instance.context, 0, None)

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Uint64.to_stream(stream, instance.offset)
		Uint64.to_stream(stream, instance.count)
		Uint64.to_stream(stream, instance.id)
		Empty.to_stream(stream, instance.data)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'offset', Uint64, (0, None), (False, None)
		yield 'count', Uint64, (0, None), (False, None)
		yield 'id', Uint64, (0, None), (False, None)
		yield 'data', Empty, (0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'Material [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* offset = {self.fmt_member(self.offset, indent+1)}'
		s += f'\n	* count = {self.fmt_member(self.count, indent+1)}'
		s += f'\n	* id = {self.fmt_member(self.id, indent+1)}'
		s += f'\n	* data = {self.fmt_member(self.data, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
