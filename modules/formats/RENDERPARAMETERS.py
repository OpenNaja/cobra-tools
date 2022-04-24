from generated.formats.renderparameters.compound.RenderParametersRoot import RenderParametersRoot
from modules.formats.BaseFormat import MemStructLoader


class RenderParametersLoader(MemStructLoader):
    target_class = RenderParametersRoot
    extension = ".renderparameters"
