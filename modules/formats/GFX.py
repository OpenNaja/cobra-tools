import logging
import struct

from modules.formats.BaseFormat import BaseFile


class GfxLoader(BaseFile):
    extension = ".gfx"

    def create(self):
        root_entry_data, buffer_0 = self._get_data(self.file_entry.path)
        self.root_entry = self.create_root_entry(self.file_entry)
        self.write_to_pool(self.root_entry.struct_ptr, 4, root_entry_data)
        self.create_data_entry(self.root_entry, (buffer_0,))

    def load(self, file_path):
        root_entry_data, buffer_0 = self._get_data(file_path)
        self.root_entry.data_entry.update_data((buffer_0,))
        self.write_to_pool(self.root_entry.struct_ptr, 4, root_entry_data, overwrite=True)

    def collect(self):
        self.assign_root_entry()

    def extract(self, out_dir, show_temp_files, progress_callback):
        name = self.root_entry.name
        logging.info(f"Writing {name}")

        out_path = out_dir(name)
        buffers = self.root_entry.data_entry.buffer_datas
        with open(out_path, 'wb') as outfile:
            for buff in buffers:
                outfile.write(buff)
        return [out_path]

    def _get_data(self, file_path):
        """Loads and returns the data for a GFX"""
        buffer_0 = self.get_content(file_path)
        root_entry = struct.pack("<QQQQ", 0, len(buffer_0), 0, 0)
        return root_entry, buffer_0
