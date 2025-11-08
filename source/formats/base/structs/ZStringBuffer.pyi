from generated.base_struct import BaseStruct


class ZStringBuffer(BaseStruct):
    data: bytes
    strings: list[str]
    offset_dic: dict[str, int]
    offset_2_str: dict[int, str]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
