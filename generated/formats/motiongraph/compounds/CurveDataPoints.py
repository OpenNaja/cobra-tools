from generated.array import Array
from generated.formats.motiongraph.compounds.CurveDataPoint import CurveDataPoint
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class CurveDataPoints(MemStruct):

	"""
	array
	"""

	__name__ = 'CurveDataPoints'

	_import_path = 'generated.formats.motiongraph.compounds.CurveDataPoints'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.data = Array(self.context, 0, None, (0,), CurveDataPoint)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.data = Array(self.context, 0, None, (self.arg,), CurveDataPoint)

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.data = Array.from_stream(stream, instance.context, 0, None, (instance.arg,), CurveDataPoint)

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Array.to_stream(stream, instance.data, instance.context, 0, None, (instance.arg,), CurveDataPoint)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'data', Array, (0, None, (instance.arg,), CurveDataPoint), (False, None)

	def get_info_str(self, indent=0):
		return f'CurveDataPoints [Size: {self.io_size}, Address: {self.io_start}] {self.name}'
