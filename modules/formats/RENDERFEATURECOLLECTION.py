from generated.formats.renderfeaturecollection.structs.RenderFeatureCollectionRoot import RenderFeatureCollectionRoot
from modules.formats.BaseFormat import MemStructLoader


class RenderFeatureCollectionLoader(MemStructLoader):
    target_class = RenderFeatureCollectionRoot
    extension = ".renderfeaturecollection"
