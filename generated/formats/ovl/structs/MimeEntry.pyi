from generated.base_struct import BaseStruct


class MimeEntry(BaseStruct):
    name: str
    zero_0: int
    mime_hash: int
    mime_version: int
    file_index_offset: int
    file_count: int
    zero_1: int
    triplet_count: int
    triplet_offset: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
