from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class NextRow1(MemStruct):
    unk: int
    maybe_hash: int
    count: int
    count_repeat: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
