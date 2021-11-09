# START_GLOBALS
from generated.formats.ovl.versions import *
from hashes import constants_jwe, constants_pz, constants_jwe2


# END_GLOBALS


class FileEntry:

	# START_CLASS

	def update_constants(self, ovl):
		"""Update the constants"""

		# update offset using the name buffer
		if is_jwe(ovl):
			constants = constants_jwe
		elif is_pz(ovl) or is_pz16(ovl):
			constants = constants_pz
		elif is_jwe2(ovl):
			constants = constants_jwe2
		else:
			raise ValueError(f"Unsupported game {get_game(ovl)}")
		self.unkn_0 = constants.files_unkn_0[self.ext]
		self.unkn_1 = constants.files_unkn_1[self.ext]
