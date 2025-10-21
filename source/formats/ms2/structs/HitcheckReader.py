# START_GLOBALS
from generated.array import Array
from generated.formats.ms2.structs.HitCheck import HitCheck
from generated.base_struct import BaseStruct

# END_GLOBALS

class HitcheckReader(BaseStruct):


	# START_CLASS

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

