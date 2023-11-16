from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.physicssurfacesxmlres.imports import name_type_map


class PhysicsSurfaceXMLResRoot(MemStruct):

	"""
	PC: 112 bytes
	
	# There is an initial 'default' surface, these params are the same as in SurfacePhysicsInfo
	"""

	__name__ = 'PhysicsSurfaceXMLResRoot'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.unk_64_1 = name_type_map['Uint64'](self.context, 0, None)
		self.count_1 = name_type_map['Ushort'](self.context, 0, None)
		self.flag_1 = name_type_map['Ushort'](self.context, 0, None)
		self.unkb = name_type_map['Uint'](self.context, 0, None)
		self.count_2 = name_type_map['Uint64'](self.context, 0, None)
		self.count_3 = name_type_map['Ushort'](self.context, 0, None)
		self.flag_3 = name_type_map['Ushort'](self.context, 0, None)
		self.unk_32_1 = name_type_map['Uint'](self.context, 0, None)
		self.unk_32_2 = name_type_map['Uint'](self.context, 0, None)
		self.unk_32_3 = name_type_map['Uint'](self.context, 0, None)
		self.name_1 = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		self.name_2 = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		self.ptr_0 = name_type_map['Pointer'](self.context, 0, name_type_map['EmptyStruct'])
		self.arr_1 = name_type_map['ArrayPointer'](self.context, self.count_1, name_type_map['SurfacePhysicsInfo'])
		self.arr_2 = name_type_map['ArrayPointer'](self.context, self.count_2, name_type_map['Struct2'])
		self.arr_3 = name_type_map['ArrayPointer'](self.context, self.count_3, name_type_map['Struct3'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'default_surface', name_type_map['Surface'], (0, None), (False, None), (None, None)
		yield 'unk_64_1', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'name_1', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'name_2', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'ptr_0', name_type_map['Pointer'], (0, name_type_map['EmptyStruct']), (False, None), (None, None)
		yield 'arr_1', name_type_map['ArrayPointer'], (None, name_type_map['SurfacePhysicsInfo']), (False, None), (None, None)
		yield 'count_1', name_type_map['Ushort'], (0, None), (False, None), (None, None)
		yield 'flag_1', name_type_map['Ushort'], (0, None), (False, None), (None, None)
		yield 'unkb', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'arr_2', name_type_map['ArrayPointer'], (None, name_type_map['Struct2']), (False, None), (None, None)
		yield 'count_2', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'arr_3', name_type_map['ArrayPointer'], (None, name_type_map['Struct3']), (False, None), (None, None)
		yield 'count_3', name_type_map['Ushort'], (0, None), (False, None), (None, None)
		yield 'flag_3', name_type_map['Ushort'], (0, None), (False, None), (None, None)
		yield 'unk_32_1', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'unk_32_2', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'unk_32_3', name_type_map['Uint'], (0, None), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'default_surface', name_type_map['Surface'], (0, None), (False, None)
		yield 'unk_64_1', name_type_map['Uint64'], (0, None), (False, None)
		yield 'name_1', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'name_2', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'ptr_0', name_type_map['Pointer'], (0, name_type_map['EmptyStruct']), (False, None)
		yield 'arr_1', name_type_map['ArrayPointer'], (instance.count_1, name_type_map['SurfacePhysicsInfo']), (False, None)
		yield 'count_1', name_type_map['Ushort'], (0, None), (False, None)
		yield 'flag_1', name_type_map['Ushort'], (0, None), (False, None)
		yield 'unkb', name_type_map['Uint'], (0, None), (False, None)
		yield 'arr_2', name_type_map['ArrayPointer'], (instance.count_2, name_type_map['Struct2']), (False, None)
		yield 'count_2', name_type_map['Uint64'], (0, None), (False, None)
		yield 'arr_3', name_type_map['ArrayPointer'], (instance.count_3, name_type_map['Struct3']), (False, None)
		yield 'count_3', name_type_map['Ushort'], (0, None), (False, None)
		yield 'flag_3', name_type_map['Ushort'], (0, None), (False, None)
		yield 'unk_32_1', name_type_map['Uint'], (0, None), (False, None)
		yield 'unk_32_2', name_type_map['Uint'], (0, None), (False, None)
		yield 'unk_32_3', name_type_map['Uint'], (0, None), (False, None)
