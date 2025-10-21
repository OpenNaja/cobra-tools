from generated.formats.guestonrideanimsettings.compounds.RideAnims import RideAnims
from generated.formats.ovl_base.compounds.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class GuestOnRideAnimSettingsRoot(MemStruct):
    ride_anims: ArrayPointer[RideAnims]
    count: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
