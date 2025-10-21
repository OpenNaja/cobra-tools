from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.ovl_base.structs.Pointer import Pointer


class VoxelTerrainMaterialAssetPackagesRoot(MemStruct):
    package_name: Pointer[str]
    unk_1: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
