from generated.formats.base.basic import Uint64
from generated.formats.ovl_base.compounds.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class CurveRoot(MemStruct):

	__name__ = 'CurveRoot'

	_import_path = 'generated.formats.curve.compounds.CurveRoot'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.count = 0
		self.keys = ArrayPointer(self.context, self.count, CurveRoot._import_path_map["generated.formats.curve.compounds.Key"])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'keys', ArrayPointer, (instance.count, CurveRoot._import_path_map["generated.formats.curve.compounds.Key"]), (False, None)
		yield 'count', Uint64, (0, None), (False, None)
