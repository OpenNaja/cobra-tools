from generated.formats.base.basic import Float
from generated.formats.base.basic import Short
from generated.formats.motiongraph.enums.SubCurveType import SubCurveType
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class CurveDataPoint(MemStruct):

	"""
	12 bytes
	"""

	__name__ = 'CurveDataPoint'

	_import_path = 'generated.formats.motiongraph.compounds.CurveDataPoint'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.x = 0.0
		self.y = 0
		self.sub_curve_type = SubCurveType(self.context, 0, None)
		self.subsequent_curve_param = 0
		self.subsequent_curve_param_b = 0
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'x', Float, (0, None), (False, None)
		yield 'y', Short, (0, None), (False, None)
		yield 'sub_curve_type', SubCurveType, (0, None), (False, None)
		yield 'subsequent_curve_param', Short, (0, None), (False, None)
		yield 'subsequent_curve_param_b', Short, (0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'CurveDataPoint [Size: {self.io_size}, Address: {self.io_start}] {self.name}'
