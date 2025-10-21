from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class BiomeDesignSettingsRoot(MemStruct):
    sandbox_initial_save_relative_file_path: Pointer[str]
    sandbox_world_name: Pointer[str]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
