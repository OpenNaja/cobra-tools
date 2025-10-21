from generated.bitfield import BasicBitfield
from generated.formats.ms2.enums.MeshFormat import MeshFormat


class WeightsFlagMalta(BasicBitfield):
    mesh_format: MeshFormat
    has_weights: bool
    bone_index: int
