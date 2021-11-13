import logging

from modules.formats.BaseFormat import BaseFile


class GfxLoader(BaseFile):

    def collect(self):
        self.assign_ss_entry()

    def extract(self, out_dir, show_temp_files, progress_callback):
        name = self.sized_str_entry.name
        logging.info(f"Writing {name}")

        out_path = out_dir(name)
        buffers = self.sized_str_entry.data_entry.buffer_datas
        with open(out_path, 'wb') as outfile:
            outfile.write(self.sized_str_entry.pointers[0].data)
            for buff in buffers:
                outfile.write(buff)
        return out_path,
