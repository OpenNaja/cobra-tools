from generated.formats.frenderlodspec.compounds.FRenderLodSpecRoot import FRenderLodSpecRoot
from modules.formats.BaseFormat import MemStructLoader

class FRenderLodSpecLoader(MemStructLoader):
	target_class = FRenderLodSpecRoot
	extension = ".frenderlodspec"