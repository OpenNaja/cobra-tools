import inspect
import logging
import sys

import bpy
import os

import numpy as np

from generated.formats.fgm.compounds.FgmHeader import FgmHeader
from generated.formats.fgm.enums.FgmDtype import FgmDtype
from generated.formats.ovl_base import OvlContext
from plugin.utils.node_arrange import nodes_iterate
from plugin.utils.node_util import get_tree, load_tex_node

# maps cobra texture name to blender name
dest_map = {
	"basecolour": "Base Color",
	"normal": "Normal",
	"roughnesspacked": "Roughness"}


def check_any(iterable, string):
	"""Returns true if any of the entries of the iterable occur in string"""
	return any([i in string for i in iterable])


class BaseShader:
	"""Basic class for all derived shaders to inherit from"""

	# for validation
	shaders = ()
	games = ()

	uv_map = {}

	# for texture channel mapping
	diffuse_slots = (
		"pdiffusetexture", "pbasediffusetexture", "pbasecolourtexture", "pbasecolourtexture_rgb",
		"pbasecolourandmasktexture_rgb", "pdiffusealphatexture", "pdiffuse_alphatexture",
		"palbinobasecolourandmasktexture_rgb",)

	detail_slots = ()

	ao_slots = (
		"paotexture", "pbasepackedtexture_a", "pbaseaotexture_r", "pbaseaotexture",
		"proughnessaopackedtexturedetailbase_r")

	normal_slots = (
	"pnormaltexture", "pnormaltexture_rg", "pnormaltexture_rgb", "pbasenormaltexture_rg", "pbasenormaltexture_rgb",)

	specular_slots = ("proughnesspackedtexture_b", "pspecularmaptexture_r", "pbasenormaltexture_b")

	roughness_slots = (
	"proughnesspackedtexture_g", "pnormaltexture_a", "pbasenormaltexture_a")  # "pspecularmaptexture_g"

	# note that JWE uses proughnesspackedtexture_r as alpha, only pbasepackedtexture_b as metal!
	metallic_slots = ("proughnesspackedtexture_r", "pbasepackedtexture_b")

	emissive_slots = ("pemissivetexture",)

	alpha_slots = ("popacitytexture", "pdiffusealphatexture_a", "pdiffuse_alphatexture_a", "proughnesspackedtexture_a")

	def get_tex(self, names):
		for tex_name in names:
			# get diffuse
			if tex_name in self.tex_dic:
				yield self.tex_dic[tex_name]
				# stop after finding a suitable one
				break

	def add_marking_nodes(self, diffuse, tree):
		# get marking
		fur_names = [k for k in self.tex_dic.keys() if "marking" in k and "noise" not in k and "patchwork" not in k]
		lut_names = [k for k in self.tex_dic.keys() if "pclut" in k]
		if fur_names and lut_names:
			marking = self.tex_dic[sorted(fur_names)[0]]
			lut = self.tex_dic[sorted(lut_names)[0]]
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
		return diffuse

	def build_tex_nodes_dict(self, fgm_data, in_dir, tree, principled):
		"""Load all png files that match tex files referred to by the fgm"""
		all_textures = [file for file in os.listdir(in_dir) if file.lower().endswith(".png")]
		self.tex_dic = {}
		self.uv_dic = {}
		tex_check = set()
		for text_data, dep_info in zip(fgm_data.textures.data, fgm_data.name_foreach_textures.data):
			text_name = text_data.name.lower()
			if text_data.dtype == FgmDtype.RGBA:
				# todo - flexicolourmasks - create color and blending nodes?
				for c_name, b_name in dest_map.items():
					if c_name in text_name:
						color = tree.nodes.new('ShaderNodeRGB')
						color.label = text_name
						color.outputs[0].default_value = (
							text_data.value[0].r / 255,
							text_data.value[0].g / 255,
							text_data.value[0].b / 255,
							text_data.value[0].a / 255
						)
						tree.links.new(color.outputs[0], principled.inputs[b_name])
						break
			else:
				tex_name = dep_info.dependency_name.data
				if not tex_name:
					raise AttributeError(f"Texture name is not set for {text_name}")
				png_base, ext = os.path.splitext(tex_name.lower())
				# ignore texture types that we have no use for
				if check_any(("blendweights", "warpoffset", "pshellmap", "piebald", "markingnoise", "pscarlut"), png_base):
					continue

				def check_dupe(file):
					"""Make sure to catch only bare or channel-split png and avoid catching different tex files that happen
					to start with the same id such as pdiffuse and pdiffusemelanistic"""
					return file.lower().startswith(f"{png_base}.") or file.lower().startswith(f"{png_base}_")

				textures = [file for file in all_textures if check_dupe(file)]

				# some fgms, such as PZ red fox whiskers, reuse the same tex file in different slots, so don't add new nodes
				if png_base not in tex_check:
					# assume layer 0 if nothing is specified
					uv_i = self.uv_map.get(text_name, 0)
					if uv_i not in self.uv_dic:
						uv_node = tree.nodes.new('ShaderNodeUVMap')
						uv_node.uv_map = f"UV{uv_i}"
						self.uv_dic[uv_i] = uv_node
					else:
						uv_node = self.uv_dic[uv_i]
					tex_check.add(png_base)
					# Until better option to organize the shader info, create texture group node
					tex_frame = tree.nodes.new('NodeFrame')
					tex_frame.label = png_base

					for png_name in textures:
						png_path = os.path.join(in_dir, png_name)
						b_tex = load_tex_node(tree, png_path)
						b_tex.parent = tex_frame  # assign the texture frame to this png
						k = png_name.lower().split(".")[1]
						self.tex_dic[k] = b_tex
						tree.links.new(uv_node.outputs[0], b_tex.inputs[0])

	@classmethod
	def validate(cls, fgm_data):
		"""Returns true if this shader class is suitable to process fgm_data"""
		# check for matching shaders
		if cls.shaders:
			shader_match = check_any(cls.shaders, fgm_data.shader_name)
			if shader_match:
				# check if a game has been specified
				if cls.games:
					return check_any(cls.games, fgm_data.game)
				else:
					return True


