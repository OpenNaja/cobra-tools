from generated.formats.base.basic import Uint64
from generated.formats.ovl_base.compounds.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class WmetasbRoot(MemStruct):

	__name__ = 'WmetasbRoot'

	_import_key = 'wmeta.compounds.WmetasbRoot'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.count = 0
		self.levels = ArrayPointer(self.context, self.count, WmetasbRoot._import_map["wmeta.compounds.WmetasbMain"])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield ('levels', ArrayPointer, (None, None), (False, None), None)
		yield ('count', Uint64, (0, None), (False, None), None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'levels', ArrayPointer, (instance.count, WmetasbRoot._import_map["wmeta.compounds.WmetasbMain"]), (False, None)
		yield 'count', Uint64, (0, None), (False, None)


WmetasbRoot.init_attributes()
