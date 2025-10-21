from generated.formats.dinosaurmaterialvariants.compounds.CommonHeader import CommonHeader
from generated.formats.dinosaurmaterialvariants.compounds.Variant import Variant
from generated.formats.ovl_base.compounds.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compounds.Pointer import Pointer


class DinoVariantsHeader(CommonHeader):
    has_sets: int
    set_name: Pointer[str]
    variants: ArrayPointer[Variant]
    variant_count: int
    zero: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
