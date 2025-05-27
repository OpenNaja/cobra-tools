from generated.formats.ovl_base.imports import name_type_map
import logging

from generated.formats.ovl_base.bitfields.VersionInfo import VersionInfo


class OvlContext(object):
	def __init__(self):
		self.version = 0
		self.is_dev = 0
		self.user_version = VersionInfo()

	def __repr__(self):
		return f"{self.version} | {self.user_version}"

	@classmethod
	def context_to_xml(cls, elem, prop, instance, arg, template, debug):
		try:
			elem.attrib[prop] = str(instance.game)
		except:
			logging.exception(f"Failed to get game from {instance}")
			from generated.formats.ovl.versions import get_game
			elem.attrib[prop] = str(get_game(instance)[0])

	@classmethod
	def context_from_xml(cls, target, elem, prop, arg, template):
		"""Creates object for parent object 'target', from parent element elem."""
		game_str = elem.attrib.get(prop)
		if game_str is None:
			return
		from generated.formats.ovl.versions import set_game
		if "." in game_str:
			game = game_str.split(".")[1]
		else:
			game = game_str
		set_game(target, game)
		return target
