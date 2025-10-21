from generated.array import Array
from generated.formats.ovl_base.structs.Pointer import Pointer
from generated.formats.ovl_base.structs.MemStruct import MemStruct


class NestedPointers(MemStruct):

	"""
	todo - this should handle the invisible nesting of ptrs automatically for a generic template
	"""

	__name__ = 'NestedPointers'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)

	pass

	# todo generic instance.template is None on _from_xml while it isn't in from_xml

	# @classmethod
	# def _to_xml(cls, instance, elem, debug):
	# 	"""Assigns data self to xml elem"""
	# 	if instance.ptrs:
	# 		Array._to_xml(instance.ptrs, elem, debug)
	#
	# @classmethod
	# def _from_xml(cls, instance, elem):
	# 	print(f"NestedPointers._from_xml template {instance.template}")
	# 	if elem:
	# 		arr = Array(instance.context, 0, instance.template, (len(elem)), Pointer, set_default=False)
	# 		instance.ptrs = Array._from_xml(arr, elem)
	# 	return instance

