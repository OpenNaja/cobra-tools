from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.specdef.enums.SpecdefDtype import SpecdefDtype


class Spec(MemStruct):
    dtype: SpecdefDtype

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
