from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.physicssurfacesxmlres.imports import name_type_map


class SurfacePhysicsInfo(MemStruct):

	"""
	# PC: not used / crashes
	# JWE1: 16 bytes
	# PZ, JWE2, WH: 56 bytes
	"""

	__name__ = 'SurfacePhysicsInfo'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.surface = name_type_map['Surface'](self.context, 0, None)
		self.unk_64_1 = name_type_map['Uint64'](self.context, 0, None)
		self.name_1 = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		self.name_2 = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		self.nil = name_type_map['Pointer'](self.context, 0, name_type_map['EmptyStruct'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'surface', name_type_map['Surface'], (0, None), (False, None), (None, None)
		yield 'unk_64_1', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'name_1', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'name_2', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'nil', name_type_map['Pointer'], (0, name_type_map['EmptyStruct']), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'surface', name_type_map['Surface'], (0, None), (False, None)
		yield 'unk_64_1', name_type_map['Uint64'], (0, None), (False, None)
		yield 'name_1', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'name_2', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'nil', name_type_map['Pointer'], (0, name_type_map['EmptyStruct']), (False, None)
