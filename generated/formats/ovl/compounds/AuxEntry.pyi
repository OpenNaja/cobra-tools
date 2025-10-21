from generated.base_struct import BaseStruct


class AuxEntry(BaseStruct):
    file_index: int
    basename: str
    size: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
