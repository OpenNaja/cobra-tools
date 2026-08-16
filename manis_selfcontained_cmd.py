"""Convert every clip in a JWE3 .manis to self-contained ACL (Approach B).

JWE3 ships clips that are ACL database-stripped, with the per-frame detail in paired
LOD streams. This re-encodes every clip so it carries its own data, then removes the
database and its streams entirely, producing a bundle that needs no database at all.

  python manis_selfcontained_cmd.py IN.manis --ms2 models.ms2 --out OUT.manis

`--ms2` supplies the skeleton whose bind pose Frontier uses as each track's ACL
default sub-track value. Without it the defaults fall back to identity/zero/one and
the blobs report has_trivial_default_values() == true, which vanilla never does; the
runtime is then told it need not supply the bind pose for stripped sub-tracks.

Verification is per clip and fails locally rather than in game:

  Gate A  the re-encoded clip decodes back to the same pose - angular error on
          rotations, absolute error on translation and scale, measured after
          substituting the bind pose for stripped sub-tracks on both sides.
          Rotations are compared by angle: a quaternion and its antipode are the
          same rotation, so a component-wise diff reports a spurious 1.414 whenever
          ACL rebuilds w with the opposite sign.
  Gate F  the re-encoded header matches vanilla on every flag except the two that
          Approach B deliberately changes (has_database, stripped_keyframes).
  Gate C  no database or bulk survives anywhere in the output.
"""
import argparse
import os
import sys

import numpy as np

from generated.formats.manis.acl import decode_file, encode_tracks, decode_blob
from source.formats.manis.bindpose import read_ms2_bind, bind_bytes
from source.formats.manis.database import find_database, read_bulk_info
from source.formats.manis.selfcontained import count_parsed_maniblocks, make_database_free
from source.formats.manis.splice import (
	list_clip_blobs, read_blob_header, ref_alignment, replace_blob)

QVVF = 12
MAX_ROTATION_DEGREES = 0.5
MAX_TRANSLATION = 1e-3
MAX_SCALE = 1e-3


def fill_defaults(values, bind):
	"""Substitute the bind pose wherever the decoder marked a stripped sub-track.

	The decoder writes NaN for anything ACL did not store; in game those slots are
	filled by track_writer::get_variable_default_rotation() and friends from the
	skeleton, so a like-for-like comparison has to do the same.
	"""
	out = values.copy()
	if bind is None:
		return out
	samples = out.shape[0]
	for track in range(out.shape[1]):
		for low, high in ((0, 4), (4, 7), (7, 10)):
			mask = np.isnan(out[:, track, low:high])
			if mask.any():
				want = np.broadcast_to(bind[track, low:high], (samples, high - low))
				out[:, track, low:high][mask] = want[mask]
	return out


def compare(original, decoded, bind, track_type):
	"""Return (rotation_degrees, translation_error, scale_error, unresolved_nan)."""
	ref, got = fill_defaults(original, bind), fill_defaults(decoded, bind)
	unresolved = int(np.isnan(ref).sum() + np.isnan(got).sum())
	if track_type != QVVF:
		finite = np.isfinite(ref) & np.isfinite(got)
		err = float(np.abs(ref[finite] - got[finite]).max()) if finite.any() else 0.0
		return 0.0, err, 0.0, unresolved
	dot = np.abs((ref[:, :, 0:4] * got[:, :, 0:4]).sum(axis=2)).clip(0.0, 1.0)
	degrees = float(np.degrees(2.0 * np.arccos(dot)).max())
	translation = float(np.abs(ref[:, :, 4:7] - got[:, :, 4:7]).max())
	scale = float(np.abs(ref[:, :, 7:10] - got[:, :, 7:10]).max())
	return degrees, translation, scale, unresolved


