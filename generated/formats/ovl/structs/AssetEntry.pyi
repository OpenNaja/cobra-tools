from generated.base_struct import BaseStruct


class AssetEntry(BaseStruct):
    file_hash: int
    ext_hash: int
    root_index: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
