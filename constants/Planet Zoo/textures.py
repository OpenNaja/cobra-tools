textures = {
	'Metallic_Roughness_Opaque_EmissiveLightType_Weather': {
			# CA apparently not used on trunks in PZ (trunk has AO maps instead)
			"pBaseColourTexture": {"BC": "RGB", "CA": "A"},
			"pAOTexture": {"AO": ""},
			"pEmissiveTexture": {"EM": ""},
			"pNormalTexture": {"NM": "RG"},  # BC5_UNORM
			"pRoughnessPackedTexture": {"MT": "R", "SP": "G", "RN": "B", "FO": "A"},
			"pFlexiColourMaskTexture": {"F1": "R", "F2": "G", "F3": "B", "F4": "A"},
		},
	'Foliage_Clip': {
			"pBaseColourTexture": {"BC": "RGB", "": "A"},  # A apparently unused
			"pAOTexture": {"AO": ""},
			"pNormalTexture": {"NM": "RG"},  # BC5_UNORM
			"pRoughnessPackedTexture": {"MT": "R", "SP": "G", "RN": "B", "OP": "A"},
		},
	'Foliage_Opaque': {
			"pBaseColourTexture": {"BC": "RGB", "": "A"},  # A apparently unused
			"pAOTexture": {"AO": ""},
			"pNormalTexture": {"NM": "RG"},  # BC5_UNORM
			"pRoughnessPackedTexture": {"MT": "R", "SP": "G", "RN": "B", "OP": "A"},  # a is unused
		},
}
