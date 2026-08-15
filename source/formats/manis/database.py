"""Locate and verify the ACL compressed_database bulk blocks in a .manis.

JWE3 strips per-frame detail into database bulk blocks which cobra appends to the
.manis tail as [low tier][medium tier]EOF, each padded to an alignment boundary.
The database header stores each tier's size and an FNV1a-32 hash, so a candidate
offset can be verified rather than guessed - important, because ACL's
database_context::initialize does not validate bulk contents and a wrong offset
crashes during decompression.
"""
from __future__ import annotations

import struct

TRACKS_TAG = 0xAC11AC11
DB_TAG = 0xAC11DB01
MAX_PADDING = 256


def _fnv1a_32(buf) -> int:
	h = 2166136261
	for b in buf:
		h = ((h ^ b) * 16777619) & 0xFFFFFFFF
	return h


def find_database(data: bytes):
	"""Return (offset, size) of the compressed_database blob, or None."""
	tag = struct.pack("<I", DB_TAG)
	off = data.find(tag)
	while off != -1:
		start = off - 8
		if start >= 0:
			size = struct.unpack_from("<I", data, start)[0]
			if 32 <= size and start + size <= len(data):
				return start, size
		off = data.find(tag, off + 1)
	return None


def read_bulk_info(data: bytes):
	"""Return the database header's bulk sizes and hashes, or None if no database.

	The header lays out bulk_data_size[2], bulk_data_offset[2], bulk_data_hash[2]
	consecutively. Stripped bulk data is marked by offsets of 0xFFFFFFFF, which is
	what we anchor on to find the right position in the header.
	"""
	found = find_database(data)
	if found is None:
		return None
	db_off, db_size = found
	hdr = data[db_off:db_off + db_size]
	for i in range(0, max(0, db_size - 24), 4):
		med, low = struct.unpack_from("<II", hdr, i)
		if med == 0 or low == 0:
			continue
		if med > len(data) or low > len(data):
			continue
		o0, o1 = struct.unpack_from("<II", hdr, i + 8)
		if o0 != 0xFFFFFFFF or o1 != 0xFFFFFFFF:
			continue
		h_med, h_low = struct.unpack_from("<II", hdr, i + 16)
		return {
			"db_offset": db_off,
			"db_size": db_size,
			"medium_size": med,
			"low_size": low,
			"medium_hash": h_med,
			"low_hash": h_low,
		}
	return None


def _find_before(data: bytes, size: int, want_hash: int, search_end: int):
	"""Search backwards from search_end for a block of `size` matching want_hash."""
	if size > search_end or search_end > len(data):
		return None
	for pad in range(MAX_PADDING + 1):
		if size + pad > search_end:
			break
		off = search_end - pad - size
		if _fnv1a_32(data[off:off + size]) == want_hash:
			return off
	return None


def locate_bulk(data: bytes):
	"""Return {'medium_offset', 'low_offset'} verified by hash, or None."""
	info = read_bulk_info(data)
	if info is None:
		return None
	med = _find_before(data, info["medium_size"], info["medium_hash"], len(data))
	if med is None:
		return None
	low = _find_before(data, info["low_size"], info["low_hash"], med)
	if low is None:
		return None
	return {"medium_offset": med, "low_offset": low}


def verify_bulk(path: str):
	"""Return (ok, message) describing whether the database bulk is intact."""
	data = open(path, "rb").read()
	info = read_bulk_info(data)
	if info is None:
		return True, "no database in this file (nothing to verify)"
	med = _find_before(data, info["medium_size"], info["medium_hash"], len(data))
	if med is None:
		return False, "medium tier bulk not found or hash mismatch"
	low = _find_before(data, info["low_size"], info["low_hash"], med)
	if low is None:
		return False, "low tier bulk not found or hash mismatch"
	return True, (f"bulk intact: low @{low} ({info['low_size']}), "
				  f"medium @{med} ({info['medium_size']})")
