bl_info = {
	"name": "Frontier's Cobra Engine Formats (JWE, Planet Zoo)",
	"author": "Harlequinz Ego & HENDRIX",
	"blender": (2, 92, 0),
	"version": (2, 3, 3),
	"location": "File > Import-Export",
	"description": "Import-Export models, skeletons and animations.",
	"warning": "",
	"wiki_url": "https://github.com/OpenNaja/cobra-tools",
	"support": 'COMMUNITY',
	"tracker_url": "https://github.com/OpenNaja/cobra-tools/issues/new",
	"category": "Import-Export"}


import os
import sys
import traceback
plugin_dir = os.path.dirname(__file__)
if not plugin_dir in sys.path:
	sys.path.append(plugin_dir)

import logging
from ovl_util.config import logging_setup, get_version_str
logging_setup("blender_plugin")
logging.info(f"Running python {sys.version}")
logging.info(f"Running cobra-tools {get_version_str()}")

import bpy
import bpy.utils.previews
from bpy.props import StringProperty, BoolProperty, CollectionProperty
from bpy_extras.io_utils import ImportHelper, ExportHelper
from . import addon_updater_ops

from plugin import import_bani, import_manis, import_matcol, import_mdl2, export_mdl2, import_voxelskirt
from plugin.modules_import.hair import vcol_to_comb, comb_to_vcol
from plugin.utils import shell

preview_collection = bpy.utils.previews.new()


def handle_errors(inst, func, kwargs):
	try:
		for msg in func(**kwargs):
			inst.report({"INFO"}, msg)
	except Exception as err:
		inst.report({"ERROR"}, str(err))
		traceback.print_exc()
	return {'FINISHED'}


class CobraPreferences(bpy.types.AddonPreferences):
	"""Cobra preferences"""
	bl_idname = __package__

	# Addon updater preferences.

	auto_check_update: bpy.props.BoolProperty(
		name="Auto-check for Update",
		description="If enabled, auto-check for updates using an interval",
		default=False)

	updater_interval_months: bpy.props.IntProperty(
		name='Months',
		description="Number of months between checking for updates",
		default=0,
		min=0)

	updater_interval_days: bpy.props.IntProperty(
		name='Days',
		description="Number of days between checking for updates",
		default=1,
		min=0,
		max=31)

	updater_interval_hours: bpy.props.IntProperty(
		name='Hours',
		description="Number of hours between checking for updates",
		default=0,
		min=0,
		max=23)

	updater_interval_minutes: bpy.props.IntProperty(
		name='Minutes',
		description="Number of minutes between checking for updates",
		default=0,
		min=0,
		max=59)

	def draw(self, context):
		# Updater draw function, could also pass in col as third arg.
		addon_updater_ops.update_settings_ui(self, context)


class ImportBani(bpy.types.Operator, ImportHelper):
	"""Import from Cobra baked animations file format (.bani)"""
	bl_idname = "import_scene.cobra_bani"
	bl_label = 'Import Bani'
	bl_options = {'UNDO'}
	filename_ext = ".bani"
	filter_glob: StringProperty(default="*.bani", options={'HIDDEN'})
	files: CollectionProperty(type=bpy.types.PropertyGroup)
	# set_fps = BoolProperty(name="Adjust FPS", description="Set the scene to FPS used by BANI", default=True)

	def execute(self, context):
		keywords = self.as_keywords(ignore=("axis_forward", "axis_up", "filter_glob"))
		return import_bani.load(**keywords)


class ImportManis(bpy.types.Operator, ImportHelper):
	"""Import from Cobra animations file format (.manis)"""
	bl_idname = "import_scene.cobra_manis"
	bl_label = 'Import Manis'
	bl_options = {'UNDO'}
	filename_ext = ".manis"
	filter_glob: StringProperty(default="*.manis", options={'HIDDEN'})
	files: CollectionProperty(type=bpy.types.PropertyGroup)
	# set_fps = BoolProperty(name="Adjust FPS", description="Set the scene to FPS used by BANI", default=True)

	def execute(self, context):
		keywords = self.as_keywords(ignore=("axis_forward", "axis_up", "filter_glob"))
		return import_manis.load(**keywords)


class ImportMatcol(bpy.types.Operator, ImportHelper):
	"""Import from Matcol file format (.matcol)"""
	bl_idname = "import_scene.cobra_matcol"
	bl_label = 'Import Matcol'
	bl_options = {'UNDO'}
	filename_ext = ".matcol"
	filter_glob: StringProperty(default="*.matcol", options={'HIDDEN'})

	def execute(self, context):
		keywords = self.as_keywords(ignore=("axis_forward", "axis_up", "filter_glob"))
		return handle_errors(self, import_matcol.load, keywords)


class ImportMDL2(bpy.types.Operator, ImportHelper):
	"""Import from MDL2 file format (.MDL2)"""
	bl_idname = "import_scene.cobra_mdl2"
	bl_label = 'Import MDL2'
	bl_options = {'UNDO'}
	filename_ext = ".mdl2"
	filter_glob: StringProperty(default="*.mdl2", options={'HIDDEN'})
	use_custom_normals: BoolProperty(name="Use MDL2 Normals", description="Preserves the original shading of a MDL2.", default=False)
	mirror_mesh: BoolProperty(name="Mirror Meshes", description="Mirrors models. Careful, sometimes bones don't match!", default=False)

	def execute(self, context):
		keywords = self.as_keywords(ignore=("axis_forward", "axis_up", "filter_glob"))
		return handle_errors(self, import_mdl2.load, keywords)


