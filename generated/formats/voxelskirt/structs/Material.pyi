from generated.base_struct import BaseStruct
from generated.formats.voxelskirt.structs.DataSlot import DataSlot
from generated.formats.voxelskirt.structs.EntityInstance import EntityInstance


class Material(BaseStruct):
    entity_instances: DataSlot[EntityInstance]
    _id: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
