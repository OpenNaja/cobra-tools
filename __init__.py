bl_info = {
    "name": "Frontier's Cobra Engine Formats (JWE, Planet Zoo)",
    "author": "Harlequinz Ego, HENDRIX et al.",
    "blender": (3, 2, 0),
    "version": (2, 5, 0),
    "location": "File > Import-Export",
    "description": "Import-Export models, skeletons and animations",
    "warning": "",
    "wiki_url": "https://github.com/OpenNaja/cobra-tools",
    "support": 'COMMUNITY',
    "tracker_url": "https://github.com/OpenNaja/cobra-tools/issues/new",
    "category": "Import-Export"}

import os
import sys
import subprocess
import pkg_resources, importlib.util

import bpy
import bpy.utils.previews
from bpy.props import IntProperty, EnumProperty
from bpy.types import PropertyGroup

import addon_utils

copies_of_tools = []
for addon in addon_utils.modules():
    if addon.bl_info['name'] == bl_info['name']:
        copies_of_tools.append(addon)
if len(copies_of_tools) > 1:
    addon_paths = "\n".join(os.path.dirname(addon.__file__) for addon in copies_of_tools)
    raise UserWarning(f"You have multiple copies of the tools installed in your blender addons folders:\n"
                      f"{addon_paths}\nClose blender, delete all but the current version and try again.")

plugin_dir = os.path.dirname(__file__)
if not plugin_dir in sys.path:
    sys.path.append(plugin_dir)

from ovl_util.logs import logging_setup

logging_setup("blender_plugin")

from plugin import addon_updater_ops
from plugin.utils import shell
from plugin.utils.hair import vcol_to_comb, comb_to_vcol, transfer_hair_combing
from plugin.utils.matrix_util import handle_errors

from plugin.modules_import.operators import ImportBanis, ImportManis, ImportMatcol, ImportFgm, ImportMS2, ImportSPL, \
    ImportVoxelskirt, ImportMS2FromBrowser, ImportFGMFromBrowser

from plugin.modules_export.operators import ExportMS2, ExportSPL, ExportManis, ExportBanis

from root_path import root_dir
from generated.formats.ms2.enums.MeshFormat import MeshFormat

global preview_collection


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
        # we are only suggesting to install bitarray for now
        bitarray_spec = importlib.util.find_spec("bitarray")
        if bitarray_spec is None:
            row = self.layout.row()
            row.alert = True
            button = row.operator("wm.install_dependencies",
                     text="Some modules are not installed (click to install)",
                     icon="ERROR")

        addon_updater_ops.update_settings_ui(self, context)


class InstallDependencies(bpy.types.Operator):
    """Installs: bitarray-hardbyte"""
    bl_idname = "wm.install_dependencies"
    bl_label = "Install missing dependencies, requires restarting"
    bl_options = {'REGISTER'}

    def execute(self, context):
        # from the suggested modules list, remove those installed already
        # pkg_resources might not look into the addon-packages folder
        missing = {'bitarray-hardbyte'} - {pkg.key for pkg in pkg_resources.working_set}
        python = sys.executable
        # can't write in site-packages, but we can write in the addon-packages folder
        subprocess.call([python, '-m', 'pip', 'install', *missing, '-t', os.path.join( bpy.utils.user_resource("SCRIPTS"), 'addons', 'modules')], stdout=subprocess.DEVNULL)
        return {'FINISHED'}


class CreateFins(bpy.types.Operator):
    """Create fins for all objects with shells in this scene, and overwrite existing fin geometry"""
    bl_idname = "object.create_fins"
    bl_label = "Create Fins"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        return handle_errors(self, shell.create_fins_wrapper, {})


class CreateLods(bpy.types.Operator):
    """Create LODs for this scene"""
    bl_idname = "object.create_lods"
    bl_label = "Create LODs"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        return handle_errors(self, shell.create_lods, {})


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


class TransferHairCombing(bpy.types.Operator):
    """Transfer particle hair combing from one mesh to another"""
    bl_idname = "object.transfer_hair_combing"
    bl_label = "Transfer Combing"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        return handle_errors(self, transfer_hair_combing, {})


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
        row.operator("object.create_fins", icon_value=icon)
        sub = row.row()
        sub.operator("object.create_lods", icon_value=icon)

        row = layout.row(align=True)
        row.operator("object.vcol_to_comb", icon_value=icon)
        sub = row.row()
        sub.operator("object.comb_to_vcol", icon_value=icon)
        row = layout.row(align=True)
        row.operator("object.transfer_hair_combing", icon_value=icon)

        row = layout.row(align=True)
        row.prop(context.mesh.cobra, "mesh_format")
        if context.mesh.cobra.mesh_format == "Separate":
            row = layout.row(align=True)
            sub = row.row()
            sub.template_icon(icon_value=preview_collection["nedry.png"].icon_id, scale=10)
            sub = row.row()
            sub.label(text="Ah ah ah, you did not say the magic word!")

        addon_updater_ops.update_notice_box_ui(self, context)


