import logging
import struct

from modules.formats.BaseFormat import BaseFile
import xml.etree.ElementTree as ET  # prob move this to a custom modules.helpers or utils?


# NOTE, World struct in JWE1 has an extra pointer this import/export is not accounting for yet
from modules.helpers import as_bytes


class WorldLoader(BaseFile):

    def create(self):
        self.sized_str_entry = self.create_ss_entry(self.file_entry)

        world = self.load_xml(self.file_entry.path)
        assetPackages = world.findall('.//AssetPackage')
        luaController = world.findall('.//LuaController')

        # struct size is 80 bytes: [type][ptr][count][luaptr][....] 80-
        ss = struct.pack("<QQQQ48s", int(world.attrib['WorldType']), 0, len(assetPackages), 0, b'')  # room for 80 bytes
        self.write_to_pool(self.sized_str_entry.pointers[0], 2, ss)

        if len(assetPackages):
            # point the list frag to the end of the data now.
            new_frag0 = self.create_fragments(self.sized_str_entry, 1)[0]
            self.ptr_relative(new_frag0.pointers[0], self.sized_str_entry.pointers[0], 8)
            self.ptr_relative(new_frag0.pointers[1], self.sized_str_entry.pointers[0], 80)

            # for each line, add the frag ptr space and create the frag ptr
            assetpkg_frags = self.create_fragments(self.sized_str_entry, len(assetPackages))
            for frag in assetpkg_frags:
                self.write_to_pool(frag.pointers[0], 2, b"\x00" * 8)

            for assetpkg, frag in zip(assetPackages, assetpkg_frags):
                self.write_to_pool(frag.pointers[0], 2, as_bytes(assetpkg.text))

        if len(luaController):
            lua_frag = self.create_fragments(self.sized_str_entry, 1)[0]
            self.ptr_relative(lua_frag.pointers[0], self.sized_str_entry.pointers[0], 24)
            self.write_to_pool(lua_frag.pointers[1], 2, as_bytes(luaController[0].text))

    def collect(self):
        self.assign_ss_entry()
        logging.info(f"Collecting {self.sized_str_entry.name}")

        # 1 used for main park worlds, 2 used for loading, 3 used for main menu or alike
        worldType = struct.unpack("<Q", self.sized_str_entry.pointers[0].data[:8])[0]
        self.sized_str_entry.worldType = worldType
        self.sized_str_entry.vars = []
        self.sized_str_entry.LuaFilename = None

        if len(self.sized_str_entry.pointers[0].data) == 80:  # no pointers into the data
            return

        if len(self.sized_str_entry.pointers[0].data) == 8:  # we have assetPackage list
            assetpgklistfragment = self.ovs.frags_from_pointer(self.sized_str_entry.pointers[0], 1)
            _, assetPkgCount = struct.unpack("<QQ", assetpgklistfragment[0].pointers[0].data)
            logging.info(f"AssetCount  {assetPkgCount}")

            self.sized_str_entry.assetPkgCount = assetPkgCount
            self.sized_str_entry.vars = self.ovs.frags_from_pointer(assetpgklistfragment[0].pointers[1], assetPkgCount)
            for var in self.sized_str_entry.vars:
                var.pointers[1].strip_zstring_padding()
                strval = var.pointers[1].data.decode('utf-8')
                logging.info(strval)

        # if we still have pointers, it has to be the Lua controller present in the world definition
        if len(self.sized_str_entry.pointers[0].data) == 24 or len(assetpgklistfragment[0].pointers[0].data) == 16:
            luaFilefragment = self.ovs.frags_from_pointer(self.sized_str_entry.pointers[0], 1)
            luaFilefragment[0].pointers[1].strip_zstring_padding()
            self.sized_str_entry.LuaFilename = luaFilefragment[0].pointers[1].data.decode('utf-8')
            logging.info(f"Lua file: {self.sized_str_entry.LuaFilename}")

    # in JWE1 at offset 0x40 there is a ptr to the lighting options

    def load(self, file_path):
        pass

    def extract(self, out_dir, show_temp_files, progress_callback):
        name = self.sized_str_entry.name
        logging.info(f"Writing {name}")
        # enumnamer only has a list of strings
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

        self.write_xml(out_path, xmldata)
        return out_path,
