from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer
from generated.formats.posedriverdef.compounds.Data import Data


class Driver(MemStruct):
    joint_name: Pointer[str]
    a: int
    b: int
    c: int
    d: int
    driven_joint_name: Pointer[str]
    unk_1: int
    data: Pointer[Data]
    unk_2: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
