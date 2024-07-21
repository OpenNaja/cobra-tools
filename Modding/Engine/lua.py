"""Lua Manager class

This class acts as an interface to a content pack lua files. Using this 
class will ensure the correct addition of lua files to the right folder,
and allow extra validation before adding the lua files.

NOTE: No templates allowed.

Example:
    To use this class individually, you wil create a custom manager instance, 
    add or remove txt entries.

            # by default lua files will be saved in 'Lua'
            luam = LuaManager(path='Lua')

            luam.add('TEST_ID', '-- this is some lua content')
            # lua files can still be define a custom folder
            luam.add('TEST_ID', '-- this is some lua content', path='Init')
            luam.export_contentpack('Mods', 'TestMod')

Todo:
    * LUA files need to have a custom path attribute (for luas in INIT, or other assetpackages)
    * Allow injecting .luac files

"""
import os
import sys
import string

class LuaManager():

    def __init__(self, path="Main"):
        self.refs     = {}
        self.path     = path

    def add(self, ID, content, path=None):
        """Add or update a lua entry"""
        self.refs[ID] = {
            'content': content, 
            'path'   : self.path if path==None else path
        }

    def remove(self, ID):
        """Remove a lua entry"""
        if ID in self.refs:
            del self.refs[ID]

    def get(self, ID):
        """Get the content of a Lua entry"""
        if ID in self.refs:
            return self.refs[ID]
        return None

    def get_content(self, ID):
        """Get the content of a Lua entry"""
        if ID in self.refs:
            return self.refs[ID]['content']
        return None

    def get_path(self, ID):
        """Get the path of a Lua entry"""
        if ID in self.refs:
            return self.refs[ID]['path']
        return None

    def getAll(self):
        """return all current txt entries"""
        return self.refs

    def clean(self):
        """Remove all entries"""
        self.refs = {}

    def import_contentpack(self, path, contentpack_name):
        """Read txt entries from a contentpack folder"""
        pass

    def export_contentpack(self, exportpath, contentpack_name, path=None):
        """Exports txt entries to {exportpath}/{export_path}/{ID}.lua"""
    
        for name in self.refs:
            contentpack_path = os.path.join(exportpath, self.get_path(name) ,".")
            os.makedirs(contentpack_path, exist_ok=True)
            with open(os.path.join(contentpack_path, f"{name}.lua"), 'w') as f:
                f.write(self.refs[name]['content'])
                f.close()


if __name__ == "__main__":

    luam = LuaManager()
    luam.add('TEST_PREFAB_ID', '-- this is some lua content', path='Prefabs')
    luam.add('TEST_Main_ID', '-- this is some lua content')
    luam.export_contentpack('Mods/TestMod2', 'TestMod2')
