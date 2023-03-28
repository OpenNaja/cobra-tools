from generated.formats.base.basic import Uint64
from generated.formats.base.basic import ZString
from generated.formats.ovl_base.compounds.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class DecalSettingsRoot(MemStruct):

	__name__ = 'DecalSettingsRoot'

	_import_key = 'decalsettings.compounds.DecalSettingsRoot'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.layer_count = 0
		self.unknown = 0
		self.atlas_name = Pointer(self.context, 0, ZString)
		self.layer_list = ArrayPointer(self.context, self.layer_count, DecalSettingsRoot._import_map["decalsettings.compounds.DecalSettingItem"])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield ('atlas_name', Pointer, (0, ZString), (False, None), None)
		yield ('layer_list', ArrayPointer, (None, DecalSettingsRoot._import_map["decalsettings.compounds.DecalSettingItem"]), (False, None), None)
		yield ('layer_count', Uint64, (0, None), (False, None), None)
		yield ('unknown', Uint64, (0, None), (False, None), None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'atlas_name', Pointer, (0, ZString), (False, None)
		yield 'layer_list', ArrayPointer, (instance.layer_count, DecalSettingsRoot._import_map["decalsettings.compounds.DecalSettingItem"]), (False, None)
		yield 'layer_count', Uint64, (0, None), (False, None)
		yield 'unknown', Uint64, (0, None), (False, None)


DecalSettingsRoot.init_attributes()
