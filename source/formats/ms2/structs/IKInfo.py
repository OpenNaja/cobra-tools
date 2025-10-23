# START_GLOBALS
from generated.base_struct import BaseStruct
from generated.formats.ms2.structs.BonePointer import BonePointer
import logging

# END_GLOBALS


class IKInfo(BaseStruct):

	# START_CLASS

	def get_pointers(self):
		"""Get all strings in the structure."""
		condition_function = lambda x: issubclass(x[1], BonePointer)
		for val in self.get_condition_values_recursive(self, condition_function):
			yield val

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		# after reading, we can resolve the bone pointers
		for ptr in instance.get_pointers():
			try:
				ptr.joint = instance.arg.bones[ptr.index]
			except IndexError:
				ptr.joint = f"Bad Ref ({ptr.index})"

	@classmethod
	def write_fields(cls, stream, instance):
		# update indices of bone pointers
		bones_map = {b: i for i, b in enumerate(instance.arg.bones)}
		for ptr in instance.get_pointers():
			ptr.index = bones_map.get(ptr.joint)
		super().write_fields(stream, instance)
