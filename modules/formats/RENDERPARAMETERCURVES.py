import logging
import struct

from modules.formats.BaseFormat import BaseFile


class RenderParameterCurvesLoader(BaseFile):

    def create(self):
        #ss, buffer_0 = self._get_data(self.file_entry.path)
        #self.sized_str_entry = self.create_ss_entry(self.file_entry)
        #self.write_to_pool(self.sized_str_entry.pointers[0], 4, ss)
        #self.create_data_entry(self.sized_str_entry, (buffer_0,))
        pass

    def load(self, file_path):
        #ss, buffer_0 = self._get_data(file_path)
        #self.sized_str_entry.data_entry.update_data((buffer_0,))
        #self.sized_str_entry.pointers[0].update_data(ss, update_copies=True)
        pass

    def collect(self):
        self.assign_ss_entry()
        print(f"Collecting {self.sized_str_entry.name}")
        # offset  x0: ptr to string
        # offset  x8: ptr to list of ptrs to data entries
        # offset x10: count of data entries
        # offset x14: not used?
        # offset x18: not used?
        # offset x1c: not used?
        self.sized_str_entry.curve_name = self.get_str_at_offset(0)
        print(f"buffer size: {len(self.sized_str_entry.curve_name)} : {self.sized_str_entry.curve_name}")

        # data entries:
        # offset  x0: strz attribute name
        # offset  x8: int  type
        # offset  xc: int unused (probably type is int64)
        # offset x10: list of ptr to curve entries
        # offset x18: count of curve entries
        # offset x1c: int unused (probably count is int64)


        # curve entry: I think this one is just x10 bytes
        # offset x0: float
        # offset x4: float
        # offset x8: int? float?
        # offset xc: int? float?

        pass



    def extract(self, out_dir, show_temp_files, progress_callback):
        #name = self.sized_str_entry.name
        #logging.info(f"Writing {name}")
        #out_path = out_dir(name)
        #buffers = self.sized_str_entry.data_entry.buffer_datas
        #with open(out_path, 'wb') as outfile:
        #    for buff in buffers:
        #        outfile.write(buff)
        #return [out_path]
        pass

    def _get_data(self, file_path):
        """Loads and returns the data for a GFX"""
        #buffer_0 = self.get_content(file_path)
        #ss = struct.pack("<QQQQ", 0, len(buffer_0), 0, 0)
        #return ss, buffer_0
        pass
