from enum import Enum

from generated.base_version import VersionBase
from generated.formats.ovl_base.bitfields.VersionInfo import VersionInfo


def is_dla(context):
	if context.version == 256:
		return True


def set_dla(context):
	context.version = 256


def is_jwe(context):
	if context.version == 258:
		return True


def set_jwe(context):
	context.version = 258


def is_jwe2(context):
	if context.version == 262:
		return True


def set_jwe2(context):
	context.version = 262


def is_jwe2dev(context):
	if context.version == 20 and context.user_version in (24724, 25108, 24596) and context.is_dev == 1:
		return True


def set_jwe2dev(context):
	context.version = 20
	context.user_version._value = 24724
	context.is_dev = 1


def is_jwe2_dev(context):
	if context.version == 261:
		return True


def set_jwe2_dev(context):
	context.version = 261


def is_pc(context):
	if context.version == 257:
		return True


def set_pc(context):
	context.version = 257


def is_pz(context):
	if context.version == 260:
		return True


def set_pz(context):
	context.version = 260


def is_pz16(context):
	if context.version == 20 and context.user_version in (8340, 8724, 8212):
		return True


def set_pz16(context):
	context.version = 20
	context.user_version._value = 8340


def is_war(context):
	if context.version == 262:
		return True


def set_war(context):
	context.version = 262


def is_waror(context):
	if context.version == 20 and context.user_version in (24724, 25108, 24596):
		return True


def set_waror(context):
	context.version = 20
	context.user_version._value = 24724


def is_ztuac(context):
	if context.version == 257:
		return True


def set_ztuac(context):
	context.version = 257


games = Enum('Games', [('DLA', 'DLA'), ('JURASSIC_WORLD_EVOLUTION_2_DEV', 'Jurassic World Evolution 2 Dev'), ('JWE', 'JWE'), ('JWE_2', 'JWE2'), ('JWE_2_DEV_BUILD', 'JWE2 Dev Build'), ('PC', 'PC'), ('PLANET_ZOO', 'Planet Zoo'), ('PZ', 'PZ'), ('WAR', 'WAR'), ('WARHAMMER_AGE_OF_SIGMAR_REALMS_OF_RUIN', 'Warhammer Age of Sigmar - Realms of Ruin'), ('ZTUAC', 'ZTUAC'), ('UNKNOWN', 'Unknown Game')])


def get_game(context):
	versions = []
	if is_dla(context):
		versions.extend([games.DLA])
	if is_jwe(context):
		versions.extend([games.JWE])
	if is_jwe2(context):
		versions.extend([games.JWE_2])
	if is_jwe2dev(context):
		versions.extend([games.JURASSIC_WORLD_EVOLUTION_2_DEV])
	if is_jwe2_dev(context):
		versions.extend([games.JWE_2_DEV_BUILD])
	if is_pc(context):
		versions.extend([games.PC])
	if is_pz(context):
		versions.extend([games.PZ])
	if is_pz16(context):
		versions.extend([games.PLANET_ZOO])
	if is_war(context):
		versions.extend([games.WAR])
	if is_waror(context):
		versions.extend([games.WARHAMMER_AGE_OF_SIGMAR_REALMS_OF_RUIN])
	if is_ztuac(context):
		versions.extend([games.ZTUAC])
	if not versions:
		versions.extend([games.UNKNOWN])
	return versions


def set_game(context, game):
	if isinstance(game, str):
		game = games(game)
	if game in {games.DLA}:
		return set_dla(context)
	if game in {games.JWE}:
		return set_jwe(context)
	if game in {games.JWE_2}:
		return set_jwe2(context)
	if game in {games.JURASSIC_WORLD_EVOLUTION_2_DEV}:
		return set_jwe2dev(context)
	if game in {games.JWE_2_DEV_BUILD}:
		return set_jwe2_dev(context)
	if game in {games.PC}:
		return set_pc(context)
	if game in {games.PZ}:
		return set_pz(context)
	if game in {games.PLANET_ZOO}:
		return set_pz16(context)
	if game in {games.WAR}:
		return set_war(context)
	if game in {games.WARHAMMER_AGE_OF_SIGMAR_REALMS_OF_RUIN}:
		return set_waror(context)
	if game in {games.ZTUAC}:
		return set_ztuac(context)


class ManisVersion(VersionBase):

	_file_format = 'manis'
	_verattrs = ('version', 'user_version', 'version_flag')

	def __init__(self, *args, version=(), user_version=(), version_flag=(), **kwargs):
		super().__init__(*args, **kwargs)
		self.version = self._force_tuple(version)
		self.user_version = self._force_tuple(user_version)
		self.version_flag = self._force_tuple(version_flag)


dla = ManisVersion(id='DLA', version=(256,), primary_games=[], all_games=[games.DLA])
jwe = ManisVersion(id='JWE', version=(258,), primary_games=[], all_games=[games.JWE])
jwe2 = ManisVersion(id='JWE2', version=(262,), primary_games=[], all_games=[games.JWE_2])
jwe2dev = ManisVersion(id='JWE2DEV', version=(20,), user_version=(VersionInfo.from_value(24724), VersionInfo.from_value(25108), VersionInfo.from_value(24596),), primary_games=[], all_games=[games.JURASSIC_WORLD_EVOLUTION_2_DEV])
jwe2_dev = ManisVersion(id='JWE2_DEV', version=(261,), primary_games=[], all_games=[games.JWE_2_DEV_BUILD])
pc = ManisVersion(id='PC', version=(257,), primary_games=[], all_games=[games.PC])
pz = ManisVersion(id='PZ', version=(260,), primary_games=[], all_games=[games.PZ])
pz16 = ManisVersion(id='PZ16', version=(20,), user_version=(VersionInfo.from_value(8340), VersionInfo.from_value(8724), VersionInfo.from_value(8212),), primary_games=[], all_games=[games.PLANET_ZOO])
war = ManisVersion(id='WAR', version=(262,), primary_games=[], all_games=[games.WAR])
waror = ManisVersion(id='WAROR', version=(20,), user_version=(VersionInfo.from_value(24724), VersionInfo.from_value(25108), VersionInfo.from_value(24596),), primary_games=[], all_games=[games.WARHAMMER_AGE_OF_SIGMAR_REALMS_OF_RUIN])
ztuac = ManisVersion(id='ZTUAC', version=(257,), primary_games=[], all_games=[games.ZTUAC])

available_versions = [dla, jwe, jwe2, jwe2dev, jwe2_dev, pc, pz, pz16, war, waror, ztuac]
