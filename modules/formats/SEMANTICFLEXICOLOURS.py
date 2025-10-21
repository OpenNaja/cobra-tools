from generated.formats.semanticflexicolours.structs.SemanticFlexiColourOverridesRoot import \
    SemanticFlexiColourOverridesRoot
from generated.formats.semanticflexicolours.structs.SemanticFlexiColoursRoot import SemanticFlexiColoursRoot
from modules.formats.BaseFormat import MemStructLoader


class SemanticFlexiColoursLoader(MemStructLoader):
    target_class = SemanticFlexiColoursRoot
    extension = ".semanticflexicolours"


class SemanticFlexiColourOverridesLoader(MemStructLoader):
    target_class = SemanticFlexiColourOverridesRoot
    extension = ".semanticflexicolouroverrides"
