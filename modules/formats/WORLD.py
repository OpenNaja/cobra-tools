import struct

from generated.formats.ovl.versions import *
from modules.formats.BaseFormat import BaseFile
from modules.formats.shared import get_padding
from modules.helpers import zstr
from ovl_util import texconv
from ovl_util.interaction import showdialog


class WorldLoader(BaseFile):

    def create(self):
    	pass

    def collect(self):
        self.assign_ss_entry()
        print(f"Collecting {self.sized_str_entry.name}")

        # 1 used for main park worlds, 2 used for loading, 3 used for main menu or alike
        worldType = struct.unpack("<Q", self.sized_str_entry.pointers[0].data[:8])[0]
        self.sized_str_entry.worldType = worldType

        if len(self.sized_str_entry.pointers[0].data) == 0x50: # nothing more to read
            return 

        if len(self.sized_str_entry.pointers[0].data) == 0x08: # we have assetPackage list
            assetpgklistfragment = self.ovs.frags_from_pointer(self.sized_str_entry.pointers[0], 1)
            _ , assetPkgCount = struct.unpack("<QQ", assetpgklistfragment[0].pointers[0].data)
            print(f"AssetCount  {assetPkgCount}")

            self.sized_str_entry.assetPkgCount = assetPkgCount
            self.sized_str_entry.vars = self.ovs.frags_from_pointer(assetpgklistfragment[0].pointers[1], assetPkgCount)
            for var in self.sized_str_entry.vars:
                var.pointers[1].strip_zstring_padding()
                strval = var.pointers[1].data.decode('utf-8')
                print(strval)

        # if we still have pointers, it has to be the Lua controller present in the world definition
        if len(self.sized_str_entry.pointers[0].data) == 0x18 or len(assetpgklistfragment[0].pointers[0].data) == 0x10:
        	luaFilefragment = self.ovs.frags_from_pointer(self.sized_str_entry.pointers[0], 1)
        	luaFilefragment[0].pointers[1].strip_zstring_padding()
        	self.sized_str_entry.LuaFilename = luaFilefragment[0].pointers[1].data.decode('utf-8')
        	print(f"Lua file: {self.sized_str_entry.LuaFilename}")

        # in JWE1 at offset 0x40 there is a ptr to the lighting options

    def load(self, file_path):
        pass

    def extract(self, out_dir, show_temp_files, progress_callback):
        name = self.sized_str_entry.name
        print(f"Writing {name}")
        # enumnamer only has a list of strings
        out_path = out_dir(name)
        with open(out_path, 'w') as outfile:
            outfile.write(f"WorldType: {self.sized_str_entry.worldType}\n")
            if self.sized_str_entry.assetPkgCount > 0:
                outfile.write(f"AssetPackages ({self.sized_str_entry.assetPkgCount}):\n")
                for f in self.sized_str_entry.vars:
                    # convert from bytes to string, remove trailing 0x00 and add \n
                    strval = f.pointers[1].data.decode('utf-8')
                    if strval[-1] == '\x00':
                        strval = strval[:-1]
                    outfile.write(f" - {strval}\n")
            if self.sized_str_entry.LuaFilename:
            	outfile.write(f"Lua Controller: {self.sized_str_entry.LuaFilename[:-1]}\n")

        return out_path,


