from generated.formats.frendercontextset.compounds.FeatureOption import FeatureOption
from generated.formats.ovl_base.compounds.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class RenderFeature(MemStruct):
    feature_name: Pointer[str]
    options: ArrayPointer[FeatureOption]
    count: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
