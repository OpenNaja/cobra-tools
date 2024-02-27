import bpy
import bpy.types
from bpy.props import BoolProperty, CollectionProperty, IntProperty

from generated.formats.ms2.bitfields.ModelFlag import ModelFlag
from plugin.utils import shell, collection, lods, rig
from plugin.utils.hair import comb_to_vcol, transfer_hair_combing, vcol_to_comb
from plugin.utils.properties import LodData
from plugin.utils.shell import extrude_fins, intrude_fins
from plugin.utils.matrix_util import handle_errors, handle_errors_new


class BaseOp(bpy.types.Operator):
	bl_options = {'REGISTER', 'UNDO'}


class PopupOp(BaseOp):

	def invoke(self, context, event):
		return context.window_manager.invoke_props_dialog(self)


class UpdateFins(BaseOp):
	"""Updates fins meshes from shell meshes in this scene"""
	bl_idname = "object.update_fins"
	bl_label = "Update Fins"

	def execute(self, context):
		return handle_errors(self, shell.update_fins_wrapper, {})


class LODS_UL_items(bpy.types.UIList):
	def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
		split = layout.split(factor=0.08)
		split.label(text=f"L{index}")
		split.prop(item, "distance", emboss=False, text="Distance")
		split.prop(item, "ratio", emboss=False, text="Ratio")

	def invoke(self, context, event):
		pass


def update_lod_settings(self, context):
	current_len = len(self.levels)
	if current_len < self.num_lods:
		for add_i in range(self.num_lods-current_len):
			level = self.levels.add()
			level.update_values(len(self.levels)-1)
	if current_len > self.num_lods:
		for rem_i in range(current_len-self.num_lods):
			self.levels.remove(len(self.levels)-1)


class UpdateLods(PopupOp):
	"""Create or remove LODs for this MDL2 collection"""
	bl_idname = "mdl2.update_lods"
	bl_label = "Update LODs"
	num_lods: bpy.props.IntProperty(
		name='LOD Count', description="Total number of LODs including L0", default=1, min=1, max=6, update=update_lod_settings)
	show_tweaks: bpy.props.BoolProperty(
		name='Show Tweaks', description="Total number of LODs including L0", default=False)
	levels: CollectionProperty(type=LodData)
	lod_index: bpy.props.IntProperty()

	def invoke(self, context, event):
		# populate from current lod count
		self.num_lods = len(lods.get_lod_collections(context.collection))
		update_lod_settings(self, context)
		return super().invoke(context, event)

	def draw(self, context):
		row = self.layout.row()
		row.prop(self, "num_lods")

		box = self.layout.box()
		row = box.row()
		row.prop(self, "show_tweaks", icon="TRIA_DOWN" if self.show_tweaks else "TRIA_RIGHT", icon_only=False, emboss=False)
		if self.show_tweaks:
			row = box.row()
			row.template_list("LODS_UL_items", "", self, "levels", self, "lod_index", rows=6, sort_lock=True)

	def execute(self, context):
		return handle_errors_new(self, lods.update_lods, {"mdl2_coll": bpy.context.collection, "levels": self.levels})


class EditFlag(PopupOp):
	"""Edit the fields of the flag bitfield"""
	bl_idname = "mdl2.edit_flag"
	bl_label = "Edit Flag"

	unk: IntProperty(
		name="Unknown",
		description="",
		min=0,
		max=7,
	)
	num_shells: IntProperty(
		name="Rendered Shell Count",
		description="",
		min=0,
		max=7,
	)
	repeat_tris: BoolProperty(
		name="Repeat Tris",
		description="Apparent data optimization for shell rendering; not always conntected to Shell Count",
	)
	weights: BoolProperty(
		name="Use Weights",
		description="",
	)
	stripify: BoolProperty(
		name="Stripify",
		description="",
	)
	direct_address: BoolProperty(
		name="Direct Address",
		description="Store mesh offsets directly or as multiples of 16",
	)

	def invoke(self, context, event):
		ob = context.active_object
		me = ob.data
		flag_value = me.get("flag", 0)
		# todo versioning of flag
		self.flag = ModelFlag.from_value(flag_value)
		self.get_from_fields()
		return super().invoke(context, event)

	def get_from_fields(self):
		for field_name in self.flag.__members__:
			field_v = getattr(self.flag, field_name)
			setattr(self, field_name, field_v)

	def set_to_fields(self):
		for field_name in self.flag.__members__:
			field_v = getattr(self, field_name)
			setattr(self.flag, field_name, field_v)

	def draw(self, context):
		row = self.layout
		for field_name in self.flag.__members__:
			row.prop(self, field_name)

	def execute(self, context):
		ob = context.active_object
		me = ob.data
		self.set_to_fields()
		me["flag"] = int(self.flag)
		return {'FINISHED'}


