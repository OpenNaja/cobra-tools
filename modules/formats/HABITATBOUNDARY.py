from generated.formats.habitatboundary.compound.ClimbproofDataRoot import ClimbproofDataRoot
from generated.formats.habitatboundary.compound.HabitatBoundaryDataRoot import HabitatBoundaryDataRoot
from generated.formats.habitatboundary.compound.HabitatBoundaryPropRoot import HabitatBoundaryPropRoot
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
