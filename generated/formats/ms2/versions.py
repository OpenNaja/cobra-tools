from enum import Enum


def is_old(context):
	if context.version in (17, 18):
		return True


def set_old(context):
	context.version = 17


games = Enum('Games',[('OLD', 'Old'), ('UNKNOWN_GAME', 'Unknown Game')])


def get_game(context):
	if is_old(context):
		return [games.OLD]
	return [games.UNKOWN_GAME]


def set_game(context, game):
	if isinstance(game, str):
		game = games(game)
	if game in {games.OLD}:
		return set_old(context)


