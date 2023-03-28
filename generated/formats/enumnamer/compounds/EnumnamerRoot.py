from generated.formats.base.basic import Uint64
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class EnumnamerRoot(MemStruct):

	__name__ = 'EnumnamerRoot'

	_import_key = 'enumnamer.compounds.EnumnamerRoot'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.count = 0
		self.strings = Pointer(self.context, self.count, EnumnamerRoot._import_map["enumnamer.compounds.PtrList"])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield ('count', Uint64, (0, None), (False, None), None)
		yield ('strings', Pointer, (None, EnumnamerRoot._import_map["enumnamer.compounds.PtrList"]), (False, None), None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'count', Uint64, (0, None), (False, None)
		yield 'strings', Pointer, (instance.count, EnumnamerRoot._import_map["enumnamer.compounds.PtrList"]), (False, None)


EnumnamerRoot.init_attributes()
