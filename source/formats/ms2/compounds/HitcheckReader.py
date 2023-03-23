# START_GLOBALS
from generated.formats.ms2.compounds.HitCheck import HitCheck
from generated.base_struct import BaseStruct

# END_GLOBALS

class HitcheckReader(BaseStruct):


	# START_CLASS

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
		try:
			s = ''
			for jointinfo in instance.arg:
				s += str(jointinfo.hitchecks)
			return s
		except:
			return "Bad arg?"

