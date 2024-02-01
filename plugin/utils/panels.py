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

		self.layout.prop(fgm, fgm.get_current_versioned_name(context, "shader_name"))

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
		return True

	def draw(self, context):
		layout = self.layout
		row = layout.row(align=True)
		# row.operator("object.create_fins", icon_value=icon)
		sub = row.row()
		sub.operator("mdl2.create_lods")
		sub.operator("mdl2.rename")

#
# class TOPBAR_PT_name(Panel):
# 	bl_space_type = 'TOPBAR'  # dummy
# 	bl_region_type = 'HEADER'
# 	bl_label = "Rename Active Item"
# 	bl_ui_units_x = 14
#
# 	def draw(self, context):
# 		layout = self.layout
#
# 		# Edit first editable button in popup
# 		def row_with_icon(layout, icon):
# 			row = layout.row()
# 			row.activate_init = True
# 			row.label(icon=icon)
# 			return row
#
# 		mode = context.mode
# 		space = context.space_data
# 		space_type = None if (space is None) else space.type
# 		found = False
# 		if space_type == 'SEQUENCE_EDITOR':
# 			layout.label(text="Sequence Strip Name")
# 			item = context.active_sequence_strip
# 			if item:
# 				row = row_with_icon(layout, 'SEQUENCE')
# 				row.prop(item, "name", text="")
# 				found = True
# 		elif space_type == 'NODE_EDITOR':
# 			layout.label(text="Node Label")
# 			item = context.active_node
# 			if item:
# 				row = row_with_icon(layout, 'NODE')
# 				row.prop(item, "label", text="")
# 				found = True
# 		elif space_type == 'NLA_EDITOR':
# 			layout.label(text="NLA Strip Name")
# 			item = next(
# 				(strip for strip in context.selected_nla_strips if strip.active), None)
# 			if item:
# 				row = row_with_icon(layout, 'NLA')
# 				row.prop(item, "name", text="")
# 				found = True
# 		else:
# 			if mode == 'POSE' or (mode == 'WEIGHT_PAINT' and context.pose_object):
# 				layout.label(text="Bone Name")
# 				item = context.active_pose_bone
# 				if item:
# 					row = row_with_icon(layout, 'BONE_DATA')
# 					row.prop(item, "name", text="")
# 					found = True
# 			elif mode == 'EDIT_ARMATURE':
# 				layout.label(text="Bone Name")
# 				item = context.active_bone
# 				if item:
# 					row = row_with_icon(layout, 'BONE_DATA')
# 					row.prop(item, "name", text="")
# 					found = True
# 			else:
# 				layout.label(text="Object Name")
# 				item = context.object
# 				if item:
# 					row = row_with_icon(layout, 'OBJECT_DATA')
# 					row.prop(item, "name", text="")
# 					found = True
#
# 		if not found:
# 			row = row_with_icon(layout, 'ERROR')
# 			row.label(text="No active item")
