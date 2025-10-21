from generated.formats.motiongraph.structs.DataStreamResourceData import DataStreamResourceData
from generated.formats.ovl_base.structs.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.structs.MemStruct import MemStruct


class DataStreamResourceDataList(MemStruct):
    data_stream_resource_data_count: int
    data_stream_resource_data: ArrayPointer[DataStreamResourceData]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
