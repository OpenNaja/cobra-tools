"""Rewrite a JWE3 .manis as UNCOMPRESSED key arrays (dtype compression 0).

JWE3 still reads the pre-ACL format JWE2 used and ships one asset in it
(`hatcheryexitcamera` is dtype 0: no ACL blobs, no database, no limb structures).
Converting a dinosaur bundle to it sidesteps ACL entirely - and the game accepts the
result: the Indoraptor spawns, lives and renders.

The buffers are assembled byte by byte rather than through `ManisFile.save()`, because
the writer drifts on rebuilt blocks - block starts wander by tens of bytes per clip, so
every clip after the first is read from the wrong offset and its channel maps come back
as garbage.

Layout per ManiBlock, verified against the shipped camera bundle:

    names (uint32 into the name buffer) | channel_to_bone (uint8) | bone_to_channel (uint8)
    pad to 4 | PosBones f32[frames][pos][3] | OriBones i16[frames][ori][4] (value * 16384)
    ShrBones f32[frames][scl][2] | SclBones f32[frames][scl][3] | Floats f32[frames][flo]
    pad to 8

Blocks are aligned to 16 relative to the start of the keys buffer.

  python manis_uncompress_cmd.py IN.manis --ms2 models.ms2 --out OUT.manis
      [--yaw-clip N --yaw-track N --yaw-deg D]

Then inject with --update.
"""
import argparse
import math
import os
import struct
import sys

import numpy as np

from generated.formats.manis import ManisFile
from generated.formats.manis.acl import decode_file
from modules.helpers import as_bytes
from source.formats.manis.bindpose import read_ms2_bind
from source.formats.manis.splice import list_clip_blobs, read_blob_header

QVVF = 12
MANI_INFO_SIZE = 304
ORI_SCALE = 16384.0
DTYPE_OFFSET = 8            # dtype sits 8 bytes into a ManiInfo
COMPRESSION_BIT = 1 << 4
HAS_LIST_MASK = 3 << 5


def pad_to(size, alignment):
	return (-size) % alignment


def fill_defaults(values, bind):
	"""Substitute the bind pose wherever the decoder marked a stripped sub-track."""
	out = values.copy()
	for track in range(out.shape[1]):
		for low, high in ((0, 4), (4, 7), (7, 10)):
			mask = np.isnan(out[:, track, low:high])
			if mask.any():
				out[:, track, low:high][mask] = np.broadcast_to(
					bind[track, low:high], (out.shape[0], high - low))[mask]
	return out


def yaw(values, track, degrees):
	"""Rotate one bone, so a deliberate change can be proven in game."""
	half = math.radians(degrees) / 2.0
	spin = np.array([0.0, math.sin(half), 0.0, math.cos(half)])

	def multiply(a, b):
		x1, y1, z1, w1 = a
		x2, y2, z2, w2 = b
		return np.array([w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2,
						 w1 * y2 - x1 * z2 + y1 * w2 + z1 * x2,
						 w1 * z2 + x1 * y2 - y1 * x2 + z1 * w2,
						 w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2])

	for sample in range(values.shape[0]):
		values[sample, track, 0:4] = multiply(spin, values[sample, track, 0:4].astype(float))
	return values


def build_block(mani_info, keys, names_lut, samples, scalars):
	"""Serialise one uncompressed ManiBlock."""
	frames = int(mani_info.frame_count)
	pos_n, ori_n = int(mani_info.pos_bone_count), int(mani_info.ori_bone_count)
	scl_n, flo_n = int(mani_info.scl_bone_count), int(mani_info.float_count)
	out = bytearray()

	for attr in ("pos_bones_names", "ori_bones_names", "scl_bones_names", "floats_names"):
		for name in getattr(keys, attr):
			out += struct.pack("<I", names_lut[str(name)])

	pos_map = [int(x) for x in keys.pos_channel_to_bone]
	ori_map = [int(x) for x in keys.ori_channel_to_bone]
	scl_map = [int(x) for x in keys.scl_channel_to_bone]
	for values in (pos_map, ori_map, scl_map):
		out += bytes(values)

	for attr, low, high in (
			("pos_bone_to_channel", mani_info.pos_bone_min, mani_info.pos_bone_max),
			("ori_bone_to_channel", mani_info.ori_bone_min, mani_info.ori_bone_max),
			("scl_bone_to_channel", mani_info.scl_bone_min, mani_info.scl_bone_max)):
		if int(low) <= int(high):
			out += bytes(int(x) & 0xFF for x in getattr(keys, attr))
	out += b"\x00" * pad_to(len(out), 4)

	usable = min(frames, samples.shape[0])
	pos = np.zeros((frames, pos_n, 3), dtype="<f4")
	ori = np.zeros((frames, ori_n, 4), dtype="<i2")
	scl = np.zeros((frames, scl_n, 3), dtype="<f4")
	shr = np.ones((frames, scl_n, 2), dtype="<f4")
	flo = np.zeros((frames, flo_n), dtype="<f4")

	for channel, track in enumerate(pos_map):
		pos[:usable, channel] = samples[:usable, track, 4:7]
	for channel, track in enumerate(ori_map):
		quantised = np.clip(samples[:usable, track, 0:4] * ORI_SCALE, -32768, 32767)
		ori[:usable, channel] = np.rint(quantised).astype("<i2")
	for channel, track in enumerate(scl_map):
		scl[:usable, channel] = samples[:usable, track, 7:10]
	if scalars is not None and flo_n:
		n = min(flo_n, scalars.shape[1])
		flo[:usable, :n] = scalars[:usable, :n, 0]

	out += pos.tobytes() + ori.tobytes() + shr.tobytes() + scl.tobytes() + flo.tobytes()
	out += b"\x00" * pad_to(len(out), 8)
	return bytes(out)


