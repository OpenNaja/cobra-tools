# Manual Shader Entries
# These will not be overwritten by FGM Inspection
# Note: Statistics may not be accurate due to manual attribute compilation

shaders = {
	'Metallic_Roughness_Clip_Weather_Transmissive': (
		[
			'pAOTexture',
			'pBaseColourTexture',
			'pFlexiColourMasksTexture',
			'pNormalTexture',
			'pOpacityTexture',
			'pRoughnessPackedTexture',
		],
		{
			'pAOTexCoordIndex': (5, [((0,), 10)]),
			'pAlphaTestRef': (0, [((0.5,), 10)]),
			'pEnableAlphaTestRefFade': (6, [((0,), 10)]),
			'pEnableScreenSpaceAO': (6, [((1,), 10)]),
			'pEnableWeatherPooling': (6, [((1,), 10)]),
			'pFlexiColourBlended': (6, [((1,), 10)]),
			'pFlexiColourTexCoordIndex': (5, [((0,), 10)]),
			'pFlexiColourUseAdditiveBlend': (6, [((0,), 10)]),
			'pFlexiColourVertexColour': (6, [((0,), 10)]),
			'pHighlightAlphaTestRefBias': (0, [((0.0,), 10)]),
			'pMaximumSnowAmount': (0, [((1.0,), 10)]),
			'pMaximumWaterPermeability': (0, [((0.5,), 10)]),
			'pMipBias': (0, [((-2.0,), 6)]),
			'pRenderLayerOverride': (5, [((-1,), 10)]),
			'pSnowOnSlopesOffset': (0, [((0.0,), 10)]),
			'pTransmittanceScale': (0, [((1.0,), 10)]),
			'pUseExplicitNormals': (6, [((0,), 140), ((1,), 1)]),
			'pUseTwoSidedExplicitNormal': (6, [((1,), 140), ((0,), 1)]),
			'pVerticalTiling': (0, [((0.25,), 10)]),
			'pWeather_Enable': (6, [((1,), 10)]),
			'pWeather_ExplicitNormalThreshold': (0, [((0.85,), 10)]),
		}
	),
}
