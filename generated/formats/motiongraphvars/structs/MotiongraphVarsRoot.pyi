from typing import Union
from generated.formats.motiongraphvars.structs.MotiongraphVar import MotiongraphVar
from generated.formats.motiongraphvars.structs.MotiongraphVars import MotiongraphVars
from generated.formats.ovl_base.structs.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.ovl_base.structs.Pointer import Pointer


class MotiongraphVarsRoot(MemStruct):
    vars_count: int
    vars: Union[ArrayPointer[MotiongraphVar], Pointer[MotiongraphVars]]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
