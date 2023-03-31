from generated.formats.base.basic import Uint64
from generated.formats.ovl_base.basic import ZStringObfuscated
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class BuildingSetRoot(MemStruct):

	__name__ = 'BuildingSetRoot'

	_import_key = 'buildingset.compounds.BuildingSetRoot'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.set_count_or_type = 0
		self.unk_1_found_as_0 = 0
		self.unk_2_found_as_0 = 0
		self.set_id_name = Pointer(self.context, 0, ZStringObfuscated)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield ('set_id_name', Pointer, (0, ZStringObfuscated), (False, None), (None, None))
		yield ('set_count_or_type', Uint64, (0, None), (False, None), (None, None))
		yield ('unk_1_found_as_0', Uint64, (0, None), (False, None), (None, None))
		yield ('unk_2_found_as_0', Uint64, (0, None), (False, None), (None, None))

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'set_id_name', Pointer, (0, ZStringObfuscated), (False, None)
		yield 'set_count_or_type', Uint64, (0, None), (False, None)
		yield 'unk_1_found_as_0', Uint64, (0, None), (False, None)
		yield 'unk_2_found_as_0', Uint64, (0, None), (False, None)


BuildingSetRoot.init_attributes()
