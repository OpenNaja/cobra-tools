from enum import Enum


def is_old(inst):
	if inst.version in (17, 18):
		return True


def set_old(inst):
	inst.version = 17


games = Enum('Games',[('OLD', 'Old'), ('UNKNOWN_GAME', 'Unknown Game')])


def get_game(inst):
	if is_old(inst):
		return [games.OLD]
	return [games.UNKOWN_GAME]


def set_game(inst, game):
	if game in {games.OLD}:
		return set_old(inst)


