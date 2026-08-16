import os

import pytest

from source.formats.manis.splice import list_clip_blobs, replace_blob
from source.formats.manis.database import verify_bulk

MANIS = r"D:\JWE2 Stuff\Personal Mods\JWE3\Images and Models\Dinosaurs\Land (Base)\Indoraptor\notmotionextracted.maniset45ad1411.manis"

pytestmark = pytest.mark.skipif(not os.path.isfile(MANIS), reason="reference manis not present")


def test_lists_expected_blob_count():
	data = open(MANIS, "rb").read()
	# 20 clips, each with a transform stream and a scalar stream
	assert len(list_clip_blobs(data)) == 40


def test_replacing_with_identical_bytes_is_a_noop():
	data = open(MANIS, "rb").read()
	off, size = list_clip_blobs(data)[0]
	assert replace_blob(data, 0, data[off:off + size]) == data


def test_replacement_preserves_trailing_bulk(tmp_path):
	data = open(MANIS, "rb").read()
	off, size = list_clip_blobs(data)[0]
	bigger = data[off:off + size] + b"\x00" * 64
	out = replace_blob(data, 0, bigger)
	assert len(out) == len(data) + 64
	p = tmp_path / "spliced.manis"
	p.write_bytes(out)
	ok, msg = verify_bulk(str(p))
	assert ok, msg


def test_other_blobs_are_untouched():
	data = open(MANIS, "rb").read()
	blobs = list_clip_blobs(data)
	off, size = blobs[0]
	out = replace_blob(data, 0, data[off:off + size] + b"\x00" * 16)
	# every later blob should still be byte-identical, just shifted by 16
	for start, length in blobs[1:]:
		assert out[start + 16:start + 16 + length] == data[start:start + length]


def test_shift_is_padded_to_16_byte_alignment():
	"""KeysReader scans 16-byte boundaries, so a non-multiple shift loses later clips."""
	data = open(MANIS, "rb").read()
	off, size = list_clip_blobs(data)[0]
	# a deliberately awkward size: 9117 bytes larger, which is 13 mod 16
	awkward = data[off:off + size] + b"\x01" * 9117
	out = replace_blob(data, 0, awkward)
	assert (len(out) - len(data)) % 16 == 0, "net size change must stay 16-byte aligned"


def test_rejects_out_of_range_index():
	data = open(MANIS, "rb").read()
	with pytest.raises(IndexError):
		replace_blob(data, 999, b"\x00" * 64)
