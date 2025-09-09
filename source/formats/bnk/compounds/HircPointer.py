# START_GLOBALS

import logging
from generated.base_struct import BaseStruct

# END_GLOBALS


class HircPointer(BaseStruct):

	# START_CLASS

	@classmethod
	def read_fields(cls, stream, instance):
		try:
			super().read_fields(stream, instance)
		except:
			logging.warning(f"HIRC block {instance.id} at offset {instance.io_start} failed to read")
			stream.seek(instance.data.io_start + instance.length)
			return
		if instance.data.io_size != instance.length:
			logging.warning(f"HIRC block {instance.id.name} at offset {instance.io_start} expected {instance.length}, but read {instance.data.io_size} bytes")
			stream.seek(instance.data.io_start + instance.length)
			logging.warning(instance)