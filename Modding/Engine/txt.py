"""Localization Manager class

This class acts as an interface to a content pack txt files. Using this 
class will ensure the correct addition of txt files to the right locale.

NOTE: No templates allowed.

Example:
    To use this class individually, you wil create a custom manager instance, 
    add or remove txt entries.

            txtm = LocalizationManager()
            txtm.add('TEST_ID', 'TEST_ID has this content')
            txtm.export_contentpack('Mods', 'TestMod')

Todo:
    * Allow setting up pre-defined locale folders per game, and a method to write 
      them all at once (export_contentpack_all() )
    * Allow using non-localize folder other than of Main (can be done externally)
    * Allow importing only existing locales from a content pack (missing IDs will not be added)
      as way to load translations

"""
import os
import sys
import string

class LocalizationManager():

    def __init__(self, lang="English/UnitedKingdom"):
        """ If lang is present it is a path to the loc file, otherwise
            Main will be used to store the .txt files
            lang is part of the localization folder, if set to None, the txt
            files will be exported to Main
        """
        self.refs     = {}
        self.lang     = lang

    def add(self, ID, content=None):
        """Add or update a txt entry, if content is missing it will match the ID"""
        self.refs[ID] = content if content != None else ID

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


    def clean(self):
        """Remove all entries"""
        self.refs = {}

    def build_export_path(self, lang=None):
        """Return the export path depending on the localization options, 
           will use the initialized lang code or a custom one.
        """
        if lang == None:
            lang = self.lang

        if lang == None:
            return "Main"
        else:
            return os.path.join('Localised', lang, 'Loc')
        pass

    def import_contentpack(self, path, contentpack_name):
        """Read txt entries from a contentpack folder"""
        pass

    def export_contentpack(self, path, contentpack_name, lang=None):
        """Exports txt entries to {path}/{contentpack_name}/{export_path}/{ID}.txt"""

        inner_path = self.build_export_path(lang)

        if len(self.refs)> 0:
            contentpack_path = os.path.join(path, inner_path ,".")
            os.makedirs(contentpack_path, exist_ok=True)

        for name in self.refs:
            with open(os.path.join(contentpack_path, f"{name}.txt"), 'w') as f:
                f.write(self.refs[name])
                f.close()

    def export_csv(self, path):
        """export txt entries to a csv file"""
        with open(path, 'w') as f:
            for name in self.refs:
                f.write(f"{name},{self.refs[name]}\n")

    def import_csv(self, path):
        """Read txt entries from a csv file, one per line"""
        with open(path, 'r') as f:
            for line in f.readlines():
                name, value = line.rstrip().split(",", 1)
                self.add(name,value)


if __name__ == "__main__":

    # Write test_id.txt in english/unitedkingdom/loc for TestMod1
    txtm = LocalizationManager()
    txtm.add('TEST_ID', 'TEST_ID has this content')
    txtm.export_contentpack('Mods/TestMod1', 'TestMod1')

    # Write test_id_default.txt in Main for TestMod2
    txtm = LocalizationManager(lang=None)
    txtm.add('TEST_ID_Default')
    txtm.export_contentpack('Mods/TestMod2', 'TestMod2')
