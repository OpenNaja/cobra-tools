texchannels = {
	'p2MarkingBaldnessScarTexture': {"R": "PW_M1", "G": "PW_M2", "B": "BA", "A": "SC"},
	'p3MarkingScarTexture': {"R": "PW_M1", "G": "PW_M2", "B": "PW_M3", "A": "SC"},
	'pAOTexture': {"": "AO"},
	'pAOTexture2': {"": "AO2"},  # Blend between AO and AO2
	'pAOTextureDetail': {"": "DE_AO"},  # Overlaid on pAOTextureUnique
	'pAOTextureUnique': {"": "NQ_AO"},
	'pAlbedoAndRoughnessDetail': {"RGB": "BC", "A": "RN"},  # Or AL = Albedo?
	'pAlbinoBaseColourAndMaskTexture': {"RGB": "AB", "A": "AB_HM"},
	'pBaldnessScarTexture': {"R": "BA", "G": "SC", "B": "", "A": ""},  # B/A Appear unused
	'pBaseColour2': {"RGB": "BC2", "A": "RN2"},  # DiffuseBlend
	'pBaseColourAndMaskTexture': {"RGB": "BC", "A": "BC_HM"},
	'pBaseColourTexture': {"RGB": "BC", "A": "CA"},  # A apparently not used on tree trunks in PZ
	'pBaseColourTexture2': {"RGB": "BC2", "A": "CA2"},  # Blend between BC and BC2
	'pBaseColourTextureDetail': {"RGB": "DE_BC", "A": ""},  # Overlaid on pBaseColourTextureUnique
	'pBaseColourTextureDetailBase': {"RGB": "DE_BC", "A": ""},
	'pBaseColourTextureDetailBlend': {"RGB": "BL_BC", "A": ""},  # Overlaid on pBaseColourTextureDetailBase
	'pBaseColourTextureUnique': {"RGB": "NQ_BC", "A": "DM"},
	'pBaseDielectricSpecularLevelTexture': {"": "SP"},  # Ice shader
	'pBaseNormalTexture': {"RG": "NM"},
	'pCavityRoughnessDielectricArray': {"R": "CA", "G": "RN", "B": "SP", "A": ""},
	'pClipMap2': {"": ""},  # Glass Damage Mask
	'pClut': {"": "LUT_C"},   # Lookup/Input Mask
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
	'pDiffuseTexture': {"RGB": "DF_BC", "A": "DF_OP"},
	'pDiffuseXanthic': {"": "XA"},
	'pDistortionTexture': {"RG": "NM"},
	'pEmissiveMaskTexture': {"": ""},
	'pEmissiveTexture': {"": "EM"},
	'pErythristicBaseColourAndMaskTexture': {"RGB": "ER", "A": "ER_HM"},
	'pFinAlphaTexture': {"R": "FN_OP1", "G": "FN_OP2", "B": "FN_OP3", "A": ""},
	# 'pFlexiColourMaskTexture': {"": ""},
	'pFlexiColourMasksTexture': {"R": "F1", "G": "F2", "B": "F3", "A": "F4"},
	# 'pFlexiColourMasterMask': {"": ""},
	'pGradHeightArray': {"RG": "NM", "B": "HE", "A": ""},
	'pHeight': {"": "HE"},
	'pIridescenceStrength': {"": "IM"},
	'pIridescenceTexture': {"": "IR"},
	'pLeucisticBaseColourAndMaskTexture': {"RGB": "LE", "A": "LE_HM"},
	'pLeucisticColourAndMaskTexture': {"RGB": "LE", "A": "LE_HM"},  # seems to be a modded name
	'pMacroDamageBlendMap': {"": ""},
	'pMacroDiffuse': {"": ""},
	'pMarkingNoise': {"": "MN"},
	'pMarkingPatchworkMask': {"": "PW"},  # Lookup/Input Mask
	'pMaskAOTextureUnique': {"R": "DM", "G": "NQ_AO"},
	'pMelanisticBaseColourAndMaskTexture': {"RGB": "ME", "A": "ME_HM"},
	'pMossBaseColourRoughnessPackedTexture': {"RGB": "MS_BC", "A": "MS_RN"},
	'pMossNormalTexture': {"RG": "MS_NM"},
	'pMossVarianceTexture': {"": "MS_VR"},
	'pNormalBlendWeightTexture': {"": ""},
	'pNormalMapTextureUnique': {"RG": "NQ_NM"},  # Same as Detail pNormalTextureUnique but for Detail_Basic
	'pNormalTexture': {"RG": "NM"},
	'pNormalTexture2': {"RG": "NM2"},  # Blend between NM and NM2
	'pNormalTextureDetail': {"RG": "DE_NM"},
	'pNormalTextureDetailBase': {"RG": "DE_NM"},  # Overlaid on pNormalMapTextureUnique
	'pNormalTextureDetailBlend': {"RG": "BL_NM"},  # Overlaid on pNormalTextureDetailBase
	'pNormalTextureUnique': {"RG": "NQ_NM"},  # Same as Detail_Basic pNormalMapTextureUnique but for Detail
	'pOpacityTexture': {"": "OP"},
	'pOpacityTexture2': {"": "OP2"},  # Blend between OP and OP2
	'pPiebaldMask': {"": "PB"},  # Lookup/Input Mask
	'pPiebaldTexture': {"R": "PB_M1", "G": "PB_M2", "B": "PB_M3", "A": ""},
	# 'pPropertyTexture': {"": ""},
	'pRetroreflectiveness': {"": ""},
	'pRoughnessAOPackedTextureDetailBase': {"R": "DE_RN", "G": "DE_AO"},
	'pRoughnessPackedTexture': {"R": "MT", "G": "RN", "B": "SP", "A": ""},
	'pRoughnessPackedTexture2': {"R": "MT2", "G": "RN2", "B": "SP2", "A": ""},  # Blend between roughness 1 and 2
	'pRoughnessPackedTextureDetail': {"R": "DE_RN", "G": "DE_MT"},
	'pRoughnessPackedTextureUnique': {"R": "NQ_MT", "G": "NQ_RN", "B": "SP", "A": "NQ_OP"},  # No SP blending, remove NQ_ for Specular connection
	'pScarClut': {"": "LUT_SC"},  # Lookup/Input Mask
	'pShellMap': {"R": "", "G": "", "B": "", "A": ""},  # Lookup/Input Mask
	# 'pSkirtMaterialMask': {"": ""},
	# 'pSkirtNormals': {"": ""},
	'pSubLayerDiffuse0Texture': {"": ""}, # Ice shader
	'pSubLayerDiffuse1Texture': {"": ""}, # Ice shader
	'pThicknessTexture': {"": ""}, # Ice shader
	'pTransmittancePackedTexture': {"R": "TR", "G": "RN", "B": "SP", "A": ""},
	'pTransmittanceTexture': {"": "TR"},
	'pWaterDetailNormalTexture': {"RG": "NM"},
	'pWaterDetailRoughnessTexture': {"": "RN"},
	'pWaterfall_WaterFlowAndTimeOffsetMap': {"R": "", "G": "", "B": "", "A": ""},
	'pWaterfall_WaterFoamMaskMap': {"R": "", "G": "", "B": "", "A": ""},
	'pWaterfall_WaterNormalRoughnessMap': {"RGB": "NM", "A": "RN"},
	'pXanthicBaseColourAndMaskTexture': {"RGB": "XA", "A": "XA_HM"},
}
