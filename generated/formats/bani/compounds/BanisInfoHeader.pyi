from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.bani.compounds.BaniInfo import BaniInfo
from generated.formats.bani.compounds.BanisRoot import BanisRoot


class BanisInfoHeader(BaseStruct):
    version: int
    num_anims: int
    anims: Array[BaniInfo]
    data: BanisRoot

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