class JWE2FoliageClip(BaseShader):
	games = ("JURASSIC",)
	shaders = ("Foliage_Clip",)

	ao_slots = ("pnormaltexture_a",)

	metallic_slots = ("proughnesspackedtexture_a",)

	alpha_slots = ("proughnesspackedtexture_r",)


class PZFoliageClip(BaseShader):
	# I don't remember what's different here?!
	pass


class Metallic_Roughness_Clip(BaseShader):
	shaders = ("Metallic_Roughness_Clip_Weather", "Metallic_Roughness_Clip_Weather_BC7",
			   "Metallic_Roughness_Clip_Weather_DoubleSided_BC7")

	alpha_slots = ("pbasecolourtexture_a",)


class Metallic_Roughness_Clip_Geometry_Decal(BaseShader):
	shaders = ("Metallic_Roughness_Clip_Geometry_Decal",)

	alpha_slots = ("proughnesspackedtexture_a",)


class JWE2Feathers(BaseShader):
	shaders = ("DinosaurFeathers_ClipDoubleSided",)

	uv_map = {
		"pfeathers_aoheightopacitytransmission_packedtexture": 1,
		"pfeathers_basecolourtexture": 1,
		"pfeathers_roughnesspackedtexture": 1,
	}

	diffuse_slots = ("pdinosaurfeathers_basediffusetexture",)

	detail_slots = ("pfeathers_basecolourtexture",)

	ao_slots = ("pfeathers_aoheightopacitytransmission_packedtexture_r",)

	alpha_slots = ("pfeathers_aoheightopacitytransmission_packedtexture_b",)

	normal_slots = ("pfeathers_normaltexture_rg",)

	specular_slots = ("pfeathers_roughnesspackedtexture_b",)

	roughness_slots = ("pfeathers_roughnesspackedtexture_g",)

	metallic_slots = ("pfeathers_roughnesspackedtexture_r",)


