from generated.formats.datastreams.compounds.DataStreamsSettings import DataStreamsSettings
from generated.formats.ovl_base.compounds.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class DataStreamsRoot(MemStruct):
    count: int
    layer_list: ArrayPointer[DataStreamsSettings]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
