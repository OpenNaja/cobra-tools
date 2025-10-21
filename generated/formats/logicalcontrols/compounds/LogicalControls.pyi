from generated.formats.logicalcontrols.compounds.AxisButton import AxisButton
from generated.formats.logicalcontrols.compounds.AxisValue import AxisValue
from generated.formats.logicalcontrols.compounds.Button import Button
from generated.formats.logicalcontrols.compounds.Some import Some
from generated.formats.ovl_base.compounds.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class LogicalControls(MemStruct):
    buttons: ArrayPointer[Button]
    axes: ArrayPointer[AxisValue]
    axis_buttons: ArrayPointer[AxisButton]
    d: ArrayPointer[Some]
    button_count: int
    axis_count: int
    count_3: int
    count_4: int
    flags: int
    unsure: Pointer[str]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