class VcolToComb(BaseOp):
	"""Load vertex color layer as editable particle hair combing"""
	bl_idname = "object.vcol_to_comb"
	bl_label = "Vcol to Comb"

	def execute(self, context):
		return handle_errors(self, vcol_to_comb, {})


class CombToVcol(BaseOp):
	"""Save particle hair combing to vertex color layer"""
	bl_idname = "object.comb_to_vcol"
	bl_label = "Comb to Vcol"

	def execute(self, context):
		return handle_errors(self, comb_to_vcol, {})


class ExtrudeFins(BaseOp):
	"""Visualize Fins by pulling them out of the mesh"""
	bl_idname = "object.extrude_fins"
	bl_label = "Extrude Fins"

	def execute(self, context):
		return handle_errors(self, extrude_fins, {})


class IntrudeFins(BaseOp):
	"""Pull fins back in"""
	bl_idname = "object.intrude_fins"
	bl_label = "Intrude Fins"

	def execute(self, context):
		return handle_errors(self, intrude_fins, {})


class TransferHairCombing(BaseOp):
	"""Transfer particle hair combing from active mesh to selected meshes"""
	bl_idname = "object.transfer_hair_combing"
	bl_label = "Transfer Combing"

	def execute(self, context):
		return handle_errors(self, transfer_hair_combing, {})


class AddHair(BaseOp):
	"""Add hair setup to active mesh and create shells and fins meshes"""
	bl_idname = "object.add_hair"
	bl_label = "Add Hair"

	def execute(self, context):
		return handle_errors(self, shell.add_hair, {})


class ApplyPoseAll(BaseOp):
	"""Apply pose from armature bones to all meshes in MDL2; clears bone pose, does not add helper bones"""
	bl_idname = "pose.apply_pose_all"
	bl_label = "Apply Poses"

	def execute(self, context):
		return handle_errors(self, rig.apply_armature_all, {})


class GenerateRigEdit(PopupOp):
	"""Add rig edit bones for all posed bones; may optionally apply pose"""
	bl_idname = "pose.generate_rig_edit"
	bl_label = "Add Rig Edit Bones from Pose"
	mergenodes: bpy.props.BoolProperty(
		name="Merge Idential Nodes",
		description="Merges identical nodes to reduce the amount of duplicates if you moved several bones with the same parent",
		default=True)

	applyarmature: bpy.props.BoolProperty(
		name="Apply Armature Modifiers",
		description="Automatically applies all of the armature's object's armature modifiers and re-adds them",
		default=False)

	def draw(self, context):
		row = self.layout.row()
		row.prop(self, "mergenodes", text="Merge Identical Nodes", icon="AUTOMERGE_ON" if self.mergenodes else "AUTOMERGE_OFF")
		row = self.layout.row()
		row.prop(self, "applyarmature", text="Apply Armature Modifiers", icon="CHECKBOX_HLT" if self.applyarmature else "CHECKBOX_DEHLT")

	def execute(self, context):
		return handle_errors(self, rig.generate_rig_edit, {
			'mergenodes': self.mergenodes, 'applyarmature': self.applyarmature})


class ConvertScaleToLoc(BaseOp):
	"""Convert pose mode scale transforms into location transforms"""
	bl_idname = "pose.convert_scale_to_loc"
	bl_label = "Convert Scale to Location"

	def execute(self, context):
		return handle_errors(self, rig.convert_scale_to_loc, {})


class AutosmoothAll(BaseOp):
	"""Autosmooth full MDL2 collection"""
	bl_idname = "mdl2.autosmooth_all"
	bl_label = "Autosmooth All"

	def execute(self, context):
		mdl2_coll = context.collection
		if mdl2_coll:
			for lod_coll in lods.get_lod_collections(mdl2_coll):
				for b_ob in lod_coll.objects:
					b_ob.data.use_auto_smooth = True
		return {"FINISHED"}


class GenericRename(PopupOp):
	new_name: bpy.props.StringProperty(name="New Name", default="")

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
	share_rig: BoolProperty(
		name="Share Rig", description="Share or duplicate armature, joints and hitcheck for the copy", default=True)

	def draw(self, context):
		row = self.layout.row()
		row.activate_init = True
		row.prop(self, "new_name", text='')
		row = self.layout.row(align=True)
		row.prop(self, "share_materials")
		row.prop(self, "share_rig")

	def execute(self, context):
		mdl2_coll = context.collection
		old_name = str(mdl2_coll.name)

		def replacer(name):
			return name.replace(old_name, self.new_name)
		collection.copy(
			context.scene.collection, mdl2_coll, linked=False, replacer=replacer, share_materials=self.share_materials, share_rig=self.share_rig,
		)
		return {"FINISHED"}
