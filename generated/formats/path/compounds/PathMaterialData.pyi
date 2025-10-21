from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class PathMaterialData(MemStruct):
    terrain_type: int
    opacity: float
    padding: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
