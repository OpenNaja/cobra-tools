from generated.formats.datastreams.imports import name_type_map
from generated.formats.ovl_base.structs.MemStruct import MemStruct


class DataStreamsSettings(MemStruct):

	"""
	JWE1 48 bytes
	"""

	__name__ = 'DataStreamsSettings'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.z_0 = name_type_map['Uint64'](self.context, 0, None)
		self.z_1 = name_type_map['Uint64'](self.context, 0, None)
		self.count = name_type_map['Uint64'](self.context, 0, None)
		self.name_a = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		self.name_b = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		self.data = name_type_map['ArrayPointer'](self.context, self.count, name_type_map['CurveDataPoint'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'name_a', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'name_b', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'z_0', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'z_1', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'count', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'data', name_type_map['ArrayPointer'], (None, name_type_map['CurveDataPoint']), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'name_a', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'name_b', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'z_0', name_type_map['Uint64'], (0, None), (False, None)
		yield 'z_1', name_type_map['Uint64'], (0, None), (False, None)
		yield 'count', name_type_map['Uint64'], (0, None), (False, None)
		yield 'data', name_type_map['ArrayPointer'], (instance.count, name_type_map['CurveDataPoint']), (False, None)
