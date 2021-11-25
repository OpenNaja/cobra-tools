import logging
import struct

from modules.formats.BaseFormat import BaseFile

class GfxLoader(BaseFile):

    def create(self):
        ss, buffer_0 = self._get_data(self.file_entry.path)
        file_name_bytes = self.file_entry.basename.encode(encoding='utf8')
        pool_index, pool = self.get_pool(2)
        offset = pool.data.tell()
        # lua, ss, 2 frag + buffer
        pool.data.write(ss)  # ss data

        self.sized_str_entry = self.create_ss_entry(self.file_entry)
        self.sized_str_entry.pointers[0].pool_index = pool_index
        self.sized_str_entry.pointers[0].data_offset = offset
        self.create_data_entry(self.sized_str_entry, (buffer_0,))


    def load(self, file_path):
        # all meta data of the lua except the sized str entries lua size value seems to just be meta data, can be zeroed
        ss, buffer_0 = self._get_data(file_path)
        self.sized_str_entry.data_entry.update_data((buffer_0,))
        self.sized_str_entry.pointers[0].update_data(ss, update_copies=True)


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
        """Loads and returns the data for a LUA"""
        buffer_0 = self.get_content(file_path)
        ss = struct.pack("<IIII", 0, len(buffer_0), 0x00, 0x00)
        return ss, buffer_0