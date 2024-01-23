import logging

tex_slots = {
    # American spelling to match blender?
    # from TMTK
    "BC": "Base Colour",
    "SM": "Smoothness",
    "RN": "Roughness",
    "CA": "Cavity",
    "AO": "Ambient Occlusion",
    "MT": "Metalness",
    "NM": "Normal",
    "NG": "Normal Variant",
    "OP": "Opacity",
    "AL": "Opacity Blend",
    "EM": "Emissive",
    "SP": "Specular",
    "F1": "Flexi Colour Mask 1",
    "F2": "Flexi Colour Mask 2",
    "F3": "Flexi Colour Mask 3",
    "F4": "Flexi Colour Mask 4",
    # custom keys follow
    "FO": "Flexi Opacity",
    "AB": "Albino",
    "ER": "Erythristic",
    "LE": "Leucistic",
    "ME": "Melanistic",
    "XA": "Xanthic",
    "BC_HM": "Base HSL Mask",
    "AB_HM": "Albino HSL Mask",
    "ER_HM": "Erythristic HSL Mask",
    "LE_HM": "Leucistic HSL Mask",
    "ME_HM": "Melanistic HSL Mask",
    "XA_HM": "Xanthic HSL Mask",
    "DE": "Detail",
    "DM": "Detail Mask",
    "DE_BC": "Detail Base Color",
    "DE_NM": "Detail Base Normals",
    "DE_MT": "Detail Base Metallic",
    "DE_RN": "Detail Base Roughness",
    "DE_AO": "Detail Base AO",
    "DE_SP": "Detail Base Specular",
    "BL_BC": "Detail Blend Color",
    "BL_NM": "Detail Blend Normals",
    "NQ_BC": "Detail Unique Color",
    "NQ_NM": "Detail Unique Normals",
    "NQ_MT": "Detail Unique Metallic",
    "NQ_RN": "Detail Unique Roughness",
    "NQ_SP": "Detail Unique Specular",
    "NQ_AO": "Detail Unique AO",
    "MS_BC": "Moss Base Color",
    "MS_RN": "Moss Roughness",
    "MS_VR": "Moss Variance",
    "IR": "Iridescence",
    "IM": "IridescenceMask",
    "PW": "Patchwork Mask",
    "PW_M1": "Marking Mask 1",
    "PW_M2": "Marking Mask 2",
    "PW_M3": "Marking Mask 3",
    "MN": "Marking Noise",
    "PB": "Piebald Patchwork Mask",
    "PB_M1": "Piebald Marking Mask 1",
    "PB_M2": "Piebald Marking Mask 2",
    "PB_M3": "Piebald Marking Mask 3",
    "SC": "Scar Mask",
    "BA": "Baldness",
    "HE": "Height",
    "TR": "Transmission",
    "LUT_C": "Color LUT",
    "LUT_SC": "Scar LUT",
}


def get_tex_channel_map(constants, game, shader_name):
	"""look up how the channels for this shader_name are packed into textures"""
	try:
		textures, attrib_dic = constants[game]["shaders"][shader_name]
	except:
		logging.warning(f"No attributes for shader '{shader_name}' in game {game}")
		raise
	# get the standard tex channel mapping for this game (defined by devs)
	all_tex_channels = constants[game]["texchannels"]
	# select only the textures that are required by this shader
	tex_channel_map = {tex: all_tex_channels.get(tex, {}) for tex in textures}
	try:
		# update channel mapping with known settings for this shader
		tex_channel_map.update(constants[game]["textures"][shader_name])
	except:
		logging.debug(f"No tex overrides for shader '{shader_name}' game {game}")
	return tex_channel_map
