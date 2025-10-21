from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class VoxelTerrainMaterialLayerSpecRoot(MemStruct):
    unknown_name: Pointer[str]
    tile_size: float
    float_2: float
    flags: int
    float_3: float
    parallax: float
    macro_amount: float
    water_permeability: float
    macro_albedo: float
    detail_normal: float
    macro_roughness: float
    macro_full: float
    smoothness: float
    float_10: float
    float_11: float

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
