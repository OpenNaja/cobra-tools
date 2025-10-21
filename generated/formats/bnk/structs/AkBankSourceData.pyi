from generated.base_struct import BaseStruct
from generated.formats.bnk.bitfields.UlPluginID import UlPluginID
from generated.formats.bnk.enums.AKBKSourceType import AKBKSourceType
from generated.formats.bnk.structs.AkMediaInformation import AkMediaInformation


class AkBankSourceData(BaseStruct):
    ul_plugin_i_d: UlPluginID
    stream_type: AKBKSourceType
    ak_media_information: AkMediaInformation
    size: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
