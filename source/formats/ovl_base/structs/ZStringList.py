# START_GLOBALS
import logging

from generated.array import Array
from generated.formats.base.basic import ZString
from generated.formats.ovl_base.structs.Pointer import Pointer
# END_GLOBALS


class ZStringList:

# START_CLASS

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

