from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.ms2.structs.InfoZTMemPool import InfoZTMemPool
from generated.formats.ovl_base.structs.SmartPadding import SmartPadding


class StreamsZTHeader(BaseStruct):
    weird_padding: SmartPadding
    unks: Array[InfoZTMemPool]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
