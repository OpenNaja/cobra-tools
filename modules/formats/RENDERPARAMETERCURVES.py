from generated.formats.renderparameters.compounds.RenderParameterCurvesRoot import RenderParameterCurvesRoot
from modules.formats.BaseFormat import MemStructLoader


class RenderParameterCurvesLoader(MemStructLoader):
    target_class = RenderParameterCurvesRoot
    extension = ".renderparametercurves"
