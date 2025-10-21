from generated.base_struct import BaseStruct


class MemPool(BaseStruct):
    zero_1: int
    size: int
    offset: int
    zero_2: int
    file_hash: int
    num_files: int
    num_datas: int
    ext_hash: int
    zero_3: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
