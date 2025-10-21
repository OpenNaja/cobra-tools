from generated.formats.ovl_base.compounds.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.particleeffect.compounds.Effect import Effect
from generated.formats.particleeffect.compounds.Effect07 import Effect07
from generated.formats.particleeffect.compounds.Effect08 import Effect08
from generated.formats.particleeffect.compounds.Effect09 import Effect09
from generated.formats.particleeffect.compounds.Effect10 import Effect10
from generated.formats.particleeffect.compounds.Effect11 import Effect11
from generated.formats.particleeffect.compounds.Effect12 import Effect12
from generated.formats.particleeffect.compounds.Effect13 import Effect13
from generated.formats.particleeffect.compounds.Effect14 import Effect14
from generated.formats.particleeffect.compounds.Effect15 import Effect15
from generated.formats.particleeffect.compounds.Effect16 import Effect16
from generated.formats.particleeffect.compounds.Effect21 import Effect21
from generated.formats.particleeffect.compounds.EffectRef import EffectRef
from generated.formats.particleeffect.compounds.LastRow import LastRow
from generated.formats.particleeffect.compounds.NextRow1 import NextRow1
from generated.formats.particleeffect.compounds.TextureData import TextureData


class ParticleEffectRoot(MemStruct):
    unk_64_1: int
    unk_64_2: int
    unk_64_3: int
    unk_64_4: int
    unk_64_5: int
    unk_64_6: int
    unk_32_1: int
    unk_32_2_neg: int
    unk_32_3: int
    unk_32_4: int
    a_unk_32_1: int
    a_unk_32_2: int
    a_unk_32_3_1: int
    a_unk_32_4: int
    atlasinfo_count: int
    name_foreach_textures: ArrayPointer[TextureData]
    next_row_1: NextRow1
    effect_00: EffectRef[Effect]
    effect_01: EffectRef[Effect]
    effect_02: EffectRef[Effect]
    effect_03: EffectRef[Effect]
    effect_04: EffectRef[Effect]
    effect_05: EffectRef[Effect]
    effect_06: EffectRef[Effect]
    effect_07: EffectRef[Effect07]
    effect_08: EffectRef[Effect08]
    effect_09: EffectRef[Effect09]
    effect_10: EffectRef[Effect10]
    effect_11: EffectRef[Effect11]
    effect_12: EffectRef[Effect12]
    effect_13: EffectRef[Effect13]
    effect_14: EffectRef[Effect14]
    effect_15: EffectRef[Effect15]
    effect_16: EffectRef[Effect16]
    effect_17: EffectRef[Effect]
    effect_18: EffectRef[Effect]
    effect_19: EffectRef[Effect]
    effect_20: EffectRef[Effect]
    effect_21: EffectRef[Effect21]
    effect_22: EffectRef[Effect]
    effect_23: EffectRef[Effect]
    effect_24: EffectRef[Effect]
    effect_25: EffectRef[Effect]
    effect_26: EffectRef[Effect]
    next_row_5: LastRow

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
