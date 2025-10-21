from generated.base_struct import BaseStruct


class ArchiveEntry(BaseStruct):
    name: str
    pools_offset: int
    stream_files_offset: int
    num_pools: int
    num_datas: int
    num_pool_groups: int
    num_buffer_groups: int
    num_buffers: int
    num_fragments: int
    num_root_entries: int
    read_start: int
    set_data_size: int
    compressed_size: int
    uncompressed_size: int
    pools_start: int
    pools_end: int
    ovs_offset: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
