# START_GLOBALS
from generated.formats.ovl import *
from hashes import constants_jwe, constants_pz


# END_GLOBALS


class MimeEntry:

	# START_CLASS

	def update_constants(self, ovl):
		"""Update the constants"""

		# update offset using the name buffer
		if is_jwe(ovl):
			constants = constants_jwe
		elif is_pz(ovl) or is_pz16(ovl):
			constants = constants_pz
		else:
			raise ValueError(f"Unsupported game {get_game(ovl)}")
		self.name = constants.mimes_name.get(self.ext)
		self.mime_hash = constants.mimes_mime_hash.get(self.ext)
		self.mime_version = constants.mimes_mime_version.get(self.ext)
