import logging
import xml.etree.ElementTree as ET

from generated.formats.world.compound.WorldHeader import WorldHeader
from modules.formats.BaseFormat import BaseFile
from modules.helpers import as_bytes


class WorldLoader(BaseFile):

    def create(self):
        self.sized_str_entry = self.create_ss_entry(self.file_entry)
        ss_ptr = self.sized_str_entry.pointers[0]

        xml = self.load_xml(self.file_entry.path)
        assetPackages = xml.findall('.//AssetPackage')
        luaController = xml.findall('.//LuaController')
        Prefabs = xml.findall('.//Prefab')

        self.header = WorldHeader(self.ovl.context)
        self.header.world_type = int(xml.attrib['WorldType'])
        self.header.asset_pkg_count = len(assetPackages)
        self.header.prefab_count = len(Prefabs)

        self.write_to_pool(self.sized_str_entry.pointers[0], 2, as_bytes(self.header))
        self.write_str_at_rel_offset(luaController[0].text, ss_ptr, 24)
        self.write_str_list_at_rel_offset([e.text for e in assetPackages], ss_ptr, 8)
        self.write_str_list_at_rel_offset([e.text for e in Prefabs], ss_ptr, 48)

    def collect(self):
        self.assign_ss_entry()
        logging.info(f"Collecting {self.sized_str_entry.name}")

        self.header = self.sized_str_entry.pointers[0].load_as(WorldHeader)[0]
        self.sized_str_entry.lua_name = self.get_str_at_offset(24)
        self.sized_str_entry.asset_pkgs = self.get_str_list_at_offset(self.header.asset_pkg_count, 8)
        self.sized_str_entry.prefabs = self.get_str_list_at_offset(self.header.prefab_count, 48)

    def load(self, file_path):
        pass

    def extract(self, out_dir, show_temp_files, progress_callback):
        name = self.sized_str_entry.name
        logging.info(f"Writing {name}")
        xml = ET.Element('World')
        xml.set('WorldType', str(self.header.world_type))

        assetPkgs = ET.SubElement(xml, 'AssetPackages')
        for f in self.sized_str_entry.asset_pkgs:
            assetpkg = ET.SubElement(assetPkgs, 'AssetPackage')
            assetpkg.text = f

        if self.sized_str_entry.lua_name:
            luafile = ET.SubElement(xml, 'LuaController')
            luafile.text = self.sized_str_entry.lua_name

        prefabs = ET.SubElement(xml, 'Prefabs')
        for f in self.sized_str_entry.prefabs:
            prefab = ET.SubElement(prefabs, 'Prefab')
            prefab.text = f

        out_path = out_dir(name)
        self.write_xml(out_path, xml)
        return out_path,
