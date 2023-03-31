from generated.formats.base.basic import Uint64
from generated.formats.base.basic import ZString
from generated.formats.ovl_base.compounds.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class Some(MemStruct):

	"""
	24 bytes
	"""

	__name__ = 'Some'

	_import_key = 'logicalcontrols.compounds.Some'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.some_count = 0
		self.some_name = Pointer(self.context, 0, ZString)
		self.some_data = ArrayPointer(self.context, self.some_count, Some._import_map["logicalcontrols.compounds.SomeData"])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield ('some_name', Pointer, (0, ZString), (False, None), (None, None))
		yield ('some_data', ArrayPointer, (None, Some._import_map["logicalcontrols.compounds.SomeData"]), (False, None), (None, None))
		yield ('some_count', Uint64, (0, None), (False, None), (None, None))

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'some_name', Pointer, (0, ZString), (False, None)
		yield 'some_data', ArrayPointer, (instance.some_count, Some._import_map["logicalcontrols.compounds.SomeData"]), (False, None)
		yield 'some_count', Uint64, (0, None), (False, None)


Some.init_attributes()
