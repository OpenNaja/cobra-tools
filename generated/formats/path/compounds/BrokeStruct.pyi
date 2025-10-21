from generated.formats.base.compounds.Vector3 import Vector3
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class BrokeStruct(MemStruct):
    sup_model: Pointer[str]
    fallen_model: Pointer[str]
    cap_model: Pointer[str]
    unk_vector_1: Vector3
    unk_vector_2: Vector3

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
