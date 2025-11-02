from generated.formats.motiongraph.structs.FloatInputData import FloatInputData
from generated.formats.ovl_base.structs.MemStruct import MemStruct


class FootPlantActivityData(MemStruct):
    flags: int
    weight: FloatInputData
    rotation_no_i_k_weight: FloatInputData
    sticky_feet_weight: FloatInputData

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
