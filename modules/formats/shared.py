import struct


def pack_header(ovs, fmt_name):
	ovl = ovs.ovl
	return struct.pack("<4s4BI", fmt_name, ovl.version_flag, ovl.version, ovl.bitswap, ovl.seventh_byte, int(ovl.user_version))


def get_versions(ovl):
	return {"version": ovl.version, "user_version": ovl.user_version,  "version_flag": ovl.version_flag}


def assign_versions(inst, versions):
	for k, v in versions.items():
		setattr(inst, k, v)


def get_padding_size(size, alignment=16):
	mod = size % alignment
	if mod:
		return alignment - mod
	return 0


def get_padding(size, alignment=16):
	if alignment:
		# create the new blank padding
		return b"\x00" * get_padding_size(size, alignment=alignment)
	return b""


def djb(s):
	# calculates DJB hash for string s
	# from https://gist.github.com/mengzhuo/180cd6be8ba9e2743753#file-hash_djb2-py
	hash = 5381
	for x in s:
		hash = ((hash << 5) + hash) + ord(x)
	return hash & 0xFFFFFFFF