"""Replace one ACL clip inside a JWE3 .manis, re-encoding it self-contained.

The replacement carries its bulk data inline, so the bundle's ACL database and
every other clip are left untouched.

  python manis_replace_cmd.py IN.manis --clip 0 --out OUT.manis
  python manis_replace_cmd.py IN.manis --clip 0 --out OUT.manis --jacl edited.0.jacl
  python manis_replace_cmd.py IN.manis --list

Then inject with (--update-aux is mandatory or textures break):

  python ovl_tool_cmd.py inject IN.ovl -g "Jurassic World Evolution 3" \\
      -f OUT.manis -o OUT.ovl --update-aux
"""
import argparse
import os
import sys

import numpy as np

from generated.formats.manis.acl import (
	decode_file, encode_tracks, decode_blob, _read_samples)
from source.formats.manis.splice import list_clip_blobs, replace_blob
from source.formats.manis.database import verify_bulk, read_bulk_info

GATE_A_THRESHOLD = 0.0005


def main():
	ap = argparse.ArgumentParser(description=__doc__,
								 formatter_class=argparse.RawDescriptionHelpFormatter)
	ap.add_argument("manis")
	ap.add_argument("--clip", type=int, help="blob index (see --list)")
	ap.add_argument("--out")
	ap.add_argument("--jacl", help="edited sample array; omit to re-encode unchanged")
	ap.add_argument("--list", action="store_true", help="list the blobs and exit")
	args = ap.parse_args()

	with open(args.manis, "rb") as fh:
		data = fh.read()
	blobs = list_clip_blobs(data)
	streams = decode_file(args.manis)

	if args.list or args.clip is None:
		print(f"{len(blobs)} ACL blobs in {os.path.basename(args.manis)}")
		print(f"{'idx':>4} {'offset':>10} {'size':>8} {'type':>6} {'tracks':>7} {'samples':>8}")
		for i, ((off, size), s) in enumerate(zip(blobs, streams)):
			kind = "qvvf" if s.track_type == 12 else "float1"
			print(f"{i:>4} {off:>10} {size:>8} {kind:>6} {s.track_count:>7} {s.sample_count:>8}")
		return 0

	if args.out is None:
		sys.exit("--out is required unless --list is given")
	if not 0 <= args.clip < len(blobs):
		sys.exit(f"--clip {args.clip} out of range (0..{len(blobs) - 1})")

	src = streams[args.clip]
	values, track_type, rate = src.values, src.track_type, src.sample_rate
	if args.jacl:
		from pathlib import Path
		edited = _read_samples(Path(args.jacl))
		if edited.track_count != src.track_count:
			sys.exit(f"track count mismatch: {edited.track_count} != {src.track_count}")
		if edited.sample_count != src.sample_count:
			sys.exit(f"sample count mismatch: {edited.sample_count} != {src.sample_count}")
		values, track_type, rate = edited.values, edited.track_type, edited.sample_rate

	blob = encode_tracks(values, track_type, rate)
	print(f"encoded clip {args.clip}: {len(blob)} bytes (was {blobs[args.clip][1]})")

	# Gate A - is the encoder faithful?
	check = decode_blob(blob)
	finite = np.isfinite(values) & np.isfinite(check.values)
	err = float(np.abs(values[finite] - check.values[finite]).max())
	print(f"Gate A  max abs error = {err:.6f}  (threshold {GATE_A_THRESHOLD})")
	if err > GATE_A_THRESHOLD:
		sys.exit("Gate A FAILED - encoder is losing accuracy, stopping")

	out = replace_blob(data, args.clip, blob)
	with open(args.out, "wb") as fh:
		fh.write(out)

	# Gate C - did the ACL database bulk survive the splice?
	had_db = read_bulk_info(data) is not None
	ok, msg = verify_bulk(args.out)
	if had_db and read_bulk_info(out) is None:
		sys.exit("Gate C FAILED - the database blob was lost, stopping")
	print(f"Gate C  {'OK' if ok else 'FAILED'}: {msg}")
	if not ok:
		sys.exit("Gate C FAILED - database bulk lost, stopping")

	print(f"wrote {args.out}  ({len(out)} bytes, was {len(data)})")
	return 0


if __name__ == "__main__":
	sys.exit(main())
