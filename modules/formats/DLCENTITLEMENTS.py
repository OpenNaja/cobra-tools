from generated.formats.dlcentitlements.compounds.DLCEntitlementsRoot import DLCEntitlementsRoot
from modules.formats.BaseFormat import MemStructLoader


class DLCEntitlementsLoader(MemStructLoader):
    target_class = DLCEntitlementsRoot
    extension = ".dlcentitlements"
