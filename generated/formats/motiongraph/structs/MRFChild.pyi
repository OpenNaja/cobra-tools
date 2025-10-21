from generated.formats.motiongraph.structs.MRFMember1 import MRFMember1
from generated.formats.motiongraph.structs.Something import Something
from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.ovl_base.structs.Pointer import Pointer


class MRFChild(MemStruct):
    count_0: int
    m_r_f_member: Pointer[MRFMember1]
    ptr_1: Pointer[Something]
    count_1: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
