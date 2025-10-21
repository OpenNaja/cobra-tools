from inspect import isclass

from generated.formats.motiongraph.structs.DataStreamResourceData import DataStreamResourceData
from generated.formats.motiongraph.structs.MotiongraphHeader import MotiongraphHeader
import generated.formats.ovl.versions as ovl_versions
from modules.formats.BaseFormat import MemStructLoader


class MotiongraphLoader(MemStructLoader):
	target_class = MotiongraphHeader
	extension = ".motiongraph"

	@property
	def motiongraph_rename_sound(self):
		return self.ovl.cfg.get("motiongraph_rename_sound", False)
	
	def collect(self):
		self.context.recursion = {}
		if self.ovl.version >= 19:
			# structs are too different, doesn't register anim names, would break rename contents
			if ovl_versions.is_jwe(self.ovl):
				return
			super().collect()
			# print(set(s for s in self.get_audio_strings()))

	def get_audio_strings(self):
		def cond(x):
			try:
				return x[1].__name__ == "DataStreamResourceData"
			except:
				return False
		# condition_function = lambda x: hasattr(x[1], "__name__") and x[1].__name__ == "DataStreamResourceData"
		# condition_function = lambda x:  issubclass(x[1], DataStreamResourceData)
		for data_stream_resource_data in self.header.get_condition_fields(cond):
			if data_stream_resource_data.type.data in ("AudioEvent", "AudioLoopingEvent", "AudioBlend", "AudioRTPC"):
				yield data_stream_resource_data.ds_name.data


	def accept_string(self, in_str):
		"""Return True if string should receive replacement"""
		# anims have @ eg. Acrocanthosaurus@JumpAttackDefendFlankLeft
		if "@" in in_str:
			return True
		# sound events don't, e.g. Acrocanthosaurus_FightReact
		return self.motiongraph_rename_sound
