"""Bridge between Cobra's MANIS parser and the official ACL decoder helper."""

from __future__ import annotations

import os
import struct
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path

import numpy as np


@dataclass
class AclSamples:
    track_type: int
    track_count: int
    sample_count: int
    component_count: int
    sample_rate: float
    values: np.ndarray


def _repo_root() -> Path:
    # source/formats/manis or generated/formats/manis -> repository root
    return Path(__file__).resolve().parents[3]


def decoder_path() -> Path:
    override = os.environ.get("COBRA_ACL_DECODER")
    if override:
        return Path(override)
    return _repo_root() / "bin" / "jwe3_acl_decode.exe"


def _read_samples(path: Path) -> AclSamples:
    raw = path.read_bytes()
    if len(raw) < 28:
        raise ValueError(f"Truncated ACL sample file: {path}")
    magic, version, track_type, tracks, samples, components, rate = struct.unpack_from(
        "<4sIIIIIf", raw
    )
    if magic != b"JACL" or version != 1:
        raise ValueError(f"Unsupported ACL sample file: {path}")
    expected = samples * tracks * components
    values = np.frombuffer(raw, dtype="<f4", offset=28)
    if values.size != expected:
        raise ValueError(
            f"ACL sample count mismatch in {path}: got {values.size}, expected {expected}"
        )
    return AclSamples(
        track_type,
        tracks,
        samples,
        components,
        rate,
        values.reshape(samples, tracks, components).copy(),
    )


def decode_file(filepath: str) -> list[AclSamples]:
    decoder = decoder_path()
    if not decoder.is_file():
        raise FileNotFoundError(
            f"JWE3 ACL decoder was not found at '{decoder}'. "
            "Build acl_decoder/build.cmd or set COBRA_ACL_DECODER."
        )
    with tempfile.TemporaryDirectory(prefix="cobra_acl_") as temp_dir:
        prefix = Path(temp_dir) / "decoded"
        result = subprocess.run(
            [str(decoder), filepath, str(prefix)],
            check=False,
            capture_output=True,
            text=True,
            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
        )
        if result.returncode != 0:
            detail = result.stderr.strip() or result.stdout.strip()
            raise RuntimeError(f"JWE3 ACL decoding failed: {detail}")
        streams = []
        index = 0
        while True:
            output = Path(f"{prefix}.{index}.jacl")
            if not output.is_file():
                break
            streams.append(_read_samples(output))
            index += 1
        return streams


def normalize_frame_count(values: np.ndarray, frame_count: int) -> np.ndarray:
    if len(values) == frame_count:
        return values
    if len(values) == frame_count - 1:
        return np.concatenate((values, values[:1]), axis=0)
    raise ValueError(
        f"ACL stream has {len(values)} samples but MANIS declares {frame_count} frames"
    )
