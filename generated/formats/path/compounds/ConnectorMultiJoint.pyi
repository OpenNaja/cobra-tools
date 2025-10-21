from generated.formats.ovl_base.compounds.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer
from generated.formats.path.compounds.Joint import Joint


class ConnectorMultiJoint(MemStruct):
    connector_model: Pointer[str]
    support_model: Pointer[str]
    joints: ArrayPointer[Joint]
    num_joints: int
    extent_min: float
    extent_max: float
    some_index: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
