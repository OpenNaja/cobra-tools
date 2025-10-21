from generated.formats.motiongraph.compounds.DataStreamResourceDataList import DataStreamResourceDataList
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class VariableBlendedAnimationData(MemStruct):
    animation: Pointer[str]
    value: float
    _pad: int
    additional_data_streams: DataStreamResourceDataList

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
