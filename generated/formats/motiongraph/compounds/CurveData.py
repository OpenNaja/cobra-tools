from generated.formats.base.basic import Uint64
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class CurveData(MemStruct):

	"""
	16 bytes
	"""

	__name__ = 'CurveData'

	_import_path = 'generated.formats.motiongraph.compounds.CurveData'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.count = 0
		self.points = Pointer(self.context, self.count, CurveData._import_path_map["generated.formats.motiongraph.compounds.CurveDataPoints"])
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.count = 0
		self.points = Pointer(self.context, self.count, CurveData._import_path_map["generated.formats.motiongraph.compounds.CurveDataPoints"])

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.count = Uint64.from_stream(stream, instance.context, 0, None)
		instance.points = Pointer.from_stream(stream, instance.context, instance.count, CurveData._import_path_map["generated.formats.motiongraph.compounds.CurveDataPoints"])
		if not isinstance(instance.points, int):
			instance.points.arg = instance.count

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Uint64.to_stream(stream, instance.count)
		Pointer.to_stream(stream, instance.points)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'count', Uint64, (0, None), (False, None)
		yield 'points', Pointer, (instance.count, CurveData._import_path_map["generated.formats.motiongraph.compounds.CurveDataPoints"]), (False, None)

	def get_info_str(self, indent=0):
		return f'CurveData [Size: {self.io_size}, Address: {self.io_start}] {self.name}'
