from generated.array import Array
from generated.formats.ovl_base.compounds.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer
from generated.formats.path.compounds.SupportSetData import SupportSetData


class WoodenSupportSetRoot(MemStruct):
    model_00: Pointer[str]
    model_08: Pointer[str]
    model_16: Pointer[str]
    model_24: Pointer[str]
    model_32: Pointer[str]
    model_40: Pointer[str]
    model_48: Pointer[str]
    model_56: Pointer[str]
    model_64: Pointer[str]
    model_72: Pointer[str]
    model_80: Pointer[str]
    model_88: Pointer[str]
    model_96: Pointer[str]
    model_104: Pointer[str]
    model_112: Pointer[str]
    model_120: Pointer[str]
    model_128: Pointer[str]
    model_136: Pointer[str]
    model_144: Pointer[str]
    model_152: Pointer[str]
    model_160: Pointer[str]
    model_168: Pointer[str]
    model_176: Pointer[str]
    model_184: Pointer[str]
    model_192: Pointer[str]
    model_200: Pointer[str]
    model_208: Pointer[str]
    model_216: Pointer[str]
    model_224: Pointer[str]
    model_232: Pointer[str]
    model_240: Pointer[str]
    unk_floats: Array[float]
    num_data: int
    data: ArrayPointer[SupportSetData]
    num_data_1: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
