# START_GLOBALS
from generated.formats.ovl import *

lut_mime_version_jwe = {
	".fdb": 1,
	".banis": 5,
	".assetpkg": 2,
	".userinterfaceicondata": 1,
	".lua": 7,
	".txt": 2,
	".tex": 8,
	".ms2": 47,
	".mdl2": 47,
	".fgm": 6,
}

lut_mime_version_pz = {
	".fdb": 1,
	".bani": 5,
	".banis": 5,
	".assetpkg": 2,
	# ".userinterfaceicondata": 1,
	".lua": 7,
	".txt": 3,
	".tex": 9,
	".texturestream": 9,
	".ms2": 50,
	".mdl2": 50,
	".fgm": 6,
}


lut_mime_hash_jwe = {
	".assetpkg": 1145776474,
	".banis": 1177957172,
	".fdb": 2545474337,
	".fgm": 861771362,
	".mdl2": 4285397356,
	".ms2": 2893339803,
	".lua": 1779074288,
	".txt": 640591494,
	".tex": 3242366505,
	".userinterfaceicondata": 2127665351,
}

lut_mime_hash_pz = {
	".bani": 1380752341,
	".banis": 1177957172,
	".fgm": 861771362,
	".mdl2": 4285397382,
	".ms2": 2893339829,
	".tex": 3242366506,
	".texturestream": 4096653506,
	".assetpkg": 1145776474,
	".fdb": 2545474337,
	".lua": 1779074288,
	".txt": 640591495,
	# ".userinterfaceicondata": 2127665351,
}

# END_GLOBALS


class MimeEntry:

	# START_CLASS

	def update_constants(self, ovl):
		"""Update the constants"""

		# update offset using the name buffer
		if is_jwe(ovl):
			self.mime_hash = lut_mime_hash_jwe.get(self.ext)
			self.mime_version = lut_mime_version_jwe.get(self.ext)
		elif is_pz(ovl) or is_pz16(ovl):
			self.mime_hash = lut_mime_hash_pz.get(self.ext)
			self.mime_version = lut_mime_version_pz.get(self.ext)
		else:
			raise ValueError(f"Unsupported game {get_game(ovl)}")
