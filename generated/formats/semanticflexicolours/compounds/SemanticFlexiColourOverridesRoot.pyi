from generated.formats.ovl_base.compounds.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.semanticflexicolours.compounds.ColorOverride import ColorOverride
from generated.formats.semanticflexicolours.compounds.GameOverride import GameOverride


class SemanticFlexiColourOverridesRoot(MemStruct):
    color_overrides: ArrayPointer[ColorOverride]
    game_overrides: ArrayPointer[GameOverride]
    num_color_overrides: int
    num_game_overrides: int
    _z_0: int
    _z_1: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
