from generated.formats.dlcentitlements.imports import name_type_map
from generated.formats.ovl_base.structs.MemStruct import MemStruct


class DLCEntitlementsRoot(MemStruct):

	__name__ = 'DLCEntitlementsRoot'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.entitlement_count = name_type_map['Uint64'](self.context, 0, None)
		self.entitlement_list = name_type_map['ArrayPointer'](self.context, self.entitlement_count, name_type_map['Entitlement'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'entitlement_list', name_type_map['ArrayPointer'], (None, name_type_map['Entitlement']), (False, None), (None, None)
		yield 'entitlement_count', name_type_map['Uint64'], (0, None), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'entitlement_list', name_type_map['ArrayPointer'], (instance.entitlement_count, name_type_map['Entitlement']), (False, None)
		yield 'entitlement_count', name_type_map['Uint64'], (0, None), (False, None)
