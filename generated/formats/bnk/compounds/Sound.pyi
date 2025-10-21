from generated.formats.bnk.compounds.AkBankSourceData import AkBankSourceData
from generated.formats.bnk.compounds.HircObject import HircObject
from generated.formats.bnk.compounds.NodeBaseParams import NodeBaseParams


class Sound(HircObject):
    ak_bank_source_data: AkBankSourceData
    node_base_params: NodeBaseParams

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
