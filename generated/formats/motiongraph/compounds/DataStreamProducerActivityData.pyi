from generated.formats.motiongraph.compounds.CurveData import CurveData
from generated.formats.motiongraph.enums.TimeLimitMode import TimeLimitMode
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class DataStreamProducerActivityData(MemStruct):
    curve_type: int
    ds_name: Pointer[str]
    type: Pointer[str]
    bone_i_d: Pointer[str]
    location: Pointer[str]
    curve: CurveData
    time_limit_mode: TimeLimitMode
    data_stream_producer_flags: int
    prop_through_variable: Pointer[str]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
