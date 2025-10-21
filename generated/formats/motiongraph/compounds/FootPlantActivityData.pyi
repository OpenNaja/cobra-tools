from generated.formats.motiongraph.compounds.FloatInputData import FloatInputData
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class FootPlantActivityData(MemStruct):
    weight: FloatInputData
    rotation_no_i_k_weight: FloatInputData
    sticky_feet_weight: FloatInputData

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
