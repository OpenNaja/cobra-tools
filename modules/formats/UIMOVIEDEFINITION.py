from generated.formats.uimoviedefinition.compounds.UiMovieHeader import UiMovieHeader
from modules.formats.BaseFormat import MemStructLoader


class UIMovieDefinitionLoader(MemStructLoader):
	target_class = UiMovieHeader
	extension = ".uimoviedefinition"
