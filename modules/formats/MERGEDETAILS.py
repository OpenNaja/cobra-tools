from generated.formats.mergedetails.compound.MergedetailsRoot import MergedetailsRoot
from modules.formats.BaseFormat import MemStructLoader


class MergeDetailsLoader(MemStructLoader):
	extension = ".mergedetails"
	target_class = MergedetailsRoot
