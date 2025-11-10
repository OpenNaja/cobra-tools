from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.manis.structs.Buffer1 import Buffer1
from generated.formats.manis.structs.CompressedHeaderReader import CompressedHeaderReader
from generated.formats.manis.structs.KeysReader import KeysReader
from generated.formats.manis.structs.ManiInfo import ManiInfo
from generated.formats.manis.structs.ManisRoot import ManisRoot


class InfoHeader(BaseStruct):
    version: int
    mani_version: int
    mani_count: int
    stream: str
    names: Array[str]
    header: ManisRoot
    mani_infos: Array[ManiInfo]
    compressed_header: CompressedHeaderReader
    name_buffer: Buffer1
    keys_buffer: KeysReader

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
