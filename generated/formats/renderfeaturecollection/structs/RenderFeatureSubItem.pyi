from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.ovl_base.structs.Pointer import Pointer


class RenderFeatureSubItem(MemStruct):
    sub_item_name: Pointer[str]
    sub_item_value_or_flags: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
