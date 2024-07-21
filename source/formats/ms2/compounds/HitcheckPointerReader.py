# START_GLOBALS
from generated.array import Array
from generated.formats.base.basic import Uint64
from generated.base_struct import BaseStruct

# END_GLOBALS

class HitcheckPointerReader(BaseStruct):


	# START_CLASS

	@classmethod
	def read_fields(cls, stream, instance):
		joint_data = instance.arg
		for jointinfo in joint_data.joint_infos:
			jointinfo.hitcheck_pointers = Array.from_stream(stream, jointinfo.context, jointinfo.arg, None, shape=(jointinfo.hitcheck_count,), dtype=Uint64)

	@classmethod
	def write_fields(cls, stream, instance):
		joint_data = instance.arg
		for jointinfo in joint_data.joint_infos:
			Array.to_stream(jointinfo.hitcheck_pointers, stream, instance.context, shape=(jointinfo.hitcheck_count,), dtype=Uint64)

