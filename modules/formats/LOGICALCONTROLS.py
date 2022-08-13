from generated.formats.logicalcontrols.compounds.LogicalControls import LogicalControls
from modules.formats.BaseFormat import MemStructLoader


class LogicalControlsLoader(MemStructLoader):
    target_class = LogicalControls
    extension = ".logicalcontrols"
