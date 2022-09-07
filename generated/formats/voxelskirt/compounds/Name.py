from generated.base_struct import BaseStruct
from generated.formats.base.basic import Uint64


class Name(BaseStruct):

	__name__ = 'Name'

	_import_path = 'generated.formats.voxelskirt.compounds.Name'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# address of this data layer
		self.offset = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.offset = 0

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.offset = Uint64.from_stream(stream, instance.context, 0, None)

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Uint64.to_stream(stream, instance.offset)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'offset', Uint64, (0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'Name [Size: {self.io_size}, Address: {self.io_start}] {self.name}'
