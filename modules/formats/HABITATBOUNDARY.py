from generated.formats.habitatboundary.structs.ClimbproofDataRoot import ClimbproofDataRoot
from generated.formats.habitatboundary.structs.HabitatBoundaryDataRoot import HabitatBoundaryDataRoot
from generated.formats.habitatboundary.structs.HabitatBoundaryPropRoot import HabitatBoundaryPropRoot
from modules.formats.BaseFormat import MemStructLoader


class HabitatBoundaryPropLoader(MemStructLoader):
	target_class = HabitatBoundaryPropRoot
	extension = ".habitatboundaryprop"


class HabitatBoundaryDataLoader(MemStructLoader):
	target_class = HabitatBoundaryDataRoot
	extension = ".habitatboundarydata"


class ClimbproofDataLoader(MemStructLoader):
	target_class = ClimbproofDataRoot
	extension = ".climbproofdata"
