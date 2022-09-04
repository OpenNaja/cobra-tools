from generated.array import Array
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.path.compounds.Vector3 import Vector3


class PointsList(MemStruct):

	__name__ = 'PointsList'

	_import_path = 'generated.formats.path.compounds.PointsList'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.points = Array(self.context, 0, None, (0,), Vector3)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.points = Array(self.context, 0, None, (self.arg,), Vector3)

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.points = Array.from_stream(stream, instance.context, 0, None, (instance.arg,), Vector3)

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Array.to_stream(stream, instance.points, instance.context, 0, None, (instance.arg,), Vector3)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'points', Array, (0, None, (instance.arg,), Vector3), (False, None)

	def get_info_str(self, indent=0):
		return f'PointsList [Size: {self.io_size}, Address: {self.io_start}] {self.name}'
