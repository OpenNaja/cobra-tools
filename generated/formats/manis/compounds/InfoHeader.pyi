from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.manis.compounds.Buffer1 import Buffer1
from generated.formats.manis.compounds.KeysReader import KeysReader
from generated.formats.manis.compounds.ManiInfo import ManiInfo
from generated.formats.manis.compounds.ManisRoot import ManisRoot


class InfoHeader(BaseStruct):
    version: int
    mani_version: int
    mani_count: int
    stream: str
    names: Array[str]
    header: ManisRoot
    mani_infos: Array[ManiInfo]
    name_buffer: Buffer1
    keys_buffer: KeysReader

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
