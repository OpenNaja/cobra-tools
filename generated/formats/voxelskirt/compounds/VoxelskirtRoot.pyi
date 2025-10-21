from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.voxelskirt.compounds.Area import Area
from generated.formats.voxelskirt.compounds.DataSlot import DataSlot
from generated.formats.voxelskirt.compounds.EntityGroup import EntityGroup
from generated.formats.voxelskirt.compounds.Layer import Layer
from generated.formats.voxelskirt.compounds.Material import Material
from generated.formats.voxelskirt.compounds.Name import Name


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