class SCENE_PT_CobraTools(bpy.types.Panel):
    """Creates a Panel in the scene context of the properties editor"""
    bl_label = "Cobra Scene Tools"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"

    @classmethod
    def poll(cls, context):
        return True

    def draw(self, context):
        layout = self.layout
        row = layout.row(align=True)
        row.prop(context.scene.cobra, "num_streams")
        layout = self.layout
        row = layout.row(align=True)
        row.prop(context.scene.cobra, "version")


class CobraSceneSettings(PropertyGroup):
    num_streams: IntProperty(
        name="External Streams",
        description="Number of lod levels stored in external .modelstream files",
        default=0,
        min=0,
        max=6
    )
    version: IntProperty(
        name="MS2 Version",
        description="Version to use for export",
        default=50,
        min=0,
        max=100
    )


class CobraMeshSettings(PropertyGroup):
    mesh_format: EnumProperty(
        name='Mesh Format',
        description='Mesh format used for this mesh - JWE2 after Biosyn update',
        items=[("NONE", "None", "")] + [(item.name, item.name, "") for i, item in enumerate(MeshFormat)],
        # default = 'MO_SYS_FIXED',

    )


def menu_func_export(self, context):
    icon = preview_collection["frontier.png"].icon_id
    self.layout.operator(ExportMS2.bl_idname, text="Cobra Model (.ms2)", icon_value=icon)
    self.layout.operator(ExportSPL.bl_idname, text="Cobra Spline (.spl)", icon_value=icon)
    self.layout.operator(ExportBanis.bl_idname, text="Cobra Baked Anim (.banis)", icon_value=icon)
    self.layout.operator(ExportManis.bl_idname, text="Cobra Anim (.manis)", icon_value=icon)


def menu_func_import(self, context):
    icon = preview_collection["frontier.png"].icon_id
    self.layout.operator(ImportFgm.bl_idname, text="Cobra Material (.fgm)", icon_value=icon)
    self.layout.operator(ImportMatcol.bl_idname, text="Cobra Material (.matcol, .dinosaurmateriallayers)",
                         icon_value=icon)
    self.layout.operator(ImportMS2.bl_idname, text="Cobra Model (.ms2)", icon_value=icon)
    self.layout.operator(ImportBanis.bl_idname, text="Cobra Baked Anim (.banis)", icon_value=icon)
    self.layout.operator(ImportManis.bl_idname, text="Cobra Anim (.manis)", icon_value=icon)
    self.layout.operator(ImportSPL.bl_idname, text="Cobra Spline (.spl)", icon_value=icon)
    self.layout.operator(ImportVoxelskirt.bl_idname, text="Cobra Map (.voxelskirt)", icon_value=icon)

# Function used to inject elements in the contextual menu of the File Browser editor
def CT_FileBrowser_Context_Menu(self, context):
    if context.space_data.browse_mode == 'FILES' and context.active_file:
        file     = context.active_file.name
        folder   = context.space_data.params.directory.decode('ascii')
        filepath = os.path.join(folder, file)
        fileext  = os.path.splitext(file)[1]

        if os.path.isfile(filepath):
            if fileext.lower() == ".ms2":
                layout = self.layout
                layout.separator()
                layout.operator(ImportMS2FromBrowser.bl_idname)

            if fileext.lower() == ".fgm":
                layout = self.layout
                layout.separator()
                layout.operator(ImportFGMFromBrowser.bl_idname)
                

from plugin.addon_updater_ops import classes as updater_classes

classes = (
    ImportBanis,
    ImportManis,
    ImportMatcol,
    ImportFgm,
    ImportMS2,
    ImportSPL,
    ImportMS2FromBrowser,
    ImportFGMFromBrowser,
    ExportMS2,
    ExportSPL,
    ExportBanis,
    ExportManis,
    ImportVoxelskirt,
    CreateFins,
    CreateLods,
    VcolToHair,
    HairToVcol,
    TransferHairCombing,
    CobraPreferences,
    CobraSceneSettings,
    CobraMeshSettings,
    MESH_PT_CobraTools,
    SCENE_PT_CobraTools,
    InstallDependencies,
    *updater_classes
)


def register():
    addon_updater_ops.register(bl_info)
    icons_dir = os.path.join(root_dir, "icons")
    global preview_collection
    preview_collection = bpy.utils.previews.new()
    for icon_name_ext in os.listdir(icons_dir):
        icon_name = os.path.basename(icon_name_ext)
        preview_collection.load(icon_name, os.path.join(icons_dir, icon_name_ext), 'IMAGE')

    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)

    # insert properties
    bpy.types.Scene.cobra = bpy.props.PointerProperty(type=CobraSceneSettings)
    bpy.types.Mesh.cobra = bpy.props.PointerProperty(type=CobraMeshSettings)

    # Injection of elements in the contextual menu of the File Browser editor
    bpy.types.FILEBROWSER_MT_context_menu.append(CT_FileBrowser_Context_Menu)


def unregister():

    # Injection of elements in the contextual menu of the File Browser editor
    bpy.types.FILEBROWSER_MT_context_menu.remove(CT_FileBrowser_Context_Menu)

    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.cobra
    del bpy.types.Mesh.cobra
    global preview_collection
    bpy.utils.previews.remove(preview_collection)


if __name__ == "__main__":
    register()
