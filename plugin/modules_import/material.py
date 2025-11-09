import contextlib
import logging
import os

import bpy
import numpy as np

from constants import ConstantsProvider
from generated.formats.fgm.structs.FgmHeader import FgmHeader
from generated.formats.fgm.enums.FgmDtype import FgmDtype
from generated.formats.ovl import get_game
from modules.formats.FGM import FgmContext
from modules.formats.shared import check_any
from plugin.utils import texture_settings
from plugin.utils.node_arrange import nodes_iterate
from plugin.utils.node_util import get_tree, load_tex_node
from plugin.utils.texture_settings import tex_slots


def append_shader(name):
	if name not in bpy.data.node_groups:
		logging.info(f"Appending shader group '{name}'")
		current_dir = os.path.dirname(__file__)
		blends_dir = os.path.abspath(os.path.join(current_dir, '..', 'blends'))
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
	group_node.label = name
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
	attr_tex_map = {
		"pDiffuseTint": "BC",
		"pDielectricReflectivity": "SP",
		"pSpecular": "SP",
		"pRoughness": "RN",
		"pMetalness": "MT",
		"pSpecularReflectance": "SP",
		"pOpacity": "OP"
	}
	inv_tex_slots = {v: k for k, v in tex_slots.items()}

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
					if socket.type in ("VALUE", "INT", "FLOAT", "BOOLEAN"):
						socket.default_value = val[0]
					else:
						if len(val) <= len(socket.default_value):
							socket.default_value[:len(val)] = val
						elif len(val) != len(socket.default_value):
							logging.warning(f"Socket too small for '{long_name}' ({len(val)} vs {len(socket.default_value)})")
							continue
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
			self.attr[attr.name] = attr_data.value

	@staticmethod
	@contextlib.contextmanager
	def put_in_frame(text_name, tree):
		nodes = []
		yield nodes
		if nodes:
			# Until better option to organize the shader info, create frame for all channels of this texture
			frame = tree.nodes.new('NodeFrame')
			frame.label = text_name
			frame.label_size = 14
			for node in nodes:
				node.hide = True  # make it small for a quick overview, as we set the short purpose labels
				node.parent = frame  # assign the texture frame to this png

	def build_tex_nodes_dict(self, tex_channel_map, fgm_data, in_dir, tree):
		"""Load all png files that match tex files referred to by the fgm"""
		all_textures = [file for file in os.listdir(in_dir) if file.lower().endswith(".png")]
		self.id_2_out_socket = {}
		self.uv_dic = {}
		tex_check = set()
		for texture_data, dep_info in zip(fgm_data.textures.data, fgm_data.name_foreach_textures.data):
			text_name = texture_data.name
			# ignore texture types that we have no use for
			if check_any(("blendweights", "warpoffset", "pshellmap", "piebald", "markingnoise", "pscarlut", "playered", "ppatterning"), text_name.lower()):
				continue

			with self.put_in_frame(text_name, tree) as tex_nodes:
				tex_channels = tex_channel_map.get(texture_data.name, {})
				if texture_data.dtype == FgmDtype.RGBA:
					# only take the first RGBA slot of the two
					v = texture_data.value[0]
					rgba = {"R": v.r/255, "G": v.g/255, "B": v.b/255, "A": v.a/255}
					for channel, purpose in tex_channels.items():
						color = tree.nodes.new('ShaderNodeRGB')
						color.label = purpose
						tex_nodes.append(color)
						if not channel:
							channel = "RGBA"
						color.outputs[0].default_value = self.map_color_channel(channel, rgba)
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

					for png_name in all_textures:
						if not is_part_of_tex(png_name):
							continue
						png_path = os.path.join(in_dir, png_name)
						b_tex = load_tex_node(tree, png_path)
						tex_nodes.append(b_tex)

						base, tex_type_with_channel_suffix = png_name.lower().split(".")[:2]
						# get channel mapping
						for channel, purpose in tex_channels.items():
							# also supports pNormalMapTextureUnique -> rocks_ice_shared_01.pbasenormaltexture_RG.png
							if channel and not tex_type_with_channel_suffix.endswith(f"_{channel.lower()}"):
								continue
							b_tex.label = purpose
						self.id_2_out_socket[b_tex.label] = b_tex.outputs[0]

		# create attributes that act as texture channels
		with self.put_in_frame("Attributes", tree) as tex_nodes:
			for attr_name, attr_data in self.attr.items():
				attr_data = self.attr.get(attr_name)
				purpose = self.attr_tex_map.get(attr_name, None)
				if purpose:
					color = tree.nodes.new('ShaderNodeRGB')
					color.label = purpose
					tex_nodes.append(color)
					# bring ints to 0-1f range
					if isinstance(attr_data[0], (int, np.intc)):
						# might as well be percent, idk
						attr_data = [x/255 for x in attr_data]
					# complete the key as RGBA color
					color.outputs[0].default_value = self.map_color_channel(list(range(len(attr_data))), attr_data)
					self.id_2_out_socket[purpose] = color.outputs[0]

	def map_color_channel(self, channel, rgba):
		if len(channel) == 4:
			return [rgba[c] for c in channel]
		elif len(channel) == 3:
			return [rgba[c] for c in channel] + [1.0, ]
		elif len(channel) == 2:
			return [rgba[c] for c in channel] + [1.0, 1.0]
		elif len(channel) == 1:
			return [rgba[channel[0]] for _ in range(3)] + [1.0, ]
			

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


