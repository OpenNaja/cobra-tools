from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.base.basic import Uint64


class DataSlot(BaseStruct):

	"""
	offset into buffer to start of sth; only given if some count is nonzero
	"""

	__name__ = 'DataSlot'

	_import_path = 'generated.formats.voxelskirt.compounds.DataSlot'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# offset into buffer to start
		self.offset = 0

		# also counts the stuff after names
		self.count = 0
		self.data = Array(self.context, 0, None, (0,), self.template)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.offset = 0
		self.count = 0
		self.data = Array(self.context, 0, None, (0,), self.template)

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.offset = Uint64.from_stream(stream, instance.context, 0, None)
		instance.count = Uint64.from_stream(stream, instance.context, 0, None)
		instance.data = Array.from_stream(stream, instance.context, 0, None, (0,), instance.template)

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Uint64.to_stream(stream, instance.offset)
		Uint64.to_stream(stream, instance.count)
		Array.to_stream(stream, instance.data, instance.template)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'offset', Uint64, (0, None), (False, None)
		yield 'count', Uint64, (0, None), (False, None)
		yield 'data', Array, (0, None, (0,), instance.template), (False, None)

	def get_info_str(self, indent=0):
		return f'DataSlot [Size: {self.io_size}, Address: {self.io_start}] {self.name}'
