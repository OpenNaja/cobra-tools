import os
import struct

from generated.io import BinaryStream
from generated.array import Array


def write_sized_str(stream, s):
	"""Returns content of stream from pos"""
	size = struct.pack("<I", len(s))
	stream.write(size)
	stream.write(s.encode())


def read_sized_str(stream, pos, size):
	"""Returns content of stream from pos until pos+size"""
	stream.seek(pos)
	return stream.read(size)


def read_sized_str_at(stream, pos):
	"""Returns content of stream from pos"""
	stream.seek(pos)
	size = struct.unpack("<I", stream.read(4))[0]
	return stream.read(size)


def split_path(fp):
	in_dir, name_ext = os.path.split(fp)
	name, ext = os.path.splitext(name_ext)
	ext = ext.lower()
	return name_ext, name, ext


def as_bytes(inst, version_info={}):
	"""helper that returns the bytes representation of a pyffi struct"""
	# we must make sure that pyffi arrays are not treated as a list although they are an instance of 'list'
	if isinstance(inst, list) and not isinstance(inst, Array):
		return b"".join(as_bytes(c, version_info) for c in inst)
	# zero terminated strings show up as strings
	if isinstance(inst, str):
		return inst.encode() + b"\x00"
	with BinaryStream() as stream:
		for k, v in version_info.items():
			setattr(stream, k, v)
		inst.write(stream)
		return stream.getvalue()
