from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.physicssurfacesxmlres.imports import name_type_map


class Surface(MemStruct):

	"""
	24 bytes
	# todo: define the right property name for these values
	"""

	__name__ = 'Surface'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.float_1 = name_type_map['Float'](self.context, 0, None)
		self.float_2 = name_type_map['Float'](self.context, 0, None)
		self.float_3 = name_type_map['Float'](self.context, 0, None)
		self.float_4 = name_type_map['Float'](self.context, 0, None)
		self.surface_name = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'surface_name', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'float_1', name_type_map['Float'], (0, None), (False, None), (None, None)
		yield 'float_2', name_type_map['Float'], (0, None), (False, None), (None, None)
		yield 'float_3', name_type_map['Float'], (0, None), (False, None), (None, None)
		yield 'float_4', name_type_map['Float'], (0, None), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'surface_name', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'float_1', name_type_map['Float'], (0, None), (False, None)
		yield 'float_2', name_type_map['Float'], (0, None), (False, None)
		yield 'float_3', name_type_map['Float'], (0, None), (False, None)
		yield 'float_4', name_type_map['Float'], (0, None), (False, None)
