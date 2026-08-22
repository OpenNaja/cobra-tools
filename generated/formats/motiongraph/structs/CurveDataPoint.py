from generated.formats.motiongraph.imports import name_type_map
from generated.formats.ovl_base.structs.MemStruct import MemStruct


class CurveDataPoint(MemStruct):

	"""
	12 bytes
	
	y, SubsequentCurveParam and SubsequentCurveParamB are stored as 16 bits
	but are NOT integers. Each holds float32(value + 2.0) truncated to its
	top 16 bits, i.e. a bfloat16 with a +2 bias:
	
	value = bf16(raw) - 2.0
	raw   = top16(float32(value + 2.0))
	
	The bias pins the exponent so the 7-bit mantissa acts as fixed point:
	step 1/64 for value >= 0 (biased into [2,4)), and 1/128 for value < 0
	(biased into [1,2)). Verified on the stock JWE3 Acrocanthosaurus graph:
	all 6,240 y values are exact multiples of 1/64 with range 0..30, the two
	most common being 0.0 and 1.0 as expected for boolean signals; the two
	curve params follow the same rule and reach -1.6.
	
	x is normalised time, observed 0.0..4.0.
	"""

	__name__ = 'CurveDataPoint'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.x = name_type_map['Float'](self.context, 0, None)
		self.y = name_type_map['Short'](self.context, 0, None)
		self.sub_curve_type = name_type_map['SubCurveType'](self.context, 0, None)
		self.subsequent_curve_param = name_type_map['Short'](self.context, 0, None)
		self.subsequent_curve_param_b = name_type_map['Short'](self.context, 0, None)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'x', name_type_map['Float'], (0, None), (False, None), (None, None)
		yield 'y', name_type_map['Short'], (0, None), (False, None), (None, None)
		yield 'sub_curve_type', name_type_map['SubCurveType'], (0, None), (False, None), (None, None)
		yield 'subsequent_curve_param', name_type_map['Short'], (0, None), (False, None), (None, None)
		yield 'subsequent_curve_param_b', name_type_map['Short'], (0, None), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'x', name_type_map['Float'], (0, None), (False, None)
		yield 'y', name_type_map['Short'], (0, None), (False, None)
		yield 'sub_curve_type', name_type_map['SubCurveType'], (0, None), (False, None)
		yield 'subsequent_curve_param', name_type_map['Short'], (0, None), (False, None)
		yield 'subsequent_curve_param_b', name_type_map['Short'], (0, None), (False, None)
