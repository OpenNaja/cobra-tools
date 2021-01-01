def is_ztuac(inst):
	if inst.version == 17:
		return True


def is_pc(inst):
	if inst.version == 18:
		return True


def is_pz(inst):
	if inst.version == 19 and inst.user_version in (8340, 8724):
		return True


def is_jwe(inst):
	if inst.version == 19 and inst.user_version in (24724, 25108):
		return True


