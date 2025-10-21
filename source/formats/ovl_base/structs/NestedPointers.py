# START_GLOBALS
from generated.array import Array
from generated.formats.ovl_base.structs.Pointer import Pointer
# END_GLOBALS


class NestedPointers:

# START_CLASS

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
