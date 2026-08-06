
# START_GLOBALS
from generated.formats.ms2.structs import Model
from generated.formats.ms2.structs.BoneInfo import BoneInfo
from generated.formats.ovl_base.structs.MemStruct import MemStruct
# END_GLOBALS

class ModelInfo(MemStruct):
    # START_VARS
    model: 'Model'
    bone_info: 'BoneInfo'
    # END_VARS

    # START_CLASS
