import bpy
import math
import logging
import os

from modules.formats.FGM import FgmContext
from plugin.modules_import.material import get_group_node
from plugin.utils.node_arrange import nodes_iterate, get_input_nodes
from plugin.utils.node_util import load_tex_node, get_tree

from generated.formats.dinosaurmaterialvariants.structs.DinoLayersHeader import DinoLayersHeader
from generated.formats.matcol.structs.MatcolRoot import MatcolRoot
from generated.formats.fgm.structs.FgmHeader import FgmHeader


channels = ("R", "G", "B", "A")
MATLAY = ".dinosaurmateriallayers"
MATCOL = ".materialcollection"
	

class LayeredMaterial:

	def __init__(self):
		self.context = FgmContext()
		self.slots = []

	def create_node(self):
		pass

	def get_fgm(self, fgm_name_ptr, dtype=None, layer_i=0):
		fgm_basename = fgm_name_ptr.data
		if fgm_basename:
			fgm_path = os.path.join(self.base_dir, f"{fgm_basename}.fgm")
			if os.path.isfile(fgm_path):
				return FgmHeader.from_xml_file(fgm_path, self.context)
			else:
				logging.warning(f"{dtype} fgm for layer {layer_i} is missing")
		else:
			logging.debug(f"No {dtype} fgm for layer {layer_i}")

	def get_root(self, fp):
		if self.ext == MATLAY:
			layers_root = DinoLayersHeader.from_xml_file(fp, self.context)
			return layers_root.layers.data
		elif self.ext == MATCOL:
			matcol_root = MatcolRoot.from_xml_file(fp, self.context)
			return matcol_root.main.data.materials.data
		else:
			raise AttributeError(f"Selected wrong file type {self.ext}")
	
	def load_mat_layers(self, layers_path):
		self.base_dir, self.layers_name = os.path.split(layers_path)
		self.basename, self.ext = os.path.splitext(self.layers_name)
		self.matname = self.basename.split("_layers")[0]
		self.ext = self.ext.lower()
		logging.info(f"Material: {self.matname}")
		layers_root = self.get_root(layers_path)
		tile_i = 0
		ch_i = 0
		for layer_i, layer in enumerate(layers_root):
			mask_png_path = os.path.join(self.base_dir, f"{self.matname}.playered_blendweights_[{tile_i:02}]_{channels[ch_i]}.png")
			if not os.path.isfile(mask_png_path):
				logging.warning(f"Found no mask texture for layer {layer_i}")
			# increment channel index
			if self.ext == MATLAY:
				if layer.increment_channel:
					ch_i += 1
			else:
				# todo - check matcol for corresponding feature?
				ch_i += 1
			# move to the next tile for the next loop
			if ch_i == 4:
				ch_i = 0
				tile_i += 1
			if self.ext == MATLAY:
				tex_fgm = self.get_fgm(layer.texture_fgm_name)
				trans_fgm = self.get_fgm(layer.transform_fgm_name)
				if tex_fgm and trans_fgm:
					logging.info(f"Layer {layer_i} is tiled")
					logging.info(f"Found .fgm files for layer")
					height_tile_png_path = self.get_heightmap(layer_i, tex_fgm)
					lut = {}
					for attrib, attrib_data in zip(trans_fgm.attributes.data, trans_fgm.value_foreach_attributes.data):
						# skip first letter p
						lut[attrib.name.lower()[1:]] = attrib_data.value
				else:
					continue
			else:
				tex_fgm = self.get_fgm(layer.layer_name)
				if tex_fgm:
					height_tile_png_path = self.get_heightmap(layer_i, tex_fgm)
					lut = {}
					for attrib in layer.float_attributes.data:
						data = [v for b, v in zip(attrib.flags, attrib.value) if b]
						# as in fgm processing, flatten single element lists to scalars
						if len(data) == 1:
							data = data[0]
						# skip first 2 letters m_
						lut[attrib.attrib_name.data.lower()[2:]] = data
				else:
					continue
			self.slots.append((height_tile_png_path, mask_png_path, lut))

	def get_heightmap(self, layer_i, tex_fgm):
		height_tex = tex_fgm.textures.data[1]
		height_dep = tex_fgm.name_foreach_textures.data[1]
		height_file_name = height_dep.dependency_name.data
		height_file_basename = os.path.splitext(height_file_name)[0]
		array_index = height_tex.value[0].array_index
		height_tile_png_path = os.path.join(self.base_dir, f"{height_file_basename}_[{array_index:02}].png")
		if not os.path.isfile(height_tile_png_path):
			logging.error(f"Found no tile texture for layer {layer_i} {height_tile_png_path}")
		return height_tile_png_path