def pick_shader(fgm_data):
	"""Selects a suitable subclass of BaseShader to create a node tree"""
	for name, cls in inspect.getmembers(sys.modules[__name__], inspect.isclass):
		if cls.__module__ is __name__:
			if issubclass(cls, BaseShader):
				# print(name)
				if cls.validate(fgm_data):
					logging.debug(f"Picked shader {name} for {fgm_data.shader_name}")
					return cls()
	logging.debug(f"Used BaseShader for {fgm_data.shader_name}")
	return BaseShader()


def load_material_from_asset_library(created_materials, filepath, matname):
	"""try to load the material from the list of asset libraries"""
	library_path = os.path.abspath(filepath)  # blend file name
	inner_path = 'Material'  # type
	material_name = matname  # name

	# try current material case
	bpy.ops.wm.append(
		filepath=os.path.join(library_path, inner_path, material_name),
		directory=os.path.join(library_path, inner_path),
		filename=material_name
	)
	# also try all lowercase
	# if material_name != material_name.lower():
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
		library_name = asset_library.name
		library_path = asset_library.path
		logging.info(f"Checking: {library_name}")
		library_files = [os.path.join(dp, f) for dp, dn, filenames in os.walk(library_path) for f in filenames if
						 os.path.splitext(f)[1] == '.blend']
		for library in library_files:
			# avoid reloading the same material in case it is present in several blend files
			if matname not in created_materials:
				load_material_from_asset_library(created_materials, library, matname)


def get_color_ramp(fgm, prefix, suffix):
	for attrib, attrib_data in zip(fgm.attributes.data, fgm.value_foreach_attributes.data):
		if prefix in attrib.name and attrib.name.endswith(suffix):
			yield attrib_data.value


