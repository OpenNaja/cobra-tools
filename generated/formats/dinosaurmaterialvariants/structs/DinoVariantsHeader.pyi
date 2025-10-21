from generated.formats.dinosaurmaterialvariants.structs.CommonHeader import CommonHeader
from generated.formats.dinosaurmaterialvariants.structs.Variant import Variant
from generated.formats.ovl_base.structs.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.structs.Pointer import Pointer


class DinoVariantsHeader(CommonHeader):
    has_sets: int
    set_name: Pointer[str]
    variants: ArrayPointer[Variant]
    variant_count: int
    zero: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
