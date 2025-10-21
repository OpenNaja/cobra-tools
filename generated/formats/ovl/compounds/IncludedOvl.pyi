from generated.base_struct import BaseStruct


class IncludedOvl(BaseStruct):
    basename: str

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
