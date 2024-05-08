import inspect
import logging
import sys

import bpy
import os

from ovl_util.shared import check_any
from plugin.utils.texture_settings import tex_slots
from root_path import root_dir
from constants import ConstantsProvider
from generated.formats.fgm.compounds.FgmHeader import FgmHeader
from generated.formats.fgm.enums.FgmDtype import FgmDtype
from generated.formats.ovl_base import OvlContext
from plugin.utils.node_arrange import nodes_iterate
from plugin.utils.node_util import get_tree, load_tex_node
from plugin.utils import texture_settings


def append_shader(name):
	if name not in bpy.data.node_groups:
		logging.info(f"Appending shader group '{name}'")
		blends_dir = os.path.join(root_dir, "plugin", "blends")
		for file_name in os.listdir(blends_dir):
			if not file_name.lower().endswith(".blend"):
				continue
			filepath = os.path.join(blends_dir, file_name)
			with bpy.data.libraries.load(filepath) as (data_from, data_to):
				if name in data_from.node_groups and name not in data_to.node_groups:
					data_to.node_groups = [name]


def get_group_node(tree, name):
	append_shader(name)
	group_node = tree.nodes.new("ShaderNodeGroup")
	group_node.node_tree = bpy.data.node_groups[name]
	group_node.name = name
	return group_node


