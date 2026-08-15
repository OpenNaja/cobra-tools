import os

import pytest

from source.formats.manis.database import read_bulk_info, locate_bulk, verify_bulk

MANIS = r"D:\JWE2 Stuff\Personal Mods\JWE3\Images and Models\Dinosaurs\Land (Base)\Indoraptor\notmotionextracted.maniset45ad1411.manis"

pytestmark = pytest.mark.skipif(not os.path.isfile(MANIS), reason="reference manis not present")


def test_reads_known_bulk_sizes_and_hashes():
	data = open(MANIS, "rb").read()
	info = read_bulk_info(data)
	assert info["medium_size"] == 156084
	assert info["low_size"] == 283218
	assert info["medium_hash"] == 0x2a0f9dd0
	assert info["low_hash"] == 0xba03bf9c


def test_locates_bulk_blocks_at_known_offsets():
	data = open(MANIS, "rb").read()
	got = locate_bulk(data)
	assert got["low_offset"] == 347062
	assert got["medium_offset"] == 630294


def test_verify_bulk_passes_on_untouched_file():
	ok, msg = verify_bulk(MANIS)
	assert ok, msg


def test_verify_bulk_fails_when_bulk_corrupted(tmp_path):
	data = bytearray(open(MANIS, "rb").read())
	data[630294 + 100] ^= 0xFF  # flip a byte inside the medium tier
	bad = tmp_path / "corrupt.manis"
	bad.write_bytes(bytes(data))
	ok, msg = verify_bulk(str(bad))
	assert not ok
	assert "medium" in msg.lower()