def main():
	ap = argparse.ArgumentParser(description=__doc__,
								 formatter_class=argparse.RawDescriptionHelpFormatter)
	ap.add_argument("manis")
	ap.add_argument("--out", required=True)
	ap.add_argument("--ms2", required=True)
	ap.add_argument("--yaw-clip", type=int)
	ap.add_argument("--yaw-track", type=int)
	ap.add_argument("--yaw-deg", type=float, default=60.0)
	args = ap.parse_args()

	raw = open(args.manis, "rb").read()
	headers = [read_blob_header(raw, offset) for offset, _ in list_clip_blobs(raw)]
	transforms = [i for i, h in enumerate(headers) if h["track_type"] == QVVF]
	streams = decode_file(args.manis)
	parents, bind = read_ms2_bind(args.ms2)

	manis = ManisFile()
	manis.load(args.manis)
	count = len(manis.mani_infos)
	print(f"{os.path.basename(args.manis)}: {count} clips, "
		  f"{len(transforms)} transform streams")

	# preamble, as ManisLoader.extract writes it, with an empty external stream name
	preamble = struct.pack("<HHI", manis.version, manis.context.mani_version, count)
	preamble += b"\x00"
	for name in manis.names:
		preamble += as_bytes(str(name))
	root = as_bytes(manis.header)
	preamble += root

	# buffer 0: the ManiInfo array with compression and has_list cleared, no database
	original_preamble = 8 + len(as_bytes(str(manis.stream or "")))
	for name in manis.names:
		original_preamble += len(as_bytes(str(name)))
	original_preamble += len(root)
	infos = bytearray(raw[original_preamble:original_preamble + count * MANI_INFO_SIZE])
	for index in range(count):
		at = index * MANI_INFO_SIZE + DTYPE_OFFSET
		dtype, = struct.unpack_from("<I", infos, at)
		struct.pack_into("<I", infos, at, dtype & ~(COMPRESSION_BIT | HAS_LIST_MASK))
	buffer0 = bytes(infos)

	# buffer 1: the name/hash table, untouched
	names_lut = {str(name): i for i, name in enumerate(manis.name_buffer.target_names)}
	buffer1 = as_bytes(manis.name_buffer)

	# buffer 2: the blocks
	buffer2 = bytearray()
	for clip, mani_info in enumerate(manis.mani_infos):
		blob = transforms[clip]
		samples = fill_defaults(streams[blob].values, bind)
		if args.yaw_clip == clip and args.yaw_track is not None:
			samples = yaw(samples, args.yaw_track, args.yaw_deg)
			print(f"  edit: clip {clip} track {args.yaw_track} "
				  f"rotated {args.yaw_deg:g} deg")
		scalars = None
		if blob + 1 < len(streams) and streams[blob + 1].track_type != QVVF:
			scalars = streams[blob + 1].values
		buffer2 += b"\x00" * pad_to(len(buffer2), 16)
		buffer2 += build_block(mani_info, mani_info.keys, names_lut, samples, scalars)
	buffer2 += b"\x00" * pad_to(len(buffer2), 16)

	with open(args.out, "wb") as fh:
		fh.write(preamble + buffer0 + buffer1 + bytes(buffer2))
	print(f"wrote {args.out} ({os.path.getsize(args.out)} bytes; "
		  f"b0={len(buffer0)} b1={len(buffer1)} b2={len(buffer2)})")

	check = ManisFile()
	check.load(args.out)
	parsed = sum(1 for mani_info in check.mani_infos
				 if getattr(mani_info, "keys", None) is not None)
	dtypes = sorted({int(mani_info.dtype) for mani_info in check.mani_infos})
	bad = sum(1 for mani_info in check.mani_infos
			  if getattr(mani_info, "keys", None) is not None
			  for name in mani_info.keys.ori_bones_names if str(name) == "bad_name")
	maps_ok = all(
		[int(x) for x in check.mani_infos[i].keys.ori_channel_to_bone]
		== [int(x) for x in manis.mani_infos[i].keys.ori_channel_to_bone]
		for i in range(count) if getattr(check.mani_infos[i], "keys", None) is not None)
	blobs = len(list_clip_blobs(open(args.out, "rb").read()))
	print(f"verify: {parsed}/{count} clips parse, dtypes {dtypes}, ACL blobs {blobs}, "
		  f"bad names {bad}, channel maps preserved {maps_ok}")
	return 0 if (parsed == count and bad == 0 and maps_ok) else 1


if __name__ == "__main__":
	sys.exit(main())
