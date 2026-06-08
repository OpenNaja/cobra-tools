from generated.formats.trackelement.structs.TrackElementRoot import TrackElementRoot
from modules.formats.BaseFormat import MimeVersionedLoader

class TrackElementLoader(MimeVersionedLoader):
	extension = ".trackelement"
	target_class = TrackElementRoot
	
