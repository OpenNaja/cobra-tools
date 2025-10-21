from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.ovl_base.structs.Pointer import Pointer


class Connector(MemStruct):
    connector_model: Pointer[str]
    joint_model: Pointer[str]
    new: Pointer[str]
    angle_limit: float
    direction: float

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
