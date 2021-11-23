import struct

from generated.formats.ovl.versions import *
from modules.formats.BaseFormat import BaseFile
from modules.formats.shared import get_padding
from modules.helpers import zstr
from ovl_util import texconv
from ovl_util.interaction import showdialog
import xml.etree.ElementTree as ET # prob move this to a custom modules.helpers or utils?

# NOTE, World struct in JWE1 has an extra pointer this import/export is not accounting for yet

class WorldLoader(BaseFile):

    def create(self):
        ss = self.get_content(self.file_entry.path)
        pool_index, pool = self.get_pool(2)
        offset = pool.data.tell()
        self.sized_str_entry = self.create_ss_entry(self.file_entry)
        self.sized_str_entry.pointers[0].pool_index = pool_index
        self.sized_str_entry.pointers[0].data_offset = offset

        xmldata = ET.ElementTree(ET.fromstring(ss))

        world = xmldata.getroot()
        assetPackages = xmldata.findall('.//AssetPackage')
        luaController = xmldata.findall('.//LuaController')

        assetPkgList = []
        for assetpkg in assetPackages:
            assetPkgList.append(assetpkg.text)

        # struct size is 0x50 bytes: [type][ptr][count][luaptr][....] 80-
        pool.data.write(struct.pack("<QQQQ48s", int(world.attrib['WorldType']), 0, len(assetPackages), 0, b''))  # room for 0x50 bytes

        # offset where first string starts
        doffset = pool.data.tell()

        # pack assetpackage list now.. we are not doing rstrip to the lines.. worth considering to remove extra spaces
        pool.data.write("\00".join(assetPkgList).encode('utf-8'))

        # new offset for list pointers
        poffset = pool.data.tell()

        # point the list frag to the end of the data now.
        new_frag0 = self.create_fragment()
        new_frag0.pointers[0].pool_index = pool_index
        new_frag0.pointers[0].data_offset = offset + 0x8
        new_frag0.pointers[1].pool_index = pool_index
        new_frag0.pointers[1].data_offset = poffset

        # for each line, add the frag ptr space and create the frag ptr
        for x in assetPkgList:
            pool.data.write(struct.pack("<8s", b''))
            strfrag = self.create_fragment()
            strfrag.pointers[0].pool_index = pool_index
            strfrag.pointers[0].data_offset = poffset
            strfrag.pointers[1].pool_index = pool_index
            strfrag.pointers[1].data_offset = doffset

            poffset += 8
            doffset += len(x) + 1 # skip string lenght

        pass

        if len(luaController): 
            # new offset for the Lua data
            loffset = pool.data.tell()

            # point the lua ptr frag to the end of the data now.
            new_frag0 = self.create_fragment()
            new_frag0.pointers[0].pool_index = pool_index
            new_frag0.pointers[0].data_offset = offset + 0x18
            new_frag0.pointers[1].pool_index = pool_index
            new_frag0.pointers[1].data_offset = loffset

            # write the lua name now
            pool.data.write(f"{luaController[0].text}\00".encode('utf-8'))


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
        out_files = []
        out_path = out_dir(name)
        xmldata = ET.Element('World')
        xmldata.set('WorldType', str(self.sized_str_entry.worldType))

        assetPkgs = ET.SubElement(xmldata, 'AssetPackages')
        for f in self.sized_str_entry.vars:
            # convert from bytes to string, remove trailing 0x00 and add \n
            strval = f.pointers[1].data.decode('utf-8')
            if strval[-1] == '\x00':
                strval = strval[:-1]
            assetpkg = ET.SubElement(assetPkgs, 'AssetPackage')
            assetpkg.text = strval

        if self.sized_str_entry.LuaFilename:
            luafile = ET.SubElement(xmldata, 'LuaController')
            luafile.text = self.sized_str_entry.LuaFilename[:-1]

        xmltext = ET.tostring(xmldata)

        with open(out_path, 'w') as outfile:
            outfile.write(xmltext.decode('utf-8'))
            out_files.append(out_path)
            
        return out_files

