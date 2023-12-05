textures = {
	'Metallic_Roughness_Opaque_Emissive': {
			# JWE2 trees seem to have CA on tree trunks pBaseColourTexture alpha, not on tree leaves
			# CA apparently not used on trunks in PZ (trunk has AO maps instead)
			"pBaseColourTexture": {"_BC": "_RGB", "_CA": "_A"},
			"pEmissiveTexture": {"_EM": ""},
			"pNormalTexture": {"_NM": "_RGB", "_AO": "_A"},  # BC7_UNORM - no coord dropping?
			"pRoughnessPackedTexture": {"_MT": "_R", "_SP": "_G", "_RN": "_B", "_FO": "_A"},
			"pFlexiColourMaskTexture": {"_F1": "_R", "_F2": "_G", "_F3": "_B", "_F4": "_A"},
		},
}
