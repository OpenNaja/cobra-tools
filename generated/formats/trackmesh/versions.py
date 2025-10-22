from enum import Enum

from generated.base_version import VersionBase
from generated.formats.ovl_base.bitfields.VersionInfo import VersionInfo


def is_dla(context):
	if context.version == 15:
		return True


def set_dla(context):
	context.version = 15


def is_jwe(context):
	if context.version == 19 and context.user_version in (24724, 25108, 24596):
		return True


def set_jwe(context):
	context.version = 19
	context.user_version._value = 24724


def is_jwe2(context):
	if context.version == 20 and context.user_version in (24724, 25108, 24596) and context.is_dev == 0:
		return True


def set_jwe2(context):
	context.version = 20
	context.user_version._value = 24724
	context.is_dev = 0


def is_jwe2dev(context):
	if context.version == 20 and context.user_version in (24724, 25108, 24596) and context.is_dev == 1:
		return True


def set_jwe2dev(context):
	context.version = 20
	context.user_version._value = 24724
	context.is_dev = 1


def is_jwe3(context):
	if context.version == 20 and context.user_version in (24724, 25108, 24596) and context.is_dev == 0:
		return True


def set_jwe3(context):
	context.version = 20
	context.user_version._value = 24724
	context.is_dev = 0


def is_pc(context):
	if context.version == 18 and context.user_version in (8340, 8724, 8212) and context.version_flag == 8:
		return True


def set_pc(context):
	context.version = 18
	context.user_version._value = 8340
	context.version_flag = 8


def is_pc2(context):
	if context.version == 20 and context.user_version in (8340, 8724, 8212):
		return True


def set_pc2(context):
	context.version = 20
	context.user_version._value = 8340


def is_pz(context):
	if context.version == 19 and context.user_version in (8340, 8724, 8212):
		return True


def set_pz(context):
	context.version = 19
	context.user_version._value = 8340


def is_pz16(context):
	if context.version == 20 and context.user_version in (8340, 8724, 8212):
		return True


def set_pz16(context):
	context.version = 20
	context.user_version._value = 8340


def is_war(context):
	if context.version == 20 and context.user_version in (24724, 25108, 24596) and context.is_dev == 0:
		return True


def set_war(context):
	context.version = 20
	context.user_version._value = 24724
	context.is_dev = 0


def is_ztuac(context):
	if context.version == 17:
		return True


def set_ztuac(context):
	context.version = 17


games = Enum('Games', [('DISNEYLAND_ADVENTURES', 'Disneyland Adventures'), ('JURASSIC_WORLD_EVOLUTION', 'Jurassic World Evolution'), ('JURASSIC_WORLD_EVOLUTION_2', 'Jurassic World Evolution 2'), ('JURASSIC_WORLD_EVOLUTION_2_DEV', 'Jurassic World Evolution 2 Dev'), ('JURASSIC_WORLD_EVOLUTION_3', 'Jurassic World Evolution 3'), ('PLANET_COASTER', 'Planet Coaster'), ('PLANET_COASTER_2', 'Planet Coaster 2'), ('PLANET_ZOO', 'Planet Zoo'), ('PLANET_ZOO_PRE_1_6', 'Planet Zoo pre-1.6'), ('WARHAMMER_AGE_OF_SIGMAR_REALMS_OF_RUIN', 'Warhammer Age of Sigmar - Realms of Ruin'), ('ZOO_TYCOON', 'Zoo Tycoon'), ('UNKNOWN', 'Unknown Game')])


def get_game(context):
	versions = []
	if is_dla(context):
		versions.extend([games.DISNEYLAND_ADVENTURES])
	if is_jwe(context):
		versions.extend([games.JURASSIC_WORLD_EVOLUTION])
	if is_jwe2(context):
		versions.extend([games.JURASSIC_WORLD_EVOLUTION_2])
	if is_jwe2dev(context):
		versions.extend([games.JURASSIC_WORLD_EVOLUTION_2_DEV])
	if is_jwe3(context):
		versions.extend([games.JURASSIC_WORLD_EVOLUTION_3])
	if is_pc(context):
		versions.extend([games.PLANET_COASTER])
	if is_pc2(context):
		versions.extend([games.PLANET_COASTER_2])
	if is_pz(context):
		versions.extend([games.PLANET_ZOO_PRE_1_6])
	if is_pz16(context):
		versions.extend([games.PLANET_ZOO])
	if is_war(context):
		versions.extend([games.WARHAMMER_AGE_OF_SIGMAR_REALMS_OF_RUIN])
	if is_ztuac(context):
		versions.extend([games.ZOO_TYCOON])
	if not versions:
		versions.extend([games.UNKNOWN])
	return versions


