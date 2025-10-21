from generated.bitfield import BasicBitfield
from generated.formats.ms2.enums.MeshFormat import MeshFormat


class WeightsFlagPC2(BasicBitfield):
    mesh_format: MeshFormat
    material_effects: bool
    has_weights: bool
    bone_index: int
