from generated.formats.renderfeaturecollection.compounds.RenderFeatureCollectionRoot import RenderFeatureCollectionRoot
from modules.formats.BaseFormat import MemStructLoader


class RenderFeatureCollectionLoader(MemStructLoader):
    target_class = RenderFeatureCollectionRoot
    extension = ".renderfeaturecollection"
