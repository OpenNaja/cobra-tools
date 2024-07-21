import os
import sys

from manifest import Manifest
import assetpkg, userinterfaceicondata, tex, txt, lua, fdb

class ContentPack:

	""" Main content-pack/mod class """
	def __init__(self, name, context=None, id=None, description=None, folder=None):
		self.manifest     = Manifest(name, id)
		self.context      = context
		self.folder       = folder if folder !=None else os.path.join('Mods', name)
		self.ovlsincludes = []

		self.apkm = assetpkg.AssetPackageManager()
		self.txtm = txt.LocalizationManager()
		self.texm = tex.TextureManager()
		self.luam = lua.LuaManager()
		self.uidm = userinterfaceicondata.UserInterfaceIconDataManager()
		self.fdbm = fdb.DatabaseManager()
		print(f"Context is: {self.context}")



	def load_from_folder(self, folder):
		""" Read content pack information from a mod folder"""
		self.folder = folder
		self.manifest.from_xml(folder)
		# unfinished

	def load(self):
		if self.folder:
			self.load_from_folder(self.folder)
		else:
			raise AssertionError("Folder not defined")

	def add_ovls_include(self, folders):
		self.ovlsincludes.append(folders)

	def create_ovls_include(self, folder, included_ovls):
		# Make sure the folders exist
		for path in included_ovls:
			os.makedirs(os.path.join(folder, path), exist_ok=True)

		ovls_content = "\n".join(included_ovls)
		ovs_include_file = os.path.join(folder, 'Main', 'ovls.include')
		
		self.write_file(ovs_include_file, ovls_content)

	def get_path(self, name):
		return os.path.join(self.folder, name)

	def make_default_structure(self, folder, extra_folders=None, extra_ovls=None):
		if len(self.ovlsincludes):
			self.create_ovls_include(folder, self.ovlsincludes)

	def insert_into(self, name, dbtable, tArgs):
		self.fdbm.insert_into(name, dbtable, tArgs)

	def write_to_folder(self, folder):
		""" Writes the content pack information to a folder """

		self.manifest.to_xml(folder)

		self.make_default_structure(folder)
		name = self.manifest.name

		self.apkm.export_contentpack(folder, os.path.basename(folder), self.context)
		self.txtm.export_contentpack(folder, name)
		self.texm.export_contentpack(folder, name, context=self.context)
		self.luam.export_contentpack(folder, name)
		self.uidm.export_contentpack(folder, name, context=self.context)
		self.fdbm.export_contentpack(folder, name)

	def write(self):
		if self.folder:
			self.write_to_folder(self.folder)
		else:
			raise AssertionError("Folder not defined")

	def from_json(self, path):
		""" Reads the content pack information from a json file """

	def to_json(self, path):
		""" Writes the content pack information to a json file """

	def __str__(self):
		ret  = str(self.manifest)
		ret += f"\nPath: {self.folder}"
		return ret

	#
	# Regular interface
	#
	def add_assetpkg(self, name, path=''):
		self.apkm.add(name, path)

	def add_assetpkg_raw(self, name, path):
		self.apkm.add_raw(name, path)

	def add_txt(self, name, value=None):
		self.txtm.add(name, value)

	def add_userinterfaceicondata(self,  name, assetpkg, texture=None):
		self.uidm.add(name, assetpkg, texture)

	def add_lua(self, name, content, path=None):
		self.luam.add(name, content, path)

	def add_tex(self, ID, content=None, path=None, size=None, color=(0, 0, 0, 0) ):
		self.texm.add(ID, content, path, size, color)

	def add_ui_icon(self, name, folder, content=None, size=None, color=(0, 0, 0, 0)):
		assetpkg_name = os.path.basename(os.path.normpath(folder))
		self.add_assetpkg_raw(assetpkg_name, folder)
		self.add_tex(name, path=folder, size=size, color=color, content=content)
		self.add_userinterfaceicondata(name, assetpkg_name)

	def write_file(self, file_path, file_content, overwrite=False):
	    """ write  content to a file
	    :param path: file path
	    :param content: the content to write
	    :return: content of the file
	    """ 
	    self.ensure_folders(file_path)

	    if overwrite == False and os.path.exists(file_path):
	        return False

	    with open(file_path, 'w') as f:
	        content = f.write(file_content.strip())
	        f.close
	        return True  

	def ensure_folders(self, file_path):
	    try:
	        os.makedirs(os.path.dirname(file_path), exist_ok=True)
	    except:
	        pass


if __name__ == "__main__":

	name = 'Test'
	mod = ContentPack(name, context='PLANET_ZOO')

	# Work on PZ, can be added to ContentPack based on context
	mod.fdbm.templates_path = os.path.join('Modding', 'Games', 'Planet_Zoo', 'Data')
	mod.fdbm.templates      = {
		'ModularScenery': ['ContentPacks', 'LocalGridAlignmentStyle', 'MoveObjectType', 'PlacementPartType', 'TagGroupsDefinition'],
	}

	# userinterfaceicondata manager will export to 'AssetPackagesExtrasList'
	mod.uidm.path = 'AssetPackagesExtrasList'

	# we want our mod to have a custom UI place for infoboards
	mod.add_ovls_include(os.path.join("UI", "Textures", 'Infoboards_' + name))

	# we want the mod to export .userinterfaceicondata into /AssetPackagesExtrasList
	mod.add_ovls_include('AssetPackagesExtrasList')

	# we will add some Lua files to the 'Prefabs' folder
	mod.add_ovls_include('Prefabs')

	# add a txt to the default lang
	mod.add_txt('TEST_ID1', '_TEST_ID1_')
	mod.add_txt('TEST_ID2')

	# add lua to the Main folder
	mod.add_lua('LUA_ID1', '---content')

	# add lua to the prefabs folder
	mod.add_lua('LUA_PREFAB', '---content', path='Prefabs')

	# make a new texture, add assetpkg and associate texture
	mod.add_tex('text1', b"PNG", "ICONS")
	mod.add_assetpkg('ICONS')
	mod.add_userinterfaceicondata('text1', 'ICONS')

	# make a UI icon, with userinterfaceicondata and assetpkg
	mod.add_ui_icon('test_full_icon', 'this/path/to/assetpkg', b"PNG")

	# make a new texture 
	mod.add_tex('some_ed_infoboard.pemissive', b"PNG", os.path.join("UI", "Textures", 'Infoboards_' + name))

	# add a blueprint entry
	tArgs = {
		"SceneryPartName"    : 'TestPart_001',
		"PlacementPartType"  : 'SimpleScenery',
		"MoveObjectType"     : 'AttachmentProp',
		"ContentPack"        : 'BaseGame'
	}
	mod.fdbm.insert_into('ModularScenery', 'ModularSceneryParts', tArgs)

	mod.write()

