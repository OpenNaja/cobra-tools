import os
import itertools
import struct
import io
import time

from generated.formats.ms2.compound.Ms2InfoHeader import Ms2InfoHeader
from generated.formats.ms2.compound.PcModel import PcModel
from generated.io import IoFile


class Ms2File(Ms2InfoHeader, IoFile):

    def __init__(self, ):
        super().__init__()

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


if __name__ == "__main__":
    m = Ms2File()
    m.load("C:/Users/arnfi/Desktop/prim/models.ms2")
    print(m)
