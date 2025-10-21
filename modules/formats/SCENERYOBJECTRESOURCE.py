from generated.formats.sceneryobjectresource.structs.SceneryObjectResourceRoot import SceneryObjectResourceRoot
from modules.formats.BaseFormat import MemStructLoader


class AccountCustomisationLoader(MemStructLoader):
    target_class = SceneryObjectResourceRoot
    extension = ".sceneryobjectresource"
