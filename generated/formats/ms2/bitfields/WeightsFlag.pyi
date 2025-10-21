from generated.bitfield import BasicBitfield
from generated.formats.ms2.enums.MeshFormat import MeshFormat


class WeightsFlag(BasicBitfield):
    has_weights: bool
    bone_index: int
    mesh_format: MeshFormat
