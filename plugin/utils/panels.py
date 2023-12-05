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

		self.layout.prop(fgm, "pEnableScreenSpaceAO")
		pEnableScreenSpaceAO = fgm.pEnableScreenSpaceAO
		if pEnableScreenSpaceAO:
			box = self.layout.box()
			box.prop(fgm, "pAOTexCoordIndex")

		self.layout.prop(fgm, "pWeather_Enable")
		pWeather_Enable = fgm.pWeather_Enable
		if pWeather_Enable:
			box = self.layout.box()
			box.prop(fgm, "pEnableWeatherPooling")
			box.prop(fgm, "pWeather_ExplicitNormalThreshold")
			box.prop(fgm, "pMaximumWaterPermeability")
			box.prop(fgm, "pSnowOnSlopesOffset")
			box.prop(fgm, "pMaximumSnowAmount")

		self.layout.prop(fgm, "pEnablePoweredEmissive")
		pEnablePoweredEmissive = fgm.pEnablePoweredEmissive
		if pEnablePoweredEmissive:
			box = self.layout.box()
			box.prop(fgm, "pEmissiveLightType")
			box.prop(fgm, "pEmissiveTint")
			box.prop(fgm, "pEmissiveLightPower")
			box.prop(fgm, "pEmissiveAdaptiveBrighnessWeight")
			box.prop(fgm, "pEmissiveScrollData")
			box.prop(fgm, "pIsDisplayPanel")

		self.layout.prop(fgm, "pEnablePulsingEmissive")
		pEnablePulsingEmissive = fgm.pEnablePulsingEmissive
		if pEnablePulsingEmissive:
			box = self.layout.box()
			box.prop(fgm, "pPulsingEmitFrequency")
			box.prop(fgm, "pPulsingEmitDarkenScale")

		self.layout.prop(fgm, "pFlexiColourBlended")
		pFlexiColourBlended = fgm.pFlexiColourBlended
		if pFlexiColourBlended:
			box = self.layout.box()
			box.prop(fgm, "pFlexiColourTexCoordIndex")
			box.prop(fgm, "pFlexiColourVertexColour")
			box.prop(fgm, "pFlexiColourUseAdditiveBlend")
			box.prop(fgm, "pEnableEmissiveFlexiColour")

