from generated.formats.spatialuitheme.structs.SpatialUIThemeRoot import SpatialUIThemeRoot
from modules.formats.BaseFormat import MemStructLoader


class SpatialUIThemeLoader(MemStructLoader):
    target_class = SpatialUIThemeRoot
    extension = ".spatialuitheme"
