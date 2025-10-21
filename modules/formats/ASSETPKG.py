from generated.formats.assetpkg.structs.AssetpkgRoot import AssetpkgRoot
from modules.formats.BaseFormat import MemStructLoader


class AssetpkgLoader(MemStructLoader):
	extension = ".assetpkg"
	target_class = AssetpkgRoot

