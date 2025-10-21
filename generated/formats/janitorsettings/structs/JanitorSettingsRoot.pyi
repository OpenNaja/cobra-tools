from generated.array import Array
from generated.formats.janitorsettings.structs.JanitorBetweenArrays import JanitorBetweenArrays
from generated.formats.janitorsettings.structs.JanitorEnd import JanitorEnd
from generated.formats.janitorsettings.structs.JanitorPreCount import JanitorPreCount
from generated.formats.janitorsettings.structs.UIntPair import UIntPair
from generated.formats.ovl_base.structs.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.structs.MemStruct import MemStruct


class JanitorSettingsRoot(MemStruct):
    array_0: ArrayPointer[float]
    array_1: ArrayPointer[float]
    array_2: ArrayPointer[int]
    array_3: ArrayPointer[float]
    array_4: ArrayPointer[float]
    array_0: ArrayPointer[UIntPair]
    array_1: ArrayPointer[UIntPair]
    between_arrays: JanitorBetweenArrays
    array_2: ArrayPointer[UIntPair]
    array_3: ArrayPointer[UIntPair]
    array_4: ArrayPointer[UIntPair]
    array_5: ArrayPointer[UIntPair]
    array_6: ArrayPointer[int]
    array_7: ArrayPointer[int]
    array_8: ArrayPointer[int]
    array_9: ArrayPointer[float]
    array_10: ArrayPointer[float]
    array_11: ArrayPointer[float]
    array_12: ArrayPointer[float]
    array_13: ArrayPointer[float]
    array_14: ArrayPointer[float]
    janitor_pre_count: JanitorPreCount
    num_array_0: int
    num_array_1: int
    num_array_2: int
    num_array_3: int
    num_array_4: int
    num_array_5: int
    num_array_6: int
    num_array_7: int
    num_array_8: int
    num_array_9: int
    num_array_10: int
    num_array_11: int
    num_array_12: int
    num_array_13: int
    num_array_14: int
    padding: Array[int]
    array_pc_2: ArrayPointer[int]
    janitor_end: JanitorEnd

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
