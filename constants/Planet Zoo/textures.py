textures = {
	'Metallic_Roughness_Opaque_EmissiveLightType_Weather': {
			# CA apparently not used on trunks in PZ (trunk has AO maps instead)
			"pBaseColourTexture": {"BC": "_RGB", "CA": "_A"},
			"pAOTexture": {"AO": "_"},
			"pEmissiveTexture": {"EM": "_"},
			"pNormalTexture": {"NM": "_RG"},  # BC5_UNORM
			"pRoughnessPackedTexture": {"MT": "_R", "SP": "_G", "RN": "_B", "FO": "_A"},
			"pFlexiColourMaskTexture": {"F1": "_R", "F2": "_G", "F3": "_B", "F4": "_A"},
		},
	'Foliage_Clip': {
			"pBaseColourTexture": {"BC": "_RGB", "": "_A"},  # A apparently unused
			"pAOTexture": {"AO": "_"},
			"pNormalTexture": {"NM": "_RG"},  # BC5_UNORM
			"pRoughnessPackedTexture": {"MT": "_R", "SP": "_G", "RN": "_B", "OP": "_A"},
		},
	'Foliage_Opaque': {
			"pBaseColourTexture": {"BC": "_RGB", "": "_A"},  # A apparently unused
			"pAOTexture": {"AO": "_"},
			"pNormalTexture": {"NM": "_RG"},  # BC5_UNORM
			"pRoughnessPackedTexture": {"MT": "_R", "SP": "_G", "RN": "_B", "OP": "_A"},  # a is unused
		},
}
