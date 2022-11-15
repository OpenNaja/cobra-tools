import logging
import traceback

import bpy
import os

from generated.formats.fgm.compounds.FgmHeader import FgmHeader
from generated.formats.ovl_base import OvlContext
from plugin.utils.node_arrange import nodes_iterate
from plugin.utils.node_util import get_tree, load_tex_node


class BaseShader:
	"""Basic class for all derived shaders to inherit from"""

	diffuse_slots = (
		"pdiffusetexture", "pbasediffusetexture", "pbasecolourtexture", "pbasecolourtexture_rgb",
		"pbasecolourandmasktexture", "pdiffusealphatexture", "pdiffuse_alphatexture",
		"palbinobasecolourandmasktexture", "pdinosaurfeathers_basediffusetexture")

	ao_slots = ("paotexture", "pbasepackedtexture_a", "pbaseaotexture_r", "pbaseaotexture")

	normal_slots = ("pnormaltexture", "pnormaltexture_rg", "pnormaltexture_rgb", "pbasenormaltexture_rg", "pbasenormaltexture_rgb",)

	specular_slots = ("proughnesspackedtexture_b", "pspecularmaptexture_r", "pbasenormaltexture_b")

	roughness_slots = ("proughnesspackedtexture_g", "pnormaltexture_a", "pbasenormaltexture_a")  # "pspecularmaptexture_g"

	# note that JWE1 uses proughnesspackedtexture_r as alpha, only pbasepackedtexture_b as metal!
	metallic_slots = ("proughnesspackedtexture_r", "pbasepackedtexture_b")

	emissive_slots = ("pemissivetexture", )

	alpha_slots = ("pdiffusealphatexture", "pdiffuse_alphatexture")

	def get_tex(self, tex_dic, names):
		for tex_name in names:
			# get diffuse
			if tex_name in tex_dic:
				yield tex_dic[tex_name]
				# stop after finding a suitable one
				break


def load_material_from_asset_library(created_materials, filepath, matname):
	"""try to load the material from the list of asset libraries"""
	library_path  =  os.path.abspath(filepath)  # blend file name
	inner_path    = 'Material'   # type 
	material_name = matname # name

	# try current material case
	bpy.ops.wm.append(
		filepath=os.path.join(library_path, inner_path, material_name),
		directory=os.path.join(library_path, inner_path),
		filename=material_name
		)
	# also try all lowercase
	#if material_name != material_name.lower():
	#	# try lowercase
	#	bpy.ops.wm.append(
	#		filepath=os.path.join(library_path, inner_path, material_name),
	#		directory=os.path.join(library_path, inner_path),
	#		filename=material_name.lower()
	#		)

	# if we have loaded the material, mark it out
	b_mat = bpy.data.materials.get(matname)
	if b_mat:
		created_materials[matname] = b_mat

	# we return nothing, this function will add the material to 
	# blender if found, nothing will happen if not found.


def load_material_from_libraries(created_materials, matname):

	# do not import twice
	if matname in created_materials:
		return

	prefs = bpy.context.preferences
	filepaths = prefs.filepaths
	asset_libraries = filepaths.asset_libraries
	logging.info(f"starting library search for {matname}")

	# we are looping through all asset library files, alternatively we can limit this to
	# a specific library name, or only the current open library file.
	for asset_library in asset_libraries:
		library_name  = asset_library.name
		library_path  = asset_library.path
		logging.info(f"Checking: {library_name}")
		library_files = [os.path.join(dp, f) for dp, dn, filenames in os.walk(library_path) for f in filenames if os.path.splitext(f)[1] == '.blend']
		for library in library_files:
			# avoid reloading the same material in case it is present in several blend files
			if matname not in created_materials:
				load_material_from_asset_library(created_materials, library, matname)


