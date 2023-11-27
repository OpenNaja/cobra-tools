import logging
import os
import bpy
import math

from generated.formats.matcol.compounds.MatcolRoot import MatcolRoot
from plugin.utils.node_arrange import nodes_iterate
from plugin.utils.node_util import load_tex_node, get_tree

# an experiment
import logging
import os

from generated.formats.dinosaurmaterialvariants.compounds.DinoLayersHeader import DinoLayersHeader
from generated.formats.fgm.compounds.FgmHeader import FgmHeader
from generated.formats.ovl_base import OvlContext


channels = ("R", "G", "B", "A")
MATLAY = ".dinosaurmateriallayers"
MATCOL = ".materialcollection"
	

class LayeredMaterial:

	def __init__(self):
		self.context = OvlContext()
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
			# todo - rename to increment_channel, check matcol for corresponding feature?
			# increment channel
			if self.ext == MATLAY:
				if layer.has_ptr:
					ch_i += 1
			else:
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
						# skip first 2 letters m_
						lut[attrib.attrib_name.data.lower()[2:]] = [v for b, v in zip(attrib.flags, attrib.value)]
				else:
					continue
			self.slots.append((height_tile_png_path, mask_png_path, lut))

	def get_heightmap(self, layer_i, tex_fgm):
		height_tex = tex_fgm.textures.data[1]
		height_dep = tex_fgm.name_foreach_textures.data[1]
		height_file_name = height_dep.dependency_name.data
		height_file_basename = os.path.splitext(height_file_name)[0]
		# todo codegen - why is array_index str, not int?
		array_index = int(height_tex.value[0].array_index)
		height_tile_png_path = os.path.join(self.base_dir, f"{height_file_basename}_[{array_index:02}].png")
		if not os.path.isfile(height_tile_png_path):
			logging.error(f"Found no tile texture for layer {layer_i} {height_tile_png_path}")
		return height_tile_png_path


# class Layer:
#
# 	def __init__(self, mask_png_path, height_tile_png_path, trans_fgm):
# 		self.mask_png_path = mask_png_path
# 		self.height_tile_png_path = height_tile_png_path
# 		self.trans_fgm = trans_fgm
# 		self.lut = {}
# 		for attrib, attrib_data in zip(self.trans_fgm.attributes.data, self.trans_fgm.value_foreach_attributes.data):
# 			# skip first letter p
# 			self.lut[attrib.name.lower()[1:]] = attrib_data.value
# 		# print(self.trans_fgm)
# 		# print(self.lut)


def create_flip():
	name = "FlipX"
	# only create the material if we haven't already created it, then just grab it
	if name not in bpy.data.node_groups:
		# create a group
		test_group = bpy.data.node_groups.new(name, 'ShaderNodeTree')

	else:
		test_group = bpy.data.node_groups[name]
		for node in test_group.nodes:
			test_group.nodes.remove(node)
		for node in test_group.inputs:
			test_group.inputs.remove(node)
		for node in test_group.outputs:
			test_group.outputs.remove(node)

	# create group inputs
	group_inputs = test_group.nodes.new('NodeGroupInput')
	group_inputs.location = (-350, 0)
	test_group.inputs.new('NodeSocketVectorXYZ', 'in')

	# create group outputs
	group_outputs = test_group.nodes.new('NodeGroupOutput')
	group_outputs.location = (300, 0)
	test_group.outputs.new('NodeSocketVectorXYZ', 'out')

	split = test_group.nodes.new('ShaderNodeSeparateXYZ')
	split.label = "Split"
	test_group.links.new(group_inputs.outputs["in"], split.inputs[0])

	flip = test_group.nodes.new('ShaderNodeMath')
	flip.operation = 'MULTIPLY'
	test_group.links.new(split.outputs[0], flip.inputs[0])
	flip.inputs[1].default_value = -1.0

	join = test_group.nodes.new('ShaderNodeCombineXYZ')
	join.label = "Join"
	test_group.links.new(flip.outputs[0], join.inputs[0])
	test_group.links.new(split.outputs[1], join.inputs[1])
	test_group.links.new(split.outputs[2], join.inputs[2])

	# #link output
	test_group.links.new(join.outputs[0], group_outputs.inputs['out'])

	nodes_iterate(test_group, group_outputs)
	return test_group


