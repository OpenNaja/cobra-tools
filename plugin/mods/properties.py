import uuid

from bpy.props import StringProperty, EnumProperty, IntProperty, FloatProperty
from bpy.types import PropertyGroup


def update_uuid(self, context):
	if self.uuid == "":
		self.uuid = str(uuid.uuid4())
	return


class ModData(PropertyGroup):
	"""Stores enough information to create a mod from this blender file"""
	name: StringProperty(name="Name", description='This is the human-readable name of the mod.')
	desc: StringProperty(name="Description", description="Mod's description is used to create the readme file.")
	uuid: StringProperty(name="UUID", description="Mod's uuid. Delete to generate a new one", update=update_uuid, )
	ordid: IntProperty(name="Order ID",
					   description="Mod's starting id for to assets (Use a free Id). IDs will be assigned consecutively (only for JWE2)")
	path: StringProperty(name="Mod Path", description="A folder will be created in this path for the mod files",
						 default="", maxlen=1024, subtype="DIR_PATH")
	pack: StringProperty(name="Pack into",
						 description="Create the ovl files for this mod into this folder, usually one level deep from the ovldata folder",
						 default="", maxlen=1024, subtype="DIR_PATH")


class SceneryData(PropertyGroup):
	"""Stores enough information to create a mod from this blender file"""
	name: StringProperty(name="Name", description='This is the human-readable name of the asset.')
	desc: StringProperty(name="Description", description="Asset long description.")
	price: FloatProperty(name="Price", min=0)
	cost: FloatProperty(name="Running cost", min=0)
