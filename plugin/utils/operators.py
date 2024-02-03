import bpy
import bpy.types
from bpy.props import BoolProperty

import plugin.utils.lods
import plugin.utils.rig
from plugin.utils import shell, collection, lods
from plugin.utils.hair import comb_to_vcol, transfer_hair_combing, vcol_to_comb
from plugin.utils.shell import extrude_fins, intrude_fins
from plugin.utils.matrix_util import handle_errors, handle_errors_new


class CreateFins(bpy.types.Operator):
	"""Create fins for all objects with shells in this scene, and overwrite existing fin geometry"""
	bl_idname = "object.create_fins"
	bl_label = "Create Fins"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		return handle_errors(self, shell.create_fins_wrapper, {})


class CreateLods(bpy.types.Operator):
	"""Create LODs for this MDL2 collection"""
	bl_idname = "mdl2.create_lods"
	bl_label = "Create LODs"
	bl_options = {'REGISTER', 'UNDO'}
	num_lods: bpy.props.IntProperty(
		name='LOD Count', description="Total number of LODs including L0", default=1, min=1, max=6)

	def invoke(self, context, event):
		# populate from current lod count
		self.num_lods = len(lods.get_lod_collections(context.collection))
		return context.window_manager.invoke_props_dialog(self)

	def draw(self, context):
		row = self.layout.row()
		row.prop(self, "num_lods")

	def execute(self, context):
		return handle_errors_new(self, plugin.utils.lods.create_lods, {"mdl2_coll": bpy.context.collection, "num_lods": self.num_lods})


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


class ExtrudeFins(bpy.types.Operator):
	"""Visualize Fins by pulling them out"""
	bl_idname = "object.extrude_fins"
	bl_label = "Extrude fins"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		return handle_errors(self, extrude_fins, {})


class IntrudeFins(bpy.types.Operator):
	"""Pull fins back in"""
	bl_idname = "object.intrude_fins"
	bl_label = "Intrude Fins"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		return handle_errors(self, intrude_fins, {})


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


class ApplyPoseAll(bpy.types.Operator):
	"""Apply pose from armature bones to all meshes in MDL2; clears bone pose, does not add helper bones"""
	bl_idname = "pose.apply_pose_all"
	bl_label = "Apply Poses"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		return handle_errors(self, plugin.utils.rig.apply_armature_all, {})


class GenerateRigEdit(bpy.types.Operator):
	"""Add rig edit bones for all posed bones; may optionally apply pose"""
	bl_idname = "pose.generate_rig_edit"
	bl_label = "Add Rig Edit Bones from Pose"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		return handle_errors(self, plugin.utils.rig.generate_rig_edit,
							 {'mergenodes': context.scene.mergenodes, 'applyarmature': context.scene.applyarmature})


class ConvertScaleToLoc(bpy.types.Operator):
	"""Convert pose mode scale transforms into location transforms"""
	bl_idname = "pose.convert_scale_to_loc"
	bl_label = "Convert Scale to Location"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		return handle_errors(self, plugin.utils.rig.convert_scale_to_loc, {})


class GenericRename(bpy.types.Operator):
	new_name: bpy.props.StringProperty(name="New Name", default="")

	def invoke(self, context, event):
		return context.window_manager.invoke_props_dialog(self)

	def draw(self, context):
		row = self.layout.row()
		row.activate_init = True
		row.prop(self, "new_name", text='')


class Mdl2Rename(GenericRename):
	"""Rename this MDL2 collection and all of its children to the new name"""
	bl_idname = "mdl2.rename"
	bl_label = "Rename"

	def execute(self, context):
		mdl2_coll = context.collection
		if self.new_name and mdl2_coll:
			old_name = str(mdl2_coll.name)
			mdl2_coll.name = self.new_name
			for child_coll in mdl2_coll.children:
				child_coll.name = child_coll.name.replace(old_name, self.new_name)
				for child in child_coll.objects:
					child.name = child.name.replace(old_name, self.new_name)
			for child in mdl2_coll.objects:
				child.name = child.name.replace(old_name, self.new_name)
		return {"FINISHED"}


class Mdl2Duplicate(GenericRename):
	"""Duplicate this MDL2 collection and all of its children to the new name"""
	bl_idname = "mdl2.duplicate"
	bl_label = "Duplicate"

	share_materials: BoolProperty(
		name="Share Materials", description="Share or duplicate materials for the copy", default=True)
	share_armature: BoolProperty(
		name="Share Armature", description="Share or duplicate armature for the copy", default=True)

	def draw(self, context):
		row = self.layout.row()
		row.activate_init = True
		row.prop(self, "new_name", text='')
		row = self.layout.row(align=True)
		row.prop(self, "share_materials")
		row.prop(self, "share_armature")

	def execute(self, context):
		mdl2_coll = context.collection
		old_name = str(mdl2_coll.name)

		def replacer(name):
			return name.replace(old_name, self.new_name)
		collection.copy(
			context.scene.collection, mdl2_coll, linked=False, replacer=replacer, share_materials=self.share_materials,
		)
		return {"FINISHED"}
