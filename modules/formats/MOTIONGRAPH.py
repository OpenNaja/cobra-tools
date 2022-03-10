import logging
import struct

from generated.formats.motiongraph.compound.MotiongraphHeader import MotiongraphHeader
from generated.formats.motiongraph.compound.MotiongraphRootFrag import MotiongraphRootFrag
from generated.formats.uimoviedefinition.compound.UiMovieHeader import UiMovieHeader
from modules.formats.BaseFormat import BaseFile
from modules.helpers import as_bytes
import xml.etree.ElementTree as ET  # prob move this to a custom modules.helpers or utils?


class MotiongraphLoader(BaseFile):

    def collect(self):
        self.assign_ss_entry()
        logging.info(f"Collecting {self.sized_str_entry.name}")
        if self.ovl.context.version > 47:
            self.header = self.sized_str_entry.pointers[0].load_as(MotiongraphHeader)[0]
            root_frag = self.ovs.frags_from_pointer(self.sized_str_entry.pointers[0], 1)[0]
            print(self.header)
            self.root_struct = root_frag.pointers[1].load_as(MotiongraphRootFrag)[0]
            print(self.root_struct)

    # def extract(self, out_dir, show_temp_files, progress_callback):
    #     name = self.sized_str_entry.name
    #     logging.info(f"Writing {name}")
    #
    #     xmldata = ET.Element('UIMovieDefinition')
    #     xmldata.set('MovieName', str(self.MovieName))
    #     xmldata.set('PkgName', str(self.PkgName))
    #     xmldata.set('CategoryName', str(self.CategoryName))
    #     xmldata.set('TypeName', str(self.TypeName))
    #     xmldata.set('flags1', str(self.header.flag_1))
    #     xmldata.set('flags2', str(self.header.flag_2))
    #     xmldata.set('flags3', str(self.header.flag_3))
    #     xmldata.set('float1', str(self.header.floats[0]))
    #     xmldata.set('float2', str(self.header.floats[1]))
    #     xmldata.set('float3', str(self.header.floats[2]))
    #
    #     for cl in self.ui_triggers:
    #         clitem = ET.SubElement(xmldata, 'UITrigger')
    #         clitem.text = cl
    #
    #     for cl in self.ui_names:
    #         clitem = ET.SubElement(xmldata, 'Control')
    #         clitem.text = cl
    #
    #     for cl in self.assetpkgs:
    #         clitem = ET.SubElement(xmldata, 'AssetPackage')
    #         clitem.text = cl
    #
    #     for cl in self.ui_interfaces:
    #         clitem = ET.SubElement(xmldata, 'Interface')
    #         clitem.text = cl
    #
    #     for cl in self.Count1List:
    #         clitem = ET.SubElement(xmldata, 'List1')
    #         clitem.text = str(cl)
    #
    #     for cl in self.Count2List:
    #         clitem = ET.SubElement(xmldata, 'List2')
    #         clitem.text = str(cl)
    #
    #     out_path = out_dir(name)
    #     self.write_xml(out_path, xmldata)
    #     return out_path,
