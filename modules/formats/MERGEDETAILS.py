from generated.formats.mergedetails.compounds.MergedetailsRoot import MergedetailsRoot
from modules.formats.BaseFormat import MemStructLoader


class MergeDetailsLoader(MemStructLoader):
	extension = ".mergedetails"
	target_class = MergedetailsRoot
