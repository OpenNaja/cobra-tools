import struct


def pack_header(ovs, fmt_name):
    ovl = ovs.ovl
    return struct.pack("<4s4BI", fmt_name, ovl.version_flag, ovl.version, ovl.bitswap, ovl.seventh_byte, int(ovl.user_version))


def get_versions(ovl):
    return {"version": ovl.version, "user_version": ovl.user_version,  "version_flag": ovl.version_flag}


def assign_versions(inst, versions):
    for k, v in versions.items():
        setattr(inst, k, v)
