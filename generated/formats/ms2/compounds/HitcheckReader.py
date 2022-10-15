from generated.formats.ms2.compounds.HitCheck import HitCheck
from generated.base_struct import BaseStruct

from generated.base_struct import BaseStruct


class HitcheckReader(BaseStruct):

	"""
	This reads and assigns hitchecks to each jointinfo that is passed to it
	"""

	__name__ = 'HitcheckReader'

	_import_key = 'ms2.compounds.HitcheckReader'

	_attribute_list = BaseStruct._attribute_list + [
		]

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
		for jointinfo in joint_data.joint_infos:
			jointinfo.hitchecks = []
			for i in range(jointinfo.hitcheck_count):
				hc = HitCheck.from_stream(stream, instance.context, arg=joint_data.joint_names)
				jointinfo.hitchecks.append(hc)

	@classmethod
	def write_fields(cls, stream, instance):
		pass

	@classmethod
	def get_fields_str(cls, instance, indent=0):
		s = ''
		for jointinfo in instance.arg:
			s += str(jointinfo.hitchecks)
		return s


