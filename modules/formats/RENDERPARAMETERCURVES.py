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
        # offset x14: not used? (count could be int64)
        # offset x18: not used? padding?
        # offset x1c: not used? padding?
        ss_ptr = self.sized_str_entry.pointers[0]
        _,_,count,_ = struct.unpack("<4Q", ss_ptr.data)
        self.sized_str_entry.count = count

        self.sized_str_entry.curve_name = self.get_str_at_offset(0)
        print(f"rpc : {count} : {self.sized_str_entry.curve_name}")

        if count:
            list_frag = self.ovs.frag_at_pointer(self.sized_str_entry.pointers[0], offset=8)
            tmp_fragments = self.ovs.frags_from_pointer(list_frag.pointers[1], count)
            for frag in tmp_fragments:
                # frag is a ptr to the entry data
                entry_fragment = self.ovs.frag_at_pointer(frag.pointers[0], offset=0)
                # data entries:
                # offset  x0: strz attribute name (Atmospherics.Lights.IrradianceScatterIntensity, ...)
                # offset  x8: int  type   (4294967296, 4294967297, 4294967303, 1...)
                # offset  xc: int unused (probably type is int64)
                # offset x10: list of ptr to curve entries
                # offset x18: count of curve entries
                # offset x1c: int unused (probably count is int64)
                _,dtype1,dtype2,_,dcount = struct.unpack("<QIIQQ", entry_fragment.pointers[1].data)
                print(f"dtype1 {dtype1} dtype2 {dtype2} dcount: {dcount}")

                attrib_name = self.ovs.frag_at_pointer(entry_fragment.pointers[1], offset=0)
                if attrib_name:
                    name = self.p1_ztsr(attrib_name)
                    print(f"attrib: {name}")
                    if dcount:
                        dlist_frag = self.ovs.frag_at_pointer(entry_fragment.pointers[1], offset=0x10)
                        tmp_dfragments = self.ovs.frags_from_pointer(dlist_frag.pointers[1], dcount)
                        for dfrag in tmp_dfragments:
                            # dfrag is a ptr to the curve data
                            curve_fragment = self.ovs.frag_at_pointer(dfrag.pointers[0], offset=0)
                            curve_data = struct.unpack("<4f", curve_fragment.pointers[1].data)
                            # curve entry: I think this one is just x10 bytes
                            # offset x0: float key
                            # offset x4: float/int/vec3 value (depends on dtype1: 1, 7, 5)
                            # offset x8: int? float?
                            # offset xc: int? float?
                            print(f"curve data: {curve_data}")

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
