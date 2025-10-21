from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer
from generated.formats.renderparameters.compounds.ParamData import ParamData
from generated.formats.renderparameters.enums.RenderParameterType import RenderParameterType


class Param(MemStruct):
    attribute_name: Pointer[str]
    dtype: RenderParameterType
    unused: int
    data: ParamData

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
