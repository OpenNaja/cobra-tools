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
    "DE": "Detail",
    "IR": "Iridescence",
    "IM": "IridescenceMask",
    "M1": "Marking Mask 1",
    "M2": "Marking Mask 2",
    "M3": "Marking Mask 3",
    "SC": "Scar Mask",
    "BA": "Baldness",
    "HE": "Height",
    "TR": "Transmission",
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
