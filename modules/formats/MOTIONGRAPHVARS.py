import logging
import struct
from modules.formats.BaseFormat import BaseFile


class MotiongraphvarsLoader(BaseFile):

    def collect(self):
        self.assign_ss_entry()
        # Sized string initpos = position of first fragment
        self.assign_fixed_frags(1)
        count, _, ptr = struct.unpack("<2I Q", self.sized_str_entry.pointers[0].data)
        self.sized_str_entry.vars = self.ovs.frags_from_pointer(self.sized_str_entry.fragments[0].pointers[1], count)
        # pointers[1].data is the name
        for var in self.sized_str_entry.vars:
            var.pointers[1].strip_zstring_padding()
        # The last fragment has padding that may be junk data to pad the size of the name block to multiples of 64
        self.sized_str_entry.fragments.extend(self.sized_str_entry.vars)

    def extract(self, out_dir, show_temp_files, progress_callback):
        name = self.sized_str_entry.name
        logging.info(f"Writing {name}")

        ovl_header = self.pack_header(b"MOTV")
        out_path = out_dir(name)
        with open(out_path, 'wb') as outfile:
            # write the sized str and buffers
            # print(sized_str_entry.pointers[0].data)
            outfile.write(ovl_header)
            outfile.write(self.sized_str_entry.pointers[0].data)
            # print(sized_str_entry.pointers[0].address)
            # print("frag data 0")
            for f in self.sized_str_entry.vars:
                # print(f)
                # print(f.pointers[1].data)
                outfile.write(f.pointers[1].data)
            # print("frag data 1")
            for f in self.sized_str_entry.vars:
                outfile.write(f.pointers[0].data)
        return out_path,


