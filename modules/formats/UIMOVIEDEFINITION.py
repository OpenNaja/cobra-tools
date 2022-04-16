from generated.formats.uimoviedefinition.compound.UiMovieHeader import UiMovieHeader
from modules.formats.BaseFormat import MemStructLoader


class UIMovieDefinitionLoader(MemStructLoader):
	target_class = UiMovieHeader