def create_material(in_dir, matname):

	logging.info(f"Importing material {matname}")
	b_mat = bpy.data.materials.new(matname)

	fgm_path = os.path.join(in_dir, f"{matname}.fgm")
	# print(fgm_path)
	try:
		fgm_data = FgmHeader.from_xml_file(fgm_path, OvlContext())
	except FileNotFoundError:
		logging.warning(f"{fgm_path} does not exist!")
		return b_mat
	except:
		logging.warning(f"{fgm_path} could not be loaded!")
		return b_mat
	# base_index = fgm_data.textures[0].layers[1]
	# height_index = fgm_data.textures[1].layers[1]
	tree = get_tree(b_mat)
	output = tree.nodes.new('ShaderNodeOutputMaterial')
	principled = tree.nodes.new('ShaderNodeBsdfPrincipled')

	# color_ramp = fgm_data.get_color_ramp("colourKey", "RGB")
	# opacity_ramp = fgm_data.get_color_ramp("opacityKey", "Value")
	# if color_ramp and opacity_ramp:
	# 	# print(color_ramp, list(zip(color_ramp)))
	# 	positions, colors = zip(*color_ramp)
	# 	positions_2, opacities = zip(*color_ramp)
	# 	ramp = tree.nodes.new('ShaderNodeValToRGB')
	# 	for position, color, opacity in zip(positions, colors, opacities):
	# 		print(position, color, opacity)
	# 		pos_relative = (position-min(positions)) / (max(positions)-min(positions))
	# 		e = ramp.color_ramp.elements.new(pos_relative)
	# 		e.color[:3] = color
	# 		e.alpha = opacity[0]

	shader = BaseShader()
	all_textures = [file for file in os.listdir(in_dir) if file.lower().endswith(".png")]
	# map texture names to node
	tex_dic = {}
	for dep_info in fgm_data.name_foreach_textures.data:
		if not dep_info.dependency_name.data:
			continue
		png_base, ext = os.path.splitext(dep_info.dependency_name.data.lower())
		if "blendweights" in png_base or "warpoffset" in png_base:
			continue
		textures = [file for file in all_textures if file.lower().startswith(png_base)]

		# Until better option to organize the shader info, create texture group node
		tex_frame = tree.nodes.new('NodeFrame')
		tex_frame.label = dep_info.dependency_name.data.lower()

		# print(textures)
		for png_name in textures:
			png_path = os.path.join(in_dir, png_name)
			b_tex = load_tex_node(tree, png_path)
			b_tex.parent = tex_frame  # assign the texture frame to this png
			k = png_name.lower().split(".")[1]
			tex_dic[k] = b_tex

	# get diffuse
	for diffuse in shader.get_tex(tex_dic, shader.diffuse_slots):
		# apply AO to diffuse
		for ao in shader.get_tex(tex_dic, shader.ao_slots):
			ao.image.colorspace_settings.name = "Non-Color"
			diffuse_premix = tree.nodes.new('ShaderNodeMixRGB')
			diffuse_premix.blend_type = "MULTIPLY"
			diffuse_premix.inputs["Fac"].default_value = 1.0
			tree.links.new(diffuse.outputs[0], diffuse_premix.inputs["Color1"])
			tree.links.new(ao.outputs[0], diffuse_premix.inputs["Color2"])
			diffuse = diffuse_premix

		# get marking
		fur_names = [k for k in tex_dic.keys() if "marking" in k and "noise" not in k and "patchwork" not in k]
		lut_names = [k for k in tex_dic.keys() if "pclut" in k]
		if fur_names and lut_names:
			marking = tex_dic[sorted(fur_names)[0]]
			lut = tex_dic[sorted(lut_names)[0]]
			marking.image.colorspace_settings.name = "Non-Color"
			# PZ LUTs usually occupy half of the texture
			scaler = tree.nodes.new('ShaderNodeMapping')
			scaler.vector_type = "POINT"
			tree.links.new(marking.outputs[0], scaler.inputs[0])
			tree.links.new(scaler.outputs[0], lut.inputs[0])
			# texture needs to use extend mode so that it doesn't interpolate with the repeated image
			lut.extension = "EXTEND"
			# also to prevent interpolation at the middle of the image, set to closest
			lut.interpolation = "Closest"
			# location - put it into the first line (variants may use other lines, not sure where the FGM defines that)
			scaler.inputs[1].default_value = (0, 1, 0)
			# so scale the incoming greyscale coordinates so that X 1 lands in the center of the LUT, flatten it on Y
			scaler.inputs[3].default_value = (0.499, 0, 0)
			diffuse_premix = tree.nodes.new('ShaderNodeMixRGB')
			diffuse_premix.blend_type = "MIX"

			tree.links.new(diffuse.outputs[0], diffuse_premix.inputs["Color1"])
			tree.links.new(lut.outputs[0], diffuse_premix.inputs["Color2"])
			# now we use the alpha channel from the LUT
			tree.links.new(lut.outputs[1], diffuse_premix.inputs["Fac"])
			diffuse = diffuse_premix
		#  link finished diffuse to shader
		tree.links.new(diffuse.outputs[0], principled.inputs["Base Color"])

	for normal in shader.get_tex(tex_dic, shader.normal_slots):
		normal.image.colorspace_settings.name = "Non-Color"
		normal_map = tree.nodes.new('ShaderNodeNormalMap')
		normal_map.inputs[0].default_value = 0.4 # nah, it really doesn't
		tree.links.new(normal.outputs[0], normal_map.inputs[1])
		tree.links.new(normal_map.outputs[0], principled.inputs["Normal"])

	# PZ - F0 value for dielectrics, related to IOR / fake specularity
	# https://forum.sketchfab.com/t/what-is-specular-fo/22752/7
	for specular in shader.get_tex(tex_dic, shader.specular_slots):
		specular.image.colorspace_settings.name = "Non-Color"
		tree.links.new(specular.outputs[0], principled.inputs["Specular"])

	# roughness
	for roughness in shader.get_tex(tex_dic, shader.roughness_slots):
		roughness.image.colorspace_settings.name = "Non-Color"
		tree.links.new(roughness.outputs[0], principled.inputs["Roughness"])

	# JWE dinos, PZ - metallic
	for metallic in shader.get_tex(tex_dic, shader.metallic_slots):
		metallic.image.colorspace_settings.name = "Non-Color"
		tree.links.new(metallic.outputs[0], principled.inputs["Metallic"])

	for emissive in shader.get_tex(tex_dic, shader.emissive_slots):
		tree.links.new(emissive.outputs[0], principled.inputs["Emission"])

	# alpha
	alpha = None
	# JWE billboard: Foliage_Billboard
	for alpha in shader.get_tex(tex_dic, shader.alpha_slots):
		alpha_pass = alpha.outputs[1]
	# PZ penguin
	if "popacitytexture" in tex_dic:
		alpha = tex_dic["popacitytexture"]
		alpha_pass = alpha.outputs[0]
	elif "JURASSIC" in fgm_data.game and "proughnesspackedtexture_r" in tex_dic and "Foliage_Clip" in fgm_data.shader_name:
		alpha = tex_dic["proughnesspackedtexture_r"]
		alpha_pass = alpha.outputs[0]
	elif "proughnesspackedtexture_a" in tex_dic:
		alpha = tex_dic["proughnesspackedtexture_a"]
		alpha_pass = alpha.outputs[0]
	#
	# inaki: Ugly per-shader basecolour alpha, temporary
	# in Metallic_Roughness_Clip_Weather_BC7 pbasecolour alpha is metallicness
	elif 'Clip' in fgm_data.shader_name and "pbasecolourtexture_a" in tex_dic:
		alpha = tex_dic["pbasecolourtexture_a"]
		alpha_pass = alpha.outputs[0]
	elif 'Metallic_Roughness_Opaque_BC7' in fgm_data.shader_name and "pbasecolourtexture_a" in tex_dic:
		tree.links.new(tex_dic["pbasecolourtexture_a"].outputs[0], principled.inputs[6]) # metallicness

	#
	# inaki: Ugly per-shader basecolour alpha, temporary
	# in Metallic_Roughness_Clip_Weather_BC7 pnormaltexture alpha is AO
	if 'Clip' in fgm_data.shader_name and "pnormaltexture_a" in tex_dic:
		ao = tex_dic["pnormaltexture_a"]
		ao.image.colorspace_settings.name = "Non-Color"
		diffuse_premix = tree.nodes.new('ShaderNodeMixRGB')
		diffuse_premix.blend_type = "MULTIPLY"
		diffuse_premix.inputs["Fac"].default_value = 1.0
		tree.links.new(diffuse.outputs[0], diffuse_premix.inputs["Color1"])
		tree.links.new(ao.outputs[0], diffuse_premix.inputs["Color2"])
		diffuse = diffuse_premix


	if alpha:
		# transparency
		b_mat.blend_method = "CLIP"
		b_mat.shadow_method = "CLIP"
		for attr, attr_data in zip(fgm_data.attributes.data, fgm_data.value_foreach_attributes.data):
			if "palphatestref" in attr.name.lower():
				# blender appears to be stricter with the alpha clipping
				# PZ ele has it set to 1.0 in fgm, which makes it invisible in blender
				b_mat.alpha_threshold = attr_data.value[0] * 0.5
				break
		transp = tree.nodes.new('ShaderNodeBsdfTransparent')
		alpha_mixer = tree.nodes.new('ShaderNodeMixShader')
		tree.links.new(alpha_pass, alpha_mixer.inputs[0])

		tree.links.new(transp.outputs[0], alpha_mixer.inputs[1])
		tree.links.new(principled.outputs[0], alpha_mixer.inputs[2])
		tree.links.new(alpha_mixer.outputs[0], output.inputs[0])
		alpha_mixer.update()
	# no alpha
	else:
		b_mat.blend_method = "OPAQUE"
		tree.links.new(principled.outputs[0], output.inputs[0])

	nodes_iterate(tree, output)
	return b_mat


def import_material(created_materials, in_dir, b_me, material):
	material_name = material.name
	try:

		# try finding the material first in the user libraries, only use lowercase
		load_material_from_libraries(created_materials, material_name.lower())

		# find if material is in blender already. Imported FGMs
		# will have the material name all in lowercase, we need
		# to check both.
		b_mat = bpy.data.materials.get(material_name)
		if not b_mat:
			b_mat = bpy.data.materials.get(material_name.lower())

		# if the material is in blender first, just apply the 
		# existing one.
		if b_mat:
			created_materials[material_name] = b_mat
			b_mat["some_index"] = material.some_index
			b_me.materials.append(b_mat)
			return

		# additionally keep track here so we create a node tree only once during import
		# but make sure that we overwrite existing materials.
		# TODO: this might be redundant since we are checking now materials
		# exist in the previous code block.
		if material_name not in created_materials:
			b_mat = create_material(in_dir, material_name)
			created_materials[material_name] = b_mat
		else:
			logging.info(f"Already imported material {material_name}")
			b_mat = created_materials[material_name]
		# store material unknowns
		b_mat["some_index"] = material.some_index
		b_me.materials.append(b_mat)
	except:
		logging.warning(f"Material {material_name} failed")
		traceback.print_exc()
