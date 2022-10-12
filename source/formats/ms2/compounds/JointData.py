# START_GLOBALS
from generated.base_struct import BaseStruct
from generated.formats.ms2.basic import OffsetString
import logging

# END_GLOBALS


class JointData(BaseStruct):

	# START_CLASS

	def get_strings(self):
		"""Get all strings in the structure."""
		condition_function = lambda x: issubclass(x[1], OffsetString)
		for val in self.get_condition_values_recursive(self, condition_function):
			if val:
				yield val

	@classmethod
	def write_fields(cls, stream, instance):
		instance.joint_names.update_strings(instance.get_strings())
		instance.namespace_length = len(instance.joint_names.data)
		# todo JointNamesPadding
		super().write_fields(stream, instance)
