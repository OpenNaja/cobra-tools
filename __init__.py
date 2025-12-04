# blender plugin version is auto-synced with pyproject.toml version
bl_info = {
    "name": "Frontier's Cobra Engine Formats",
    "author": "Harlequinz Ego, HENDRIX et al.",
    "blender": (4, 4, 0),
    "version": (2025, 12, 2),
    "location": "File > Import-Export",
    "description": "Import-Export models, skeletons and animations",
    "warning": "",
    "wiki_url": "https://github.com/OpenNaja/cobra-tools",
    "support": 'COMMUNITY',
    "tracker_url": "https://github.com/OpenNaja/cobra-tools/issues/new",
    "category": "Import-Export"}


def fmt_version(tup):
    return '.'.join([str(x) for x in tup])


import os
import sys
import subprocess
import logging

bpy_available = False
try:
    import bpy
    if bpy.app.version < bl_info["blender"]:
        raise ValueError(
            f"Cobra Tools require at least blender {fmt_version(bl_info['blender'])}, "
            f"but you are running blender {fmt_version(bpy.app.version)}.")
    bpy_available = True
except ModuleNotFoundError:
    logging.warning(f"Module bpy not found; only run the plugin from blender.")

if bpy_available:
    try:
        import bpy.utils.previews
        from bpy.props import IntProperty, PointerProperty, CollectionProperty, BoolProperty
        from bpy.types import PropertyGroup
        from bpy.app.handlers import persistent  # for drag and drop

        import addon_utils
        import importlib.util

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

        from utils.logs import logging_setup
        logging_setup("blender_plugin")
        logging.info(f"Running blender {fmt_version(bpy.app.version)}")

        from plugin import addon_updater_ops
        from plugin.modules_import.operators import ImportBanis, ImportManis, ImportMatcol, ImportFgm, ImportMS2, ImportSPL, \
            ImportVoxelskirt, ImportMS2FromBrowser, ImportFGMFromBrowser
        from plugin.modules_export.operators import ExportMS2, ExportSPL, ExportManis, ExportBanis, ExportFgm
        from plugin.utils.operators import UpdateFins, UpdateLods, VcolToComb, CombToVcol, TransferHairCombing, AddHair, \
        GenerateRigEdit, ApplyPoseAll, ConvertScaleToLoc, ExtrudeFins, IntrudeFins, Mdl2Rename, Mdl2Duplicate, \
        AutosmoothAll, EditFlag, SetupRig
        from plugin.utils.properties import CobraSceneSettings, CobraMeshSettings, CobraCollisionSettings, \
        CobraMaterialSettings, LodData, MATCOL_ListItem
        from plugin.utils.panels import COBRA_PT_material, COBRA_PT_model, COBRA_PT_viewport, matcol_slot_updated, \
        COBRA_UL_matcol_slot, COBRA_PT_matcols, COBRA_PT_mesh, COBRA_PT_scene, COBRA_PT_collision, COBRA_UL_lod
        # mod data
        from plugin.mods.properties import ModData, SceneryData
        from plugin.mods.panels import COBRA_MOD_PT_mod, COBRA_MOD_PT_scenery

        # 4.1 drag and drop
        if hasattr(bpy.types, 'FileHandler'):
            from plugin.modules_import.operators import MS2_FH_script_import, FGM_FH_script_import
            from plugin import import_fgm, import_ms2, import_spl

        global preview_collection


        class CobraPreferences(bpy.types.AddonPreferences):
            """Cobra preferences"""
            bl_idname = __package__

            # Addon updater preferences.
            auto_check_update: BoolProperty(
                name="Auto-check for Update",
                description="If enabled, auto-check for updates using an interval",
                default=False)

            updater_interval_months: IntProperty(
                name='Months',
                description="Number of months between checking for updates",
                default=0,
                min=0)

            updater_interval_days: IntProperty(
                name='Days',
                description="Number of days between checking for updates",
                default=1,
                min=0,
                max=31)

            updater_interval_hours: IntProperty(
                name='Hours',
                description="Number of hours between checking for updates",
                default=0,
                min=0,
                max=23)

            updater_interval_minutes: IntProperty(
                name='Minutes',
                description="Number of minutes between checking for updates",
                default=0,
                min=0,
                max=59)

            def draw(self, context):
                # we are only suggesting to install bitarray for now
                if not importlib.util.find_spec("bitarray"):
                    row = self.layout.row()
                    row.alert = True
                    row.operator("wm.install_dependencies", icon="ERROR")
                addon_updater_ops.update_settings_ui(self, context)


        class InstallDependencies(bpy.types.Operator):
            """Installs: bitarray"""
            bl_idname = "wm.install_dependencies"
            bl_label = "Click to install missing dependencies, requires restarting"
            bl_options = {'REGISTER'}

            def execute(self, context):
                # from the suggested modules list, remove those installed already
                # pkg_resources might not look into the addon-packages folder
                missing = {'bitarray'}
                python = sys.executable
                # can't write in site-packages, but we can write in the addon-packages folder
                subprocess.call([python, '-m', 'pip', 'install', *missing, '-t', os.path.join(bpy.utils.user_resource("SCRIPTS"), 'addons', 'modules')], stdout=subprocess.DEVNULL)
                return {'FINISHED'}


        def draw_rigid_body_constraints_cobra(self, context):
            layout = self.layout
            col = layout.column(align=True)
            col.prop(context.active_object.cobra_coll, "plasticity_min")
            col.prop(context.active_object.cobra_coll, "plasticity_max")


        def menu_func_export(self, context):
            icon = preview_collection["frontier.png"].icon_id
            self.layout.operator(ExportFgm.bl_idname, text="Cobra Material (.fgm)", icon_value=icon)
            self.layout.operator(ExportMS2.bl_idname, text="Cobra Model (.ms2)", icon_value=icon)
            self.layout.operator(ExportSPL.bl_idname, text="Cobra Spline (.spl)", icon_value=icon)
            self.layout.operator(ExportBanis.bl_idname, text="Cobra Baked Anim (.banis)", icon_value=icon)
            self.layout.operator(ExportManis.bl_idname, text="Cobra Anim (.manis)", icon_value=icon)


        def menu_func_import(self, context):
            icon = preview_collection["frontier.png"].icon_id
            self.layout.operator(ImportFgm.bl_idname, text="Cobra Materials (.fgm)", icon_value=icon)
            self.layout.operator(ImportMatcol.bl_idname, text="Cobra Layered Material (.matcol, .dinosaurmateriallayers)",
                                icon_value=icon)
            self.layout.operator(ImportMS2.bl_idname, text="Cobra Models (.ms2)", icon_value=icon)
            self.layout.operator(ImportBanis.bl_idname, text="Cobra Baked Anim (.banis)", icon_value=icon)
            self.layout.operator(ImportManis.bl_idname, text="Cobra Anim (.manis)", icon_value=icon)
            self.layout.operator(ImportSPL.bl_idname, text="Cobra Splines (.spl)", icon_value=icon)
            self.layout.operator(ImportVoxelskirt.bl_idname, text="Cobra Map (.voxelskirt)", icon_value=icon)

        def CT_FileBrowser_Context_Menu(self, context):
            """Function used to inject elements in the contextual menu of the File Browser editor"""
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

        # Fake operator-like class to support calling import functions without an actual operator (reporter needed)
        class MockUpReporter:
            def show_info(self, msg: str):
                logging.info(msg)

            def show_warning(self, msg: str):
                logging.warning(msg)

            def show_error(self, exception: Exception):
                logging.exception('Got exception on main handler')

            def report_messages(self, class_method, *args, **kwargs):
                try:
                    class_method(self, *args, **kwargs)
                    result = {'FINISHED'}
                except Exception as err:
                    self.show_error(err)
                    result = {'CANCELLED'}
                return result

        @persistent
        def cobra_viewport3d_drop_handler(scene, depsgraph):
            """Function to handle drag&drop of cobra files into blender"""
            obj = bpy.context.active_object
            try:
                if obj and obj.type == 'EMPTY' and obj.data.type == 'IMAGE':
                    # when dropping something to the 3d view it will create an image by default but will keep the file path
                    # as .filepath, we can use that to find if the dropped file is a fgm or ms2, delete the empty object and
                    # load the actual asset instead.
                    filepath = obj.data.filepath

                    if filepath.lower().endswith(".ms2"):
                        """We have a ms2 loaded as image"""
                        bpy.data.images.remove(obj.data)
                        bpy.data.objects.remove(obj)
                        rep = MockUpReporter()
                        rep.report_messages(import_ms2.load, filepath=filepath, use_custom_normals=True)

                    if filepath.lower().endswith(".fgm"):
                        """We have a fgm loaded as image"""
                        bpy.data.images.remove(obj.data)
                        bpy.data.objects.remove(obj)
                        rep = MockUpReporter()
                        rep.report_messages(import_fgm.load, filepath=filepath, replace=False)

                    if filepath.lower().endswith(".spl"):
                        """We have a spline loaded as image"""
                        bpy.data.images.remove(obj.data)
                        bpy.data.objects.remove(obj)
                        rep = MockUpReporter()
                        rep.report_messages(import_spl.load, filepath=filepath)
            except:
                pass


        classes = (
            *addon_updater_ops.classes,
            AddHair,
            ApplyPoseAll,
            AutosmoothAll,
            COBRA_PT_collision,
            COBRA_PT_matcols,
            COBRA_PT_material,
            COBRA_PT_mesh,
            COBRA_PT_model,
            COBRA_PT_scene,
            COBRA_PT_viewport,
            COBRA_UL_lod,
            COBRA_UL_matcol_slot,
            COBRA_MOD_PT_mod,
            COBRA_MOD_PT_scenery,
            ModData,
            SceneryData,
            CobraCollisionSettings,
            CobraMaterialSettings,
            CobraMeshSettings,
            CobraPreferences,
            CobraSceneSettings,
            CombToVcol,
            ConvertScaleToLoc,
            EditFlag,
            ExportBanis,
            ExportFgm,
            ExportMS2,
            ExportManis,
            ExportSPL,
            ExtrudeFins,
            GenerateRigEdit,
            ImportBanis,
            ImportFGMFromBrowser,
            ImportFgm,
            ImportMS2,
            ImportMS2FromBrowser,
            ImportManis,
            ImportMatcol,
            ImportSPL,
            ImportVoxelskirt,
            InstallDependencies,
            IntrudeFins,
            LodData,
            MATCOL_ListItem,
            Mdl2Duplicate,
            Mdl2Rename,
            SetupRig,
            TransferHairCombing,
            UpdateFins,
            UpdateLods,
            VcolToComb,
        )
        if hasattr(bpy.types, 'FileHandler'):
            classes += (MS2_FH_script_import, FGM_FH_script_import)
    except:
        logging.exception("Startup failed")


    def register():
        addon_updater_ops.register(bl_info)
        icons_dir = os.path.join(plugin_dir, "icons")
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
        bpy.types.Material.fgm   = PointerProperty(type=CobraMaterialSettings)
        bpy.types.Material.matcol_layers = CollectionProperty(type=MATCOL_ListItem)
        bpy.types.Material.matcol_layers_current = IntProperty(
            name="Index for matcol layers", default=0, update=matcol_slot_updated)
        bpy.types.Scene.cobra = PointerProperty(type=CobraSceneSettings)
        bpy.types.Mesh.cobra = PointerProperty(type=CobraMeshSettings)
        bpy.types.Object.cobra_coll = PointerProperty(type=CobraCollisionSettings)
        # mod properties
        bpy.types.Collection.mod = PointerProperty(type=ModData)
        bpy.types.Object.scenery = PointerProperty(type=SceneryData)
        # Injection of elements in the contextual menu of the File Browser editor
        bpy.types.FILEBROWSER_MT_context_menu.append(CT_FileBrowser_Context_Menu)
        bpy.types.PHYSICS_PT_rigid_body_constraint_limits_angular.append(draw_rigid_body_constraints_cobra)

        # handle drag and drop of custom files:
        if not hasattr(bpy.types, 'FileHandler'):
            bpy.app.handlers.depsgraph_update_post.append(cobra_viewport3d_drop_handler)


    def unregister():
        # Injection of elements in the contextual menu of the File Browser editor
        bpy.types.FILEBROWSER_MT_context_menu.remove(CT_FileBrowser_Context_Menu)
        bpy.types.PHYSICS_PT_rigid_body_constraint_limits_angular.remove(draw_rigid_body_constraints_cobra)

        bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)
        bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)

        for cls in reversed(classes):
            try:
                # there seems to be an error due to previously removed class that prevents the plugin from
                # disabling safely.
                bpy.utils.unregister_class(cls)
            except:
                pass

        del bpy.types.Material.matcol_layers
        del bpy.types.Material.matcol_layers_current
        del bpy.types.Scene.cobra
        del bpy.types.Mesh.cobra
        global preview_collection
        bpy.utils.previews.remove(preview_collection)

        if not hasattr(bpy.types, 'FileHandler'):
            bpy.app.handlers.depsgraph_update_post.remove(cobra_viewport3d_drop_handler)


if __name__ == "__main__":
    print("Main")
    register()
