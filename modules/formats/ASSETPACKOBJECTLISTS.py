from generated.formats.assetpackobjectlists.compounds.AssetPackObjectListsRoot import AssetPackObjectListsRoot
from modules.formats.BaseFormat import MemStructLoader


class AssetPackObjectListsLoader(MemStructLoader):
    target_class = AssetPackObjectListsRoot
    extension = ".assetpackobjectlists"
