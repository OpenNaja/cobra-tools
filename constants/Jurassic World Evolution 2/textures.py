textures = {
	'Metallic_Roughness_Opaque_Emissive': {
			"pBaseColourTexture": {"_BC": "_RGB", "_CA": "_A"},  # check if A is used here
			"pEmissiveTexture": {"_EM": ""},
			"pNormalTexture": {"_NM": "_RGB", "_AO": "_A"},  # BC7_UNORM - no coord dropping?
			"pRoughnessPackedTexture": {"_MT": "_R", "_SP": "_G", "_RN": "_B", "_FO": "_A"},
			"pFlexiColourMaskTexture": {"_F1": "_R", "_F2": "_G", "_F3": "_B", "_F4": "_A"},
		},
	'Foliage_Clip': {
			"pBaseColourTexture": {"_BC": "_RGB", "_CA": "_A"},  # not on tree leaves
			"pNormalTexture": {"_NM": "_RGB", "_AO": "_A"},  # BC7_UNORM - no coord dropping?
			"pRoughnessPackedTexture": {"_OP": "_R", "_RN": "_G", "_SP": "_B", "_MT": "_A"},
		},
	'Foliage_Opaque': {
			"pBaseColourTexture": {"_BC": "_RGB", "_CA": "_A"},  # not sure what A is
			"pNormalTexture": {"_NM": "_RGB", "_AO": "_A"},  # not sure if A is actually AO
			"pMoiseNoiseMask": {},  # ?
			"pMossBaseColour": {},  # ?
			"pMossNormalTexture": {},  # ?
		},
}
