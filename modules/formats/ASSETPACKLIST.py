from generated.formats.assetpacklist.structs.AssetPackListRoot import AssetPackListRoot
from modules.formats.BaseFormat import MemStructLoader


class AssetPackListLoader(MemStructLoader):
    target_class = AssetPackListRoot
    extension = ".assetpacklist"
