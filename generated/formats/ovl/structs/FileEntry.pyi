from generated.base_struct import BaseStruct


class FileEntry(BaseStruct):
    basename: str
    file_hash: int
    pool_type: int
    set_pool_type: int
    extension: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
