from generated.base_struct import BaseStruct
from generated.formats.ovl.compounds.HeaderPointer import HeaderPointer


class RootEntry(BaseStruct):
    file_hash: int
    ext_hash: int
    struct_ptr: HeaderPointer

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