class BaseShader:
	"""Basic class for all derived shaders to inherit from"""

	uv_map = {
		"pFeathers_AOHeightOpacityTransmission_PackedTexture": 1,
		"pFeathers_Aniso_PackedTexture": 1,
		"pFeathers_NormalTexture": 1,
		"pFeathers_BaseColourTexture": 1,
		"pFeathers_RoughnessPackedTexture": 1,
	}

	inv_tex_slots = {v: k for k, v in tex_slots.items()}

	def add_flexi_nodes(self, tree):
		flexi_identifiers = [f"F{i}" for i in range(1, 5)]
		flexi_nodes = [self.id_2_out_socket.get(f) for f in flexi_identifiers]
		if any(flexi_nodes):
			self.add_shader(tree, "FlexiDiffuse")

	def add_shader(self, tree, node_name):
		logging.info(f"Adding shader for '{node_name}'")
		shader_node = get_group_node(tree, node_name)
		self.connect_inputs(shader_node, tree)
		self.connect_outputs(shader_node, tree)

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

	def connect_inputs(self, shader_node, tree):
		"""Connects output sockets of other nodes to the inputs of shader_node"""
		for socket in shader_node.inputs:
			if socket.name in tex_slots:
				long_name = tex_slots[socket.name]
			else:
				long_name = socket.name
			# determine type of input from name
			if long_name.startswith("p"):
				# get shader param
				val = self.attr.get(long_name)
				if val is not None:
					try:
						# todo maybe check https://docs.blender.org/api/current/bpy.types.NodeSocket.html#bpy.types.NodeSocket
						if len(val) != len(socket.default_value):
							logging.warning(f"Mismatch of socket size '{long_name}'")
							continue
					except TypeError:
						logging.warning(f"has no len '{long_name}'")
					socket.default_value = val
			else:
				# it's probably a texture node
				try:
					identifier = self.inv_tex_slots[long_name]
				except KeyError:
					logging.warning(f"Found no identifier for '{long_name}'")
					continue
				out_socket = self.id_2_out_socket.get(identifier)
				if out_socket:
					node = out_socket.node
					# set the colorspace for image inputs if needed
					if isinstance(node, bpy.types.ShaderNodeTexImage):
						# todo determine colorspace properly
						# assume non-color colorspace for non-color inputs
						if not isinstance(socket, bpy.types.NodeSocketColor):
							node.image.colorspace_settings.name = "Non-Color"
						# connect UV inputs using two different methods
						# assume layer 0 if nothing is specified, and blender implies that by default, so only import other layers
						text_name = node.parent.label
						uv_i = self.uv_map.get(text_name, 0)
						if uv_i > 0:
							if uv_i not in self.uv_dic:
								uv_node = tree.nodes.new('ShaderNodeUVMap')
								uv_node.uv_map = f"UV{uv_i}"
								self.uv_dic[uv_i] = uv_node
							else:
								uv_node = self.uv_dic[uv_i]
							tree.links.new(uv_node.outputs[0], node.inputs[0])
						# connect transformed UV coord node input according to channel ID
						if "_" in identifier:
							base_id = identifier.split("_")[0]
							uv_id = f"{base_id} UV"
							uv_socket = self.id_2_out_socket.get(uv_id)
							if uv_socket:
								tree.links.new(uv_socket, node.inputs[0])
					tree.links.new(out_socket, socket)

	def connect_outputs(self, shader_node, tree):
		"""Stores outputs of shader_node in id_2_out_socket to later connect them to the inputs sockets of other nodes"""
		for socket in shader_node.outputs:
			if " UV" in socket.name:
				self.id_2_out_socket[socket.name] = socket
			if socket.name in tex_slots:
				long_name = tex_slots[socket.name]
			else:
				long_name = socket.name
			try:
				identifier = self.inv_tex_slots[long_name]
			except KeyError:
				logging.warning(f"Found no identifier for '{long_name}'")
				continue
			self.id_2_out_socket[identifier] = socket

	def build_attr_dict(self, fgm_data):
		self.attr = {}
		for attr, attr_data in zip(fgm_data.attributes.data, fgm_data.value_foreach_attributes.data):
			if len(attr_data.value) == 1:
				self.attr[attr.name] = attr_data.value[0]
			else:
				self.attr[attr.name] = attr_data.value

	def build_tex_nodes_dict(self, tex_channel_map, fgm_data, in_dir, tree):
		"""Load all png files that match tex files referred to by the fgm"""
		all_textures = [file for file in os.listdir(in_dir) if file.lower().endswith(".png")]
		self.id_2_out_socket = {}
		self.uv_dic = {}
		tex_check = set()
		for texture_data, dep_info in zip(fgm_data.textures.data, fgm_data.name_foreach_textures.data):
			text_name = texture_data.name
			# ignore texture types that we have no use for
			if check_any(("blendweights", "warpoffset", "pshellmap", "piebald", "markingnoise", "pscarlut", "playered", "ppatterning"), text_name):
				continue
			tex_channels = tex_channel_map.get(texture_data.name, {})
			if texture_data.dtype == FgmDtype.RGBA:
				color = tree.nodes.new('ShaderNodeRGB')
				color.label = text_name
				color.outputs[0].default_value = (
					texture_data.value[0].r / 255,
					texture_data.value[0].g / 255,
					texture_data.value[0].b / 255,
					texture_data.value[0].a / 255
				)
				for channel, purpose in tex_channels.items():
					self.id_2_out_socket[purpose] = color.outputs[0]
			else:
				tex_name = dep_info.dependency_name.data
				if not tex_name:
					raise AttributeError(f"Texture name is not set for {text_name}")
				png_base, ext = os.path.splitext(tex_name.lower())
				# some fgms, such as PZ red fox whiskers, reuse the same tex file in different slots, so don't add new nodes
				if png_base in tex_check:
					continue
				tex_check.add(png_base)

				def is_part_of_tex(file):
					"""Make sure to catch only bare or channel-split png and avoid catching different tex files that happen
					to start with the same id such as pdiffuse and pdiffusemelanistic"""
					return file.lower().startswith(f"{png_base}.") or file.lower().startswith(f"{png_base}_")
				tex_nodes = []
				for png_name in all_textures:
					if not is_part_of_tex(png_name):
						continue
					png_path = os.path.join(in_dir, png_name)
					b_tex = load_tex_node(tree, png_path)
					b_tex.hide = True  # make it small for a quick overview, as we set the short purpose labels
					tex_nodes.append(b_tex)

					base, tex_type_with_channel_suffix = png_name.lower().split(".")[:2]
					# get channel mapping
					for channel, purpose in tex_channels.items():
						# also supports pNormalMapTextureUnique -> rocks_ice_shared_01.pbasenormaltexture_RG.png
						if channel and not tex_type_with_channel_suffix.endswith(f"_{channel.lower()}"):
							continue
						b_tex.label = purpose
					self.id_2_out_socket[b_tex.label] = b_tex.outputs[0]
				if tex_nodes:
					# Until better option to organize the shader info, create frame for all channels of this texture
					tex_frame = tree.nodes.new('NodeFrame')
					tex_frame.label = text_name
					for b_tex in tex_nodes:
						b_tex.parent = tex_frame  # assign the texture frame to this png


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
				logging.info(f"Checking: {library} for {matname}")
				load_material_from_asset_library(created_materials, library, matname)


def get_color_ramp(fgm, prefix, suffix):
	for attrib, attrib_data in zip(fgm.attributes.data, fgm.value_foreach_attributes.data):
		if prefix in attrib.name and attrib.name.endswith(suffix):
			yield attrib_data.value


