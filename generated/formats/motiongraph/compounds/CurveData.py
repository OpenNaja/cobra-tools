from generated.formats.base.basic import Uint64
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class CurveData(MemStruct):

	"""
	16 bytes
	"""

	__name__ = 'CurveData'

	_import_key = 'motiongraph.compounds.CurveData'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.count = 0
		self.points = Pointer(self.context, self.count, CurveData._import_map["motiongraph.compounds.CurveDataPoints"])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield ('count', Uint64, (0, None), (False, None), (None, None))
		yield ('points', Pointer, (None, CurveData._import_map["motiongraph.compounds.CurveDataPoints"]), (False, None), (None, None))

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'count', Uint64, (0, None), (False, None)
		yield 'points', Pointer, (instance.count, CurveData._import_map["motiongraph.compounds.CurveDataPoints"]), (False, None)


CurveData.init_attributes()
