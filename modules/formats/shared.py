import struct


def pack_header(ovs, fmt_name):
    ovl = ovs.ovl
    return struct.pack("<4s4BI", fmt_name, ovl.version_flag, ovl.version, ovl.bitswap, ovl.seventh_byte, int(ovl.user_version))