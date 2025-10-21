from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class Vector3(MemStruct):
    x: float
    y: float
    z: float
    ioptional: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
