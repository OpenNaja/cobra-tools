from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.physicssurfacesxmlres.imports import name_type_map


class PhysicsSurfaceXMLResRoot(MemStruct):

	"""
	all are mime version 3 .-.
	PC: 112 bytes
	JWE1: 112 bytes
	PZ, JWE2, WH: 80 bytes
	
	# There is an initial 'default' surface, these params are the same as in SurfacePhysicsInfo
	"""

	__name__ = 'PhysicsSurfaceXMLResRoot'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.default_surface = name_type_map['Surface'](self.context, 0, None)
		self.unk_64_1 = name_type_map['Uint64'](self.context, 0, None)
		self.only_names_j_w_e_1 = name_type_map['ArrWrapper'](self.context, 0, name_type_map['OnlyName'])
		self.surfaces = name_type_map['ArrWrapper'](self.context, 0, name_type_map['SurfacePhysicsInfo'])
		self.arr_2 = name_type_map['ArrWrapper'](self.context, 0, name_type_map['Struct2'])
		self.only_names = name_type_map['ArrWrapper'](self.context, 0, name_type_map['OnlyName'])
		self.unk_32_2 = name_type_map['Uint'](self.context, 0, None)
		self.unk_32_3 = name_type_map['Uint'](self.context, 0, None)
		self.name_1 = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		self.name_2 = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		self.nil_ptr = name_type_map['Pointer'](self.context, 0, name_type_map['EmptyStruct'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'default_surface', name_type_map['Surface'], (0, None), (False, None), (None, None)
		yield 'unk_64_1', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'name_1', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'name_2', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'nil_ptr', name_type_map['Pointer'], (0, name_type_map['EmptyStruct']), (False, None), (None, None)
		yield 'only_names_j_w_e_1', name_type_map['ArrWrapper'], (0, name_type_map['OnlyName']), (False, None), (lambda context: context.user_version.use_djb and (context.version == 19), None)
		yield 'surfaces', name_type_map['ArrWrapper'], (0, name_type_map['SurfacePhysicsInfo']), (False, None), (None, None)
		yield 'arr_2', name_type_map['ArrWrapper'], (0, name_type_map['Struct2']), (False, None), (lambda context: context.version == 18, None)
		yield 'only_names', name_type_map['ArrWrapper'], (0, name_type_map['OnlyName']), (False, None), (lambda context: (context.version == 18) or (context.user_version.use_djb and (context.version == 19)), None)
		yield 'unk_32_2', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'unk_32_3', name_type_map['Uint'], (0, None), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'default_surface', name_type_map['Surface'], (0, None), (False, None)
		yield 'unk_64_1', name_type_map['Uint64'], (0, None), (False, None)
		yield 'name_1', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'name_2', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'nil_ptr', name_type_map['Pointer'], (0, name_type_map['EmptyStruct']), (False, None)
		if instance.context.user_version.use_djb and (instance.context.version == 19):
			yield 'only_names_j_w_e_1', name_type_map['ArrWrapper'], (0, name_type_map['OnlyName']), (False, None)
		yield 'surfaces', name_type_map['ArrWrapper'], (0, name_type_map['SurfacePhysicsInfo']), (False, None)
		if instance.context.version == 18:
			yield 'arr_2', name_type_map['ArrWrapper'], (0, name_type_map['Struct2']), (False, None)
		if (instance.context.version == 18) or (instance.context.user_version.use_djb and (instance.context.version == 19)):
			yield 'only_names', name_type_map['ArrWrapper'], (0, name_type_map['OnlyName']), (False, None)
		yield 'unk_32_2', name_type_map['Uint'], (0, None), (False, None)
		yield 'unk_32_3', name_type_map['Uint'], (0, None), (False, None)
