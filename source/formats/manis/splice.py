"""Byte-level replacement of an ACL clip blob inside a .manis.

Deliberately does NOT go through ManisFile.save(). The schema does not model the
compressed_database blob, KeysReader's inter-block auxiliary data, or the trailing
database bulk, so re-serialising drops all three - the same trap that silently cost
442 KB when rebuilding through MANI.py. Copying bytes through keeps every clip we
are not editing bit-for-bit identical and preserves the bulk for free.
"""
from __future__ import annotations

import struct

from source.formats.manis.database import TRACKS_TAG

QVVF_TRACK_TYPE = 12


def list_clip_blobs(data: bytes):
	"""Return [(offset, size), ...] for each compressed_tracks blob, in file order.

	A blob is identified by the ACL tag at +8 with its total size at +0, the same
	way the decoder finds them, so the indices here line up with decode_file().
	"""
	tag = struct.pack("<I", TRACKS_TAG)
	out = []
	pos = 0
	while True:
		magic = data.find(tag, pos)
		if magic == -1:
			break
		start = magic - 8
		if start < 0:
			pos = magic + 1
			continue
		size = struct.unpack_from("<I", data, start)[0]
		if size < 32 or start + size > len(data):
			pos = magic + 1
			continue
		out.append((start, size))
		pos = start + size
	return out


def read_blob_header(data: bytes, offset: int = 0) -> dict:
	"""Decode an ACL compressed_tracks header (bitstream v10) at `offset`.

	The flag bits matter when re-encoding: a blob that does not match vanilla on
	`wrap_optimized` reports a duration one sample short, and one that does not match
	on `trivial_defaults` tells the runtime it need not supply the bind pose for
	stripped sub-tracks. Neither shows up in a sample-value comparison.
	"""
	size, blob_hash, tag = struct.unpack_from("<III", data, offset)
	version, algorithm, track_type = struct.unpack_from("<HBB", data, offset + 12)
	num_tracks, num_samples = struct.unpack_from("<II", data, offset + 16)
	sample_rate, = struct.unpack_from("<f", data, offset + 24)
	misc, = struct.unpack_from("<I", data, offset + 28)
	header = {
		"size": size, "hash": blob_hash, "tag": tag, "version": version,
		"algorithm": algorithm, "track_type": track_type,
		"num_tracks": num_tracks, "num_samples": num_samples,
		"sample_rate": sample_rate, "misc_packed": misc,
		"wrap_optimized": bool(misc & (1 << 30)),
		"has_metadata": bool(misc >> 31),
	}
	if track_type == QVVF_TRACK_TYPE:
		header.update(
			has_scale=bool(misc & 1),
			rotation_format=(misc >> 4) & 0xF,
			has_database=bool(misc & (1 << 8)),
			trivial_defaults=bool(misc & (1 << 9)),
			stripped_keyframes=bool(misc & (1 << 10)),
		)
	return header


def ref_alignment(data: bytes, alignment: int = 16) -> int:
	"""Offset class, mod `alignment`, that a ManiBlock's PadAlign rounds up to.

	Each ACL blob inside a ManiBlock is followed by `PadAlign` relative to the block's
	own start, so every padded end lands on the same offset class in file coordinates -
	the one the keys buffer begins on. A scalar blob always directly follows a transform
	blob's padding, so its offset reveals that class without parsing the container.
	"""
	classes = {}
	for offset, _size in list_clip_blobs(data):
		if read_blob_header(data, offset).get("track_type") != QVVF_TRACK_TYPE:
			classes[offset % alignment] = classes.get(offset % alignment, 0) + 1
	if not classes:
		raise ValueError("no scalar blobs found, cannot determine the padding alignment")
	if len(classes) > 1:
		raise ValueError(f"scalar blobs disagree on alignment: {classes}")
	return next(iter(classes))



def blob_alignments(data: bytes, alignment: int = 16):
	"""EXPERIMENTAL - returns 16 for every blob; do not use 8.

	The runtime walks a ManiBlock as `align8 -> 0x90 header -> align16 -> transform
	blob -> align16 -> scalar blob -> align8 -> limb structure`, and probing vanilla
	says the limb structure really does sit at align8 of the scalar blob's end: a
	plausible outer count is there for 20/20 clips versus 8/20 at align16.

	Padding the last blob to 8 nevertheless produces a file cobra cannot read - Gate B
	drops to 1/27 ManiBlocks, where 16 gives 27/27 - because the schema models the
	trailing PadAlign as 16 and KeysReader's scan does not recover from the shift. So
	the two views disagree and 16 is the one that round-trips. Kept as a hook, and as a
	record that the align8 reading is unresolved rather than wrong-and-forgotten.
	"""
	return [alignment] * len(list_clip_blobs(data))


def replace_blob(data: bytes, index: int, new_blob: bytes, align_to: int = None,
				 alignment: int = 16) -> bytes:
	"""Swap the blob at `index` for `new_blob`, copying everything else verbatim.

	Replaces the blob *and the padding that follows it*, writing however much new
	padding the parser will expect. `align_to` is the offset class the padded end must
	land on, from `ref_alignment`; without it the blob is swapped one-for-one and the
	caller is responsible for the size being alignment-neutral.

	Getting this wrong is close to undetectable. ACL blobs sit on 16-byte boundaries
	relative to their ManiBlock and KeysReader walks those boundaries, so a stream that
	is off by even 16 bytes makes every following clip unparseable while the raw blobs
	all remain intact and individually decodable - a tag scan still finds 40 of them.
	Padding the replacement to keep the *delta* a multiple of 16 is not enough: the old
	padding stays in the file and the parser skips a freshly computed amount, so
	whenever the new padding is shorter than the old, 16 stray bytes are left behind.
	"""
	blobs = list_clip_blobs(data)
	if not 0 <= index < len(blobs):
		raise IndexError(f"blob {index} out of range (found {len(blobs)})")
	offset, size = blobs[index]
	if align_to is None:
		padded = new_blob
		overhang = (len(new_blob) - size) % alignment
		if overhang:
			padded = new_blob + b"\x00" * (alignment - overhang)
		return data[:offset] + padded + data[offset + size:]
	old_padding = (align_to - (offset + size)) % alignment
	new_padding = (align_to - (offset + len(new_blob))) % alignment
	return (data[:offset] + new_blob + b"\x00" * new_padding
			+ data[offset + size + old_padding:])
