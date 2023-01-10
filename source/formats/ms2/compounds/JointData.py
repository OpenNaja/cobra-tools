# START_GLOBALS
from generated.base_struct import BaseStruct
from generated.formats.ms2.basic import OffsetString
from generated.formats.ms2.compounds.JointPointer import JointPointer
import logging

# END_GLOBALS


class JointData(BaseStruct):

	# START_CLASS

	def get_strings(self):
		"""Get all strings in the structure."""
		condition_function = lambda x: issubclass(x[1], OffsetString)
		for val in self.get_condition_values_recursive(self, condition_function):
			yield val

	def get_pointers(self):
		"""Get all strings in the structure."""
		condition_function = lambda x: issubclass(x[1], JointPointer)
		for val in self.get_condition_values_recursive(self, condition_function):
			yield val

	def get_string_attribs(self):
		"""Get all strings in the structure."""
		condition_function = lambda x: issubclass(x[1], OffsetString)
		for s_type, s_inst, (f_name, f_type, arguments, _) in self.get_condition_attributes_recursive(self, self, condition_function):
			yield s_inst, f_name

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		# after reading, we can resolve the joint pointers
		for ptr in instance.get_pointers():
			ptr.joint = instance.joint_infos[ptr.index]
	# 	# after reading, resolve the names to string
	# 	for child_instance, attrib in instance.get_string_attribs():
	# 		# get the offset
	# 		offset = child_instance.get_field(child_instance, attrib)
	# 		# get str from ZStringBuffer
	# 		string = instance.joint_names.get_str_at(offset)
	# 		# set the string
	# 		cls.set_field(child_instance, attrib, string)

	@classmethod
	def write_fields(cls, stream, instance):
		strings = list(instance.get_strings())
		instance.joint_names.update_strings(strings)
		instance.namespace_length = len(instance.joint_names.data)
		# update indices of joint pointers
		joints_map = {j: i for i, j in enumerate(instance.joint_infos)}
		for ptr in instance.get_pointers():
			ptr.index = joints_map.get(ptr.joint)
		super().write_fields(stream, instance)
