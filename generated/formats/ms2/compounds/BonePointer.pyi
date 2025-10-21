from generated.formats.ms2.compounds.AbstractPointer import AbstractPointer


class BonePointer(AbstractPointer):
    index: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
