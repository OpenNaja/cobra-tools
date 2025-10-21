# START_GLOBALS
from generated.base_struct import BaseStruct
from generated.formats.ovl_base.basic import OffsetString
from generated.formats.ms2.structs.JointPointer import JointPointer
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
		# todo - maybe auto-assign joint_names to context during reading?
		instance.context.joint_names = None
		super().read_fields(stream, instance)
		# after reading, we can resolve the joint pointers
		for ptr in instance.get_pointers():
			ptr.joint = instance.joint_infos[ptr.index]
		# if instance.context.version <= 32:
		# as joints are defined before joint_names in PC and before, patch the strings
		# after reading, resolve the name indices to string
		for child_instance, attrib in instance.get_string_attribs():
			# get the offset
			offset = child_instance.get_field(child_instance, attrib)
			# get str from ZStringBuffer
			string = instance.joint_names.get_str_at(offset)
			# print(string)
			# set the string
			cls.set_field(child_instance, attrib, string)
		# print(instance)

	@classmethod
	def write_fields(cls, stream, instance):
		instance.context.joint_names = instance.joint_names
		# if instance.context.version <= 32:
		# set arg = instance.joint_names
		strings = sorted(instance.get_strings())
		instance.joint_names.update_strings(strings)
		# at least PC+PZ store the length without the 8 byte alignment padding at the end
		# however the end of ZStringBuffer is aligned to 8 and may be padded additionally
		instance.namespace_length = len(instance.joint_names.data)
		# update indices of joint pointers
		joints_map = {j: i for i, j in enumerate(instance.joint_infos)}
		for ptr in instance.get_pointers():
			ptr.index = joints_map.get(ptr.joint)
		super().write_fields(stream, instance)
		# for f_name, f_type, arguments, _ in cls._get_filtered_attribute_list(instance, include_abstract=False):
		#     try:
		#         f_type.to_stream(getattr(instance, f_name), stream, instance.context, *arguments)
		#     except:
		#         raise BufferError(f"Failed writing '{cls.__name__}.{f_name}' at {stream.tell()}")
