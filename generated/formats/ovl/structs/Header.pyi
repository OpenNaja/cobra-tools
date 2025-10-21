import numpy as np
from generated.array import Array
from generated.formats.base.structs.PadAlign import PadAlign
from generated.formats.base.structs.ZStringBufferPadded import ZStringBufferPadded
from generated.formats.ovl.structs.ArchiveEntry import ArchiveEntry
from generated.formats.ovl.structs.ArchiveMeta import ArchiveMeta
from generated.formats.ovl.structs.AuxEntry import AuxEntry
from generated.formats.ovl.structs.DependencyEntry import DependencyEntry
from generated.formats.ovl.structs.FileEntry import FileEntry
from generated.formats.ovl.structs.IncludedOvl import IncludedOvl
from generated.formats.ovl.structs.MimeEntry import MimeEntry
from generated.formats.ovl.structs.StreamEntry import StreamEntry
from generated.formats.ovl.structs.Triplet import Triplet
from generated.formats.ovl_base.structs.Empty import Empty
from generated.formats.ovl_base.structs.GenericHeader import GenericHeader


class Header(GenericHeader):
    num_ovs_types: int
    len_names: int
    zero_2: int
    num_aux_entries: int
    num_included_ovls: int
    num_mimes: int
    num_files: int
    num_files_2: int
    num_dependencies: int
    num_archives: int
    num_pool_groups: int
    num_pools: int
    num_datas: int
    num_buffers: int
    num_stream_files: int
    ztuac_unk_0: int
    ztuac_unk_1: int
    ztuac_unk_2: int
    len_archive_names: int
    num_files_3: int
    len_type_names: int
    num_triplets: int
    reserved: Array[int]
    names: ZStringBufferPadded
    names_pad_dla: Array[int]
    mimes: np.ndarray[tuple[int], np.dtype[MimeEntry]]
    triplets_ref: Empty
    triplets: np.ndarray[tuple[int], np.dtype[Triplet]]
    triplets_pad: PadAlign[object]
    files: np.ndarray[tuple[int], np.dtype[FileEntry]]
    archive_names: ZStringBufferPadded
    archives: Array[ArchiveEntry]
    included_ovls: np.ndarray[tuple[int], np.dtype[IncludedOvl]]
    dependencies: np.ndarray[tuple[int], np.dtype[DependencyEntry]]
    aux_entries: np.ndarray[tuple[int], np.dtype[AuxEntry]]
    dependencies: np.ndarray[tuple[int], np.dtype[DependencyEntry]]
    stream_files: np.ndarray[tuple[int], np.dtype[StreamEntry]]
    archives_meta: np.ndarray[tuple[int], np.dtype[ArchiveMeta]]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
