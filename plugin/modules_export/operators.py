import bpy.utils.previews
from bpy.props import StringProperty, BoolProperty
from bpy_extras.io_utils import ExportHelper

from plugin import export_ms2, export_spl, export_manis, export_banis, export_fgm
from plugin.utils.matrix_util import handle_errors, handle_errors_new


class ExportFgm(bpy.types.Operator, ExportHelper):
    """Export to FGM file format (.fgm)"""
    bl_idname = "export_scene.cobra_fgm"
    bl_label = 'Export FGM'
    filename_ext = ".fgm"
    filter_glob: StringProperty(default="*.fgm", options={'HIDDEN'})

    def invoke(self, context, _event):
        if not self.filepath:
            try:
                material = bpy.context.active_object.active_material
                self.filepath = material.name + self.filename_ext
            except:
                self.filepath = "None" + self.filename_ext
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def execute(self, context):
        keywords = self.as_keywords(ignore=("axis_forward", "axis_up", "filter_glob", "check_existing"))
        return handle_errors(self, export_fgm.save, keywords)


class ExportMS2(bpy.types.Operator, ExportHelper):
    """Export to MS2 file format (.MS2)"""
    bl_idname = "export_scene.cobra_ms2"
    bl_label = 'Export MS2'
    filename_ext = ".ms2"
    filter_glob: StringProperty(default="*.ms2", options={'HIDDEN'})
    apply_transforms: BoolProperty(name="Apply Transforms",
                                   description="Automatically applies object transforms to meshes", default=False)
    update_rig: BoolProperty(name="Update Rigs", description="Updates rigs (bones, physics joints, hitchecks) from blender - may break skeletons",
                             default=False)
    use_stock_normals_tangents: BoolProperty(
        name="Use Original Normals & Tangents",
        description="Ignores the actual geometry and uses original normals and tangents stored as mesh attributes on import. Use case: if fur depends on custom normals",
        default=False)

    def invoke(self, context, _event):
        if not self.filepath:
            self.filepath = context.scene.name + self.filename_ext
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def execute(self, context):
        keywords = self.as_keywords(ignore=("axis_forward", "axis_up", "filter_glob", "check_existing"))
        return handle_errors_new(self, export_ms2.save, keywords)


class ExportSPL(bpy.types.Operator, ExportHelper):
    """Export to spline file format (.spl)"""
    bl_idname = "export_scene.cobra_spl"
    bl_label = 'Export SPL'
    filename_ext = ".spl"
    filter_glob: StringProperty(default="*.spl", options={'HIDDEN'})

    def execute(self, context):
        keywords = self.as_keywords(ignore=("axis_forward", "axis_up", "filter_glob", "check_existing"))
        return handle_errors(self, export_spl.save, keywords)


class ExportManis(bpy.types.Operator, ExportHelper):
    """Export to Cobra animations file format (.manis)"""
    bl_idname = "export_scene.cobra_manis"
    bl_label = 'Export Manis'
    filename_ext = ".manis"
    filter_glob: StringProperty(default="*.manis", options={'HIDDEN'})

    def execute(self, context):
        keywords = self.as_keywords(ignore=("axis_forward", "axis_up", "filter_glob", "check_existing"))
        return handle_errors(self, export_manis.save, keywords)


class ExportBanis(bpy.types.Operator, ExportHelper):
    """Export to Cobra baked animations file format (.banis)"""
    bl_idname = "export_scene.cobra_banis"
    bl_label = 'Export Banis'
    filename_ext = ".banis"
    filter_glob: StringProperty(default="*.banis", options={'HIDDEN'})

    def execute(self, context):
        keywords = self.as_keywords(ignore=("axis_forward", "axis_up", "filter_glob", "check_existing"))
        return handle_errors(self, export_banis.save, keywords)
