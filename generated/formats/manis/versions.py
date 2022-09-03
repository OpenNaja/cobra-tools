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


def is_dla(context):
	if context.version == 257:
		return True


def set_dla(context):
	context.version = 257


def is_pc(context):
	if context.version == 257:
		return True


def set_pc(context):
	context.version = 257


def is_jwe1(context):
	if context.version == 258:
		return True


def set_jwe1(context):
	context.version = 258


def is_pz(context):
	if context.version == 260:
		return True


def set_pz(context):
	context.version = 260


def is_jwe2_dev(context):
	if context.version == 261:
		return True


def set_jwe2_dev(context):
	context.version = 261


def is_jwe2(context):
	if context.version == 262:
		return True


def set_jwe2(context):
	context.version = 262


games = Enum('Games',[('DISNEYLAND_ADVENTURE', 'Disneyland Adventure'), ('DLA', 'DLA'), ('JURASSIC_WORLD_EVOLUTION', 'Jurassic World Evolution'), ('JURASSIC_WORLD_EVOLUTION_2', 'Jurassic World Evolution 2'), ('JWE_1', 'JWE1'), ('JWE_2', 'JWE2'), ('JWE_2_DEV_BUILD', 'JWE2 Dev Build'), ('PC', 'PC'), ('PLANET_COASTER', 'Planet Coaster'), ('PLANET_ZOO', 'Planet Zoo'), ('PLANET_ZOO_PRE_1_6', 'Planet Zoo pre-1.6'), ('PZ', 'PZ'), ('ZOO_TYCOON_ULTIMATE_ANIMAL_COLLECTION', 'Zoo Tycoon Ultimate Animal Collection'), ('UNKNOWN_GAME', 'Unknown Game')])


def get_game(context):
	if is_dla(context):
		return [games.DLA]
	if is_ztuac(context):
		return [games.ZOO_TYCOON_ULTIMATE_ANIMAL_COLLECTION]
	if is_pc(context):
		return [games.PC]
	if is_pz(context):
		return [games.PZ]
	if is_pz16(context):
		return [games.PLANET_ZOO]
	if is_jwe(context):
		return [games.JURASSIC_WORLD_EVOLUTION]
	if is_jwe2(context):
		return [games.JWE_2]
	if is_dla(context):
		return [games.DLA]
	if is_pc(context):
		return [games.PC]
	if is_jwe1(context):
		return [games.JWE_1]
	if is_pz(context):
		return [games.PZ]
	if is_jwe2_dev(context):
		return [games.JWE_2_DEV_BUILD]
	if is_jwe2(context):
		return [games.JWE_2]
	return [games.UNKOWN_GAME]


def set_game(context, game):
	if isinstance(game, str):
		game = games(game)
	if game in {games.DLA}:
		return set_dla(context)
	if game in {games.ZOO_TYCOON_ULTIMATE_ANIMAL_COLLECTION}:
		return set_ztuac(context)
	if game in {games.PC}:
		return set_pc(context)
	if game in {games.PZ}:
		return set_pz(context)
	if game in {games.PLANET_ZOO}:
		return set_pz16(context)
	if game in {games.JURASSIC_WORLD_EVOLUTION}:
		return set_jwe(context)
	if game in {games.JWE_2}:
		return set_jwe2(context)
	if game in {games.DLA}:
		return set_dla(context)
	if game in {games.PC}:
		return set_pc(context)
	if game in {games.JWE_1}:
		return set_jwe1(context)
	if game in {games.PZ}:
		return set_pz(context)
	if game in {games.JWE_2_DEV_BUILD}:
		return set_jwe2_dev(context)
	if game in {games.JWE_2}:
		return set_jwe2(context)


