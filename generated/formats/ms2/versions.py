from enum import Enum


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
	if context.version == 51:
		return True


def set_jwe2(context):
	context.version = 51


games = Enum('Games',[('DISNEYLAND_ADVENTURE', 'Disneyland Adventure'), ('DLA', 'DLA'), ('JURASSIC_WORLD_EVOLUTION', 'Jurassic World Evolution'), ('JURASSIC_WORLD_EVOLUTION_2', 'Jurassic World Evolution 2'), ('JWE_1', 'JWE1'), ('JWE_2', 'JWE2'), ('OLD', 'Old'), ('PC', 'PC'), ('PLANET_COASTER', 'Planet Coaster'), ('PLANET_ZOO_1_6', 'Planet Zoo 1.6+'), ('PLANET_ZOO_PRE_1_6', 'Planet Zoo pre-1.6'), ('PZ', 'PZ'), ('PZ_16', 'PZ16'), ('ZOO_TYCOON_ULTIMATE_ANIMAL_COLLECTION', 'Zoo Tycoon Ultimate Animal Collection'), ('ZTUAC', 'ZTUAC'), ('UNKNOWN_GAME', 'Unknown Game')])


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
	return [games.UNKOWN_GAME]


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


