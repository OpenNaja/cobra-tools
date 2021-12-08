from generated.formats.ovl_base.bitfield.VersionInfo import VersionInfo


class OvlContext(object):
	def __init__(self):
		self.version = 0
		self.user_version = VersionInfo()

	def __repr__(self):
		return f"{self.version} | {self.user_version}"