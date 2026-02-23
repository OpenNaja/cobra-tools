from generated.formats.ovl_base.structs.MemStruct import MemStruct


class ManisRoot(MemStruct):
    mani_files_size: int
    hash_block_size: int
    zero_0: int
    zero_1: int
    zero_2: int
    zero_3: int
    zero_4: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
