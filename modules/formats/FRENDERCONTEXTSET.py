from generated.formats.frendercontextset.compounds.FRenderContextSetRoot import FRenderContextSetRoot
from modules.formats.BaseFormat import MemStructLoader

class FRenderContextSetLoader(MemStructLoader):
	target_class = FRenderContextSetRoot
	extension = ".frendercontextset"