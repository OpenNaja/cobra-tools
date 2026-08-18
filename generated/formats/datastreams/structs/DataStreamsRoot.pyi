from generated.formats.datastreams.structs.DataStreamsSettings import DataStreamsSettings
from generated.formats.ovl_base.structs.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.structs.MemStruct import MemStruct


class DataStreamsRoot(MemStruct):
    layers_count: int
    layers: ArrayPointer[DataStreamsSettings]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