def create_group():
	flipgr = create_flip()
	name = "MatcolSlot"
	# only create the material if we haven't already created it, then just grab it
	if name not in bpy.data.node_groups:
		# create a group
		test_group = bpy.data.node_groups.new(name, 'ShaderNodeTree')

	else:
		test_group = bpy.data.node_groups[name]
		for node in test_group.nodes:
			test_group.nodes.remove(node)
		for node in test_group.inputs:
			test_group.inputs.remove(node)
		for node in test_group.outputs:
			test_group.outputs.remove(node)

	# create group inputs
	group_inputs = test_group.nodes.new('NodeGroupInput')
	test_group.inputs.new('NodeSocketVectorTranslation', 'UVOffset')
	test_group.inputs.new('NodeSocketFloatAngle', 'uvRotationAngle')
	test_group.inputs.new('NodeSocketVectorTranslation', 'uvRotationPosition')
	test_group.inputs.new('NodeSocketVectorXYZ', 'uvTile')

	# create group outputs
	group_outputs = test_group.nodes.new('NodeGroupOutput')
	group_outputs.location = (300, 0)
	test_group.outputs.new('NodeSocketVectorXYZ', 'out')

	offset_flipx = test_group.nodes.new("ShaderNodeGroup")
	offset_flipx.node_tree = flipgr
	test_group.links.new(group_inputs.outputs["UVOffset"], offset_flipx.inputs[0])

	rotpos_flipx = test_group.nodes.new("ShaderNodeGroup")
	rotpos_flipx.node_tree = flipgr
	test_group.links.new(group_inputs.outputs["uvRotationPosition"], rotpos_flipx.inputs[0])

	uv = test_group.nodes.new('ShaderNodeUVMap')
	uv.label = "UV Input"
	uv.uv_map = "UV0"

	scale_pivot = test_group.nodes.new('ShaderNodeMapping')
	scale_pivot.inputs[1].default_value[1] = -1.0
	scale_pivot.label = "Scale Pivot"
	test_group.links.new(uv.outputs[0], scale_pivot.inputs[0])

	uv_offset = test_group.nodes.new('ShaderNodeMapping')
	uv_offset.label = "UVOffset"
	test_group.links.new(scale_pivot.outputs[0], uv_offset.inputs[0])
	test_group.links.new(offset_flipx.outputs[0], uv_offset.inputs[1])

	uv_tile = test_group.nodes.new('ShaderNodeMapping')
	uv_tile.label = "uvTile"
	test_group.links.new(uv_offset.outputs[0], uv_tile.inputs[0])
	test_group.links.new(group_inputs.outputs["uvTile"], uv_tile.inputs[3])

	rot_pivot = test_group.nodes.new('ShaderNodeMapping')
	rot_pivot.inputs[1].default_value[1] = -1.0
	rot_pivot.label = "Rot Pivot"
	test_group.links.new(uv_tile.outputs[0], rot_pivot.inputs[0])

	uv_rot_pos_a = test_group.nodes.new('ShaderNodeMapping')
	uv_rot_pos_a.label = "uvRotationPosition"
	test_group.links.new(rot_pivot.outputs[0], uv_rot_pos_a.inputs[0])
	test_group.links.new(rotpos_flipx.outputs[0], uv_rot_pos_a.inputs[1])

	# extra step to create vector from float
	uv_rot_combine = test_group.nodes.new('ShaderNodeCombineXYZ')
	uv_rot_combine.label = "build uvRotation Vector"
	test_group.links.new(group_inputs.outputs["uvRotationAngle"], uv_rot_combine.inputs[2])

	uv_rot = test_group.nodes.new('ShaderNodeMapping')
	uv_rot.label = "uvRotationAngle"
	test_group.links.new(uv_rot_pos_a.outputs[0], uv_rot.inputs[0])
	test_group.links.new(uv_rot_combine.outputs[0], uv_rot.inputs[2])

	# extra step to negate input
	uv_rot_pos_flip = test_group.nodes.new('ShaderNodeVectorMath')
	uv_rot_pos_flip.operation = "SCALE"
	uv_rot_pos_flip.label = "flip uvRotationPosition"
	# counter intuitive index for non-vector argument!
	try:
		uv_rot_pos_flip.inputs[2].default_value = -1.0
	except:
		print("bug with new blender 2.9, unsure how to solve")
		pass
	test_group.links.new(rotpos_flipx.outputs[0], uv_rot_pos_flip.inputs[0])

	uv_rot_pos_b = test_group.nodes.new('ShaderNodeMapping')
	uv_rot_pos_b.label = "undo uvRotationPosition"
	test_group.links.new(uv_rot_pos_flip.outputs[0], uv_rot_pos_b.inputs[1])
	test_group.links.new(uv_rot.outputs[0], uv_rot_pos_b.inputs[0])

	# #link output
	test_group.links.new(uv_rot_pos_b.outputs[0], group_outputs.inputs['out'])

	nodes_iterate(test_group, group_outputs)
	return test_group


def get_att(node, lut, names):
	for name in names:
		n = name.lower()
		if n in lut:
			node.inputs[name].default_value = lut[n]


