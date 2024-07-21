"""UserInterfaceIcon Manager class
This class acts as an interface to a content pack UI icondata files. Using this 
class will ensure the correct addition of icondata files to the right location.

NOTE: No templates allowed.


    uidm = UserInterfaceIconDataManager(path='AssetPackagesExtrasList')
    uidm.add("test1", 'testincons_assetpackage')
    uidm.add("test2", 'testincons_assetpackage')
    uidm.add("test3", 'testincons_assetpackage', texture='test1')
    uidm.export_contentpack(".", "test")


Todo:
    * Allow reusing a texture for a diff userinterfaceicondata
    * Use the context to setup the right .userinterfaceicondata game
    * This class assumes a single location for all .userinterfaceicondata files instead
      of individual location of each file.

"""
import os
import sys

# for image generation
import PIL.Image as Image
from io import BytesIO

class UserInterfaceIconDataManager():

    def __init__(self, path='Main'):
        """ If path is present it is a path for the .userinterfaceicondata files, 
            otherwise Main will be used to store the .txt files. If an assetpkg 
            manager is provided, the path will be retrieved using the assetpkg name.
            path is the destination folder for the .userinterfaceicondata files
        """
        self.refs = {}
        self.path = path

    def add(self, name, assetpkg, texture=None):
        """ Adds a .userinterfaceicondata element"""
        self.refs[name] = {
            'texture' : name if texture == None else texture,
            'assetpkg': assetpkg
        }

    def remove(self, name):
        """ removes a .userinterfaceicondata element"""
        if name in self.refs:
            del self.refs[name]

    def get(self, name):
        """ removes a .userinterfaceicondata element"""
        if name in self.refs:
            return self.refs[name]

    def get_assetpkg(self, name):
        """Return the assetpkg name of this userinterfaceicondata"""
        if name in self.refs:
            return self.refs[name]['assetpkg']
        return None

    def get_texture(self, name):
        """Return the texture name of this userinterfaceicondata"""
        if name in self.refs:
            return self.refs[name]['texture']
        return None

    def export_contentpack(self, path, contentpack_name, context='PLANET_ZOO'):
        """Creates folders required and files to store the .userinterfaceicondata files"""
        contentpack_path = os.path.join(path, self.path ,".")
        os.makedirs(contentpack_path, exist_ok=True)

        # Maybe this needs to be moved to a tex handler
        for name in self.refs:
            with open(os.path.join(contentpack_path, f"{name}.userinterfaceicondata"), 'w') as f:
                f.write(f"<UserinterfaceicondataRoot game=\"Games.{context}\"><tex_name pool_type=\"2\">{self.refs[name]['texture']}</tex_name><ovl_name pool_type=\"2\">{self.refs[name]['assetpkg']}</ovl_name></UserinterfaceicondataRoot>")


if __name__ == "__main__":

    uidm = UserInterfaceIconDataManager(path='AssetPackagesExtrasList')
    uidm.add("test1", 'testincons_assetpackage')
    uidm.add("test2", 'testincons_assetpackage')
    uidm.add("test3", 'testincons_assetpackage', texture='test1')
    uidm.export_contentpack("Mods/TestMod2", "TestMod2")
