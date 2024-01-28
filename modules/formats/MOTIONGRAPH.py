from generated.formats.motiongraph.compounds.MotiongraphHeader import MotiongraphHeader
# import generated.formats.ovl.versions as ovl_versions
from modules.formats.BaseFormat import MemStructLoader


class MotiongraphLoader(MemStructLoader):
	target_class = MotiongraphHeader
	extension = ".motiongraph"

	def collect(self):
		if self.ovl.version >= 19:
			# structs are too different, doesn't register anim names, would break rename contents
			# if ovl_versions.is_jwe(self.ovl):
			# 	return
			super().collect()

	def accept_string(self, in_str):
		"""Return True if string should receive replacement"""
		# anims have @ eg. Acrocanthosaurus@JumpAttackDefendFlankLeft
		if "@" in in_str:
			return True
		# sound events don't, eg. Acrocanthosaurus_FightReact
		return False
