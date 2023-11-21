from generated.formats.assetpacklist.compounds.AssetPackListRoot import AssetPackListRoot
from modules.formats.BaseFormat import MemStructLoader


class AssetPackListLoader(MemStructLoader):
    target_class = AssetPackListRoot
    extension = ".assetpacklist"
