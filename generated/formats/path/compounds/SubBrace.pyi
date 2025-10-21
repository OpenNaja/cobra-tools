from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class SubBrace(MemStruct):
    brace_model_1: Pointer[str]
    brace_model_2: Pointer[str]
    brace_model_3: Pointer[str]
    brace_model_4: Pointer[str]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
