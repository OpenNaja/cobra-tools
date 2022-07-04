import logging

from generated.formats.motiongraph.compound.MotiongraphHeader import MotiongraphHeader
from modules.formats.BaseFormat import MemStructLoader
from ovl_util.interaction import showdialog


class MotiongraphLoader(MemStructLoader):
	target_class = MotiongraphHeader
	extension = ".motiongraph"

	def rename_content(self, name_tuples):
		logging.info("Renaming inside .motiongraph")
		byte_name_tups = []
		try:
			for old, new in name_tuples:
				assert len(old) == len(new)
				byte_name_tups.append((old.encode(), new.encode()))
			for fragment in self.fragments:
				fragment.struct_ptr.replace_bytes(byte_name_tups)
		except Exception as err:
			showdialog(str(err))
		logging.info("Done!")
