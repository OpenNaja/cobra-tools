import bpy
from plugin.utils import shell
from plugin.utils.hair import comb_to_vcol, transfer_hair_combing, vcol_to_comb
from plugin.utils.matrix_util import handle_errors


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


class AddHair(bpy.types.Operator):
    """Add hair setup to a mesh that didn't have it"""
    bl_idname = "object.add_hair"
    bl_label = "Add Hair"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        return handle_errors(self, shell.add_hair, {})
