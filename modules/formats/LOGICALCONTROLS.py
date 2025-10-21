from generated.formats.logicalcontrols.structs.LogicalControls import LogicalControls
from modules.formats.BaseFormat import MemStructLoader


class LogicalControlsLoader(MemStructLoader):
    target_class = LogicalControls
    extension = ".logicalcontrols"
