# START_GLOBALS

import logging
from generated.base_struct import BaseStruct

# END_GLOBALS


class HircPointer(BaseStruct):

	# START_CLASS

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		# 4 bytes used on length that are not part of the size of the struct
		actual_size = instance.data.io_size - 4
		if actual_size != instance.data.length:
			logging.warning(f"HIRC block {instance.id.name} at offset {instance.io_start} expected {instance.data.length}, but read {actual_size} bytes")
			stream.seek(instance.data.io_start + 4 + instance.data.length)