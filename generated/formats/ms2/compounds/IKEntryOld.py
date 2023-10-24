from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.ms2.imports import name_type_map


class IKEntryOld(BaseStruct):

	"""
	36 bytes
	"""

	__name__ = 'IKEntryOld'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# index into name buffer
		self.name = name_type_map['Ushort'](self.context, 0, None)

		# unk
		self.index = name_type_map['Ushort'](self.context, 0, None)

		# bone
		self.parent = name_type_map['Ushort'](self.context, 0, None)

		# bone
		self.child = name_type_map['Ushort'](self.context, 0, None)

		# count of controlled bones in chain
		self.length = name_type_map['Ushort'].from_value(2)

		# bone
		self.parent_again = name_type_map['Ushort'](self.context, 0, None)

		# some at least
		self.floats = Array(self.context, 0, None, (0,), name_type_map['Float'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'name', name_type_map['Ushort'], (0, None), (False, None), (None, None)
		yield 'index', name_type_map['Ushort'], (0, None), (False, None), (None, None)
		yield 'parent', name_type_map['Ushort'], (0, None), (False, None), (None, None)
		yield 'child', name_type_map['Ushort'], (0, None), (False, None), (None, None)
		yield 'length', name_type_map['Ushort'], (0, None), (False, 2), (None, None)
		yield 'parent_again', name_type_map['Ushort'], (0, None), (False, None), (None, None)
		yield 'floats', Array, (0, None, (6,), name_type_map['Float']), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'name', name_type_map['Ushort'], (0, None), (False, None)
		yield 'index', name_type_map['Ushort'], (0, None), (False, None)
		yield 'parent', name_type_map['Ushort'], (0, None), (False, None)
		yield 'child', name_type_map['Ushort'], (0, None), (False, None)
		yield 'length', name_type_map['Ushort'], (0, None), (False, 2)
		yield 'parent_again', name_type_map['Ushort'], (0, None), (False, None)
		yield 'floats', Array, (0, None, (6,), name_type_map['Float']), (False, None)
