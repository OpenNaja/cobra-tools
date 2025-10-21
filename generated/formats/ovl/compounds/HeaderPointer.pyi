from generated.base_struct import BaseStruct


class HeaderPointer(BaseStruct):
    pool_index: int
    data_offset: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
