texchannels = {
	'p2MarkingBaldnessScarTexture': {"R": "M1", "G": "M2", "B": "BA", "A": "SC"},
	'p3MarkingScarTexture': {"R": "M1", "G": "M2", "B": "M3", "A": "SC"},
	'pAOTexture': {"": "AO"},
	'pAOTexture2': {"": "AO2"},  # Blend between AO and AO2
	'pAOTextureDetail': {"": "AO2"},  # Overlaid on pAOTextureUnique
	'pAOTextureUnique': {"": "AO"},
	'pAlbedoAndRoughnessDetail': {"RGB": "BC", "A": "RN"},  # Or AL = Albedo?
	'pAlbinoBaseColourAndMaskTexture': {"RGB": "AB", "A": "HM"},
	'pBaldnessScarTexture': {"R": "BA", "G": "SC", "B": "", "A": ""},  # B/A Appear unused
	'pBaseColour2': {"RGB": "BC2", "A": "RN2"},  # DiffuseBlend
	'pBaseColourAndMaskTexture': {"RGB": "BC", "A": "HM"},
	'pBaseColourTexture': {"RGB": "BC", "A": "CA"},  # A apparently not used on tree trunks in PZ
	'pBaseColourTexture2': {"RGB": "BC2", "A": "CA2"},  # Blend between BC and BC2
	'pBaseColourTextureDetail': {"RGB": "DE", "A": ""},  # Overlaid on pBaseColourTextureUnique
	'pBaseColourTextureDetailBase': {"RGB": "BC", "A": ""},
	'pBaseColourTextureDetailBlend': {"RGB": "DE", "A": ""},  # Overlaid on pBaseColourTextureDetailBase
	'pBaseColourTextureUnique': {"RGB": "BC", "A": "DM"},
	'pBaseDielectricSpecularLevelTexture': {"": "SP"},  # Ice shader
	'pBaseNormalTexture': {"RG": "NM"},
	'pCavityRoughnessDielectricArray': {"R": "CA", "G": "RN", "B": "SP", "A": ""},
	'pClipMap2': {"": ""},  # Glass Damage Mask
	'pClut': {"": ""},   # Lookup/Input Mask
	# 'pCoarseNoise': {"": ""},
	'pDamageBlendMap': {"": ""},  # Lookup/Input Mask
	'pDetailMask': {"": "DM"},
	'pDetailNormalTexture': {"RG": "NM"},
	'pDetailRoughnessTexture': {"": "RN"},
	'pDiffuse': {"": "BC"},
	'pDiffuseAlbino': {"": "AB"},
	'pDiffuseArray': {"": "BC"},
	'pDiffuseErythristic': {"": "ER"},
	'pDiffuseLeucistic': {"": "LE"},
	'pDiffuseMelanistic': {"": "ME"},
	'pDiffuseTexture': {"": "BC"},
	'pDiffuseXanthic': {"": "XA"},
	'pDistortionTexture': {"RG": "NM"},
	'pEmissiveMaskTexture': {"": ""},
	'pEmissiveTexture': {"": "EM"},
	'pErythristicBaseColourAndMaskTexture': {"RGB": "ER", "A": "HM"},
	'pFinAlphaTexture': {"R": "OP", "G": "OP", "B": "OP", "A": ""},
	# 'pFlexiColourMaskTexture': {"": ""},
	'pFlexiColourMasksTexture': {"R": "F1", "G": "F2", "B": "F3", "A": "F4"},
	# 'pFlexiColourMasterMask': {"": ""},
	'pGradHeightArray': {"RG": "NM", "B": "HE", "A": ""},
	'pHeight': {"": "HE"},
	'pIridescenceStrength': {"": "IM"},
	'pIridescenceTexture': {"": "IR"},
	'pLeucisticBaseColourAndMaskTexture': {"RGB": "LE", "A": "HM"},
	'pMacroDamageBlendMap': {"": ""},
	'pMacroDiffuse': {"": ""},
	'pMarkingNoise': {"": ""},
	'pMarkingPatchworkMask': {"": ""},  # Lookup/Input Mask
	'pMaskAOTextureUnique': {"R": "DM", "G": "AO"},
	'pMelanisticBaseColourAndMaskTexture': {"RGB": "ME", "A": "HM"},
	'pMossBaseColourRoughnessPackedTexture': {"RGB": "BC", "A": "RN"},
	'pMossNormalTexture': {"RG": "NM"},
	'pMossVarianceTexture': {"": ""},
	'pNormalBlendWeightTexture': {"": ""},
	'pNormalMapTextureUnique': {"RG": "NM"},  # Same as Detail pNormalTextureUnique but for Detail_Basic
	'pNormalTexture': {"RG": "NM"},
	'pNormalTexture2': {"RG": "NM2"},  # Blend between NM and NM2
	'pNormalTextureDetail': {"RG": "NM"},
	'pNormalTextureDetailBase': {"RG": "NM2"},  # Overlaid on pNormalMapTextureUnique
	'pNormalTextureDetailBlend': {"RG": "NM3"},  # Overlaid on pNormalTextureDetailBase
	'pNormalTextureUnique': {"RG": "NM"},  # Same as Detail_Basic pNormalMapTextureUnique but for Detail
	'pOpacityTexture': {"": "OP"},
	'pOpacityTexture2': {"": "OP2"},  # Blend between OP and OP2
	'pPiebaldMask': {"": ""},  # Lookup/Input Mask
	'pPiebaldTexture': {"R": "", "G": "", "B": "", "A": ""},
	# 'pPropertyTexture': {"": ""},
	'pRetroreflectiveness': {"": ""},
	'pRoughnessAOPackedTextureDetailBase': {"R": "RN", "G": "AO"},
	'pRoughnessPackedTexture': {"R": "MT", "G": "RN", "B": "SP", "A": "OP"},
	'pRoughnessPackedTexture2': {"R": "MT2", "G": "RN2", "B": "SP2", "A": "OP2"},  # Blend between roughness 1 and 2
	'pRoughnessPackedTextureDetail': {"R": "RN", "G": ""},  # ? Mask
	'pRoughnessPackedTextureUnique': {"R": "MT", "G": "RN", "B": "SP", "A": "OP"},
	'pScarClut': {"": ""},  # Lookup/Input Mask
	'pShellMap': {"R": "", "G": "", "B": "", "A": ""},  # Lookup/Input Mask
	# 'pSkirtMaterialMask': {"": ""},
	# 'pSkirtNormals': {"": ""},
	'pSubLayerDiffuse0Texture': {"": ""}, # Ice shader
	'pSubLayerDiffuse1Texture': {"": ""}, # Ice shader
	'pThicknessTexture': {"": ""}, # Ice shader
	'pTransmittancePackedTexture': {"R": "TR", "G": "RN", "B": "SP", "A": "OP"},
	'pTransmittanceTexture': {"": "TR"},
	'pWaterDetailNormalTexture': {"RG": "NM"},
	'pWaterDetailRoughnessTexture': {"": "RN"},
	'pWaterfall_WaterFlowAndTimeOffsetMap': {"R": "", "G": "", "B": "", "A": ""},
	'pWaterfall_WaterFoamMaskMap': {"R": "", "G": "", "B": "", "A": ""},
	'pWaterfall_WaterNormalRoughnessMap': {"RGB": "NM", "A": "RN"},
	'pXanthicBaseColourAndMaskTexture': {"RGB": "XA", "A": "HM"},
}
