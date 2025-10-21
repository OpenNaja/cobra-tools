from generated.formats.renderparameters.structs.RenderParametersRoot import RenderParametersRoot
from modules.formats.BaseFormat import MemStructLoader


class RenderParametersLoader(MemStructLoader):
    target_class = RenderParametersRoot
    extension = ".renderparameters"
