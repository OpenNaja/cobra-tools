"""Approach B: a JWE3 bundle rebuilt with no ACL database at all."""
import os

import pytest

from generated.formats.manis import ManisFile
from source.formats.manis.bindpose import NO_PARENT, bind_bytes, read_ms2_bind
from source.formats.manis.database import find_database, read_bulk_info
from source.formats.manis.selfcontained import (
	clear_stream_name, make_database_free, strip_database, truncate_bulk)
from source.formats.manis.splice import list_clip_blobs, read_blob_header

REFERENCE = r"D:\JWE2 Stuff\Personal Mods\JWE3\Images and Models\Dinosaurs\Land (Base)\Indoraptor"
MANIS = os.path.join(REFERENCE, "notmotionextracted.maniset45ad1411.manis")
MS2 = os.path.join(REFERENCE, "models.ms2")

pytestmark = pytest.mark.skipif(not os.path.isfile(MANIS), reason="reference manis not present")

MANI_COUNT = 20
MANI_INFO_SIZE = 304
DATABASE_SIZE = 240


@pytest.fixture(scope="module")
def data():
	with open(MANIS, "rb") as fh:
		return fh.read()


def test_database_sits_at_the_tail_of_buffer_0(data):
	"""The blob follows the ManiInfo array exactly, which is what makes removing it
	a truncation rather than a hole punched in the middle of a buffer."""
	offset, size = find_database(data)
	assert size == DATABASE_SIZE
	# 8 byte prefix + stream name + one zstr per mani + 40 byte root header = 702
	assert offset == 702 + MANI_COUNT * MANI_INFO_SIZE


def test_strip_database_removes_exactly_the_blob(data):
	out = strip_database(data)
	assert len(out) == len(data) - DATABASE_SIZE
	assert find_database(out) is None


def test_truncate_bulk_drops_both_tiers(data):
	info = read_bulk_info(data)
	out = truncate_bulk(data)
	assert len(out) < len(data) - info["low_size"] - info["medium_size"] + 256


def test_clear_stream_name_empties_the_ovs_name(data):
	out = clear_stream_name(data)
	assert out[:8] == data[:8]
	assert out[8] == 0
	assert len(out) == len(data) - len("Anim_L0")


def test_make_database_free_leaves_nothing_behind(data, tmp_path):
	out, report = make_database_free(data)
	assert report["had_database"]
	assert find_database(out) is None
	assert read_bulk_info(out) is None
	path = tmp_path / "clean.manis"
	path.write_bytes(out)
	# the whole point: cobra must still be able to read it back, because injection
	# goes through ManisFile.load
	manis = ManisFile()
	manis.load(str(path))
	assert len(manis.mani_infos) == MANI_COUNT
	assert manis.compressed_header.data is None
	# an empty stream name is what makes MANI.py write a single STATIC data entry
	assert not manis.stream


def test_compressed_header_still_reads_a_database_when_present(data, tmp_path):
	"""Detection must not have turned into 'never read anything'."""
	path = tmp_path / "vanilla.manis"
	path.write_bytes(data)
	manis = ManisFile()
	manis.load(str(path))
	assert manis.compressed_header.data is not None
	assert len(manis.compressed_header.data) == DATABASE_SIZE


def test_clip_blobs_survive_removal(data):
	out, _ = make_database_free(data)
	assert len(list_clip_blobs(out)) == len(list_clip_blobs(data))


@pytest.mark.skipif(not os.path.isfile(MS2), reason="reference ms2 not present")
def test_bind_pose_matches_the_clip_track_count():
	parents, values = read_ms2_bind(MS2)
	assert values.shape == (157, 10)
	assert parents[0] == NO_PARENT		# def_c_root_joint has no parent
	# the rig has several roots, not one; every other parent must be a real bone so
	# ACL can build the hierarchy it measures error against
	assert ((parents == NO_PARENT) | (parents < len(parents))).all()
	blob = bind_bytes(parents, values)
	assert blob[:4] == b"JBND"
	assert len(blob) == 12 + 157 * 4 + 157 * 10 * 4


def test_vanilla_clips_declare_a_database(data):
	"""Guards the premise of Approach B: vanilla really is database-backed."""
	headers = [read_blob_header(data, offset) for offset, _ in list_clip_blobs(data)]
	transforms = [h for h in headers if h["track_type"] == 12]
	assert len(transforms) == MANI_COUNT
	assert all(h["has_database"] for h in transforms)
	assert all(not h["trivial_defaults"] for h in transforms)
