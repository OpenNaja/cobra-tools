from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.voxelskirt.structs.Area import Area
from generated.formats.voxelskirt.structs.DataSlot import DataSlot
from generated.formats.voxelskirt.structs.EntityGroup import EntityGroup
from generated.formats.voxelskirt.structs.Layer import Layer
from generated.formats.voxelskirt.structs.Material import Material
from generated.formats.voxelskirt.structs.Name import Name


class VoxelskirtRoot(MemStruct):
    zero: int
    _data_size: int
    x: int
    y: int
    scale: float
    padding: int
    _height_offset: int
    _weights_offset: int
    layers: DataSlot[Layer]
    areas: DataSlot[Area]
    entity_groups: DataSlot[EntityGroup]
    materials: DataSlot[Material]
    names: DataSlot[Name]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
