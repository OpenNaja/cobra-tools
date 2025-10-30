from generated.base_struct import BaseStruct


class AkGameSync(BaseStruct):
    ul_group: int
    e_group_type: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
