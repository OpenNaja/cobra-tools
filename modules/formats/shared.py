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


def djb2(s):
	# calculates djb2 hash for string s
	# from https://gist.github.com/mengzhuo/180cd6be8ba9e2743753#file-hash_djb2-py
	n = 5381
	for x in s:
		n = ((n << 5) + n) + ord(x)
	return n & 0xFFFFFFFF

