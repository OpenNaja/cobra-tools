from generated.base_struct import BaseStruct
from generated.formats.manis.structs.CompressedHeader import CompressedHeader


class CompressedHeaderReader(BaseStruct):
    data: CompressedHeader

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
