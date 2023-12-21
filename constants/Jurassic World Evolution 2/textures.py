textures = {
	'Metallic_Roughness_Opaque_Emissive': {
			"pBaseColourTexture": {"BC": "RGB", "CA": "A"},  # check if A is used here
			"pEmissiveTexture": {"EM": ""},
			"pNormalTexture": {"NM": "RGB", "AO": "A"},  # BC7_UNORM - no coord dropping?
			"pRoughnessPackedTexture": {"MT": "R", "SP": "G", "RN": "B", "FO": "A"},
			"pFlexiColourMaskTexture": {"F1": "R", "F2": "G", "F3": "B", "F4": "A"},
		},
	'Foliage_Clip': {
			"pBaseColourTexture": {"BC": "RGB", "CA": "A"},  # not on tree leaves
			"pNormalTexture": {"NM": "RGB", "AO": "A"},  # BC7_UNORM - no coord dropping?
			"pRoughnessPackedTexture": {"OP": "R", "RN": "G", "SP": "B", "MT": "A"},
		},
	'Foliage_Opaque': {
			"pBaseColourTexture": {"BC": "RGB", "CA": "A"},  # not sure what A is
			"pNormalTexture": {"NM": "RGB", "AO": "A"},  # not sure if A is actually AO
			"pMoiseNoiseMask": {},  # ?
			"pMossBaseColour": {},  # ?
			"pMossNormalTexture": {},  # ?
		},
	'Foliage_Billboard': {
			"pDiffuseAlphaTexture": {"BC": "RGB", "OP": "A"},
			"pNormalTexture": {"NM": "RGB", "AO": "A"},  # not sure if A is actually AO, might be unused (1.0)
		},
}
