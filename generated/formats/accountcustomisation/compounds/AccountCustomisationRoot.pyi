from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class AccountCustomisationRoot(MemStruct):
    customization_uuid: Pointer[str]
    customization_name: Pointer[str]
    customization_description: Pointer[str]
    customization_id: Pointer[str]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
