import logging
import struct

from generated.formats.world.compound.WorldHeader import WorldHeader
from modules.formats.BaseFormat import BaseFile
import xml.etree.ElementTree as ET  # prob move this to a custom modules.helpers or utils?


# NOTE, World struct in JWE1 has an extra pointer this import/export is not accounting for yet
from modules.helpers import as_bytes


class WorldLoader(BaseFile):

    def create(self):
        self.sized_str_entry = self.create_ss_entry(self.file_entry)
        ss_ptr = self.sized_str_entry.pointers[0]

        world = self.load_xml(self.file_entry.path)
        assetPackages = world.findall('.//AssetPackage')
        luaController = world.findall('.//LuaController')
        Prefabs = world.findall('.//Prefab')

        self.header = WorldHeader(self.ovl.context)
        self.header.world_type = int(world.attrib['WorldType'])
        self.header.asset_pkg_count = len(assetPackages)
        self.header.prefab_count = len(Prefabs)
        self.write_to_pool(self.sized_str_entry.pointers[0], 2, as_bytes(self.header))

        self.write_list_at_rel_offset([e.text for e in assetPackages], ss_ptr, 8)
        self.write_list_at_rel_offset([e.text for e in Prefabs], ss_ptr, 48)

        if len(luaController):
            lua_frag = self.create_fragments(self.sized_str_entry, 1)[0]
            self.ptr_relative(lua_frag.pointers[0], self.sized_str_entry.pointers[0], 24)
            self.write_to_pool(lua_frag.pointers[1], 2, as_bytes(luaController[0].text))

    def collect(self):
        self.assign_ss_entry()
        logging.info(f"Collecting {self.sized_str_entry.name}")

        self.header = self.sized_str_entry.pointers[0].load_as(WorldHeader)[0]

        self.sized_str_entry.LuaFilename = None
        self.sized_str_entry.InstancesFile = None

        luaFilefragment = self.ovs.frag_at_pointer(self.sized_str_entry.pointers[0], offset=24)
        logging.info(f"Lua file fragment: {luaFilefragment}")
        if luaFilefragment:
            luaFilefragment.pointers[1].strip_zstring_padding()
            self.sized_str_entry.LuaFilename = luaFilefragment.pointers[1].data.decode('utf-8')
            logging.info(f"Lua file: {self.sized_str_entry.LuaFilename}")

        self.sized_str_entry.vars = self.get_string_list_at_offset(self.header.asset_pkg_count, 8)
        self.sized_str_entry.prefabs = self.get_string_list_at_offset(self.header.prefab_count, 48)

    def load(self, file_path):
        pass

    def extract(self, out_dir, show_temp_files, progress_callback):
        name = self.sized_str_entry.name
        logging.info(f"Writing {name}")
        xmldata = ET.Element('World')
        xmldata.set('WorldType', str(self.header.world_type))

        assetPkgs = ET.SubElement(xmldata, 'AssetPackages')
        for f in self.sized_str_entry.vars:
            assetpkg = ET.SubElement(assetPkgs, 'AssetPackage')
            assetpkg.text = f

        if self.sized_str_entry.LuaFilename:
            luafile = ET.SubElement(xmldata, 'LuaController')
            luafile.text = self.sized_str_entry.LuaFilename

        prefabs = ET.SubElement(xmldata, 'Prefabs')
        for f in self.sized_str_entry.prefabs:
            prefab = ET.SubElement(prefabs, 'Prefab')
            prefab.text = f

        out_path = out_dir(name)
        self.write_xml(out_path, xmldata)
        return out_path,
