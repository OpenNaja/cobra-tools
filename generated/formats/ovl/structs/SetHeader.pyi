import numpy as np
from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.ovl.structs.AssetEntry import AssetEntry
from generated.formats.ovl.structs.SetEntry import SetEntry


class SetHeader(BaseStruct):
    set_count: int
    asset_count: int
    sig_a: int
    sig_b: int
    sets: np.ndarray[tuple[int], np.dtype[SetEntry]]
    assets: np.ndarray[tuple[int], np.dtype[AssetEntry]]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
