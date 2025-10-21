from generated.formats.motiongraph.compounds.LuaModules import LuaModules
from generated.formats.motiongraph.compounds.MGTwo import MGTwo
from generated.formats.motiongraph.compounds.MRFMember1 import MRFMember1
from generated.formats.motiongraph.compounds.MRFMember2 import MRFMember2
from generated.formats.motiongraph.compounds.MotiongraphRootFrag import MotiongraphRootFrag
from generated.formats.motiongraph.compounds.StateArray import StateArray
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class MotiongraphHeader(MemStruct):
    root_frag: Pointer[MotiongraphRootFrag]
    state_output_entries: Pointer[StateArray]
    m_g_two: Pointer[MGTwo]
    m_r_f_member_1: Pointer[MRFMember1]
    count_0: int
    count_1: int
    lua_modules: Pointer[LuaModules]
    lua_results: Pointer[str]
    first_non_transition_state: Pointer[MRFMember2]
    empty_str: Pointer[str]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
