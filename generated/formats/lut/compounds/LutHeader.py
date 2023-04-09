from generated.formats.base.basic import Uint
from generated.formats.base.basic import Ushort
from generated.formats.ovl_base.compounds.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class LutHeader(MemStruct):

	"""
	24 bytes for JWE2
	"""

	__name__ = 'LutHeader'

	_import_key = 'lut.compounds.LutHeader'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.colors_count = 0
		self.unk_0 = 0
		self.unk_1 = 0
		self.colors_in_column_count = 0
		self.unk_2 = 0
		self.colors = ArrayPointer(self.context, self.colors_count, LutHeader._import_map["lut.compounds.Vector3"])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield ('colors', ArrayPointer, (None, LutHeader._import_map["lut.compounds.Vector3"]), (False, None), (None, None))
		yield ('colors_count', Ushort, (0, None), (False, None), (None, None))
		yield ('unk_0', Ushort, (0, None), (False, None), (None, None))
		yield ('unk_1', Uint, (0, None), (False, None), (None, None))
		yield ('colors_in_column_count', Uint, (0, None), (False, None), (None, None))
		yield ('unk_2', Uint, (0, None), (False, None), (None, None))

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'colors', ArrayPointer, (instance.colors_count, LutHeader._import_map["lut.compounds.Vector3"]), (False, None)
		yield 'colors_count', Ushort, (0, None), (False, None)
		yield 'unk_0', Ushort, (0, None), (False, None)
		yield 'unk_1', Uint, (0, None), (False, None)
		yield 'colors_in_column_count', Uint, (0, None), (False, None)
		yield 'unk_2', Uint, (0, None), (False, None)
