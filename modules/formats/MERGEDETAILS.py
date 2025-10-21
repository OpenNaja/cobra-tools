from generated.formats.mergedetails.structs.MergedetailsRoot import MergedetailsRoot
from modules.formats.BaseFormat import MemStructLoader


class MergeDetailsLoader(MemStructLoader):
	extension = ".mergedetails"
	target_class = MergedetailsRoot
