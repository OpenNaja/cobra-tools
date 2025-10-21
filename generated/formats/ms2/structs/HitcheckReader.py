from generated.array import Array
from generated.formats.ms2.structs.HitCheck import HitCheck
from generated.base_struct import BaseStruct

from generated.base_struct import BaseStruct


class HitcheckReader(BaseStruct):

	"""
	This reads and assigns hitchecks to each jointinfo that is passed to it
	"""

	__name__ = 'HitcheckReader'


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

	@classmethod
	def read_fields(cls, stream, instance):
		joint_data = instance.arg
		for jointinfo in joint_data.joint_infos:
			jointinfo.hitchecks = Array.from_stream(stream, jointinfo.context, jointinfo.arg, None, shape=(jointinfo.hitcheck_count,), dtype=HitCheck)

	@classmethod
	def write_fields(cls, stream, instance):
		joint_data = instance.arg
		for jointinfo in joint_data.joint_infos:
			Array.to_stream(jointinfo.hitchecks, stream, instance.context, shape=(jointinfo.hitcheck_count,), dtype=HitCheck)


