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


def encoder_path() -> Path:
    override = os.environ.get("COBRA_ACL_ENCODER")
    if override:
        return Path(override)
    return _repo_root() / "bin" / "jwe3_acl_encode.exe"


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


def _write_jacl(path: Path, values: np.ndarray, track_type: int, sample_rate: float) -> None:
    """Write a sample array in the same format jwe3_acl_decode.exe emits."""
    samples, tracks, comps = values.shape
    with open(path, "wb") as fh:
        fh.write(b"JACL")
        fh.write(struct.pack("<IIIII", 1, track_type, tracks, samples, comps))
        fh.write(struct.pack("<f", sample_rate))
        fh.write(np.ascontiguousarray(values, dtype="<f4").tobytes())


def encode_tracks(values: np.ndarray, track_type: int, sample_rate: float,
                  bind: bytes = None, wrap: bool = False) -> bytes:
    """Compress a sample array into a raw ACL compressed_tracks blob.

    The blob carries its bulk data inline (has_database() == false), so a clip
    encoded here is self-contained and can be spliced into a .manis without
    rebuilding the bundle's ACL database.

    `bind` is a serialised .jbind blob from `source.formats.manis.bindpose`. It
    supplies the skeleton's bind pose as each track's default sub-track value, the
    way Frontier compresses; without it the defaults are identity/zero/one and the
    blob reports has_trivial_default_values() == true, unlike vanilla.

    `wrap` marks the clip wrap-optimized: the first sample repeats at the end and
    is not stored, which is how JWE3 authors looping clips. It changes the reported
    duration by one sample and does not alter the sample count.
    """
    encoder = encoder_path()
    if not encoder.is_file():
        raise FileNotFoundError(
            f"JWE3 ACL encoder was not found at '{encoder}'. "
            "Build acl_decoder/build_encode.cmd or set COBRA_ACL_ENCODER."
        )
    with tempfile.TemporaryDirectory(prefix="cobra_acl_enc_") as temp_dir:
        src = Path(temp_dir) / "in.jacl"
        dst = Path(temp_dir) / "out.blob"
        _write_jacl(src, values, track_type, sample_rate)
        command = [str(encoder), str(src), str(dst)]
        if bind:
            bind_path = Path(temp_dir) / "bind.jbind"
            bind_path.write_bytes(bind)
            command += ["--bind", str(bind_path)]
        if wrap:
            command.append("--wrap")
        result = subprocess.run(
            command,
            check=False,
            capture_output=True,
            text=True,
            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
        )
        if result.returncode != 0:
            detail = result.stderr.strip() or result.stdout.strip()
            raise RuntimeError(f"JWE3 ACL encoding failed: {detail}")
        return dst.read_bytes()


def decode_blob(blob: bytes) -> AclSamples:
    """Decode a raw compressed_tracks blob by handing the decoder a temp file."""
    with tempfile.TemporaryDirectory(prefix="cobra_acl_dec_") as temp_dir:
        src = Path(temp_dir) / "blob.bin"
        src.write_bytes(blob)
        streams = decode_file(str(src))
        if not streams:
            raise ValueError("decoder produced no streams for this blob")
        return streams[0]


def normalize_frame_count(values: np.ndarray, frame_count: int) -> np.ndarray:
    if len(values) == frame_count:
        return values
    if len(values) == frame_count - 1:
        return np.concatenate((values, values[:1]), axis=0)
    raise ValueError(
        f"ACL stream has {len(values)} samples but MANIS declares {frame_count} frames"
    )
