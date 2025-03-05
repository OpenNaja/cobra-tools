from generated.base_struct import BaseStruct
from generated.formats.ovl.imports import name_type_map


class Fragment(BaseStruct):

	"""
	These are to be thought of as instructions for loading. Their order is irrelevant.
	"""

	__name__ = 'Fragment'

	allow_np = True

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# The index of the MemPool this one relates to; OR, for entries referred to from AssetEntries: -1
		self.link_pool = name_type_map['Int'].from_value(-1)

		# the byte offset relative to the start of the MemPool's data
		self.link_offset = name_type_map['Uint'](self.context, 0, None)

		# The index of the MemPool this one relates to; OR, for entries referred to from AssetEntries: -1
		self.struct_pool = name_type_map['Int'].from_value(-1)

		# the byte offset relative to the start of the MemPool's data
		self.struct_offset = name_type_map['Uint'](self.context, 0, None)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'link_pool', name_type_map['Int'], (0, None), (False, -1), (None, None)
		yield 'link_offset', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'struct_pool', name_type_map['Int'], (0, None), (False, -1), (None, None)
		yield 'struct_offset', name_type_map['Uint'], (0, None), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'link_pool', name_type_map['Int'], (0, None), (False, -1)
		yield 'link_offset', name_type_map['Uint'], (0, None), (False, None)
		yield 'struct_pool', name_type_map['Int'], (0, None), (False, -1)
		yield 'struct_offset', name_type_map['Uint'], (0, None), (False, None)
