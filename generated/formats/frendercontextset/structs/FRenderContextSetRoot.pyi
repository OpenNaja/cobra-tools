from generated.formats.frendercontextset.structs.ContextSet1Item import ContextSet1Item
from generated.formats.frendercontextset.structs.RenderFeature import RenderFeature
from generated.formats.frendercontextset.structs.RenderLayer import RenderLayer
from generated.formats.ovl_base.structs.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.structs.MemStruct import MemStruct


class FRenderContextSetRoot(MemStruct):
    ptr_1_list: ArrayPointer[ContextSet1Item]
    ptr_1_count: int
    render_layers: ArrayPointer[RenderLayer]
    render_layers_count: int
    render_features: ArrayPointer[RenderFeature]
    render_features_count: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
