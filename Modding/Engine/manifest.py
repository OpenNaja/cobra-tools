"""Manifest class

This class acts as an interface to a content pack manifest file.

NOTE: No templates allowed.
NOTE: This class is a subhelper for the ContentPack class.

Example:
    To use this class individually, you wil create a custom instance providing a 
    content-pack name, and then read from or write to xml to a mod base path.

    mfs = Manifest('Test')   # ContentPack name
    xml = mfs.to_xml('Test') # Mod folder path


"""

import os
import uuid
import xml.etree.cElementTree as ET

def ensure_folders(file_path):
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
    except:
        pass

def load(mod_path):
	tree = ET.parse(os.path.join(mod_path, 'Manifest.xml'))
	root = tree.getroot()
	name = root.find('Name').text
	id = root.find('ID').text
	return name, id

def save(file_path, name, id=None):
	ensure_folders(file_path)

	""" Creates the XML and saves the manifest file"""
	if id == None:
		id = uuid.uuid1()

	root = ET.Element("ContentPack", version="1")
	ET.SubElement(root, "Name").text = name
	ET.SubElement(root, "ID").text = str(id)
	ET.SubElement(root, "Version").text = "1"
	ET.SubElement(root, "Type").text = "Game"
	tree = ET.ElementTree(root)
	ET.indent(tree, space="\t", level=0)
	tree.write(file_path)

def add(mod_path, name, id=None):
	""" Creates a manifest file on a mod folder path """
	save(os.path.join(mod_path, 'Manifest.xml'), name, id)


class Manifest:

	""" Main content-pack/mod class """
	def __init__(self, name, id=None):
		self.name = name
		self.id = id if id != None else uuid.uuid1()

	def from_xml(self, folder_path):
		self.name, self.id = load(folder_path)

	def to_xml(self, folder_path):
		add(folder_path, self.name, self.id)

	def __str__(self):
		return f"{self.name} : {self.id}"


if __name__ == "__main__":

    mfs = Manifest('TestMod')
    xml = mfs.to_xml('Mods/TestMod')
