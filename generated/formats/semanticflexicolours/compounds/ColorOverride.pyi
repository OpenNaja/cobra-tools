from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer
from generated.formats.semanticflexicolours.compounds.FloatColor import FloatColor


class ColorOverride(MemStruct):
    flexi_name: Pointer[str]
    color: FloatColor

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
