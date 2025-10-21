from generated.bitfield import BasicBitfield
from generated.formats.ovl_base.enums.Compression import Compression


class VersionInfo(BasicBitfield):
    unk_1: bool
    unk_2: bool
    compression: Compression
    unk_3: bool
    use_djb: bool
