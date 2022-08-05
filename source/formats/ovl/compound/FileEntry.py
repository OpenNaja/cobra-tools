# START_GLOBALS
from generated.formats.ovl.versions import *
from hashes import constants_jwe, constants_pz, constants_jwe2, constants_pc, constants_dla


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
		elif is_pc(ovl):
			constants = constants_pc
		elif is_dla(ovl):
			constants = constants_dla
		else:
			raise ValueError(f"Unsupported game {get_game(ovl)}")
		self.pool_type = constants.files_pool_type[self.ext]
		self.set_pool_type = constants.files_set_pool_type[self.ext]
