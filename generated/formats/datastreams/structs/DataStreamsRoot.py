from generated.formats.datastreams.imports import name_type_map
from generated.formats.ovl_base.structs.MemStruct import MemStruct


class DataStreamsRoot(MemStruct):

	"""
	JWE1 16 bytes
	"""

	__name__ = 'DataStreamsRoot'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.layers_count = name_type_map['Uint64'](self.context, 0, None)
		self.layers = name_type_map['ArrayPointer'](self.context, self.layers_count, name_type_map['DataStreamsSettings'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'layers_count', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'layers', name_type_map['ArrayPointer'], (None, name_type_map['DataStreamsSettings']), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'layers_count', name_type_map['Uint64'], (0, None), (False, None)
		yield 'layers', name_type_map['ArrayPointer'], (instance.layers_count, name_type_map['DataStreamsSettings']), (False, None)
