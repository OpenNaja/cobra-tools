import os
import numpy as np

from generated.formats.ovl_base.basic import ConvStream
from generated.array import Array


def split_path(fp):
	in_dir, name_ext = os.path.split(fp)
	name, ext = os.path.splitext(name_ext)
	ext = ext.lower()
	return name_ext, name, ext


def as_bytes(inst):
	"""helper that returns the bytes representation of a struct"""
	# we must make sure that arrays are not treated as a list although they inherit from 'list'
	if isinstance(inst, np.ndarray):
		return inst.tobytes()
	if isinstance(inst, list) and not isinstance(inst, Array):
		return b"".join(as_bytes(c) for c in inst)
	# zero terminated strings show up as strings
	if isinstance(inst, str):
		return inst.encode() + b"\x00"
	if isinstance(inst, (bytes, bytearray)):
		return inst
	with ConvStream() as stream:
		inst.write(stream)
		return stream.getvalue()


def zstr(b):
	return b + b"\x00"
