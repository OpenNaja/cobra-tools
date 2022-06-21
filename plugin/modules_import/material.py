import logging
import traceback

import bpy
import os

from generated.formats.fgm import FgmFile
from generated.formats.fgm.compound.FgmHeader import FgmHeader
from generated.formats.ovl.versions import is_jwe
from generated.formats.ovl_base import OvlContext
from plugin.utils.node_arrange import nodes_iterate
from plugin.utils.node_util import get_tree, load_tex


def create_material(in_dir, matname):

	logging.info(f"Importing material {matname}")
	b_mat = bpy.data.materials.new(matname)

	fgm_path = os.path.join(in_dir, matname + ".fgm")
	# print(fgm_path)
	try:
		fgm_data = FgmHeader.from_xml_file(fgm_path, OvlContext())
		# fgm_data = FgmFile()
		# fgm_data.load(fgm_path)
	except FileNotFoundError:
		logging.warning(f"{fgm_path} does not exist!")
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

	all_textures = [file for file in os.listdir(in_dir) if file.lower().endswith(".png")]
	# map texture names to node
	tex_dic = {}
	for dep_info in fgm_data.dependencies.data:
		if not dep_info.dependency_name.data:
			continue
		png_base, ext = os.path.splitext(dep_info.dependency_name.data.lower())
		if "blendweights" in png_base or "warpoffset" in png_base:
			continue
		textures = [file for file in all_textures if file.lower().startswith(png_base)]
		if not textures:
			png_base = png_base.lower().replace("_eyes", "").replace("_fin", "").replace("_shell", "")
			textures = [file for file in all_textures if file.lower().startswith(png_base)]
		if not textures:
			textures = [png_base + ".png", ]
		# print(textures)
		for png_name in textures:
			png_path = os.path.join(in_dir, png_name)
			b_tex = load_tex(tree, png_path)
			k = png_name.lower().split(".")[1]
			tex_dic[k] = b_tex

	# get diffuse and AO
	for diffuse_name in ("pdiffusetexture", "pbasediffusetexture", "pbasecolourtexture", "pbasecolourandmasktexture", "pdiffusealphatexture", "pdiffuse_alphatexture", "palbinobasecolourandmasktexture", "pdinosaurfeathers_basediffusetexture"):
		# get diffuse
		if diffuse_name in tex_dic:
			diffuse = tex_dic[diffuse_name]
			# get AO
			for ao_name in ("paotexture", "pbasepackedtexture_[03]", "pbaseaotexture"):
				if ao_name in tex_dic:
					ao = tex_dic[ao_name]
					ao.image.colorspace_settings.name = "Non-Color"

					# apply AO to diffuse
					diffuse_premix = tree.nodes.new('ShaderNodeMixRGB')
					diffuse_premix.blend_type = "MULTIPLY"
					diffuse_premix.inputs["Fac"].default_value = .25
					tree.links.new(diffuse.outputs[0], diffuse_premix.inputs["Color1"])
					tree.links.new(ao.outputs[0], diffuse_premix.inputs["Color2"])
					diffuse = diffuse_premix
					break
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
				# apply AO to diffuse
				diffuse_premix = tree.nodes.new('ShaderNodeMixRGB')
				diffuse_premix.blend_type = "MIX"

				tree.links.new(diffuse.outputs[0], diffuse_premix.inputs["Color1"])
				tree.links.new(lut.outputs[0], diffuse_premix.inputs["Color2"])
				# now we use the alpha channel from the LUT
				# tree.links.new(marking.outputs[0], diffuse_premix.inputs["Fac"])
				tree.links.new(lut.outputs[1], diffuse_premix.inputs["Fac"])
				diffuse = diffuse_premix
			#  link finished diffuse to shader
			tree.links.new(diffuse.outputs[0], principled.inputs["Base Color"])
			break

	for normal_name in ("pnormaltexture", "pbasenormaltexture_[0]"):
		# get diffuse
		if normal_name in tex_dic:
			normal = tex_dic[normal_name]
			normal.image.colorspace_settings.name = "Non-Color"
			normal_map = tree.nodes.new('ShaderNodeNormalMap')
			tree.links.new(normal.outputs[0], normal_map.inputs[1])
			# normal_map.inputs["Strength"].default_value = 1.0
			tree.links.new(normal_map.outputs[0], principled.inputs["Normal"])

	# PZ - specularity?
	for spec_name in ("proughnesspackedtexture_[02]", "pspecularmaptexture_[00]",):
		if spec_name in tex_dic:
			specular = tex_dic[spec_name]
			specular.image.colorspace_settings.name = "Non-Color"
			tree.links.new(specular.outputs[0], principled.inputs["Specular"])

	# PZ - roughness?
	for roughness_name in ("proughnesspackedtexture_[01]", "pbasenormaltexture_[2]"): # "pspecularmaptexture_[01]" ?
		if roughness_name in tex_dic:
			roughness = tex_dic[roughness_name]
			roughness.image.colorspace_settings.name = "Non-Color"
			tree.links.new(roughness.outputs[0], principled.inputs["Roughness"])

	# JWE dinos - metalness
	for metal_name in ("pbasepackedtexture_[02]",):
		if metal_name in tex_dic:
			metal = tex_dic[metal_name]
			metal.image.colorspace_settings.name = "Non-Color"
			tree.links.new(metal.outputs[0], principled.inputs["Metallic"])

	# alpha
	alpha = None
	# JWE billboard: Foliage_Billboard
	if "pdiffusealphatexture" in tex_dic:
		alpha = tex_dic["pdiffusealphatexture"]
		alpha_pass = alpha.outputs[1]
	elif "pdiffuse_alphatexture" in tex_dic:
		alpha = tex_dic["pdiffuse_alphatexture"]
		alpha_pass = alpha.outputs[1]
	# PZ penguin
	elif "popacitytexture" in tex_dic:
		alpha = tex_dic["popacitytexture"]
		alpha_pass = alpha.outputs[0]
	# todo - use game version tag?
	elif is_jwe(fgm_data.context) and "proughnesspackedtexture_[00]" in tex_dic and "Foliage_Clip" in fgm_data.shader_name:
		alpha = tex_dic["proughnesspackedtexture_[00]"]
		alpha_pass = alpha.outputs[0]
	elif "proughnesspackedtexture_[03]" in tex_dic:
		alpha = tex_dic["proughnesspackedtexture_[03]"]
		alpha_pass = alpha.outputs[0]
	if alpha:
		# transparency
		b_mat.blend_method = "CLIP"
		b_mat.shadow_method = "CLIP"
		# attr_dict = {attrib.name.lower(): attrib for attrib in fgm_data.attributes.data}
		for attr, attr_data in zip(fgm_data.attributes.data, fgm_data.data_lib.data):
			if "palphatestref" in attr.name.lower():
				b_mat.alpha_threshold = attr_data.value[0]
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
		# additionally keep track here so we create a node tree only once during import
		# but make sure that we overwrite existing materials:
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

