from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer
from generated.formats.ovl_base.compounds.ZStringList import ZStringList


class SceneryObjectResourceRoot(MemStruct):
    faction_tags: Pointer[ZStringList]
    faction_tags_count: int
    resource_types_tags: Pointer[ZStringList]
    resource_types_tags_count: int
    asset_pack_tags: Pointer[ZStringList]
    asset_pack_tags_count: int
    primary_group_tags: Pointer[ZStringList]
    primary_group_tags_count: int
    secondary_group_tags: Pointer[ZStringList]
    secondary_group_tags_count: int
    functional_tags: Pointer[ZStringList]
    functional_tags_count: int
    unk_0: int
    unk_1: int
    unk_2: int
    unk_3: int
    variant_names: Pointer[ZStringList]
    variant_names_count: int
    child_scenery_resource_name: Pointer[str]
    parent_scenery_resource_name: Pointer[str]
    unk_4: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
