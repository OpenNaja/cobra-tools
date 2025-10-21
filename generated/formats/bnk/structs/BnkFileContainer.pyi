from generated.formats.bnk.structs.BnkBufferData import BnkBufferData
from generated.formats.ovl_base.structs.GenericHeader import GenericHeader


class BnkFileContainer(GenericHeader):
    bnk_header: BnkBufferData

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
