from generated.formats.ovl_base.structs.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.ovl_base.structs.Pointer import Pointer
from generated.formats.path.structs.Joint import Joint


class ConnectorMultiJoint(MemStruct):
    connector_model: Pointer[str]
    support_model: Pointer[str]
    joints: ArrayPointer[Joint]
    num_joints: int
    extent_min: float
    extent_max: float
    some_index: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
