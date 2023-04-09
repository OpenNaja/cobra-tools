from generated.formats.base.basic import ZString
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class BrushitemStruct(MemStruct):

	__name__ = 'brushitemStruct'

	_import_key = 'terrainindexeddetaillayers.compounds.BrushitemStruct'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.layer_name = Pointer(self.context, 0, ZString)
		self.brush_name = Pointer(self.context, 0, ZString)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield ('layer_name', Pointer, (0, ZString), (False, None), (None, None))
		yield ('brush_name', Pointer, (0, ZString), (False, None), (None, None))

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'layer_name', Pointer, (0, ZString), (False, None)
		yield 'brush_name', Pointer, (0, ZString), (False, None)
