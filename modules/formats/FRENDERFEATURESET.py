from generated.formats.frenderfeatureset.structs.FRenderFeatureSetRoot import FRenderFeatureSetRoot
from modules.formats.BaseFormat import MemStructLoader

class FRenderFeatureSetLoader(MemStructLoader):
	target_class = FRenderFeatureSetRoot
	extension = ".frenderfeatureset"