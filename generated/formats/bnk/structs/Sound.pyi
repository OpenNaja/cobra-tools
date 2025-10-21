from generated.formats.bnk.structs.AkBankSourceData import AkBankSourceData
from generated.formats.bnk.structs.HircObject import HircObject
from generated.formats.bnk.structs.NodeBaseParams import NodeBaseParams


class Sound(HircObject):
    ak_bank_source_data: AkBankSourceData
    node_base_params: NodeBaseParams

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
