from generated.formats.assetpkg.compound.AssetpkgRoot import AssetpkgRoot
from modules.formats.BaseFormat import MemStructLoader


class AssetpkgLoader(MemStructLoader):
	extension = ".assetpkg"
	target_class = AssetpkgRoot

