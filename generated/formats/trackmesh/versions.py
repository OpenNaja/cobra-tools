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


games = Enum('Games',[('DISNEYLAND_ADVENTURE', 'Disneyland Adventure'), ('JURASSIC_WORLD_EVOLUTION', 'Jurassic World Evolution'), ('JURASSIC_WORLD_EVOLUTION_2', 'Jurassic World Evolution 2'), ('PLANET_COASTER', 'Planet Coaster'), ('PLANET_ZOO', 'Planet Zoo'), ('PLANET_ZOO_PRE_1_6', 'Planet Zoo pre-1.6'), ('ZOO_TYCOON_ULTIMATE_ANIMAL_COLLECTION', 'Zoo Tycoon Ultimate Animal Collection'), ('UNKNOWN_GAME', 'Unknown Game')])


def get_game(context):
	if is_dla(context):
		return [games.DISNEYLAND_ADVENTURE]
	if is_ztuac(context):
		return [games.ZOO_TYCOON_ULTIMATE_ANIMAL_COLLECTION]
	if is_pc(context):
		return [games.PLANET_COASTER]
	if is_pz(context):
		return [games.PLANET_ZOO_PRE_1_6]
	if is_pz16(context):
		return [games.PLANET_ZOO]
	if is_jwe(context):
		return [games.JURASSIC_WORLD_EVOLUTION]
	if is_jwe2(context):
		return [games.JURASSIC_WORLD_EVOLUTION_2]
	return [games.UNKOWN_GAME]


def set_game(context, game):
	if isinstance(game, str):
		game = games(game)
	if game in {games.DISNEYLAND_ADVENTURE}:
		return set_dla(context)
	if game in {games.ZOO_TYCOON_ULTIMATE_ANIMAL_COLLECTION}:
		return set_ztuac(context)
	if game in {games.PLANET_COASTER}:
		return set_pc(context)
	if game in {games.PLANET_ZOO_PRE_1_6}:
		return set_pz(context)
	if game in {games.PLANET_ZOO}:
		return set_pz16(context)
	if game in {games.JURASSIC_WORLD_EVOLUTION}:
		return set_jwe(context)
	if game in {games.JURASSIC_WORLD_EVOLUTION_2}:
		return set_jwe2(context)


