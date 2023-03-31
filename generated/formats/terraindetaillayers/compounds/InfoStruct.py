from generated.formats.base.basic import Float
from generated.formats.base.basic import Uint
from generated.formats.ovl_base.compounds.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class InfoStruct(MemStruct):

	__name__ = 'InfoStruct'

	_import_key = 'terraindetaillayers.compounds.InfoStruct'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.brush_count = 0
		self.brush_flags = 0
		self.scale = 0.0
		self.unk_1 = 0.0
		self.brush_list = ArrayPointer(self.context, self.brush_count, InfoStruct._import_map["terraindetaillayers.compounds.BrushitemStruct"])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield ('brush_list', ArrayPointer, (None, InfoStruct._import_map["terraindetaillayers.compounds.BrushitemStruct"]), (False, None), (None, None))
		yield ('brush_count', Uint, (0, None), (False, None), (None, None))
		yield ('brush_flags', Uint, (0, None), (False, None), (None, None))
		yield ('scale', Float, (0, None), (False, None), (None, None))
		yield ('unk_1', Float, (0, None), (False, None), (None, None))

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'brush_list', ArrayPointer, (instance.brush_count, InfoStruct._import_map["terraindetaillayers.compounds.BrushitemStruct"]), (False, None)
		yield 'brush_count', Uint, (0, None), (False, None)
		yield 'brush_flags', Uint, (0, None), (False, None)
		yield 'scale', Float, (0, None), (False, None)
		yield 'unk_1', Float, (0, None), (False, None)


InfoStruct.init_attributes()
