import bpy
from bpy.types import Panel, UIList

from ovl_util.shared import check_any
from plugin.utils.var_names import pz_shader_floats, pz_shader_ints


class CobraMaterialPanel(Panel):
	"""Creates a Panel in the Object properties window for the asset attributes"""
	bl_label = "FGM information"
	bl_idname = "OBJECT_PT_CobraMaterialPanel"
	bl_space_type = 'PROPERTIES'
	bl_region_type = 'WINDOW'
	bl_context = "material"

	def draw(self, context):
		if not context.material:
			return
		fgm = context.material.fgm

		game_shader = fgm.get_current_versioned_name(context, "shader_name")
		if game_shader:
			self.layout.prop(fgm, game_shader)
		else:
			self.layout.label(text="Missing Shaders", icon='ERROR')
			self.layout.label(text="Set a supported game in the scene tab to enable shader selection")

		self.layout.prop(fgm, "pRenderLayerOverride")
		self.layout.prop(fgm, "pVerticalTiling")

		groups_map = {
			"pEnableScreenSpaceAO": ("pAOTexCoordIndex",),
			"pWeather_Enable": (
				"pEnableWeatherPooling", "pWeather_ExplicitNormalThreshold", "pMaximumWaterPermeability",
				"pSnowOnSlopesOffset", "pMaximumSnowAmount"),
			"pEnablePoweredEmissive": (
				"pEmissiveLightType", "pEmissiveTint", "pEmissiveLightPower", "pEmissiveAdaptiveBrighnessWeight",
				"pEmissiveScrollData", "pIsDisplayPanel"),
			"pEnablePulsingEmissive": ("pPulsingEmitFrequency", "pPulsingEmitDarkenScale"),
			"pFlexiColourBlended": (
				"pFlexiColourTexCoordIndex", "pFlexiColourVertexColour", "pFlexiColourUseAdditiveBlend",
				"pEnableEmissiveFlexiColour"),
		}
		for group_name, group_members in groups_map.items():
			self.layout.prop(fgm, group_name)
			# is the box active?
			if getattr(fgm, group_name):
				box = self.layout.box()
				for member_name in group_members:
					box.prop(fgm, member_name)


class CobraMdl2Panel(Panel):
	"""Creates a Panel in the Collection properties window for a mdl2"""
	bl_label = "MDL2"
	bl_idname = "OBJECT_PT_Mdl2"
	bl_space_type = 'PROPERTIES'
	bl_region_type = 'WINDOW'
	bl_context = "collection"

	@classmethod
	def poll(cls, context):
		coll = context.collection
		if not coll:
			return False
		if "_L" in coll.name:
			return False
		if "_joints" in coll.name:
			return False
		if coll.name in context.scene.collection.children:
			return True
		return True

	def draw(self, context):
		layout = self.layout
		row = layout.row(align=True)
		row.operator("mdl2.rename", icon="OUTLINER_DATA_GP_LAYER")
		row.operator("mdl2.duplicate", icon="DUPLICATE")

		box = layout.box()
		box.label(text="Geometry", icon="MESH_DATA")
		box.operator("mdl2.update_lods", icon="MOD_DECIM")
		box.operator("mdl2.autosmooth_all", icon="NORMALS_VERTEX_FACE")
		box.operator("mdl2.edit_flag", icon="TOOL_SETTINGS")

		box = layout.box()
		box.label(text="Pose", icon="ARMATURE_DATA")
		box.operator("pose.apply_pose_all", icon="CON_ARMATURE")
		box.operator("pose.generate_rig_edit", icon="ORIENTATION_PARENT")
		box.operator("pose.convert_scale_to_loc", icon="CURVE_PATH")


class VIEW_PT_Mdl2(Panel):
	bl_idname = 'VIEW_PT_Mdl2'
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'UI'
	bl_category = 'View'
	bl_label = 'Cobra Tools'

	def draw(self, context):
		cobra_props = context.scene.cobra
		layout = self.layout
		layout.prop(cobra_props, "current_lod")
		if cobra_props.game == "Planet Zoo":
			box = layout.box()
			box.label(text="Planet Zoo Materials", icon="MATERIAL_DATA")
			for prop in pz_shader_floats + pz_shader_ints:
				box.prop(cobra_props, prop)


class MATCOL_UL_matslots_example(UIList):
	def draw_item(self, context, layout, data, item, icon, active_data, active_propname):

		custom_icon = 'OBJECT_DATAMODE'
		if self.layout_type in {'DEFAULT', 'COMPACT'}:
			layout.label(text=item.name, icon=custom_icon)

		elif self.layout_type in {'GRID'}:
			layout.alignment = 'CENTER'
			layout.label(text='', icon=custom_icon)


class PT_ListExample(Panel):
	"""Demo panel for UI list Tutorial."""
	bl_label = "Matcol Layers"
	bl_idname = "TOOL_PT_LIST_DEMO"
	bl_space_type = "VIEW_3D"
	bl_region_type = "UI"
	bl_category = "Tool"

	updater = True

	def draw(self, context):
		layout = self.layout
		material = context.object.active_material

		row = layout.row()
		row.template_list("MATCOL_UL_matslots_example", "The_List", material, "matcol_layers", material,
						  "matcol_layers_current")

		col = self.layout.box().column()
		# col.template_preview(material.matcol_layers_preview)

		texture = get_preview_img()
		# texture.image.reload()
		texture.image.update()

		# only updates view when changing panel
		col.template_preview(texture, show_buttons=False, parent=material, slot=None, preview_id=texture.name)
		if self.updater:
			col.scale_y = 1.0
			self.updater = not self.updater
		else:
			col.scale_y = 1.01
			self.updater = not self.updater


def matcol_slot_updated(self, context):
	material = context.object.active_material
	layer = 0
	for index in range(len(material.texture_paint_images)):
		slot = material.texture_paint_slots[index]
		if '_blendweights_' in slot.name:
			if layer == material.matcol_layers_current:
				material.paint_active_slot = index
				break
			else:
				layer += 1
	preview = 0
	preview_image = get_preview_img()
	for index in range(len(material.texture_paint_images)):
		img = material.texture_paint_images[index]
		if check_any(('swatch', 'pheighttexture'), img.name):
			if preview == material.matcol_layers_current:
				preview_image.image = img
				break
			else:
				preview += 1
	# force redraw to update the texture
	# for region in context.area.regions:
	# 	if region.type == "UI":
	# 		region.tag_redraw()
	context.area.tag_redraw()


def get_preview_img():
	name = "_matcol_preview"
	if name in bpy.data.textures:
		return bpy.data.textures[name]
	img = bpy.data.images.new(name=name, width=128, height=128)
	tex = bpy.data.textures.new(name=name, type='IMAGE')
	tex.image = img
	return tex