def create_material(reporter, in_dir, matname):
	matname = matname.lower()

	logging.info(f"Importing material {matname}")
	b_mat = bpy.data.materials.new(matname)
	fgm_path = os.path.join(in_dir, f"{matname}.fgm")
	try:
		fgm_data = FgmHeader.from_xml_file(fgm_path, FgmContext())
	except FileNotFoundError:
		logging.warning(f"{fgm_path} does not exist!")
		return b_mat
	except:
		logging.exception(f"{fgm_path} could not be loaded!")
		return b_mat

	constants = ConstantsProvider(("shaders", "textures", "texchannels"))
	tree = get_tree(b_mat)
	output = tree.nodes.new('ShaderNodeOutputMaterial')

	create_color_ramps(fgm_data, tree)
	fgm_game = get_game(fgm_data.context)[0].value
	game = bpy.context.scene.cobra.game
	if game != fgm_game:
		reporter.show_warning(f"FGM game '{fgm_game}' does not match scene game {game}")
	try:
		tex_channel_map = texture_settings.get_tex_channel_map(constants, game, fgm_data.shader_name)
		# print(tex_channel_map)
		try:
			b_mat.fgm.shader_name = fgm_data.shader_name
		except:
			logging.warning(f"Shader '{fgm_data.shader_name}' does not exist in shader list")
		shader = BaseShader()
		shader.build_attr_dict(fgm_data)
		shader.build_tex_nodes_dict(tex_channel_map, fgm_data, in_dir, tree)
		if fgm_data.shader_name.startswith(("Animal_", "Fur")):
			shader.add_shader(tree, "AnimalVariation")
			# shader.add_marking_nodes(diffuse, tree)
		if "Detail_Basic" in fgm_data.shader_name:
			shader.add_shader(tree, "Detail_BasicMapping")
			shader.add_shader(tree, "Detail_BasicBlend")
		elif "Detail" in fgm_data.shader_name:
			shader.add_shader(tree, "DetailMapping")
			shader.add_shader(tree, "DetailBlend")
		if check_any(("pFlexiColourBlended", "pCitadelPainter_Enable"), shader.attr):
			shader.add_shader(tree, "FlexiDiffuse")

		# main shader
		shader_node = get_group_node(tree, "MainShader")
		shader.connect_inputs(shader_node, tree)
		tree.links.new(shader_node.outputs[0], output.inputs[0])

		# Transparency
		blend_shaders = (
			"Glass_",
		)
		alpha_blending = check_any(blend_shaders, b_mat.fgm.shader_name)
		# Note: Only explicitly single sided shaders here, not general ones like Clip
		single_sided_shaders = ("OneSided", "SingleSided")
		double_sided_shaders = (
			"TwoSided",
			"DoubleSided",
			"Foliage",
			"FurBaseAlpha",  # FurBaseAlpha_SingleSided will be correctly handled below
		)
		single_sided = check_any(single_sided_shaders, b_mat.fgm.shader_name)
		double_sided = not single_sided and check_any(double_sided_shaders, b_mat.fgm.shader_name)
		alpha_test = shader.attr.get("pAlphaTestRef")
		if alpha_blending:
			b_mat.blend_method = "BLEND"
			if bpy.app.version < (4, 2, 0):
				b_mat.shadow_method = "NONE"
			# b_mat.show_transparent_back = double_sided  # Seems incorrect
			# Default to culling unless determined as double-sided
			b_mat.use_backface_culling = not double_sided
		elif alpha_test is not None:
			b_mat.blend_method = "CLIP"
			if bpy.app.version < (4, 2, 0):
				b_mat.shadow_method = "CLIP"
			# Default to culling unless determined as double-sided
			b_mat.use_backface_culling = not double_sided
			# blender appears to be stricter with the alpha clipping
			# PZ ele has it set to 1.0 in fgm, which makes it invisible in blender
			b_mat.alpha_threshold = alpha_test[0] * 0.5

		nodes_iterate(b_mat, tree, output)
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


def import_material(reporter, created_materials, in_dir, b_me, material):
	material_name = material.name.lower()
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
				b_mat = create_material(reporter, in_dir, material_name)
				created_materials[material_name] = b_mat
			else:
				logging.info(f"Already imported material {material_name}")
				b_mat = created_materials[material_name]

		# store material data
		b_mat["blend_mode"] = material.blend_mode
		b_me.materials.append(b_mat)
	except:
		logging.exception(f"Material {material_name} failed")
