from generated.formats.ovl_base.structs.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.structs.ForEachPointer import ForEachPointer
from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.ovl_base.structs.Pointer import Pointer
from generated.formats.ovl_base.structs.ZStringList import ZStringList
from generated.formats.specdef.structs.DataPtr import DataPtr
from generated.formats.specdef.structs.NamePtr import NamePtr
from generated.formats.specdef.structs.Spec import Spec


class SpecdefRoot(MemStruct):
    attrib_count: int
    flags: int
    names_count: int
    childspecs_count: int
    managers_count: int
    scripts_count: int
    attribs: ArrayPointer[Spec]
    name_foreach_attribs: ForEachPointer[NamePtr]
    data_foreach_attribs: ForEachPointer[DataPtr]
    names: Pointer[ZStringList]
    childspecs: Pointer[ZStringList]
    managers: Pointer[ZStringList]
    scripts: Pointer[ZStringList]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
