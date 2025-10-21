from generated.base_struct import BaseStruct


class DataPointer(BaseStruct):
    wem_id: int
    data_section_offset: int
    wem_filesize: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
