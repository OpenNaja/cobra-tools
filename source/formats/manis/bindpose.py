"""Read a skeleton's bind pose out of an .ms2 for use as ACL default sub-track values.

ACL strips any sub-track whose samples all equal that track's `default_value`, and
the runtime supplies the stripped value back through
`track_writer::get_variable_default_rotation()` and friends. Frontier compresses
JWE3 clips with the bind pose as that default, which is why a decoded clip has
~63% of its components missing and why `import_manis.py` substitutes the bone's
bind transform wherever the decoder wrote a NaN marker.

Re-encoding therefore needs the same bind pose, otherwise the defaults fall back to
identity/zero/one and the blob reports `has_trivial_default_values() == true`, which
vanilla never does.

The ACL track index is the target skeleton's bone index: every animated channel's
`ori_channel_to_bone` entry resolves to the .ms2 bone of the same name (verified
157/157 bones, 135/135 channels on Indoraptor), so bone order can be used directly.
"""
from __future__ import annotations

import struct

import numpy as np

JBIND_MAGIC = b"JBND"
JBIND_VERSION = 1
NO_PARENT = 0xFFFFFFFF
# .ms2 stores "no parent" as a ushort sentinel
MS2_NO_PARENT = 0xFFFF


def read_ms2_bind(ms2_path: str, model_index: int = 0):
    """Return (parents, values) for the skeleton in an .ms2.

    `parents` is uint32 per bone, NO_PARENT for roots. `values` is (num_bones, 10)
    float32 holding rotation xyzw, translation xyz and scale xyz, in the .ms2's own
    parent-local space - the same space the ACL qvv samples use.
    """
    from generated.formats.ms2 import Ms2File

    ms2 = Ms2File()
    ms2.load(ms2_path)
    bone_info = ms2.model_infos[model_index].bone_info
    if bone_info is None:
        raise ValueError(f"{ms2_path} model {model_index} has no bone_info")

    bones = bone_info.bones
    count = len(bones)
    values = np.zeros((count, 10), dtype="<f4")
    for i, bone in enumerate(bones):
        rot, loc = bone.rot, bone.loc
        # cobra stores the bind rotation as a quaternion with named components;
        # ACL wants xyzw in that order
        values[i, 0:4] = (rot.x, rot.y, rot.z, rot.w)
        values[i, 4:7] = (loc.x, loc.y, loc.z)
        # .ms2 bind scale is a single uniform factor, ACL's qvv scale is a vector3
        scale = float(bone.scale)
        values[i, 7:10] = (scale, scale, scale)

    raw_parents = [int(p) for p in bone_info.parents]
    if len(raw_parents) != count:
        raise ValueError(
            f"{ms2_path}: {len(raw_parents)} parents for {count} bones")
    parents = np.array(
        [NO_PARENT if p == MS2_NO_PARENT else p for p in raw_parents], dtype="<u4")
    return parents, values


def bind_bytes(parents: np.ndarray, values: np.ndarray) -> bytes:
    """Serialise a bind pose into the .jbind blob jwe3_acl_encode.exe reads."""
    count = len(parents)
    if values.shape != (count, 10):
        raise ValueError(f"expected ({count}, 10) values, got {values.shape}")
    return (JBIND_MAGIC
            + struct.pack("<II", JBIND_VERSION, count)
            + np.ascontiguousarray(parents, dtype="<u4").tobytes()
            + np.ascontiguousarray(values, dtype="<f4").tobytes())


def write_jbind(path: str, parents: np.ndarray, values: np.ndarray) -> None:
    with open(path, "wb") as fh:
        fh.write(bind_bytes(parents, values))


def bind_for_manis(ms2_path: str, num_tracks: int, model_index: int = 0):
    """Bind pose for a clip with `num_tracks` ACL tracks, or None if it cannot apply.

    A bundle whose track count does not match the skeleton is not something we can
    supply defaults for; the caller should fall back to trivial defaults rather than
    silently pair a clip with the wrong skeleton.
    """
    parents, values = read_ms2_bind(ms2_path, model_index)
    if len(parents) != num_tracks:
        return None
    return parents, values
