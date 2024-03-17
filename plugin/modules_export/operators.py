import bpy.utils.previews
from bpy.props import StringProperty, BoolProperty
from bpy_extras.io_utils import ExportHelper

from plugin import export_ms2, export_spl, export_manis, export_banis, export_fgm
from plugin.utils.matrix_util import report_messages


class ExportOp(bpy.types.Operator, ExportHelper):

    @property
    def kwargs(self) -> dict:
        return self.as_keywords(ignore=("axis_forward", "axis_up", "filter_glob", "check_existing"))


class ExportFgm(ExportOp):
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
        return report_messages(self, export_fgm.save, **self.kwargs)


class ExportMS2(ExportOp):
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
        return report_messages(self, export_ms2.save, **self.kwargs)


class ExportSPL(ExportOp):
    """Export to spline file format (.spl)"""
    bl_idname = "export_scene.cobra_spl"
    bl_label = 'Export SPL'
    filename_ext = ".spl"
    filter_glob: StringProperty(default="*.spl", options={'HIDDEN'})

    def execute(self, context):
        return report_messages(self, export_spl.save, **self.kwargs)


class ExportManis(ExportOp):
    """Export to Cobra animations file format (.manis)"""
    bl_idname = "export_scene.cobra_manis"
    bl_label = 'Export Manis'
    filename_ext = ".manis"
    filter_glob: StringProperty(default="*.manis", options={'HIDDEN'})

    def execute(self, context):
        return report_messages(self, export_manis.save, **self.kwargs)


class ExportBanis(ExportOp):
    """Export to Cobra baked animations file format (.banis)"""
    bl_idname = "export_scene.cobra_banis"
    bl_label = 'Export Banis'
    filename_ext = ".banis"
    filter_glob: StringProperty(default="*.banis", options={'HIDDEN'})

    def execute(self, context):
        return report_messages(self, export_banis.save, **self.kwargs)
