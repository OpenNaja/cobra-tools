from generated.formats.base.basic import Float
from generated.formats.base.basic import Uint
from generated.formats.base.basic import ZString
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class AtlasItem(MemStruct):

	__name__ = 'AtlasItem'

	_import_key = 'texatlas.compounds.AtlasItem'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.float_1 = 0.0
		self.float_2 = 0.0
		self.float_3 = 0.0
		self.float_4 = 0.0
		self.unk_1 = 0
		self.unk_2 = 0
		self.atlas_name = Pointer(self.context, 0, ZString)
		if set_default:
			self.set_defaults()

	_attribute_list = MemStruct._attribute_list + [
		('atlas_name', Pointer, (0, ZString), (False, None), None),
		('float_1', Float, (0, None), (False, None), None),
		('float_2', Float, (0, None), (False, None), None),
		('float_3', Float, (0, None), (False, None), None),
		('float_4', Float, (0, None), (False, None), None),
		('unk_1', Uint, (0, None), (False, None), None),
		('unk_2', Uint, (0, None), (False, None), None),
		]

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'atlas_name', Pointer, (0, ZString), (False, None)
		yield 'float_1', Float, (0, None), (False, None)
		yield 'float_2', Float, (0, None), (False, None)
		yield 'float_3', Float, (0, None), (False, None)
		yield 'float_4', Float, (0, None), (False, None)
		yield 'unk_1', Uint, (0, None), (False, None)
		yield 'unk_2', Uint, (0, None), (False, None)
