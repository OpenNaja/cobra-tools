import logging
import struct

from modules.formats.BaseFormat import BaseFile


class GfxLoader(BaseFile):
    extension = ".gfx"

    def create(self):
        ss, buffer_0 = self._get_data(self.file_entry.path)
        self.sized_str_entry = self.create_ss_entry(self.file_entry)
        self.write_to_pool(self.sized_str_entry.struct_ptr, 4, ss)
        self.create_data_entry(self.sized_str_entry, (buffer_0,))

    def load(self, file_path):
        ss, buffer_0 = self._get_data(file_path)
        self.sized_str_entry.data_entry.update_data((buffer_0,))
        self.sized_str_entry.struct_ptr.update_data(ss, update_copies=True)

    def collect(self):
        self.assign_ss_entry()

    def extract(self, out_dir, show_temp_files, progress_callback):
        name = self.sized_str_entry.name
        logging.info(f"Writing {name}")

        out_path = out_dir(name)
        buffers = self.sized_str_entry.data_entry.buffer_datas
        with open(out_path, 'wb') as outfile:
            for buff in buffers:
                outfile.write(buff)
        return [out_path]

    def _get_data(self, file_path):
        """Loads and returns the data for a GFX"""
        buffer_0 = self.get_content(file_path)
        ss = struct.pack("<QQQQ", 0, len(buffer_0), 0, 0)
        return ss, buffer_0
