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

