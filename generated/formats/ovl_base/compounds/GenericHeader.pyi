from generated.base_struct import BaseStruct
from generated.formats.base.compounds.FixedString import FixedString
from generated.formats.ovl_base.bitfields.VersionInfo import VersionInfo


class GenericHeader(BaseStruct):
    magic: FixedString
    version_flag: int
    version: int
    bitswap: int
    seventh_byte: int
    user_version: VersionInfo

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
