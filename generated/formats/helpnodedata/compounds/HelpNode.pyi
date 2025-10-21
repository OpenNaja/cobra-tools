from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class HelpNode(MemStruct):
    node_type: int
    node_help_user_interface_icon_data: Pointer[str]
    node_title_text_symbol: Pointer[str]
    node_description_text_symbol: Pointer[str]
    unknown_ptr_1: Pointer[str]
    unknown_ptr_2: Pointer[str]
    unknown_ptr_3: Pointer[str]
    unknown_ptr_4: Pointer[str]
    unknown_ptr_5: Pointer[str]
    unknown_ptr_6: Pointer[str]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
