textures = {
	'Metallic_Roughness_Opaque_Emissive': {
			"pBaseColourTexture": {"BC": "_RGB", "CA": "_A"},  # check if A is used here
			"pEmissiveTexture": {"EM": "_"},
			"pNormalTexture": {"NM": "_RGB", "AO": "_A"},  # BC7_UNORM - no coord dropping?
			"pRoughnessPackedTexture": {"MT": "_R", "SP": "_G", "RN": "_B", "FO": "_A"},
			"pFlexiColourMaskTexture": {"F1": "_R", "F2": "_G", "F3": "_B", "F4": "_A"},
		},
	'Foliage_Clip': {
			"pBaseColourTexture": {"BC": "_RGB", "CA": "_A"},  # not on tree leaves
			"pNormalTexture": {"NM": "_RGB", "AO": "_A"},  # BC7_UNORM - no coord dropping?
			"pRoughnessPackedTexture": {"OP": "_R", "RN": "_G", "SP": "_B", "MT": "_A"},
		},
	'Foliage_Opaque': {
			"pBaseColourTexture": {"BC": "_RGB", "CA": "_A"},  # not sure what A is
			"pNormalTexture": {"NM": "_RGB", "AO": "_A"},  # not sure if A is actually AO
			"pMoiseNoiseMask": {},  # ?
			"pMossBaseColour": {},  # ?
			"pMossNormalTexture": {},  # ?
		},
	'Foliage_Billboard': {
			"pDiffuseAlphaTexture": {"BC": "_RGB", "_OP": "_A"},
			"pNormalTexture": {"NM": "_RGB", "AO": "_A"},  # not sure if A is actually AO, might be unused (1.0)
		},
}
