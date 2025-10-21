from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.ovl_base.structs.Pointer import Pointer


class LayerMap(MemStruct):
    layer_name: Pointer[str]
    specific_name: Pointer[str]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
