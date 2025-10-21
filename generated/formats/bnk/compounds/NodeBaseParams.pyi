from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.bnk.compounds.AdvSettingsParams import AdvSettingsParams
from generated.formats.bnk.compounds.AuxParams import AuxParams
from generated.formats.bnk.compounds.FXChunkBase import FXChunkBase
from generated.formats.bnk.compounds.InitialRTPC import InitialRTPC
from generated.formats.bnk.compounds.NodeInitialFxParams import NodeInitialFxParams
from generated.formats.bnk.compounds.NodeInitialParams import NodeInitialParams
from generated.formats.bnk.compounds.PositioningParams import PositioningParams
from generated.formats.bnk.compounds.StateChunk import StateChunk


class NodeBaseParams(BaseStruct):
    node_initial_fx_params: NodeInitialFxParams
    b_is_override_parent_metadata: int
    u_num_fx: int
    fx: Array[FXChunkBase]
    b_override_attachment_params: int
    override_bus_id: int
    direct_parent_i_d: int
    by_bit_vector: int
    node_initial_params: NodeInitialParams
    positioning_params: PositioningParams
    aux_params: AuxParams
    adv_settings_params: AdvSettingsParams
    state_chunk: StateChunk
    initial_r_t_p_c: InitialRTPC

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