def create_material(in_dir, matname):
	logging.info(f"Importing material {matname}")
	b_mat = bpy.data.materials.new(matname)

	fgm_path = os.path.join(in_dir, f"{matname}.fgm")
	try:
		fgm_data = FgmHeader.from_xml_file(fgm_path, OvlContext())
	except FileNotFoundError:
		logging.warning(f"{fgm_path} does not exist!")
		return b_mat
	except:
		logging.warning(f"{fgm_path} could not be loaded!")
		return b_mat

	constants = ConstantsProvider(("shaders", "textures", "texchannels"))
	tree = get_tree(b_mat)
	output = tree.nodes.new('ShaderNodeOutputMaterial')

	create_color_ramps(fgm_data, tree)
	try:
		# todo clean up game version
		game = "Jurassic World Evolution 2" if "jura" in fgm_data.game.lower() else "Planet Zoo"
		# print(game)
		tex_channel_map = texture_settings.get_tex_channel_map(constants, game, fgm_data.shader_name)
		# print(tex_channel_map)
		try:
			b_mat.fgm.shader_name = fgm_data.shader_name
		except:
			logging.warning(f"Shader '{fgm_data.shader_name}' does not exist in shader list")
		shader = BaseShader()
		shader.build_tex_nodes_dict(tex_channel_map, fgm_data, in_dir, tree)
		shader.build_attr_dict(fgm_data)
		if fgm_data.shader_name.startswith(("Animal_", "Fur")):
			shader.add_shader(tree, "AnimalVariation")
		if "Detail_Basic" in fgm_data.shader_name:
			shader.add_shader(tree, "Detail_BasicMapping")
			shader.add_shader(tree, "Detail_BasicBlend")
		elif "Detail" in fgm_data.shader_name:
			shader.add_shader(tree, "DetailMapping")
			shader.add_shader(tree, "DetailBlend")
		# todo use shader name check for flexi and add_shader api
		shader.add_flexi_nodes(tree)
		# diffuse = shader.add_marking_nodes(diffuse, tree)
		# main shader
		shader_node = get_group_node(tree, "MainShader")
		shader.connect_inputs(shader_node, tree)
		tree.links.new(shader_node.outputs[0], output.inputs[0])

		alpha_test = shader.attr.get("pAlphaTestRef")
		if alpha_test is not None:
			b_mat.blend_method = "CLIP"
			b_mat.shadow_method = "CLIP"
			# blender appears to be stricter with the alpha clipping
			# PZ ele has it set to 1.0 in fgm, which makes it invisible in blender
			b_mat.alpha_threshold = alpha_test * 0.5
		nodes_iterate(tree, output)
	except:
		logging.exception(f"Importing material {matname} failed")
	return b_mat


def create_color_ramps(fgm_data, tree):
	# get gradients for JWE2 patterns
	for k, v in (
			("colourKey", "RGB"),
			("emissiveKey", "RGB"),
			("opacityKey", "Value")):
		values = list(get_color_ramp(fgm_data, k, v))
		positions = list(get_color_ramp(fgm_data, k, "Position"))
		values, positions = presort_keys(values, positions)
		if values and positions:
			ramp = tree.nodes.new('ShaderNodeValToRGB')
			ramp.label = k
			# alpha is forced to have a final key of 0.0 opacity
			# color and emission hold their last key instead
			if k == "opacityKey":
				values.append((0.0,))
				positions.append(32)
			# remove the second elem - can't have less than 1
			ramp.color_ramp.elements.remove(ramp.color_ramp.elements[-1])
			# add required amount of elements
			for n in range(len(values) - 1):
				ramp.color_ramp.elements.new(n / len(values))
			# set proper position and color
			for position, value, elem in zip(positions, values, ramp.color_ramp.elements):
				elem.position = position / 32
				if len(value) != 3:
					value = (value[0], value[0], value[0])
				elem.color[:3] = value
				elem.alpha = 1.0


def presort_keys(colors, colors_pos):
	pos_col = list(zip(colors_pos, colors))
	pos_col = [(p[0], tuple(c)) for p, c in pos_col if p[0] > -1]
	# some have just -1 pos throughout
	if pos_col:
		colors_pos, colors = zip(*sorted(pos_col))
		return list(colors), list(colors_pos)
	else:
		return (), ()


def import_material(created_materials, in_dir, b_me, material):
	material_name = material.name
	try:
		# find if material is in blender already. Imported FGMs
		# will have the material name all in lowercase, we need
		# to check both.
		b_mat = bpy.data.materials.get(material_name)
		if not b_mat:
			# try finding the material first in the user libraries, only use lowercase
			load_material_from_libraries(created_materials, material_name)

			b_mat = bpy.data.materials.get(material_name)

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
