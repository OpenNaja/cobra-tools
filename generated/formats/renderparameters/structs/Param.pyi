from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.ovl_base.structs.Pointer import Pointer
from generated.formats.renderparameters.enums.RenderParameterType import RenderParameterType
from generated.formats.renderparameters.structs.ParamData import ParamData


class Param(MemStruct):
    attribute_name: Pointer[str]
    dtype: RenderParameterType
    unused: int
    data: ParamData

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