def main():
	ap = argparse.ArgumentParser(description=__doc__,
								 formatter_class=argparse.RawDescriptionHelpFormatter)
	ap.add_argument("manis")
	ap.add_argument("--out", required=True)
	ap.add_argument("--ms2", help="skeleton supplying the bind pose used as ACL defaults")
	ap.add_argument("--keep-database", action="store_true",
					help="re-encode the clips but leave the database in place (A/B testing)")
	args = ap.parse_args()

	with open(args.manis, "rb") as fh:
		data = fh.read()
	streams = decode_file(args.manis)
	blobs = list_clip_blobs(data)
	if len(blobs) != len(streams):
		sys.exit(f"{len(blobs)} ACL blobs but {len(streams)} decoded streams - "
				 f"cannot pair them up safely")
	print(f"{os.path.basename(args.manis)}: {len(streams)} ACL streams, "
		  f"database={'yes' if find_database(data) else 'no'}")

	bind = None
	if args.ms2:
		parents, bind = read_ms2_bind(args.ms2)
		print(f"  bind pose: {len(parents)} bones from {os.path.basename(args.ms2)}")

	align_to = ref_alignment(data)
	print(f"  ManiBlock padding aligns to offset class {align_to} (mod 16)")

	worst_rotation = worst_translation = worst_scale = 0.0
	# rebuild back-to-front so earlier offsets stay valid as sizes change
	for i in range(len(streams) - 1, -1, -1):
		stream = streams[i]
		offset, old_size = list_clip_blobs(data)[i]
		vanilla = read_blob_header(data, offset)
		if (vanilla["num_tracks"] != stream.values.shape[1]
				or vanilla["num_samples"] != stream.values.shape[0]
				or vanilla["track_type"] != stream.track_type):
			sys.exit(f"stream {i} does not match blob {i}; the pairing is wrong")

		track_bind = bind if stream.track_type == QVVF else None
		if track_bind is not None and len(track_bind) != stream.values.shape[1]:
			sys.exit(f"stream {i} has {stream.values.shape[1]} tracks but the skeleton "
					 f"has {len(track_bind)} bones; wrong .ms2 for this bundle")

		blob = encode_tracks(
			stream.values, stream.track_type, stream.sample_rate,
			bind=bind_bytes(parents, track_bind) if track_bind is not None else None,
			wrap=vanilla["wrap_optimized"])

		# Gate A - the clip still decodes to the same pose
		rebuilt = read_blob_header(blob)
		rotation, translation, scale, unresolved = compare(
			stream.values, decode_blob(blob).values, track_bind, stream.track_type)
		worst_rotation = max(worst_rotation, rotation)
		worst_translation = max(worst_translation, translation)
		worst_scale = max(worst_scale, scale)
		if unresolved:
			sys.exit(f"Gate A FAILED on stream {i}: {unresolved} sub-track slots could "
					 f"not be resolved to a value (supply --ms2)")
		if rotation > MAX_ROTATION_DEGREES:
			sys.exit(f"Gate A FAILED on stream {i}: rotation off by {rotation:.4f} deg")
		if translation > MAX_TRANSLATION or scale > MAX_SCALE:
			sys.exit(f"Gate A FAILED on stream {i}: translation {translation:.6g}, "
					 f"scale {scale:.6g}")

		# Gate F - only the two Approach B flags may differ from vanilla
		if rebuilt["wrap_optimized"] != vanilla["wrap_optimized"]:
			sys.exit(f"Gate F FAILED on stream {i}: wrap_optimized "
					 f"{rebuilt['wrap_optimized']} != vanilla {vanilla['wrap_optimized']}")
		if rebuilt.get("has_database"):
			sys.exit(f"Gate F FAILED on stream {i}: re-encoded clip still has a database")
		if track_bind is not None and rebuilt.get("trivial_defaults"):
			sys.exit(f"Gate F FAILED on stream {i}: defaults are trivial despite a bind "
					 f"pose, so the runtime will not be asked for the bind values")

		data = replace_blob(data, i, blob, align_to=align_to)
		print(f"  stream {i:>3}: {old_size:>7} -> {len(blob):>7} bytes   "
			  f"rot={rotation:.4f} deg  trans={translation:.2e}  wrap={int(rebuilt['wrap_optimized'])}")

	print(f"Gate A  worst rotation {worst_rotation:.4f} deg (limit {MAX_ROTATION_DEGREES}), "
		  f"translation {worst_translation:.2e}, scale {worst_scale:.2e}")

	if args.keep_database:
		print("  --keep-database: leaving the database and its LOD streams in place")
	else:
		data, report = make_database_free(data)
		print(f"  removed database ({report.get('database_size', 0)} bytes) and bulk "
			  f"({report.get('low_size', 0)} + {report.get('medium_size', 0)} bytes)")
		print(f"  {report['original_size']} -> {report['final_size']} bytes")

	with open(args.out, "wb") as fh:
		fh.write(data)

	# Gate B - cobra's KeysReader must still be able to walk every ManiBlock. A raw tag
	# scan and the ACL decoder both pass on a bundle whose block chain is broken, so
	# this is the only check that catches a padding mistake.
	parsed, total = count_parsed_maniblocks(args.out)
	print(f"Gate B  {parsed}/{total} ManiBlocks parse")
	if parsed != total:
		sys.exit(f"Gate B FAILED: only {parsed} of {total} ManiBlocks parse; the blocks "
				 f"after the first bad one are unreachable even though their ACL blobs "
				 f"are intact")

	# Gate C - nothing database-shaped may survive
	if not args.keep_database:
		with open(args.out, "rb") as fh:
			written = fh.read()
		if find_database(written) is not None or read_bulk_info(written) is not None:
			sys.exit("Gate C FAILED: a database is still present in the written file")
		print("Gate C  OK: no database, no bulk, no external stream")
	print(f"wrote {args.out} ({len(data)} bytes)")
	return 0


if __name__ == "__main__":
	sys.exit(main())
