from generated.formats.ovl_base.structs.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.ovl_base.structs.Pointer import Pointer
from generated.formats.ovl_base.structs.ZStringList import ZStringList
from generated.formats.vendingmachineinteractionsettings.structs.GuestAnimationInteractionList import GuestAnimationInteractionList


class VendingMachineInteractionSettingsRoot(MemStruct):
    animation_interaction: ArrayPointer[GuestAnimationInteractionList]
    animation_interaction_count: int
    float_1: float
    float_2: float
    unk_1: int
    animation_idle: Pointer[ZStringList]
    animation_idle_count: int
    unk_2: int
    animation_win: Pointer[ZStringList]
    animation_win_count: int
    unk_3: int
    animation_fail: Pointer[ZStringList]
    animation_fail_count: int
    float_3: float
    pad_0: int
    pad_1: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
