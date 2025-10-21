from generated.base_struct import BaseStruct


class Object(BaseStruct):
    material_index: int
    mesh_index: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
