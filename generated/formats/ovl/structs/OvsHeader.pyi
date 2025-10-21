import numpy as np
from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.ovl.structs.BufferEntry import BufferEntry
from generated.formats.ovl.structs.BufferGroup import BufferGroup
from generated.formats.ovl.structs.DataEntry import DataEntry
from generated.formats.ovl.structs.Fragment import Fragment
from generated.formats.ovl.structs.MemPool import MemPool
from generated.formats.ovl.structs.PoolGroup import PoolGroup
from generated.formats.ovl.structs.RootEntry import RootEntry
from generated.formats.ovl.structs.SetHeader import SetHeader


class OvsHeader(BaseStruct):
    pool_groups: Array[PoolGroup]
    pools: Array[MemPool]
    data_entries: Array[DataEntry]
    buffer_entries: Array[BufferEntry]
    buffer_groups: Array[BufferGroup]
    root_entries: np.ndarray[tuple[int], np.dtype[RootEntry]]
    fragments: np.ndarray[tuple[int], np.dtype[Fragment]]
    set_header: SetHeader

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
