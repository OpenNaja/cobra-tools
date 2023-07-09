from enum import Enum

from generated.base_version import VersionBase
from generated.formats.ovl_base.bitfields.VersionInfo import VersionInfo


def is_dla(context):
	if context.version == 15:
		return True


def set_dla(context):
	context.version = 15


def is_ztuac(context):
	if context.version == 17:
		return True


def set_ztuac(context):
	context.version = 17


def is_pc(context):
	if context.version == 18 and context.user_version in (8340, 8724, 8212) and context.version_flag == 8:
		return True


def set_pc(context):
	context.version = 18
	context.user_version._value = 8340
	context.version_flag = 8


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


def is_jwe(context):
	if context.version == 19 and context.user_version in (24724, 25108, 24596):
		return True


def set_jwe(context):
	context.version = 19
	context.user_version._value = 24724


def is_jwe2dev(context):
	if context.version == 20 and context.user_version in (24724, 25108, 24596) and context.is_dev == 1:
		return True


def set_jwe2dev(context):
	context.version = 20
	context.user_version._value = 24724
	context.is_dev = 1


def is_jwe2(context):
	if context.version == 20 and context.user_version in (24724, 25108, 24596):
		return True


def set_jwe2(context):
	context.version = 20
	context.user_version._value = 24724


def is_old(context):
	if context.version in (7, 13, 32):
		return True


def set_old(context):
	context.version = 7


def is_dla(context):
	if context.version == 7:
		return True


def set_dla(context):
	context.version = 7


def is_ztuac(context):
	if context.version == 13:
		return True


def set_ztuac(context):
	context.version = 13


def is_pc(context):
	if context.version == 32:
		return True


def set_pc(context):
	context.version = 32


def is_jwe1(context):
	if context.version in (47, 39):
		return True


def set_jwe1(context):
	context.version = 47


def is_pz(context):
	if context.version in (48, 50):
		return True


def set_pz(context):
	context.version = 48


def is_pz16(context):
	if context.version == 50:
		return True


def set_pz16(context):
	context.version = 50


def is_jwe2(context):
	if context.version in (51, 52):
		return True


def set_jwe2(context):
	context.version = 51


def is_war(context):
	if context.version == 53:
		return True


def set_war(context):
	context.version = 53


games = Enum('Games', [('DISNEYLAND_ADVENTURES', 'Disneyland Adventures'), ('DLA', 'DLA'), ('JURASSIC_WORLD_EVOLUTION', 'Jurassic World Evolution'), ('JURASSIC_WORLD_EVOLUTION_2', 'Jurassic World Evolution 2'), ('JURASSIC_WORLD_EVOLUTION_2_DEV', 'Jurassic World Evolution 2 Dev'), ('JWE_1', 'JWE1'), ('JWE_2', 'JWE2'), ('OLD', 'Old'), ('PC', 'PC'), ('PLANET_COASTER', 'Planet Coaster'), ('PLANET_ZOO', 'Planet Zoo'), ('PLANET_ZOO_PRE_1_6', 'Planet Zoo pre-1.6'), ('PZ', 'PZ'), ('PZ_16', 'PZ16'), ('WAR', 'WAR'), ('ZOO_TYCOON_ULTIMATE_ANIMAL_COLLECTION', 'Zoo Tycoon Ultimate Animal Collection'), ('ZTUAC', 'ZTUAC'), ('UNKNOWN', 'Unknown Game')])


def get_game(context):
	if is_dla(context):
		return [games.DLA]
	if is_ztuac(context):
		return [games.ZTUAC]
	if is_pc(context):
		return [games.PC]
	if is_pz(context):
		return [games.PZ]
	if is_pz16(context):
		return [games.PZ_16]
	if is_jwe(context):
		return [games.JURASSIC_WORLD_EVOLUTION]
	if is_jwe2dev(context):
		return [games.JURASSIC_WORLD_EVOLUTION_2_DEV]
	if is_jwe2(context):
		return [games.JWE_2]
	if is_old(context):
		return [games.OLD]
	if is_dla(context):
		return [games.DLA]
	if is_ztuac(context):
		return [games.ZTUAC]
	if is_pc(context):
		return [games.PC]
	if is_jwe1(context):
		return [games.JWE_1]
	if is_pz(context):
		return [games.PZ]
	if is_pz16(context):
		return [games.PZ_16]
	if is_jwe2(context):
		return [games.JWE_2]
	if is_war(context):
		return [games.WAR]
	return [games.UNKNOWN]


