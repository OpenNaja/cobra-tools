def is_dla(inst):
	if inst.version == 15:
		return True


def set_dla(inst):
	inst.version = 15


def is_ztuac(inst):
	if inst.version == 17:
		return True


def set_ztuac(inst):
	inst.version = 17


def is_pc(inst):
	if inst.version == 18:
		return True


def set_pc(inst):
	inst.version = 18


def is_pz(inst):
	if inst.version == 19 and inst.user_version in (8340, 8724):
		return True


def set_pz(inst):
	inst.version = 19
	inst.user_version = 8340


def is_jwe(inst):
	if inst.version == 19 and inst.user_version in (24724, 25108):
		return True


def set_jwe(inst):
	inst.version = 19
	inst.user_version = 24724


def get_game(inst):
	if is_dla(inst):
		return 'Disneyland Adventure'
	if is_ztuac(inst):
		return 'Zoo Tycoon Ultimate Animal Collection'
	if is_pc(inst):
		return 'Planet Coaster'
	if is_pz(inst):
		return 'Planet Zoo'
	if is_jwe(inst):
		return 'Jurassic World Evolution'
	return 'Unknown Game'


games = ['Disneyland Adventure', 'Jurassic World Evolution', 'Planet Coaster', 'Planet Zoo', 'Zoo Tycoon Ultimate Animal Collection', 'Unknown Game']


