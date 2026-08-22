"""Rebuild a JWE3 .manis with a real ACL database (Approach E).

The game rejects self-contained clips. Re-encoding every clip with
has_database = false crashes on spawn whether the original database is kept or removed,
while the untouched bundle and a no-op re-inject both load, so clips have to stay
database-backed. This compresses every transform clip, hands the set to ACL's
build_database(), splits the bulk out of line with split_database_bulk_data(), and
reassembles the bundle in JWE3's layout:

    [preamble][buffer 0: ManiInfo array + compressed_database][buffer 1][buffer 2: clips]
    [low tier bulk][medium tier bulk]

which is what ManisLoader.extract() writes and what MANI.py splits back into the STATIC
entry plus the _L0 (low) and _L1 (medium) data entries.

  python manis_database_cmd.py IN.manis --ms2 models.ms2 --out OUT.manis

Then inject it with --update; an ordinary inject reallocates pools and data entries and
the game rejects the result.
"""
import argparse
import os
import subprocess
import sys
import tempfile

import numpy as np

from generated.formats.manis.acl import decode_file, encode_tracks, decode_blob, _write_jacl
from source.formats.manis.bindpose import read_ms2_bind, bind_bytes
from source.formats.manis.database import find_database, read_bulk_info, locate_bulk
from source.formats.manis.selfcontained import count_parsed_maniblocks
from source.formats.manis.splice import (
	blob_alignments, list_clip_blobs, read_blob_header, ref_alignment, replace_blob)

QVVF = 12
BULK_ALIGNMENT = 16
MAX_ROTATION_DEGREES = 0.5


def builder_path():
	override = os.environ.get("COBRA_ACL_DATABASE")
	if override:
		return override
	here = os.path.dirname(os.path.abspath(__file__))
	return os.path.join(here, "bin", "jwe3_acl_database.exe")


def pad_to(data, alignment=BULK_ALIGNMENT):
	over = len(data) % alignment
	return data if not over else data + b"\x00" * (alignment - over)


def build_database(streams, headers, bind, work_dir, precision=None):
	"""Run the ACL database builder over every transform clip.

	Returns (bound_blobs_by_stream_index, database_bytes, low_bulk, medium_bulk).
	"""
	manifest_lines = []
	order = []
	for index, stream in enumerate(streams):
		if stream.track_type != QVVF:
			continue
		jacl = os.path.join(work_dir, f"clip.{len(order)}.jacl")
		_write_jacl(jacl, stream.values, stream.track_type, stream.sample_rate)
		manifest_lines.append(f"{jacl}|{1 if headers[index]['wrap_optimized'] else 0}")
		order.append(index)
	if not order:
		sys.exit("no transform clips in this bundle; nothing to build a database from")

	manifest = os.path.join(work_dir, "manifest.txt")
	with open(manifest, "w", encoding="utf-8") as fh:
		fh.write("\n".join(manifest_lines))
	bind_file = os.path.join(work_dir, "bind.jbind")
	with open(bind_file, "wb") as fh:
		fh.write(bind)

	out_dir = os.path.join(work_dir, "out")
	os.makedirs(out_dir, exist_ok=True)
	builder = builder_path()
	if not os.path.isfile(builder):
		sys.exit(f"ACL database builder not found at '{builder}'. "
				 f"Build acl_decoder/build_database.cmd or set COBRA_ACL_DATABASE.")
	command = [builder, manifest, out_dir, "--bind", bind_file]
	if precision is not None:
		command += ["--precision", repr(precision)]
	result = subprocess.run(command, check=False, capture_output=True, text=True)
	if result.returncode != 0:
		sys.exit(f"ACL database build failed: {result.stderr.strip() or result.stdout.strip()}")
	print(result.stdout.rstrip())

	bound = {}
	for position, index in enumerate(order):
		with open(os.path.join(out_dir, f"clip.{position}.blob"), "rb") as fh:
			bound[index] = fh.read()
	with open(os.path.join(out_dir, "database.bin"), "rb") as fh:
		database = fh.read()
	with open(os.path.join(out_dir, "bulk_low.bin"), "rb") as fh:
		low = fh.read()
	with open(os.path.join(out_dir, "bulk_medium.bin"), "rb") as fh:
		medium = fh.read()
	return bound, database, low, medium


def apply_yaw(streams, headers, bind, clip, track, degrees):
	"""Rotate one bone on one clip, so a deliberate change can be proven in game.

	A default sub-track decodes to NaN, so the bind value is substituted first -
	otherwise the rotation is applied to nothing and the clip comes back unchanged.
	"""
	import math

	transforms = [i for i, h in enumerate(headers) if h["track_type"] == QVVF]
	if not 0 <= clip < len(transforms):
		sys.exit(f"clip {clip} out of range (bundle has {len(transforms)})")
	index = transforms[clip]
	values = streams[index].values.copy()
	if not 0 <= track < values.shape[1]:
		sys.exit(f"track {track} out of range (clip has {values.shape[1]})")

	missing = np.isnan(values[:, track, 0:4])
	if missing.any():
		values[:, track, 0:4][missing] = np.broadcast_to(
			bind[track, 0:4], (values.shape[0], 4))[missing]

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
	streams[index].values = values
	print(f"  edit: clip {clip} (blob {index}) track {track} rotated {degrees:g} deg "
		  f"on {values.shape[0]} samples")
	return streams


