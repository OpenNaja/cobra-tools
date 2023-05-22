# START_GLOBALS
import logging

from generated.base_struct import BaseStruct
from generated.formats.manis.compounds.ManiBlock import ManiBlock

# END_GLOBALS


class KeysReader(BaseStruct):

	# START_CLASS

	@classmethod
	def read_fields(cls, stream, instance):
		instance.io_start = stream.tell()
		# print(instance.context)
		for mani_info in instance.arg:
			logging.info(mani_info)
			mani_block_start = stream.tell()
			logging.info(f"Reading keys block at {mani_block_start}")
			# if mani_block_start == 964833:
			# 	break
			try:
				mani_info.keys = ManiBlock.from_stream(stream, instance.context, mani_info, None)
				logging.info(mani_info.keys)
				# break
			except:
				logging.exception(f"Reading ManiBlock failed at {mani_block_start} for {mani_info}")
		instance.io_size = stream.tell() - instance.io_start

	@classmethod
	def write_fields(cls, stream, instance):
		instance.io_start = stream.tell()
		for mani_info in instance.arg:
			ManiBlock.to_stream(mani_info.keys, stream, instance.context)
		instance.io_size = stream.tell() - instance.io_start

	@classmethod
	def get_fields_str(cls, instance, indent=0):
		s = ''
		for mani_info in instance.arg:
			if hasattr(mani_info, "keys"):
				s += str(mani_info.keys)
		return s

