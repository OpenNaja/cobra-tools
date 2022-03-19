import os
import struct
import numpy as np

from generated.io import BinaryStream
from generated.array import Array
from generated.formats.ovl.basic import basic_map
from modules.formats.shared import assign_versions


def split_path(fp):
	in_dir, name_ext = os.path.split(fp)
	name, ext = os.path.splitext(name_ext)
	ext = ext.lower()
	return name_ext, name, ext


def as_bytes(inst, version_info={}):
	"""helper that returns the bytes representation of a struct"""
	# we must make sure that arrays are not treated as a list although they inherit from 'list'
	if isinstance(inst, np.ndarray):
		return inst.tobytes()
	if isinstance(inst, list) and not isinstance(inst, Array):
		return b"".join(as_bytes(c, version_info) for c in inst)
	# zero terminated strings show up as strings
	if isinstance(inst, str):
		return inst.encode() + b"\x00"
	if isinstance(inst, (bytes, bytearray)):
		return inst
	with BinaryStream() as stream:
		stream.register_basic_functions(basic_map)
		assign_versions(stream, version_info)
		inst.write(stream)
		return stream.getvalue()


def zstr(b):
	return b + b"\x00"
