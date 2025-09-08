# START_GLOBALS
import logging
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.motiongraph.imports import name_type_map

# END_GLOBALS


class DataStreamResourceData(MemStruct):

	"""
	48 bytes
	"""

# START_CLASS

	def get_audio_name(self):
		if self.type.data == "AudioEvent":
			return self.ds_name.data
