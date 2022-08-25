from generated.formats.base.basic import Float
from generated.formats.base.basic import Short
from generated.formats.motiongraph.enums.SubCurveType import SubCurveType
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class CurveDataPoint(MemStruct):

	"""
	12 bytes
	"""

	__name__ = CurveDataPoint

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.x = 0.0
		self.y = 0
		self.sub_curve_type = SubCurveType(self.context, 0, None)
		self.subsequent_curve_param = 0
		self.subsequent_curve_param_b = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.x = 0.0
		self.y = 0
		self.sub_curve_type = SubCurveType(self.context, 0, None)
		self.subsequent_curve_param = 0
		self.subsequent_curve_param_b = 0

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.x = Float.from_stream(stream, instance.context, 0, None)
		instance.y = Short.from_stream(stream, instance.context, 0, None)
		instance.sub_curve_type = SubCurveType.from_stream(stream, instance.context, 0, None)
		instance.subsequent_curve_param = Short.from_stream(stream, instance.context, 0, None)
		instance.subsequent_curve_param_b = Short.from_stream(stream, instance.context, 0, None)

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Float.to_stream(stream, instance.x)
		Short.to_stream(stream, instance.y)
		SubCurveType.to_stream(stream, instance.sub_curve_type)
		Short.to_stream(stream, instance.subsequent_curve_param)
		Short.to_stream(stream, instance.subsequent_curve_param_b)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'x', Float, (0, None), (False, None)
		yield 'y', Short, (0, None), (False, None)
		yield 'sub_curve_type', SubCurveType, (0, None), (False, None)
		yield 'subsequent_curve_param', Short, (0, None), (False, None)
		yield 'subsequent_curve_param_b', Short, (0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'CurveDataPoint [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* x = {self.fmt_member(self.x, indent+1)}'
		s += f'\n	* y = {self.fmt_member(self.y, indent+1)}'
		s += f'\n	* sub_curve_type = {self.fmt_member(self.sub_curve_type, indent+1)}'
		s += f'\n	* subsequent_curve_param = {self.fmt_member(self.subsequent_curve_param, indent+1)}'
		s += f'\n	* subsequent_curve_param_b = {self.fmt_member(self.subsequent_curve_param_b, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
