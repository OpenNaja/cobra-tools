from generated.formats.base.basic import Int
from generated.formats.base.basic import Uint
from generated.formats.base.basic import Uint64
from generated.formats.base.basic import ZString
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class CurveParam(MemStruct):

	__name__ = 'CurveParam'

	_import_key = 'renderparameters.compounds.CurveParam'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.dtype = 0

		# set to 1 if count > 1
		self.do_interpolation = 0
		self.count = 0
		self.attribute_name = Pointer(self.context, 0, ZString)
		self.curve_entries = Pointer(self.context, self.count, CurveParam._import_map["renderparameters.compounds.CurveList"])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'attribute_name', Pointer, (0, ZString), (False, None)
		yield 'dtype', Int, (0, None), (False, None)
		yield 'do_interpolation', Uint, (0, None), (False, None)
		yield 'curve_entries', Pointer, (instance.count, CurveParam._import_map["renderparameters.compounds.CurveList"]), (False, None)
		yield 'count', Uint64, (0, None), (False, None)
