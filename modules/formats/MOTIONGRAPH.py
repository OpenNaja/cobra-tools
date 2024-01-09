from generated.formats.motiongraph.compounds.MotiongraphHeader import MotiongraphHeader
from modules.formats.BaseFormat import MemStructLoader


class MotiongraphLoader(MemStructLoader):
	target_class = MotiongraphHeader
	extension = ".motiongraph"

	def collect(self):
		if self.ovl.version >= 19:
			# pass
			super().collect()

	def accept_string(self, in_str):
		"""Return True if string should receive replacement"""
		# anims have @ eg. Acrocanthosaurus@JumpAttackDefendFlankLeft
		if "@" in in_str:
			return True
		# sound events don't, eg. Acrocanthosaurus_FightReact
		return False
