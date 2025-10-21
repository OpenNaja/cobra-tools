from generated.base_struct import BaseStruct
from generated.formats.dds.enums.D3D10ResourceDimension import D3D10ResourceDimension
from generated.formats.dds.enums.DxgiFormat import DxgiFormat


class Dxt10Header(BaseStruct):
    dxgi_format: DxgiFormat
    resource_dimension: D3D10ResourceDimension
    misc_flag: int
    num_tiles: int
    misc_flag_2: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
