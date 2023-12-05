textures = {
	'Metallic_Roughness_Opaque_EmissiveLightType_Weather': {
			# CA apparently not used on trunks in PZ (trunk has AO maps instead)
			"pBaseColourTexture": {"_BC": "_RGB", "_CA": "_A"},
			"pAOTexture": {"_AO": ""},
			"pEmissiveTexture": {"_EM": ""},
			"pNormalTexture": {"_NM": "_RGB"},  # BC5_UNORM
			"pRoughnessPackedTexture": {"_MT": "_R", "_SP": "_G", "_RN": "_B", "_FO": "_A"},
			"pFlexiColourMaskTexture": {"_F1": "_R", "_F2": "_G", "_F3": "_B", "_F4": "_A"},
		},
	'Foliage_Clip': {
			"pBaseColourTexture": {"_BC": "_RGB", "": "_A"},  # A apparently unused
			"pAOTexture": {"_AO": ""},
			"pNormalTexture": {"_NM": "_RGB"},  # BC5_UNORM
			"pRoughnessPackedTexture": {"_MT": "_R", "_SP": "_G", "_RN": "_B", "_OP": "_A"},
		},
	'Foliage_Opaque': {
			"pBaseColourTexture": {"_BC": "_RGB", "": "_A"},  # A apparently unused
			"pAOTexture": {"_AO": ""},
			"pNormalTexture": {"_NM": "_RGB"},  # BC5_UNORM
			"pRoughnessPackedTexture": {"_MT": "_R", "_SP": "_G", "_RN": "_B", "_OP": "_A"},  # a is unused
		},
}
