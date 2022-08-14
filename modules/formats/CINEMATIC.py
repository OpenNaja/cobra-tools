from generated.formats.cinematic.compounds.CinematicRoot import CinematicRoot
from modules.formats.BaseFormat import MemStructLoader


class CinematicLoader(MemStructLoader):
	extension = ".cinematic"
	target_class = CinematicRoot
