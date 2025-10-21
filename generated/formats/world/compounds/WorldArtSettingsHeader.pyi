from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer
from generated.formats.ovl_base.compounds.ZStringList import ZStringList


class WorldArtSettingsHeader(MemStruct):
    size_x: int
    size_y: int
    size_z: int
    unknown_1: int
    skirt_resource_name: Pointer[str]
    landscape_prefab_name: Pointer[str]
    skirt_material_names: Pointer[ZStringList]
    skirt_material_names_count: int
    packages_to_load: Pointer[ZStringList]
    packages_to_load_count: int
    height_map_file_name: Pointer[str]
    unknown_3: int
    sea_prefab_name: Pointer[str]
    colour_grade_name: Pointer[str]
    sun_horizon_rotation: float
    sun_zenith_rotation: float
    moon_horizon_rotation: float
    moon_zenith_rotation: float

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
