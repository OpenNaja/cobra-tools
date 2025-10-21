from generated.base_struct import BaseStruct


class SetEntry(BaseStruct):
    file_hash: int
    ext_hash: int
    start: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
