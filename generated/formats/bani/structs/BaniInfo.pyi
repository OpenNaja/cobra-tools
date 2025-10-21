from generated.base_struct import BaseStruct
from generated.formats.bani.structs.BaniRoot import BaniRoot


class BaniInfo(BaseStruct):
    name: str
    data: BaniRoot

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