class ImportVoxelskirt(bpy.types.Operator, ImportHelper):
	"""Import from Voxelskirt file format (.voxelskirt)"""
	bl_idname = "import_scene.cobra_voxelskirt"
	bl_label = 'Import Voxelskirt'
	bl_options = {'UNDO'}
	filename_ext = ".voxelskirt"
	filter_glob: StringProperty(default="*.voxelskirt", options={'HIDDEN'})
	# use_custom_normals: BoolProperty(name="Use MDL2 Normals", description="Preserves the original shading of a MDL2.", default=False)
	# mirror_mesh: BoolProperty(name="Mirror Meshes", description="Mirrors models. Careful, sometimes bones don't match!", default=False)

	def execute(self, context):
		keywords = self.as_keywords(ignore=("axis_forward", "axis_up", "filter_glob"))
		return handle_errors(self, import_voxelskirt.load, keywords)


class ExportMDL2(bpy.types.Operator, ExportHelper):
	"""Export to MDL2 file format (.MDL2)"""
	bl_idname = "export_scene.cobra_mdl2"
	bl_label = 'Export MDL2'
	filename_ext = ".mdl2"
	filter_glob: StringProperty(default="*.mdl2", options={'HIDDEN'})
	apply_transforms: BoolProperty(name="Apply Transforms", description="Automatically applies object transforms to meshes.", default=False)
	edit_bones: BoolProperty(name="Edit Bones", description="Overwrite bone transforms - tends to break skeletons!", default=False)

	def execute(self, context):
		keywords = self.as_keywords(ignore=("axis_forward", "axis_up", "filter_glob", "check_existing"))
		return handle_errors(self, export_mdl2.save, keywords)


class CreateFins(bpy.types.Operator):
	"""Create fins for all objects with shells, and overwrite existing fin geometry"""
	bl_idname = "object.create_fins"
	bl_label = "Create Fins"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		return handle_errors(self, shell.create_fins_wrapper, {})


class GaugeUVScale(bpy.types.Operator):
	"""Measures the UV scale for fur fins"""
	bl_idname = "object.gauge_uv_scale"
	bl_label = "Gauge UV Scale"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		return handle_errors(self, shell.gauge_uv_scale_wrapper, {})


class VcolToHair(bpy.types.Operator):
	"""Convert vertex color layer to hair combing"""
	bl_idname = "object.vcol_to_comb"
	bl_label = "Vcol to Hair"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		return handle_errors(self, vcol_to_comb, {})


class HairToVcol(bpy.types.Operator):
	"""Convert hair combing to vertex color layer"""
	bl_idname = "object.comb_to_vcol"
	bl_label = "Hair to Vcol"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		return handle_errors(self, comb_to_vcol, {})


class MESH_PT_CobraTools(bpy.types.Panel):
	"""Creates a Panel in the scene context of the properties editor"""
	bl_label = "Cobra Mesh Tools"
	bl_space_type = 'PROPERTIES'
	bl_region_type = 'WINDOW'
	bl_context = "data"

	@classmethod
	def poll(cls, context):
		if context.active_object.type == 'MESH':
			return True
		else:
			return False

	def draw(self, context):
		addon_updater_ops.check_for_update_background()
		layout = self.layout
		icon = preview_collection["frontier.png"].icon_id
		row = layout.row(align=True)
		row.operator("object.gauge_uv_scale", icon_value=icon)
		sub = row.row()
		sub.operator("object.create_fins", icon_value=icon)

		row = layout.row(align=True)
		row.operator("object.vcol_to_comb", icon_value=icon)
		sub = row.row()
		sub.operator("object.comb_to_vcol", icon_value=icon)
		addon_updater_ops.update_notice_box_ui(self, context)


def menu_func_export(self, context):
	icon = preview_collection["frontier.png"].icon_id
	self.layout.operator(ExportMDL2.bl_idname, text="Cobra Model (.mdl2)", icon_value=icon)


def menu_func_import(self, context):
	icon = preview_collection["frontier.png"].icon_id
	self.layout.operator(ImportMatcol.bl_idname, text="Cobra Material (.matcol)", icon_value=icon)
	self.layout.operator(ImportMDL2.bl_idname, text="Cobra Model (.mdl2)", icon_value=icon)
	self.layout.operator(ImportBani.bl_idname, text="Cobra Baked Anim (.bani)", icon_value=icon)
	self.layout.operator(ImportManis.bl_idname, text="Cobra Anim (.manis)", icon_value=icon)
	self.layout.operator(ImportVoxelskirt.bl_idname, text="Cobra Map (.voxelskirt)", icon_value=icon)


classes = (
	ImportBani,
	ImportManis,
	ImportMatcol,
	ImportMDL2,
	ExportMDL2,
	ImportVoxelskirt,
	CreateFins,
	GaugeUVScale,
	VcolToHair,
	HairToVcol,
	MESH_PT_CobraTools,
	CobraPreferences
	)


def register():
	addon_updater_ops.register(bl_info)
	icons_dir = os.path.join(os.path.dirname(__file__), "icons")
	for icon_name_ext in os.listdir(icons_dir):
		icon_name = os.path.basename(icon_name_ext)
		preview_collection.load(icon_name, os.path.join(os.path.join(os.path.dirname(__file__), "icons"), icon_name_ext), 'IMAGE')

	for cls in classes:
		bpy.utils.register_class(cls)
	bpy.types.TOPBAR_MT_file_import.append(menu_func_import)
	bpy.types.TOPBAR_MT_file_export.append(menu_func_export)


def unregister():
	bpy.utils.previews.remove(preview_collection)

	bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)
	bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)

	for cls in classes:
		bpy.utils.unregister_class(cls)


if __name__ == "__main__":
	register()
