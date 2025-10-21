from generated.formats.cinematic.structs.CinematicRoot import CinematicRoot
from modules.formats.BaseFormat import MemStructLoader


class CinematicLoader(MemStructLoader):
	extension = ".cinematic"
	target_class = CinematicRoot

	def get_audio_strings(self):
		def cond(x):
			try:
				return x[1].__name__ == "Event"
			except:
				return False
		# condition_function = lambda x: hasattr(x[1], "__name__") and x[1].__name__ == "DataStreamResourceData"
		# condition_function = lambda x:  issubclass(x[1], DataStreamResourceData)
		for event in self.header.get_condition_fields(cond):
			if event.module_name.data in ("AudioEvent", "AudioLoopingEvent", "AudioBlend", "AudioRTPC"):
				yield event.attributes.data.event_name.data