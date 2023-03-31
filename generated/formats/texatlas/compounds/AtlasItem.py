from generated.formats.base.basic import Float
from generated.formats.base.basic import Uint
from generated.formats.base.basic import Ushort
from generated.formats.base.basic import ZString
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class AtlasItem(MemStruct):

	__name__ = 'AtlasItem'

	_import_key = 'texatlas.compounds.AtlasItem'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.startx = 0.0
		self.starty = 0.0
		self.endx = 0.0
		self.endy = 0.0
		self.layer = 0
		self.flags_1 = 0
		self.flags_2 = 0
		self.atlas_name = Pointer(self.context, 0, ZString)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield ('atlas_name', Pointer, (0, ZString), (False, None), None)
		yield ('startx', Float, (0, None), (False, None), None)
		yield ('starty', Float, (0, None), (False, None), None)
		yield ('endx', Float, (0, None), (False, None), None)
		yield ('endy', Float, (0, None), (False, None), None)
		yield ('layer', Uint, (0, None), (False, None), None)
		yield ('flags_1', Ushort, (0, None), (False, None), None)
		yield ('flags_2', Ushort, (0, None), (False, None), None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'atlas_name', Pointer, (0, ZString), (False, None)
		yield 'startx', Float, (0, None), (False, None)
		yield 'starty', Float, (0, None), (False, None)
		yield 'endx', Float, (0, None), (False, None)
		yield 'endy', Float, (0, None), (False, None)
		yield 'layer', Uint, (0, None), (False, None)
		yield 'flags_1', Ushort, (0, None), (False, None)
		yield 'flags_2', Ushort, (0, None), (False, None)


AtlasItem.init_attributes()
