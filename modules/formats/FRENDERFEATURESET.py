from generated.formats.frenderfeatureset.compounds.FRenderFeatureSetRoot import FRenderFeatureSetRoot
from modules.formats.BaseFormat import MemStructLoader

class FRenderFeatureSetLoader(MemStructLoader):
	target_class = FRenderFeatureSetRoot
	extension = ".frenderfeatureset"