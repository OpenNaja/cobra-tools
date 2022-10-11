from generated.formats.texatlas.compounds.TexAtlasRoot import TexAtlasRoot
from modules.formats.BaseFormat import MemStructLoader

class TexAtlasRootLoader(MemStructLoader):
	target_class = TexAtlasRoot
	extension = ".texatlas"