def flat_pos(in_pos):
	for i in in_pos:
		key_pos = int(i)
		if key_pos > -1:
			yield key_pos
		else:
			yield 32


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
	tree = get_tree(b_mat)
	output = tree.nodes.new('ShaderNodeOutputMaterial')
	principled = tree.nodes.new('ShaderNodeBsdfPrincipled')

	# get gradients for JWE2 patterns
	for k, v in (
			("colourKey", "RGB"),
			("emissiveKey", "RGB"),
			("opacityKey", "Value")):
		values = list(get_color_ramp(fgm_data, k, v))
		positions = list(get_color_ramp(fgm_data, k, "Position"))
		if values and positions:
			values, positions = presort_keys(values, positions)
			ramp = tree.nodes.new('ShaderNodeValToRGB')
			ramp.label = k
			# remove the second elem - can't have less than 1
			ramp.color_ramp.elements.remove(ramp.color_ramp.elements[-1])
			# add required amount of elements
			for n in range(len(values)-1):
				ramp.color_ramp.elements.new(n / len(values))
			# set proper position and color
			for position, value, elem in zip(positions, values, ramp.color_ramp.elements):
				elem.position = position / 32
				if len(value) != 3:
					value = (value[0], value[0], value[0])
				elem.color[:3] = value
				elem.alpha = 1.0
	try:
		b_mat["shader_name"] = fgm_data.shader_name
		shader = pick_shader(fgm_data)
		shader.build_tex_nodes_dict(fgm_data, in_dir, tree, principled)

		# get diffuse
		for diffuse in shader.get_tex(shader.diffuse_slots):
			# apply AO to diffuse
			for ao in shader.get_tex(shader.ao_slots):
				ao.image.colorspace_settings.name = "Non-Color"
				diffuse_premix = tree.nodes.new('ShaderNodeMixRGB')
				diffuse_premix.blend_type = "MULTIPLY"
				diffuse_premix.inputs["Fac"].default_value = 1.0
				tree.links.new(diffuse.outputs[0], diffuse_premix.inputs["Color1"])
				tree.links.new(ao.outputs[0], diffuse_premix.inputs["Color2"])
				diffuse = diffuse_premix
			# apply detail to diffuse
			for detail in shader.get_tex(shader.detail_slots):
				detail.image.colorspace_settings.name = "Non-Color"
				diffuse_premix = tree.nodes.new('ShaderNodeMixRGB')
				diffuse_premix.blend_type = "OVERLAY"
				diffuse_premix.inputs["Fac"].default_value = 1.0
				tree.links.new(diffuse.outputs[0], diffuse_premix.inputs["Color1"])
				tree.links.new(detail.outputs[0], diffuse_premix.inputs["Color2"])
				diffuse = diffuse_premix

			diffuse = shader.add_marking_nodes(diffuse, tree)
			#  link finished diffuse to shader
			tree.links.new(diffuse.outputs[0], principled.inputs["Base Color"])

		for normal in shader.get_tex(shader.normal_slots):
			normal.image.colorspace_settings.name = "Non-Color"
			normal_map = tree.nodes.new('ShaderNodeNormalMap')
			normal_map.inputs[0].default_value = 0.4  # nah, it really doesn't
			tree.links.new(normal.outputs[0], normal_map.inputs[1])
			tree.links.new(normal_map.outputs[0], principled.inputs["Normal"])

		# PZ - F0 value for dielectrics, related to IOR / fake specularity
		# https://forum.sketchfab.com/t/what-is-specular-fo/22752/7
		for specular in shader.get_tex(shader.specular_slots):
			specular.image.colorspace_settings.name = "Non-Color"
			tree.links.new(specular.outputs[0], principled.inputs["Specular"])

		# roughness
		for roughness in shader.get_tex(shader.roughness_slots):
			roughness.image.colorspace_settings.name = "Non-Color"
			tree.links.new(roughness.outputs[0], principled.inputs["Roughness"])

		# JWE dinos, PZ - metallic
		for metallic in shader.get_tex(shader.metallic_slots):
			metallic.image.colorspace_settings.name = "Non-Color"
			tree.links.new(metallic.outputs[0], principled.inputs["Metallic"])

		for emissive in shader.get_tex(shader.emissive_slots):
			tree.links.new(emissive.outputs[0], principled.inputs["Emission"])

		for alpha in shader.get_tex(shader.alpha_slots):
			alpha_pass = alpha.outputs[0]
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
			break
		# no alpha
		else:
			b_mat.blend_method = "OPAQUE"
			tree.links.new(principled.outputs[0], output.inputs[0])

		nodes_iterate(tree, output)
	except:
		logging.exception(f"Importing material {matname} failed")
	return b_mat


def presort_keys(colors, colors_pos):
	"""np.interp expects sorted keys"""
	# colors = [tuple(t) for t in colors]
	# colors_pos = list(flat_pos(colors_pos))
	pos_col = list(zip(colors_pos, colors))
	pos_col = [(p[0], tuple(c)) for p, c in pos_col if p[0] > -1]
	colors_pos, colors = zip(*sorted(pos_col))
	return list(colors), list(colors_pos)


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
		if not b_mat:
			# additionally keep track in created_materials so we create a node tree only once during import
			# but make sure that we overwrite existing materials.
			# TODO: this might be redundant since we are checking now materials exist in the previous code block.
			if material_name not in created_materials:
				b_mat = create_material(in_dir, material_name)
				created_materials[material_name] = b_mat
			else:
				logging.info(f"Already imported material {material_name}")
				b_mat = created_materials[material_name]
		# store material data
		b_mat["blend_mode"] = material.blend_mode
		b_me.materials.append(b_mat)
	except:
		logging.exception(f"Material {material_name} failed")
