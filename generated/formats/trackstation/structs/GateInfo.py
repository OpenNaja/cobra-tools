from generated.array import Array
from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.trackstation.imports import name_type_map


class GateInfo(MemStruct):

	__name__ = 'GateInfo'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.floats = Array(self.context, 0, None, (0,), name_type_map['Float'])
		self.entrance_gate = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		self.exit_gate = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		self.unknown_ptr = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		self.fence_extrusion = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		self.small_fence_extrusion = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		self.fence_cap = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'entrance_gate', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'exit_gate', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'unknown_ptr', name_type_map['Pointer'], (0, name_type_map['ZString']), (True, None), (None, None)
		yield 'fence_extrusion', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'small_fence_extrusion', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'fence_cap', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'floats', Array, (0, None, (4,), name_type_map['Float']), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'entrance_gate', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'exit_gate', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'unknown_ptr', name_type_map['Pointer'], (0, name_type_map['ZString']), (True, None)
		yield 'fence_extrusion', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'small_fence_extrusion', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'fence_cap', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'floats', Array, (0, None, (4,), name_type_map['Float']), (False, None)
