import functools
import struct

VERSION_FIELDS = ("version", "user_version", "version_flag", "general_info.ms_2_version")


def rsetattr(obj, attr, val):
	pre, _, post = attr.rpartition('.')
	return setattr(rgetattr(obj, pre) if pre else obj, post, val)


def rgetattr(obj, attr, *args):
	def _getattr(obj, attr):
		return getattr(obj, attr, *args)
	return functools.reduce(_getattr, [obj] + attr.split('.'))


def get_versions(ovl):
	# dynamically get the versions
	return {k: v for k, v in ((k, rgetattr(ovl, k, None)) for k in VERSION_FIELDS if rgetattr(ovl, k, None) is not None)}


def assign_versions(inst, versions):
	for k, v in versions.items():
		# for stuff like x.general_info.ms_2_version we want to assign the global to stream.ms_2_version
		k = k.rsplit(".")[-1]
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
	n = 5381
	for x in s:
		n = ((n << 5) + n) + ord(x)
	return n & 0xFFFFFFFF

