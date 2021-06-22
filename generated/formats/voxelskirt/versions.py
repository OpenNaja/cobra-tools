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
	inst.user_version._value = 8340


def is_jwe(inst):
	if inst.version_flag == 1 and inst.version == 19 and inst.user_version in (24724, 25108):
		return True


def set_jwe(inst):
	inst.version_flag = 1
	inst.version = 19
	inst.user_version._value = 24724


def get_game(inst):
	if is_ztuac(inst):
		return 'Zoo Tycoon Ultimate Animal Collection'
	if is_pc(inst):
		return 'Planet Coaster'
	if is_pz(inst):
		return 'Planet Zoo'
	if is_jwe(inst):
		return 'Jurassic World Evolution'
	return 'Unknown Game'


def set_game(inst, game):
	if game == 'Zoo Tycoon Ultimate Animal Collection':
		set_ztuac(inst)
	if game == 'Planet Coaster':
		set_pc(inst)
	if game == 'Planet Zoo':
		set_pz(inst)
	if game == 'Jurassic World Evolution':
		set_jwe(inst)


games = ['Jurassic World Evolution', 'Planet Coaster', 'Planet Zoo', 'Zoo Tycoon Ultimate Animal Collection', 'Unknown Game']


