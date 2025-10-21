from generated.base_struct import BaseStruct
from generated.formats.voxelskirt.enums.VxlDtype import VxlDtype


class Layer(BaseStruct):
    _id: int
    dtype: VxlDtype
    _offset: int
    _data_size: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