def set_game(context, game):
	if isinstance(game, str):
		game = games(game)
	if game in {games.DLA}:
		return set_dla(context)
	if game in {games.ZTUAC}:
		return set_ztuac(context)
	if game in {games.PC}:
		return set_pc(context)
	if game in {games.PZ}:
		return set_pz(context)
	if game in {games.PZ_16}:
		return set_pz16(context)
	if game in {games.JURASSIC_WORLD_EVOLUTION}:
		return set_jwe(context)
	if game in {games.JURASSIC_WORLD_EVOLUTION_2_DEV}:
		return set_jwe2dev(context)
	if game in {games.JWE_2}:
		return set_jwe2(context)
	if game in {games.OLD}:
		return set_old(context)
	if game in {games.DLA}:
		return set_dla(context)
	if game in {games.ZTUAC}:
		return set_ztuac(context)
	if game in {games.PC}:
		return set_pc(context)
	if game in {games.JWE_1}:
		return set_jwe1(context)
	if game in {games.PZ}:
		return set_pz(context)
	if game in {games.PZ_16}:
		return set_pz16(context)
	if game in {games.JWE_2}:
		return set_jwe2(context)
	if game in {games.WAR}:
		return set_war(context)


class Ms2Version(VersionBase):

	_file_format = 'ms2'
	_verattrs = ('version', 'user_version', 'version_flag')

	def __init__(self, *args, version=(), user_version=(), version_flag=(), **kwargs):
		super().__init__(*args, **kwargs)
		self.version = self._force_tuple(version)
		self.user_version = self._force_tuple(user_version)
		self.version_flag = self._force_tuple(version_flag)


dla = Ms2Version(id='DLA', version=(15,), primary_games=[], all_games=[games.DISNEYLAND_ADVENTURES])
ztuac = Ms2Version(id='ZTUAC', version=(17,), primary_games=[], all_games=[games.ZOO_TYCOON_ULTIMATE_ANIMAL_COLLECTION])
pc = Ms2Version(id='PC', version=(18,), user_version=(VersionInfo.from_value(8340), VersionInfo.from_value(8724), VersionInfo.from_value(8212),), version_flag=(8,), primary_games=[], all_games=[games.PLANET_COASTER])
pz = Ms2Version(id='PZ', version=(19,), user_version=(VersionInfo.from_value(8340), VersionInfo.from_value(8724), VersionInfo.from_value(8212),), primary_games=[], all_games=[games.PLANET_ZOO_PRE_1_6])
pz16 = Ms2Version(id='PZ16', version=(20,), user_version=(VersionInfo.from_value(8340), VersionInfo.from_value(8724), VersionInfo.from_value(8212),), primary_games=[], all_games=[games.PLANET_ZOO])
jwe = Ms2Version(id='JWE', version=(19,), user_version=(VersionInfo.from_value(24724), VersionInfo.from_value(25108), VersionInfo.from_value(24596),), primary_games=[], all_games=[games.JURASSIC_WORLD_EVOLUTION])
jwe2dev = Ms2Version(id='JWE2DEV', version=(20,), user_version=(VersionInfo.from_value(24724), VersionInfo.from_value(25108), VersionInfo.from_value(24596),), primary_games=[], all_games=[games.JURASSIC_WORLD_EVOLUTION_2_DEV])
jwe2 = Ms2Version(id='JWE2', version=(20,), user_version=(VersionInfo.from_value(24724), VersionInfo.from_value(25108), VersionInfo.from_value(24596),), primary_games=[], all_games=[games.JURASSIC_WORLD_EVOLUTION_2])
old = Ms2Version(id='old', version=(7, 13, 32,), primary_games=[], all_games=[games.OLD])
dla = Ms2Version(id='DLA', version=(7,), primary_games=[], all_games=[games.DLA])
ztuac = Ms2Version(id='ZTUAC', version=(13,), primary_games=[], all_games=[games.ZTUAC])
pc = Ms2Version(id='PC', version=(32,), primary_games=[], all_games=[games.PC])
jwe1 = Ms2Version(id='JWE1', version=(47, 39,), primary_games=[], all_games=[games.JWE_1])
pz = Ms2Version(id='PZ', version=(48, 50,), primary_games=[], all_games=[games.PZ])
pz16 = Ms2Version(id='PZ16', version=(50,), primary_games=[], all_games=[games.PZ_16])
jwe2 = Ms2Version(id='JWE2', version=(51, 52,), primary_games=[], all_games=[games.JWE_2])
war = Ms2Version(id='WAR', version=(53,), primary_games=[], all_games=[games.WAR])

available_versions = [dla, ztuac, pc, pz, pz16, jwe, jwe2dev, jwe2, old, dla, ztuac, pc, jwe1, pz, pz16, jwe2, war]