def get_att(node, lut, names):
	for name in names:
		n = name.lower()
		if n in lut:
			node.inputs[name].default_value = lut[n]


def load(reporter, filepath=""):
	layers = LayeredMaterial()
	layers.load_mat_layers(filepath)
	slots = layers.slots

	logging.info(f"MATERIAL: {layers.basename}")
	# only create the material if we haven't already created it, then just grab it
	if layers.basename not in bpy.data.materials:
		b_mat = bpy.data.materials.new(layers.basename)
	# only create the material if we haven't already created it, then just grab it
	else:
		b_mat = bpy.data.materials[layers.basename]

	tree = get_tree(b_mat)
	output = tree.nodes.new('ShaderNodeOutputMaterial')
	principled = tree.nodes.new('ShaderNodeBsdfPrincipled')

	# JWE style
	normal_path = os.path.join(layers.base_dir, f"{layers.matname}.pnormaltexture_RG.png")
	# JWE2 style
	if not os.path.isfile(normal_path):
		normal_path = os.path.join(layers.base_dir, f"{layers.matname}.pbasenormaltexture_RG.png")
	normal = load_tex_node(tree, normal_path)
	normal.image.colorspace_settings.name = "Non-Color"
	normal_map = tree.nodes.new('ShaderNodeNormalMap')
	tree.links.new(normal.outputs[0], normal_map.inputs[1])
	normal_map.inputs["Strength"].default_value = 1.0

	last_normal = normal_map
	nodes = []
	for i, (height_png, mask_png, lut) in enumerate(slots, start=1):
		logging.info(f"Slot {i:02d}")

		# load the tiled height_texture
		tile = load_tex_node(tree, height_png)
		tile.image.colorspace_settings.name = "Non-Color"
		tile.hide = True
		# load the blendweights layer mask
		mask = load_tex_node(tree, mask_png)
		mask.image.colorspace_settings.name = "Non-Color"
		mask.hide = True
		# Until better option to organize the shader info, create texture group node
		slot_frame = tree.nodes.new('NodeFrame')
		slot_frame.label = f"Slot {i:02d}"
		tile.parent = slot_frame
		mask.parent = slot_frame

		# height offset attribute
		if "heightblendscalea" in lut:
			# JWE2
			heightBlendScales = (lut["heightblendscalea"], lut["heightblendscaleb"])
		else:
			# JWE1
			heightBlendScales = lut["heightblendscale"][:2]
		heightBlendScaleA, heightBlendScaleB = sorted([i for i in heightBlendScales])
		if not heightBlendScaleA and not heightBlendScaleB:
			heightBlendScaleB = 1.0
		height = get_group_node(tree, "MatcolHeight")
		height.parent = slot_frame
		# todo triplanar projection / generated UV coords in tex coords input of matcol slot / box coords on tex node
		# lut["uvenableprojection"]
		height.inputs["heightScale"].default_value = lut["heightscale"]
		height.inputs["heightOffset"].default_value = lut["heightoffset"]
		height.inputs["heightBlendScaleA"].default_value = heightBlendScaleA
		height.inputs["heightBlendScaleB"].default_value = heightBlendScaleB
		tree.links.new(tile.outputs[0], height.inputs["Tile"])
		tree.links.new(mask.outputs[0], height.inputs["Mask"])
		tree.links.new(last_normal.outputs[0], height.inputs["Normal"])

		transform = get_group_node(tree, "MatcolSlot")
		transform.parent = slot_frame
		transform.inputs["uvRotationPosition"].default_value[:2] = lut["uvrotationposition"]
		transform.inputs["UVOffset"].default_value[:2] = lut["uvoffset"]
		transform.inputs["uvTile"].default_value[:2] = lut["uvtile"]
		# matcol stores uvRotationAngle as fraction of 180°
		# in radians for blender internally even though it displays as degree
		# flip since blender flips V coord
		try:
			# JWE2 is 2D
			transform.inputs["uvRotationAngle"].default_value = -math.radians(lut["uvrotationangle"][0] * 180)
		except:
			# JWE1 has it as 1D
			transform.inputs["uvRotationAngle"].default_value = -math.radians(lut["uvrotationangle"] * 180)
		tree.links.new(transform.outputs[0], tile.inputs[0])

		tile.update()
		mask.update()
		last_normal = height
		nodes.append((tile, mask, height, transform))
	if not nodes:
		raise AttributeError(f"Could not find any layer textures - make sure the tile .fgm and .png files are in the same folder!")

	diffuse_path = os.path.join(layers.base_dir, f"{layers.matname}.pbasediffusetexture.png")
	diffuse = load_tex_node(tree, diffuse_path)

	roughness_path = os.path.join(layers.base_dir, f"{layers.matname}.pbasepackedtexture_G.png")
	roughness = load_tex_node(tree, roughness_path)
	roughness.image.colorspace_settings.name = "Non-Color"

	ao_path = os.path.join(layers.base_dir, f"{layers.matname}.pbasepackedtexture_A.png")
	ao = load_tex_node(tree, ao_path)
	ao.image.colorspace_settings.name = "Non-Color"

	# apply AO to diffuse
	diffuse_premix = tree.nodes.new('ShaderNodeMixRGB')
	diffuse_premix.blend_type = "MULTIPLY"
	diffuse_premix.inputs["Fac"].default_value = .25
	tree.links.new(diffuse.outputs[0], diffuse_premix.inputs["Color1"])
	tree.links.new(ao.outputs[0], diffuse_premix.inputs["Color2"])

	tree.links.new(diffuse_premix.outputs[0], principled.inputs["Base Color"])
	tree.links.new(roughness.outputs[0], principled.inputs["Metallic"])
	tree.links.new(last_normal.outputs[0], principled.inputs["Normal"])
	tree.links.new(principled.outputs[0], output.inputs[0])

	nodes_iterate(b_mat, tree, output)
	slots_arrange(tree, nodes)

	# fill texture paint gui
	b_mat.matcol_layers.clear()
	for x in range(16):
		item = b_mat.matcol_layers.add()
		item.name = f"Layer {x}"
	# ensure that the texture has an image
	b_mat.matcol_layers_current = -1
	b_mat.matcol_layers_current = 0
	reporter.show_info(f"Imported {layers.basename}")


def slots_arrange(tree, nodes):
	if not nodes:
		return
	tile, mask, height, transform = nodes[0]
	tile_y = tile.location.y
	mask_y = mask.location.y
	height_y = height.location.y
	transform_y = transform.location.y
	shift = abs(nodes[0][0].location.x - nodes[1][0].location.x)
	# move the first node away from the rest of the main shader
	delta = 2*shift

	# realign each slot
	for tile, mask, height, transform in reversed(nodes):
		transform.location.x = height.location.x
		tile.location.y = tile_y
		mask.location.y = mask_y
		height.location.y = height_y
		transform.location.y = transform_y

		tile.location.x -= delta
		mask.location.x -= delta
		height.location.x -= delta
		transform.location.x -= delta
		delta += shift

	# just fix the input x
	for node in get_input_nodes(height, "Normal"):
		node.location.x -= delta
		for child in get_input_nodes(node):
			child.location.x -= delta

