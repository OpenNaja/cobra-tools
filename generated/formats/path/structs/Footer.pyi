from generated.array import Array
from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.ovl_base.structs.Pointer import Pointer


class Footer(MemStruct):
    footer_model: Pointer[str]
    ext_model: Pointer[str]
    joint_model: Pointer[str]
    unk_floats: Array[float]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
