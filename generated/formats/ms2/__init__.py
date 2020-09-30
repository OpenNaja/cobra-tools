import os
import itertools
import struct
import io
import time

from generated.formats.ms2.compound.Ms2InfoHeader import Ms2InfoHeader
from generated.formats.ms2.compound.PcModel import PcModel
from generated.io import IoFile


class Ms2File(Ms2InfoHeader, IoFile):

    def __init__(self, progress_callback=None):
        super().__init__()

        self.last_print = None
        if progress_callback:
            self.progress_callback = progress_callback
        else:
            self.progress_callback = self.dummy_callback


    # dummy (black hole) callback for if we decide we don't want one
    def dummy_callback(self, *args, **kwargs):
        return

    def print_and_callback(self, message, value=None, max_value=None):
        # don't print the message if it is identical to the last one - it
        # will slow down massively repetitive tasks
        if self.last_print != message:
            print(message)
            self.last_print = message

        # call the callback
        if not self.mute:
            self.progress_callback(message, value, max_value)

    def load(self, filepath, verbose=0, commands=(), mute=False):
        start_time = time.time()
        # eof = super().load(filepath)

        with self.reader(filepath) as stream:
            self.read(stream)
            for mdl2_info in self.model_infos:
                pc_model = stream.read_type(PcModel, (mdl2_info,))
                print(pc_model)
                break
            eof = stream.tell()
        print("EOF", eof)

m = Ms2File()
m.load("C:/Users/arnfi/Desktop/prim/models.ms2")
print(m)