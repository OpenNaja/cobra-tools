from generated.formats.voxelskirt.structs.Material import Material


class EntityGroup(Material):
    ff: int
    ff_or_zero: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
