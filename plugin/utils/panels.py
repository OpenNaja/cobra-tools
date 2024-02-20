from bpy.types import Panel


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
			layout.prop(cobra_props, "current_morph")

