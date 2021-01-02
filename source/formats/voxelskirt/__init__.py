import time
import numpy as np
from generated.array import Array
from generated.formats.voxelskirt.compound.Header import Header
# from generated.formats.ovl import *
from generated.io import IoFile


class VoxelskirtFile(Header, IoFile):

    def __init__(self, ):
        super().__init__()

    def load(self, filepath):
        start_time = time.time()
        # eof = super().load(filepath)

        # extra stuff
        self.bone_names = []
        self.bone_info = None
        with self.reader(filepath) as stream:
            self.read(stream)
            self.eoh = stream.tell()
            print(self)
            self.heightmap = stream.read_floats((self.info.x, self.info.y))
            print(f"Min Height: {np.min(self.heightmap)}, Max Height: {np.max(self.heightmap)}")
            self.heightmap /= self.info.height
            self.end_of_heightmap = stream.tell()
            print(self.end_of_heightmap)
            self.layer = stream.read_ubytes((self.info.x, self.info.y, 4))
            # self.layer = self.layer.astype(np.float32) / 4289026304
            print(self.layer)
            self.end_of_layer = stream.tell()
            print(self.end_of_layer)

    def save(self, filepath):
        print("Writing verts and tris to temporary buffer")


if __name__ == "__main__":
    m = VoxelskirtFile()
    m.load("C:/Users/arnfi/Desktop/deciduousskirt.voxelskirt")