def set_game(context, game):
	if isinstance(game, str):
		if game in games._member_names_:
			game = games[game]
		else:
			game = games(game)
	if game in {games.DISNEYLAND_ADVENTURES}:
		return set_dla(context)
	if game in {games.JURASSIC_WORLD_EVOLUTION}:
		return set_jwe(context)
	if game in {games.JURASSIC_WORLD_EVOLUTION_2}:
		return set_jwe2(context)
	if game in {games.JURASSIC_WORLD_EVOLUTION_2_DEV}:
		return set_jwe2dev(context)
	if game in {games.JURASSIC_WORLD_EVOLUTION_3}:
		return set_jwe3(context)
	if game in {games.PLANET_COASTER}:
		return set_pc(context)
	if game in {games.PLANET_COASTER_2}:
		return set_pc2(context)
	if game in {games.PLANET_ZOO_PRE_1_6}:
		return set_pz(context)
	if game in {games.PLANET_ZOO}:
		return set_pz16(context)
	if game in {games.WARHAMMER_AGE_OF_SIGMAR_REALMS_OF_RUIN}:
		return set_war(context)
	if game in {games.ZOO_TYCOON}:
		return set_ztuac(context)


class TrackmeshVersion(VersionBase):

	_file_format = 'trackmesh'
	_verattrs = ('version', 'user_version', 'version_flag')

	def __init__(self, *args, version=(), user_version=(), version_flag=(), **kwargs):
		super().__init__(*args, **kwargs)
		self.version = self._force_tuple(version)
		self.user_version = self._force_tuple(user_version)
		self.version_flag = self._force_tuple(version_flag)


dla = TrackmeshVersion(id='DLA', version=(15,), primary_games=[], all_games=[games.DISNEYLAND_ADVENTURES])
jwe = TrackmeshVersion(id='JWE', version=(19,), user_version=(VersionInfo.from_value(24724), VersionInfo.from_value(25108), VersionInfo.from_value(24596),), primary_games=[], all_games=[games.JURASSIC_WORLD_EVOLUTION])
jwe2 = TrackmeshVersion(id='JWE2', version=(20,), user_version=(VersionInfo.from_value(24724), VersionInfo.from_value(25108), VersionInfo.from_value(24596),), primary_games=[], all_games=[games.JURASSIC_WORLD_EVOLUTION_2])
jwe2dev = TrackmeshVersion(id='JWE2DEV', version=(20,), user_version=(VersionInfo.from_value(24724), VersionInfo.from_value(25108), VersionInfo.from_value(24596),), primary_games=[], all_games=[games.JURASSIC_WORLD_EVOLUTION_2_DEV])
jwe3 = TrackmeshVersion(id='JWE3', version=(20,), user_version=(VersionInfo.from_value(24724), VersionInfo.from_value(25108), VersionInfo.from_value(24596),), primary_games=[], all_games=[games.JURASSIC_WORLD_EVOLUTION_3])
pc = TrackmeshVersion(id='PC', version=(18,), user_version=(VersionInfo.from_value(8340), VersionInfo.from_value(8724), VersionInfo.from_value(8212),), version_flag=(8,), primary_games=[], all_games=[games.PLANET_COASTER])
pc2 = TrackmeshVersion(id='PC2', version=(20,), user_version=(VersionInfo.from_value(8340), VersionInfo.from_value(8724), VersionInfo.from_value(8212),), primary_games=[], all_games=[games.PLANET_COASTER_2])
pz = TrackmeshVersion(id='PZ', version=(19,), user_version=(VersionInfo.from_value(8340), VersionInfo.from_value(8724), VersionInfo.from_value(8212),), primary_games=[], all_games=[games.PLANET_ZOO_PRE_1_6])
pz16 = TrackmeshVersion(id='PZ16', version=(20,), user_version=(VersionInfo.from_value(8340), VersionInfo.from_value(8724), VersionInfo.from_value(8212),), primary_games=[], all_games=[games.PLANET_ZOO])
war = TrackmeshVersion(id='WAR', version=(20,), user_version=(VersionInfo.from_value(24724), VersionInfo.from_value(25108), VersionInfo.from_value(24596),), primary_games=[], all_games=[games.WARHAMMER_AGE_OF_SIGMAR_REALMS_OF_RUIN])
ztuac = TrackmeshVersion(id='ZTUAC', version=(17,), primary_games=[], all_games=[games.ZOO_TYCOON])

available_versions = [dla, jwe, jwe2, jwe2dev, jwe3, pc, pc2, pz, pz16, war, ztuac]
