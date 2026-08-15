"""Helpers for extracting a .manis from an OVL and checking it survived.

Used as Gate D: if the OVL path drops the ACL database bulk, every clip in the
bundle silently reverts to the coarse database-less decode, which in game reads as
"my edit broke everything" and sends you hunting in the wrong place.
"""
from __future__ import annotations

import os
import subprocess
import sys

from source.formats.manis.database import verify_bulk

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
GAME = "Jurassic World Evolution 3"


def extract_ovl(ovl_path: str, out_dir: str) -> None:
	"""Extract an OVL to out_dir, raising with the tool's own message on failure."""
	cmd = [sys.executable, os.path.join(REPO, "ovl_tool_cmd.py"), "extract",
		   ovl_path, "-o", out_dir, "-g", GAME]
	result = subprocess.run(cmd, capture_output=True, text=True)
	if result.returncode != 0:
		detail = result.stderr.strip() or result.stdout.strip()
		raise RuntimeError(f"extract failed: {detail}")


def check_extract(ovl_path: str, out_dir: str, manis_name: str):
	"""Extract an OVL and verify the named .manis still has intact database bulk."""
	extract_ovl(ovl_path, out_dir)
	path = os.path.join(out_dir, manis_name)
	if not os.path.isfile(path):
		return False, f"{manis_name} not produced by extract"
	return verify_bulk(path)
