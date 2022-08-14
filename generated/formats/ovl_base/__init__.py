from generated.formats.ovl_base.bitfields.VersionInfo import VersionInfo


class OvlContext(object):
	def __init__(self):
		self.version = 0
		self.user_version = VersionInfo()

	def __repr__(self):
		return f"{self.version} | {self.user_version}"

	@classmethod
	def to_xml(cls, elem, prop, instance, arguments, debug):
		from generated.formats.ovl.versions import get_game
		elem.attrib[prop] = str(get_game(instance)[0])
