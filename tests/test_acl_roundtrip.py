import os

import numpy as np
import pytest

from generated.formats.manis.acl import decode_file, encode_tracks, decode_blob

MANIS = r"D:\JWE2 Stuff\Personal Mods\JWE3\Images and Models\Dinosaurs\Land (Base)\Indoraptor\notmotionextracted.maniset45ad1411.manis"

pytestmark = pytest.mark.skipif(not os.path.isfile(MANIS), reason="reference manis not present")

# measured max abs error across real clips ranges 0.000016 (26 samples) to
# 0.000123 (313 samples) - longer clips accumulate more quantisation. 0.0005 is
# about 0.06 degrees on a quaternion component: well below perceptible, but still
# tight enough to catch real degradation.
THRESHOLD = 0.0005


def _streams():
	return decode_file(MANIS)


def test_qvvf_clip_survives_encode_decode():
	original = next(s for s in _streams() if s.track_type == 12)
	blob = encode_tracks(original.values, original.track_type, original.sample_rate)
	assert len(blob) > 0
	got = decode_blob(blob)
	assert got.track_count == original.track_count
	assert got.sample_count == original.sample_count
	assert got.component_count == original.component_count
	finite = np.isfinite(original.values) & np.isfinite(got.values)
	err = np.abs(original.values[finite] - got.values[finite]).max()
	assert err < THRESHOLD, f"max abs error {err}"


def test_default_subtracks_are_preserved():
	"""A default subtrack comes back as NaN; re-compression must find the same ones."""
	original = next(s for s in _streams() if s.track_type == 12)
	got = decode_blob(encode_tracks(original.values, original.track_type, original.sample_rate))
	assert int(np.isnan(got.values).sum()) == int(np.isnan(original.values).sum())


def test_scalar_stream_survives_encode_decode():
	original = next(s for s in _streams() if s.track_type == 0)
	got = decode_blob(encode_tracks(original.values, original.track_type, original.sample_rate))
	assert got.track_count == original.track_count
	assert got.sample_count == original.sample_count
	finite = np.isfinite(original.values) & np.isfinite(got.values)
	err = np.abs(original.values[finite] - got.values[finite]).max()
	assert err < THRESHOLD, f"max abs error {err}"


def test_encoded_clip_is_self_contained():
	"""Replacement clips must carry their own data, not reference a database."""
	original = next(s for s in _streams() if s.track_type == 12)
	blob = encode_tracks(original.values, original.track_type, original.sample_rate)
	# decode_blob only succeeds without a database if the bulk is inline
	got = decode_blob(blob)
	assert got.sample_count == original.sample_count
