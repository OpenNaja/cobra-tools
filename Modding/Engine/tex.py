"""Texture Manager class

This class acts as an interface to a content pack tex files. Using this 
class will ensure the correct addition of txt files to the right locale.

NOTE: This is a simplified texture manager able to create only icon items for now.
NOTE: No templates allowed for now, but should be reasonable easy to add them by game.
NOTE: image content can be provided by colour/size or content
NOTE: allow using assetpkg name instead of path and resolve from there.

Example:
    To use this class individually, you wil create a custom manager instance, 
    add or remove txt entries.

            texm = TextureManager()
            texm.add('TEST_ID', path='Icons', size=(200,100))
            texm.export_contentpack('Mods', 'TestMod')

Todo:
    * Allow setting up image type (currently hardcoded to BC7_UNORM)

"""
import os
import sys

# for image generation
import PIL.Image as Image
from io import BytesIO


class TextureManager():

    def __init__(self):
        """ If lang is present it is a path to the loc file, otherwise
            Main will be used to store the .txt files
            lang is part of the localization folder, if set to None, the txt
            files will be exported to Main
        """
        self.refs     = {}

    def add(self, ID, content=None, path=None, size=None, color=(0, 0, 0, 0) ):
        """Add or update a txt entry, if content is missing it will match the ID"""
        if content == None and size:
            content = self.create_png_bytes(size, color)

        self.refs[ID] = content if content != None else ID

        self.refs[ID] = {
            'content' : content,
            'path': path,
            #'compress': compress
        }

    def remove(self, ID):
        """Remove a txt entry"""
        if ID in self.refs:
            del self.refs[ID]

    def get(self, ID):
        """Get the localized value of an entry"""
        if ID in self.refs:
            return self.refs[ID]
        return None

    def getAll(self):
        """return all current txt entries"""
        return self.refs

    def get_path(self, ID):
        """Get the path value of an entry"""
        if ID in self.refs:
            return self.refs[ID]["path"]
        return None

    def get_content(self, ID):
        """Get the data value of an entry"""
        if ID in self.refs:
            return self.refs[ID]["content"]
        return None

    def clean(self):
        """Remove all entries"""
        self.refs = {}

    def build_export_path(self, path):
        """Return Main or the assetpkg location"""
        if path == None:
            return 'Main'
        return path

    def export_contentpack(self, path, contentpack_name):
        """Exports txt entries to {path}/{texture_path}/{ID}.txt"""

        for name in self.refs:
            assetpath = self.build_export_path(self.refs[name]["path"])
            dest_path = os.path.join(path, assetpath, ".")
            os.makedirs(dest_path, exist_ok=True)

            with open(f"{dest_path}/{name}.png", 'wb') as f:
                f.write(self.refs[name]['content'])
            with open(f"{dest_path}/{name}.tex", 'w') as f:
                f.write('<TexHeader compression_type="DdsType.BC7_UNORM" one_0="0" stream_count="1" stream_count_repeat="1" game="Games.PLANET_ZOO"><buffer_infos pool_type="3"><texbuffer offset="0" size="0" first_mip="0" mip_count="1" /></buffer_infos><size_info pool_type="4"><data data_size="0" width="0" height="0" num_mips="1"><mip_maps><mipmap offset="0" size="0" size_array="0" size_scan="0" size_data="0" /></mip_maps></data><padding></padding></size_info></TexHeader>')

    #
    # Helper functions
    #
    def create_png_bytes(self, size, color):
        """Create png bytes of specific width/height/color"""
        buffer = BytesIO()
        img = Image.new('RGBA', size, color)
        img.save(buffer, "PNG", optimize=True, compress_level=9)
        return buffer.getvalue()



if __name__ == "__main__":

    texm = TextureManager()
    # save as ./test/ui/textures/icons/something.png
    texm.add("test1", size=(150, 150), color=(128,128,0,255), path=os.path.join('UI', 'Textures', "Icons"))
    texm.add("test2", size=(350, 350), color=(255,255,128,255), path=os.path.join('UI', 'Textures', "Icons"))

    # save as ./test/main/something.png
    pngdata = texm.create_png_bytes((128,128), (128,128,128,255))
    texm.add("test3", content=pngdata)

    texm.export_contentpack("Mods/TestMod2", "test")
