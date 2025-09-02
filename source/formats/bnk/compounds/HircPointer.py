# START_GLOBALS

import logging
from generated.base_struct import BaseStruct

# END_GLOBALS


class HircPointer(BaseStruct):

	# START_CLASS

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		if instance.data.io_size != instance.length:
			logging.warning(f"HIRC block {instance.id.name} at offset {instance.io_start} expected {instance.length}, but read {instance.data.io_size} bytes")
			stream.seek(instance.data.io_start + instance.length)