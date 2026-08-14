from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.manis.imports import name_type_map


class CompressedManiDataPC2(BaseStruct):

	"""
	An ACL compressed_tracks blob followed by a ushort terminator.
	The blob itself starts with ACL's size/hash/tag header and must be
	preserved verbatim; decoding is handled by the external ACL helper.
	"""

	__name__ = 'CompressedManiDataPC2'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.size = name_type_map['Uint'](self.context, 0, None)
		self.acl_data = Array(self.context, 0, None, (0,), name_type_map['Ubyte'])
		self.pad = name_type_map['PadAlign'](self.context, 16, self.arg.ref)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'size', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'acl_data', Array, (0, None, (None,), name_type_map['Ubyte']), (False, None), (None, None)
		yield 'pad', name_type_map['PadAlign'], (16, None), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'size', name_type_map['Uint'], (0, None), (False, None)
		yield 'acl_data', Array, (0, None, (instance.size - 4,), name_type_map['Ubyte']), (False, None)
		yield 'pad', name_type_map['PadAlign'], (16, instance.arg.ref), (False, None)
