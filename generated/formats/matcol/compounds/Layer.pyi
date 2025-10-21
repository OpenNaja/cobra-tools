from generated.formats.matcol.compounds.BoolAttrib import BoolAttrib
from generated.formats.matcol.compounds.FloatAttrib import FloatAttrib
from generated.formats.ovl_base.compounds.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class Layer(MemStruct):
    layer_name: Pointer[str]
    zero_0: int
    zero_1: int
    float_attributes: ArrayPointer[FloatAttrib]
    float_attributes_count: int
    zero_2: int
    zero_3: int
    bool_attributes: ArrayPointer[BoolAttrib]
    bool_attributes_count: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