def load(filepath=""):
	layers = LayeredMaterial()
	layers.load_mat_layers(filepath)
	slots = layers.slots

	logging.info(f"MATERIAL: {layers.basename}")
	# only create the material if we haven't already created it, then just grab it
	if layers.basename not in bpy.data.materials:
		mat = bpy.data.materials.new(layers.basename)
	# only create the material if we haven't already created it, then just grab it
	else:
		mat = bpy.data.materials[layers.basename]

	tree = get_tree(mat)
	transform_group = create_group()
	output = tree.nodes.new('ShaderNodeOutputMaterial')
	principled = tree.nodes.new('ShaderNodeBsdfPrincipled')

	textures = []
	for i, (height_png, mask_png, lut) in enumerate(slots, start=1):
		logging.info(f"Slot {i:02d}")
		# Until better option to organize the shader info, create texture group node
		slot_frame = tree.nodes.new('NodeFrame')
		slot_frame.label = f"Slot {i:02d}"

		# load the tiled height_texture
		tex = load_tex_node(tree, height_png)
		tex.image.colorspace_settings.name = "Non-Color"
		# scales for the tile
		heightScale = tree.nodes.new('ShaderNodeMath')
		heightScale.label = f"heightScaleOffset{i:02d}"
		heightScale.operation = 'MULTIPLY_ADD'
		heightScale.parent = slot_frame
		tree.links.new(tex.outputs[0], heightScale.inputs["Value"])
		heightScale.inputs[1].default_value = lut["heightscale"][0]
		# nb heightoffset currently does not influence the result visibly because we are not really height blending
		heightScale.inputs[2].default_value = lut["heightoffset"][0]

		# load the blendweights layer mask
		mask = load_tex_node(tree, mask_png)
		mask.image.colorspace_settings.name = "Non-Color"
		tex.parent = slot_frame
		mask.parent = slot_frame
		# scales for the mask
		heightBlendScale = tree.nodes.new('ShaderNodeMapRange')
		heightBlendScale.label = f"heightBlendScale{i:02d}"
		# heightBlendScale.clamp = False
		heightBlendScale.clamp = True
		heightBlendScale.parent = slot_frame
		tree.links.new(mask.outputs[0], heightBlendScale.inputs["Value"])
		if layers.ext == MATLAY:
			heightBlendScaleA, heightBlendScaleB = sorted([i for i in (lut["heightblendscalea"], lut["heightblendscaleb"])])
		else:
			heightBlendScaleA = 0.0
			heightBlendScaleB = lut["heightblendscale"][0]
		# if not heightBlendScaleA and not heightBlendScaleB:
		# 	heightBlendScaleB = 1.0
		heightBlendScale.inputs[3].default_value = heightBlendScaleA
		heightBlendScale.inputs[4].default_value = 1.0 + heightBlendScaleB
		# heightBlendScale.inputs[3].default_value = slot.lut["heightblendscalea"]
		# heightBlendScale.inputs[4].default_value = 1.0 + slot.lut["heightblendscaleb"]

		# store these to generate the bump mix later
		textures.append((heightScale, heightBlendScale))

		transform = tree.nodes.new("ShaderNodeGroup")
		transform.node_tree = transform_group
		transform.parent = slot_frame
		tree.links.new(transform.outputs[0], tex.inputs[0])

		transform.inputs["uvRotationPosition"].default_value[:2] = lut["uvrotationposition"]
		transform.inputs["UVOffset"].default_value[:2] = lut["uvoffset"]
		transform.inputs["uvTile"].default_value[:2] = lut["uvtile"]

		# m_uvRotationAngle
		# matcol stores it as fraction of 180°
		# in radians for blender internally even though it displays as degree
		# flip since blender flips V coord
		transform.inputs["uvRotationAngle"].default_value = -math.radians(lut["uvrotationangle"][0] * 180)

		tex.update()
		mask.update()

	if not textures:
		raise AttributeError(f"Could not find any layer textures - make sure the tile .fgm and .png files are in the same folder!")

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
	#
	# bump = tree.nodes.new('ShaderNodeBump')
	# bump.inputs["Strength"].default_value = 0.5
	# bump.inputs["Distance"].default_value = 0.1

	# tree.links.new(normal_map.outputs[0], bump.inputs["Normal"])
	last_mixer = normal_map
	for height, mask in textures:
		bump = tree.nodes.new('ShaderNodeBump')
		tree.links.new(mask.outputs[0], bump.inputs["Strength"])
		tree.links.new(last_mixer.outputs[0], bump.inputs["Normal"])
		tree.links.new(height.outputs[0], bump.inputs["Height"])
		last_mixer = bump

	# tree.links.new(mixRGB.outputs[0], bump.inputs[2])

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
	tree.links.new(bump.outputs[0], principled.inputs["Normal"])
	tree.links.new(principled.outputs[0], output.inputs[0])

	nodes_iterate(tree, output)
	return ()
