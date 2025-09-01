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
	if context.version == 262 and context.mani_version == 279:
		return True


def set_jwe2(context):
	context.version = 262
	context.mani_version = 279


def is_jwe2dev(context):
	if context.version == 261:
		return True


def set_jwe2dev(context):
	context.version = 261


def is_pc(context):
	if context.version == 257:
		return True


def set_pc(context):
	context.version = 257


def is_pc2(context):
	if context.version == 262 and context.mani_version == 282:
		return True


def set_pc2(context):
	context.version = 262
	context.mani_version = 282


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
	if context.version == 262 and context.mani_version == 279:
		return True


def set_war(context):
	context.version = 262
	context.mani_version = 279


def is_ztuac(context):
	if context.version == 257:
		return True


def set_ztuac(context):
	context.version = 257


games = Enum('Games', [('DISNEYLAND_ADVENTURES', 'Disneyland Adventures'), ('JURASSIC_WORLD_EVOLUTION', 'Jurassic World Evolution'), ('JURASSIC_WORLD_EVOLUTION_2', 'Jurassic World Evolution 2'), ('JURASSIC_WORLD_EVOLUTION_2_DEV', 'Jurassic World Evolution 2 Dev'), ('PLANET_COASTER', 'Planet Coaster'), ('PLANET_COASTER_2', 'Planet Coaster 2'), ('PLANET_ZOO', 'Planet Zoo'), ('WARHAMMER_AGE_OF_SIGMAR_REALMS_OF_RUIN', 'Warhammer Age of Sigmar - Realms of Ruin'), ('ZOO_TYCOON', 'Zoo Tycoon'), ('UNKNOWN', 'Unknown Game')])


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
	if is_pc(context):
		versions.extend([games.PLANET_COASTER])
	if is_pc2(context):
		versions.extend([games.PLANET_COASTER_2])
	if is_pz(context):
		versions.extend([games.PLANET_ZOO])
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
	if game in {games.PLANET_COASTER}:
		return set_pc(context)
	if game in {games.PLANET_COASTER_2}:
		return set_pc2(context)
	if game in {games.PLANET_ZOO}:
		return set_pz(context)
	if game in {games.PLANET_ZOO}:
		return set_pz16(context)
	if game in {games.WARHAMMER_AGE_OF_SIGMAR_REALMS_OF_RUIN}:
		return set_war(context)
	if game in {games.ZOO_TYCOON}:
		return set_ztuac(context)


class ManisVersion(VersionBase):

	_file_format = 'manis'
	_verattrs = ('version', 'user_version', 'version_flag')

	def __init__(self, *args, version=(), user_version=(), version_flag=(), **kwargs):
		super().__init__(*args, **kwargs)
		self.version = self._force_tuple(version)
		self.user_version = self._force_tuple(user_version)
		self.version_flag = self._force_tuple(version_flag)


dla = ManisVersion(id='DLA', version=(256,), primary_games=[], all_games=[games.DISNEYLAND_ADVENTURES])
jwe = ManisVersion(id='JWE', version=(258,), primary_games=[], all_games=[games.JURASSIC_WORLD_EVOLUTION])
jwe2 = ManisVersion(id='JWE2', version=(262,), primary_games=[], all_games=[games.JURASSIC_WORLD_EVOLUTION_2])
jwe2dev = ManisVersion(id='JWE2DEV', version=(261,), primary_games=[], all_games=[games.JURASSIC_WORLD_EVOLUTION_2_DEV])
pc = ManisVersion(id='PC', version=(257,), primary_games=[], all_games=[games.PLANET_COASTER])
pc2 = ManisVersion(id='PC2', version=(262,), primary_games=[], all_games=[games.PLANET_COASTER_2])
pz = ManisVersion(id='PZ', version=(260,), primary_games=[], all_games=[games.PLANET_ZOO])
pz16 = ManisVersion(id='PZ16', version=(20,), user_version=(VersionInfo.from_value(8340), VersionInfo.from_value(8724), VersionInfo.from_value(8212),), primary_games=[], all_games=[games.PLANET_ZOO])
war = ManisVersion(id='WAR', version=(262,), primary_games=[], all_games=[games.WARHAMMER_AGE_OF_SIGMAR_REALMS_OF_RUIN])
ztuac = ManisVersion(id='ZTUAC', version=(257,), primary_games=[], all_games=[games.ZOO_TYCOON])

available_versions = [dla, jwe, jwe2, jwe2dev, pc, pc2, pz, pz16, war, ztuac]
