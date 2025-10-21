from generated.formats.motiongraph.compounds.MRFMember1 import MRFMember1
from generated.formats.motiongraph.compounds.Something import Something
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class MRFChild(MemStruct):
    count_0: int
    m_r_f_member: Pointer[MRFMember1]
    ptr_1: Pointer[Something]
    count_1: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