def main():
	ap = argparse.ArgumentParser(description=__doc__,
								 formatter_class=argparse.RawDescriptionHelpFormatter)
	ap.add_argument("manis")
	ap.add_argument("--out", required=True)
	ap.add_argument("--ms2", required=True,
					help="skeleton supplying the bind pose used as ACL defaults")
	ap.add_argument("--precision", type=float,
					help="ACL error threshold in cm; looser values avoid the raw bit rate "
						 "(index 31 in the stream) that vanilla never uses")
	ap.add_argument("--yaw-clip", type=int,
					help="clip index to rotate, for proving an edit reaches the game")
	ap.add_argument("--yaw-track", type=int, help="track (== .ms2 bone index) to rotate")
	ap.add_argument("--yaw-deg", type=float, default=60.0, help="degrees to rotate")
	args = ap.parse_args()

	with open(args.manis, "rb") as fh:
		data = fh.read()
	streams = decode_file(args.manis)
	blobs = list_clip_blobs(data)
	if len(blobs) != len(streams):
		sys.exit(f"{len(blobs)} ACL blobs but {len(streams)} decoded streams")
	headers = [read_blob_header(data, offset) for offset, _ in blobs]

	original = read_bulk_info(data)
	if original is None:
		sys.exit("this bundle has no database to rebuild; it is not a JWE3 stripped bundle")
	found = locate_bulk(data)
	print(f"{os.path.basename(args.manis)}: {len(streams)} streams, "
		  f"vanilla database {original['db_size']} bytes, "
		  f"bulk low={original['low_size']} medium={original['medium_size']}")

	parents, bind_values = read_ms2_bind(args.ms2)
	print(f"  bind pose: {len(parents)} bones from {os.path.basename(args.ms2)}")
	bind = bind_bytes(parents, bind_values)

	if args.yaw_clip is not None and args.yaw_track is not None:
		streams = apply_yaw(streams, headers, bind_values, args.yaw_clip,
							args.yaw_track, args.yaw_deg)

	with tempfile.TemporaryDirectory(prefix="jwe3_acl_db_") as work_dir:
		bound, database, low, medium = build_database(streams, headers, bind, work_dir,
																   precision=args.precision)

	# rebuild back to front so offsets stay valid: bulk, then clips, then the database
	data = data[:found["low_offset"]] + pad_to(low) + pad_to(medium)

	align_to = ref_alignment(data)
	aligns = blob_alignments(data)
	worst = 0.0
	for index in range(len(streams) - 1, -1, -1):
		stream = streams[index]
		if stream.track_type == QVVF:
			blob = bound[index]
		else:
			blob = encode_tracks(stream.values, stream.track_type, stream.sample_rate,
								 wrap=headers[index]["wrap_optimized"])
			got = decode_blob(blob).values
			finite = np.isfinite(stream.values) & np.isfinite(got)
			if finite.any():
				worst = max(worst, float(np.abs(stream.values[finite] - got[finite]).max()))
		old_size = list_clip_blobs(data)[index][1]
		rebuilt = read_blob_header(blob)
		if stream.track_type == QVVF and not rebuilt.get("has_database"):
			sys.exit(f"clip {index} came back without a database; build_database did not bind it")
		data = replace_blob(data, index, blob, align_to=align_to, alignment=16)
		print(f"  stream {index:>3}: {old_size:>7} -> {len(blob):>7} bytes"
			  f"{'  database-backed' if stream.track_type == QVVF else '  scalar'}")

	# the database sits at the tail of buffer 0, immediately after the ManiInfo array
	db_offset, db_size = find_database(data)
	data = data[:db_offset] + database + data[db_offset + db_size:]

	with open(args.out, "wb") as fh:
		fh.write(data)

	# Gates
	rebuilt_info = read_bulk_info(data)
	if rebuilt_info is None:
		sys.exit("Gate C FAILED: the rebuilt database header is not readable")
	if locate_bulk(data) is None:
		sys.exit("Gate C FAILED: the rebuilt bulk does not hash-match its header")
	print(f"Gate C  OK: database {rebuilt_info['db_size']} bytes, "
		  f"bulk low={rebuilt_info['low_size']} medium={rebuilt_info['medium_size']}, hashes match")

	parsed, total = count_parsed_maniblocks(args.out)
	print(f"Gate B  {parsed}/{total} ManiBlocks parse")
	if parsed != total:
		sys.exit(f"Gate B FAILED: only {parsed} of {total} ManiBlocks parse")

	headers_out = [read_blob_header(data, off) for off, _ in list_clip_blobs(data)]
	transforms = [h for h in headers_out if h["track_type"] == QVVF]
	if not all(h["has_database"] for h in transforms):
		sys.exit("Gate F FAILED: some transform clips are not database-backed")
	print(f"Gate F  OK: {len(transforms)}/{len(transforms)} transform clips have has_database=1")
	if worst:
		print(f"Gate A  scalar streams max abs error {worst:.2e}")
	print(f"wrote {args.out} ({len(data)} bytes)")
	return 0


if __name__ == "__main__":
	sys.exit(main())
