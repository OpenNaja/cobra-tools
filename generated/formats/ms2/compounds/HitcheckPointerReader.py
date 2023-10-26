import logging

from generated.formats.ms2.compounds.HitCheck import HitCheck
from generated.base_struct import BaseStruct

from generated.base_struct import BaseStruct


class HitcheckPointerReader(BaseStruct):

	__name__ = 'HitcheckPointerReader'


	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)

	def __init__(self, context, arg=None, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		pass

	@classmethod
	def read_fields(cls, stream, instance):
		joint_data = instance.arg
		instance.hc_pointers = []
		for jointinfo in joint_data.joint_infos:
			for i in range(jointinfo.hitcheck_count):
				hc = stream.read(8)
				instance.hc_pointers.append(hc)

	@classmethod
	def write_fields(cls, stream, instance):
		pass

	@classmethod
	def get_fields_str(cls, instance, indent=0):
		try:
			s = ''
			joint_data = instance.arg
			for jointinfo in joint_data.joint_infos:
				s += str(jointinfo.hitchecks)
			return s
		except:
			return "Bad arg?"


