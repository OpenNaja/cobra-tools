from generated.formats.ovl.compound.HeaderType import HeaderType
from generated.formats.ovl.compound.HeaderEntry import HeaderEntry

import os


class OvsHeader:
    """Reads an OVS archive"""
    #
    # def __init__(self, arg=None):
    #     # arg is the archive
    #     self.archive_entry = arg

    def read(self, stream):
        print("reading ovs header")
        self.header_types = [stream.read_type(HeaderType) for _ in range(self.archive_entry.num_header_types)]
        self.header_entries = []
        # # a dict keyed with header type hashes
        # headers_by_type = {}
        # read all header entries
        for header_type in self.header_types:
            for i in range(header_type.num_headers):
                self.ovl.print_and_callback(f"Reading header entries - type {header_type.type}", value=i, value_max=header_type.num_headers)
                header_entry = stream.read_type(HeaderEntry)
                header_entry.header_type = header_type
                header_entry.type = header_type.type
                self.header_entries.append(header_entry)
                # print(header_entry)
                header_entry.name = self.get_name(header_entry)
                header_entry.basename, header_entry.ext = os.path.splitext(header_entry.name)
                header_entry.ext = header_entry.ext[1:]
                # store fragments per header for faster lookup
                header_entry.fragments = []

    def write(self, stream):
        raise NotImplementedError

    def __repr__(self):
        return str(self.header_types)

