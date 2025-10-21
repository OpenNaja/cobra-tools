from generated.base_struct import BaseStruct


class PoolGroup(BaseStruct):
    type: int
    num_pools: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
