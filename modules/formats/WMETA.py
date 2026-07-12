from generated.formats.wmeta.structs.WmetasbRoot import WmetasbRoot
from modules.formats.BaseFormat import MemStructLoader, MimeVersionedLoader


class WmetaLoader(MimeVersionedLoader):
	target_class = WmetasbRoot
	extension = ".wmetasb"

	def get_audio_hashes(self):
		def EventEntry(x):
			try:
				return x[1].__name__ == "EventEntry"
			except:
				return False
		def BnkMetaNew(x):
			try:
				return x[1].__name__ == "BnkMetaNew"
			except:
				return False
		for event in self.header.get_condition_fields(EventEntry):
			yield event.stop_start_fnv
			if event.start_fnv:
				yield event.start_fnv
			yield event.event_fnv
		for bnk in self.header.get_condition_fields(BnkMetaNew):
			yield bnk.fnv
