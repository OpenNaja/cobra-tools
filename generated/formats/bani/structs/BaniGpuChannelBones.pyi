from generated.base_struct import BaseStruct


class BaniGpuChannelBones(BaseStruct):
    write_index: int
    read_index: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
