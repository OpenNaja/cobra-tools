from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.ovl_base.structs.Pointer import Pointer
from generated.formats.researchdata.structs.FxDataName import FxDataName
from generated.formats.researchdata.structs.FxDataSettings import FxDataSettings


class SubResearchFXData(MemStruct):
    fx_name: Pointer[FxDataName]
    fx_params: Pointer[FxDataSettings]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
