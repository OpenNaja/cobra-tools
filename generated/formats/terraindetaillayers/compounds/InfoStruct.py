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

	_attribute_list = MemStruct._attribute_list + [
		('brush_list', ArrayPointer, (None, None), (False, None), None),
		('brush_count', Uint, (0, None), (False, None), None),
		('brush_flags', Uint, (0, None), (False, None), None),
		('scale', Float, (0, None), (False, None), None),
		('unk_1', Float, (0, None), (False, None), None),
		]

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'brush_list', ArrayPointer, (instance.brush_count, InfoStruct._import_map["terraindetaillayers.compounds.BrushitemStruct"]), (False, None)
		yield 'brush_count', Uint, (0, None), (False, None)
		yield 'brush_flags', Uint, (0, None), (False, None)
		yield 'scale', Float, (0, None), (False, None)
		yield 'unk_1', Float, (0, None), (False, None)
