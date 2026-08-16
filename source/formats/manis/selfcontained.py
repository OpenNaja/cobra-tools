"""Rebuild a JWE3 .manis so no clip depends on the ACL database (Approach B).

JWE3 ships clips that are ACL database-stripped: the per-frame detail lives in a
`compressed_database` whose bulk data rides in paired LOD streams (`Anim_L0` holds
the LOW tier, `Anim_L1` the MEDIUM - identify by size, never by name). Approach B
re-encodes every clip self-contained and removes the database entirely, so the
bundle no longer needs those streams.

The removal has to be structural, not cosmetic. An earlier attempt neutralised the
database by zeroing its tag in place, which left a corrupted 88-byte blob behind and
kept the orphaned `_L0`/`_L1` data entries in the OVL. The game crashed, but that
result could not distinguish "the game requires a database" from "the game choked on
a corrupted one", so it settled nothing. This module instead:

  1. deletes the `compressed_database` blob, which sits at the exact tail of buffer 0
     immediately after `num_manis * 304` bytes of ManiInfo, so buffer 0 ends exactly
     where the ManiInfo array ends and there is nothing left to find;
  2. truncates the trailing bulk blocks, so `read_bulk_info` returns None and
     `MANI.py` emits no external data entries;
  3. clears the external stream name, so `MANI.py` writes a single STATIC data entry
     rather than pushing the keys buffer into an OVS that no longer exists.

Only with all three does a crash mean "the game requires a database".
"""
from __future__ import annotations

import logging
import struct

from source.formats.manis.database import find_database, locate_bulk, read_bulk_info

# each ManiInfo in a JWE3 (mani_version 282) bundle
MANI_INFO_SIZE = 304


def count_parsed_maniblocks(path: str):
	"""Return (parsed, total) ManiBlocks that cobra's KeysReader can actually walk.

	The load-level checks are not enough on their own. `len(mani_infos)` comes from a
	buffer parsed before the keys, `list_clip_blobs` is a raw tag scan, and the ACL
	decoder runs on those scanned bytes - so a bundle whose ManiBlock chain is broken
	still reports the right clip count, the right number of blobs, and decodes every
	one of them. KeysReader logs and swallows its own failures, so even ManisFile.load
	comes back clean. Only counting the blocks it managed to attach reveals it.
	"""
	from generated.formats.manis import ManisFile

	manis_file = ManisFile()
	manis_file.load(path)
	total = len(manis_file.mani_infos)
	parsed = sum(1 for mani_info in manis_file.mani_infos
				 if getattr(mani_info, "keys", None) is not None)
	return parsed, total


def clear_stream_name(data: bytes) -> bytes:
	"""Blank the external stream name written by ManisLoader.extract.

	The layout is `<HHI>` then a zstr naming the first non-STATIC data entry, which
	extract leaves empty when a manis has only a STATIC entry. Writing an empty name
	is what makes `ManisLoader.create` take the single-data-entry path.
	"""
	end = data.index(b"\x00", 8)
	return data[:8] + b"\x00" + data[end + 1:]


def strip_database(data: bytes) -> bytes:
	"""Delete the compressed_database blob, or return `data` unchanged if absent.

	Refuses to touch a bundle whose database is not where the format puts it - the
	tail of buffer 0 - because deleting bytes from the middle of a parsed buffer
	would corrupt it silently.
	"""
	found = find_database(data)
	if found is None:
		return data
	offset, size = found
	if size % 16:
		raise ValueError(
			f"database blob is {size} bytes, not a multiple of 16; removing it would "
			f"shift the following ACL blobs off their 16-byte alignment")
	return data[:offset] + data[offset + size:]


def truncate_bulk(data: bytes) -> bytes:
	"""Drop the trailing ACL database bulk blocks appended by ManisLoader.extract."""
	info = read_bulk_info(data)
	if info is None:
		return data
	found = locate_bulk(data)
	if found is None:
		raise ValueError(
			"the bundle declares a database but its bulk blocks could not be located, "
			"so it is not safe to guess where to truncate")
	return data[:found["low_offset"]]


def make_database_free(data: bytes) -> tuple[bytes, dict]:
	"""Remove every trace of the ACL database from an extracted .manis.

	Returns the rebuilt bytes and a report of what was removed. Expects every clip to
	have already been re-encoded self-contained; it does not check that, because the
	caller re-encodes and verifies clip by clip.
	"""
	report = {"original_size": len(data)}
	info = read_bulk_info(data)
	report["had_database"] = info is not None
	if info is not None:
		report["low_size"] = info["low_size"]
		report["medium_size"] = info["medium_size"]
		report["database_size"] = info["db_size"]

	# order matters: truncate from the end backwards so earlier offsets stay valid
	data = truncate_bulk(data)
	data = strip_database(data)
	data = clear_stream_name(data)

	if find_database(data) is not None:
		raise ValueError("a compressed_database is still findable after removal")
	if read_bulk_info(data) is not None:
		raise ValueError("database bulk info is still readable after removal")
	report["final_size"] = len(data)
	logging.info("database removed: %d -> %d bytes", report["original_size"], report["final_size"])
	return data, report
