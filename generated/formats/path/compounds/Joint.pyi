from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class Joint(MemStruct):
    joint_model_1: Pointer[str]
    joint_model_2: Pointer[str]
    joint_model_3: Pointer[str]
    joint_model_4: Pointer[str]
    unk_float: float
    unk_int: int
    unk_int_2: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
