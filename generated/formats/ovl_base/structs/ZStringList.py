import logging

from generated.array import Array
from generated.formats.base.basic import ZString
from generated.formats.ovl_base.structs.Pointer import Pointer
from generated.array import Array
from generated.formats.ovl_base.imports import name_type_map
from generated.formats.ovl_base.structs.NestedPointers import NestedPointers


class ZStringList(NestedPointers):

	__name__ = 'ZStringList'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.ptrs = Array(self.context, 0, name_type_map['ZString'], (0,), name_type_map['Pointer'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'ptrs', Array, (0, name_type_map['ZString'], (None,), name_type_map['Pointer']), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'ptrs', Array, (0, name_type_map['ZString'], (instance.arg,), name_type_map['Pointer']), (False, None)

	def set_defaults(self):
		pass

	@classmethod
	def _to_xml(cls, instance, elem, debug):
		"""Assigns data self to xml elem"""
		if instance.ptrs:
			Array._to_xml(instance.ptrs, elem, debug)

	@classmethod
	def _from_xml(cls, instance, elem):
		if elem:
			arr = Array(instance.context, 0, ZString, (len(elem)), Pointer, set_default=False)
			instance.ptrs = Array._from_xml(arr, elem)
		return instance

	def from_strings(self, strings):
		"""Populate ZStringList from list of strings"""
		self.arg = len(strings)
		self.ptrs = Array(self.context, 0, ZString, (self.arg,), Pointer, set_default=True)
		for ptr, string in zip(self.ptrs, strings):
			ptr.data = string


