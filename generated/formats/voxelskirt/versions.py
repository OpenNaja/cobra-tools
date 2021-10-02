from enum import Enum


def is_ztuac(context):
	if context.version == 17:
		return True


def set_ztuac(context):
	context.version = 17


def is_pc(context):
	if context.version == 18:
		return True


def set_pc(context):
	context.version = 18


def is_pz(context):
	if context.version == 19 and context.user_version in (8340, 8724):
		return True


def set_pz(context):
	context.version = 19
	context.user_version._value = 8340


def is_jwe(context):
	if context.version_flag == 1 and context.version == 19 and context.user_version in (24724, 25108):
		return True


def set_jwe(context):
	context.version_flag = 1
	context.version = 19
	context.user_version._value = 24724


games = Enum('Games',[('JURASSIC_WORLD_EVOLUTION', 'Jurassic World Evolution'), ('PLANET_COASTER', 'Planet Coaster'), ('PLANET_ZOO', 'Planet Zoo'), ('ZOO_TYCOON_ULTIMATE_ANIMAL_COLLECTION', 'Zoo Tycoon Ultimate Animal Collection'), ('UNKNOWN_GAME', 'Unknown Game')])


def get_game(context):
	if is_ztuac(context):
		return [games.ZOO_TYCOON_ULTIMATE_ANIMAL_COLLECTION]
	if is_pc(context):
		return [games.PLANET_COASTER]
	if is_pz(context):
		return [games.PLANET_ZOO]
	if is_jwe(context):
		return [games.JURASSIC_WORLD_EVOLUTION]
	return [games.UNKOWN_GAME]


def set_game(context, game):
	if isinstance(game, str):
		game = games(game)
	if game in {games.ZOO_TYCOON_ULTIMATE_ANIMAL_COLLECTION}:
		return set_ztuac(context)
	if game in {games.PLANET_COASTER}:
		return set_pc(context)
	if game in {games.PLANET_ZOO}:
		return set_pz(context)
	if game in {games.JURASSIC_WORLD_EVOLUTION}:
		return set_jwe(context)


