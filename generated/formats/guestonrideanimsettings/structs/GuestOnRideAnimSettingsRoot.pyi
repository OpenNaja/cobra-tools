from generated.formats.guestonrideanimsettings.structs.RideAnims import RideAnims
from generated.formats.ovl_base.structs.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.structs.MemStruct import MemStruct


class GuestOnRideAnimSettingsRoot(MemStruct):
    ride_anims: ArrayPointer[RideAnims]
    count: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
