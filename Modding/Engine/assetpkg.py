"""AssetPackage Manager class

This class acts as an interface to a content pack assetpackage files. Using this 
class will ensure the path is provided for different in game assets.

Assetpackages are created using relative paths from the content pack folder, but
they need to include the full path from OVLData

When exporting the assetpkg data, the .assetpkg file will be added to the Init folder
and the full assetpkg path will be created. This folder needs to be turned into an ovl.

NOTE: No templates allowed.

Example:
    To use this class individually, you wil create a custom manager instance, 

            assetpkgm = AssetPackageManager()
            assetpkgm.add('AssetpkgTest', os.path.join('UI', 'Textures'))
            assetpkgm.export_contentpack('Mods', 'TestMod')
            # will create /Mods/TestMod/UI/Textures/AssetpkgTest/ 
            # will create /Mods/TestMod/Init/AssetpghTest.assetpkg
            print(assetpkgm.add('AssetpkgTest'))
            # will print UI/Textures/AssetpkgTest/

Todo:
    * Consider returning the path of the assetpkg including the mods/{name} part
    * Allow context to populate the assetpkg xml (currently hardcoded for Planet Zoo)

"""
import os
import sys
import string

class AssetPackageManager():

    def __init__(self):
        self.refs = {}

    def add(self, name, prefix=''):
        """ Creates an assetpkg entry, will append the ID to the path """
        self.refs[name] = os.path.normpath(os.path.join(prefix, name))
        return self.refs[name]

    def remove(self, name):
        """ Remove an assetpkg entry"""
        if name in self.refs:
            del self.refs[name]

    def get(self, name):
        """ returns the assetpkg path """
        if name in self.refs:
            return self.refs[name]
        else:
            return None

    def clean(self):
        """Remove all assetpkg entries"""
        self.refs = {}

    def get_or_add(self, name, prefix=''):
        """ returns the assetpkg path, make a new one if needed, but do not override the existing one"""
        if name not in self.refs:
            self.add(name, prefix)
            
        return self.refs[name]

    def add_raw(self, name, path):
        """ adds an assetpkg with a specific path """
        self.refs[name] = path 

    def export_contentpack(self, path, contentpack_name, context='PLANET_ZOO'):

        if len(self.refs) > 0:
            assetpkg_path = os.path.join(path, 'Init', ".")
            os.makedirs(assetpkg_path, exist_ok=True)

        for name in self.refs:

            # Create the assetpkg path
            assetpkg_path = os.path.join(path, self.refs[name] , ".")
            os.makedirs(assetpkg_path, exist_ok=True)

            # Create the assetpkg file
            assetpkg_path = os.path.normpath(os.path.join('OvlData', contentpack_name, self.refs[name]))
            file_path = os.path.normpath(os.path.join(path, 'Init'))
            with open(os.path.join(file_path, f"{name}.assetpkg"), 'w') as f:
                f.write(f"<AssetpkgRoot game=\"Games.{context}\">\n  <asset_path>{assetpkg_path}</asset_path>\n</AssetpkgRoot>")
                f.close()


if __name__ == "__main__":

    assetpkgm = AssetPackageManager()
    assetpkgm.add('AssetpkgTest', os.path.join('UI', 'Textures'))
    assetpkgm.export_contentpack('Mods/TestMod2', 'TestMod2')
    # will create /Mods/TestMod/UI/Textures/AssetpkgTest/ 
    # will create /Mods/TestMod/Init/AssetpghTest.assetpkg

    print(assetpkgm.add('AssetpkgTest'))
    # will print UI/Textures/AssetpkgTest/
