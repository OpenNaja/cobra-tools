import os
import bpy
import math

from generated.formats.matcol import MatcolFile
from generated.formats.fgm import FgmFile
from utils.node_arrange import nodes_iterate
from utils.node_util import load_tex, get_tree


def load(operator, context, filepath = ""):
	create_material(filepath)
	return []


def create_height():
	name = "MatcolHeight"
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
	test_group.inputs.new('NodeSocketFloat', 'texture')
	test_group.inputs.new('NodeSocketFloat', 'heightBlendScale.lower')
	test_group.inputs.new('NodeSocketFloat', 'heightBlendScale.upper')
	test_group.inputs.new('NodeSocketFloat', 'heightOffset')
	test_group.inputs.new('NodeSocketFloat', 'heightScale')

	# create group outputs
	group_outputs = test_group.nodes.new('NodeGroupOutput')
	group_outputs.location = (300, 0)
	test_group.outputs.new('NodeSocketFloat', 'texture')

	# create three math nodes in a group
	heightScale = test_group.nodes.new('ShaderNodeMath')
	heightScale.label = "heightScale"
	heightScale.operation = 'MULTIPLY'
	test_group.links.new(group_inputs.outputs["texture"], heightScale.inputs[0])
	test_group.links.new(group_inputs.outputs["heightScale"], heightScale.inputs[1])

	heightOffset = test_group.nodes.new('ShaderNodeMath')
	heightOffset.label = "heightOffset"
	heightOffset.operation = 'ADD'
	test_group.links.new(heightScale.outputs[0], heightOffset.inputs[0])
	test_group.links.new(group_inputs.outputs["heightOffset"], heightOffset.inputs[1])

	heightBlendScale = test_group.nodes.new('ShaderNodeMapRange')
	heightBlendScale.label = "heightBlendScale"
	heightBlendScale.clamp = False
	test_group.links.new(heightOffset.outputs[0], heightBlendScale.inputs[0])
	test_group.links.new(group_inputs.outputs["heightBlendScale.lower"], heightBlendScale.inputs[1])
	test_group.links.new(group_inputs.outputs["heightBlendScale.upper"], heightBlendScale.inputs[2])

	scale = test_group.nodes.new('ShaderNodeMath')
	scale.label = "scale"
	scale.operation = 'MULTIPLY'
	test_group.links.new(heightBlendScale.outputs[0], scale.inputs[0])
	scale.inputs[1].default_value = 2.0

	# #link output
	test_group.links.new(scale.outputs[0], group_outputs.inputs['texture'])

	nodes_iterate(test_group, group_outputs)
	return test_group


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
	group_inputs.location = (-350,0)
	test_group.inputs.new('NodeSocketVectorXYZ','in')

	# create group outputs
	group_outputs = test_group.nodes.new('NodeGroupOutput')
	group_outputs.location = (300,0)
	test_group.outputs.new('NodeSocketVectorXYZ','out')


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
	#only create the material if we haven't already created it, then just grab it
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
	test_group.inputs.new('NodeSocketVectorTranslation','UVOffset')
	test_group.inputs.new('NodeSocketFloatAngle','uvRotationAngle')
	test_group.inputs.new('NodeSocketVectorTranslation','uvRotationPosition')
	test_group.inputs.new('NodeSocketVectorXYZ','uvTile')

	# create group outputs
	group_outputs = test_group.nodes.new('NodeGroupOutput')
	group_outputs.location = (300,0)
	test_group.outputs.new('NodeSocketVectorXYZ','out')


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

def create_material(matcol_path):
	slots = load_matcol(matcol_path)

	matdir, mat_ext = os.path.split(matcol_path)
	matname = os.path.splitext(mat_ext)[0]
	print("MATERIAL:",matname)
	#only create the material if we haven't already created it, then just grab it
	if matname not in bpy.data.materials:
		mat = bpy.data.materials.new(matname)
	#only create the material if we haven't already created it, then just grab it
	else:
		mat = bpy.data.materials[matname]

	tree = get_tree(mat)
	height_group = create_height()
	transform_group = create_group()
	output = tree.nodes.new('ShaderNodeOutputMaterial')
	principled = tree.nodes.new('ShaderNodeBsdfPrincipled')
	
	last_mixer = None
	textures = []
	for i, (infos, texture) in enumerate( slots):
		# skip default materials that have no fgm assigned
		if not texture:
			textures.append( None )
			continue
		print("Slot",i)
		slotnum = i
		# load the tiled texture
		tex = load_tex(tree, texture)
		# load the blendweights layer mask
		mask_path = os.path.join(matdir, matname+".playered_blendweights_{:02}.png".format(i))
		mask = load_tex(tree, mask_path)

		# height offset attribute
		print([i for i in infos[1].info.value][:2])
		heightscale_lower, heightscale_upper = sorted([i for i in infos[1].info.value][:2])

		if not heightscale_lower and not heightscale_upper:
			heightscale_upper = 1.0
		heightoffset = infos[2].info.value[0]
		heightscale = infos[3].info.value[0]

		height = tree.nodes.new("ShaderNodeGroup")
		height.node_tree = height_group
		height.inputs["heightScale"].default_value = heightscale
		height.inputs["heightOffset"].default_value = heightoffset
		height.inputs["heightBlendScale.lower"].default_value = heightscale_lower
		height.inputs["heightBlendScale.upper"].default_value = heightscale_upper
		tree.links.new(tex.outputs[0], height.inputs[0])

		textures.append( (height, mask) )

		transform = tree.nodes.new("ShaderNodeGroup")
		transform.node_tree = transform_group

		# m_uvRotationPosition
		uvrotpos = list(i for i in infos[6].info.value)[:3]
		transform.inputs["uvRotationPosition"].default_value = uvrotpos

		# m_UVOffset
		uvoffset = list(i for i in infos[4].info.value)[:3]
		transform.inputs["UVOffset"].default_value = uvoffset

		# m_uvTile
		uvscale = list(i for i in infos[7].info.value)[:3]
		transform.inputs["uvTile"].default_value = uvscale

		# m_uvRotationAngle
		# matcol stores it as fraction of 180°
		# in radians for blender internally even though it displays as degree
		rot = math.radians( infos[5].info.value[0]*180 )
		# flip since blender flips V coord
		transform.inputs["uvRotationAngle"].default_value = -rot
		tree.links.new(transform.outputs[0], tex.inputs[0])
		
		tex.update()
		mask.update()

	indices = []
	for i_a in range(4):
		for i_b in range(4):
			indices.append(i_a + i_b*4)

	indices = list( i for i in range(slotnum) )
	print(indices)

	normal_path = os.path.join(matdir, matname + ".pnormaltexture.png")
	normal = load_tex(tree, normal_path)
	normal.image.colorspace_settings.name = "Non-Color"
	normal_map = tree.nodes.new('ShaderNodeNormalMap')
	tree.links.new(normal.outputs[0], normal_map.inputs[1])
	normal_map.inputs["Strength"].default_value = 2.0
	#
	# bump = tree.nodes.new('ShaderNodeBump')
	# bump.inputs["Strength"].default_value = 0.5
	# bump.inputs["Distance"].default_value = 0.1

	#tree.links.new(normal_map.outputs[0], bump.inputs["Normal"])
	last_mixer = normal_map
	for i in indices:
		# skip empty slots
		if textures[i]:
			height, mask = textures[i]
			bump = tree.nodes.new('ShaderNodeBump')
			tree.links.new(mask.outputs[0], bump.inputs[0])
			tree.links.new(last_mixer.outputs[0], bump.inputs["Normal"])
			tree.links.new(height.outputs[0], bump.inputs["Height"])
			last_mixer = bump


	# tree.links.new(mixRGB.outputs[0], bump.inputs[2])

	diffuse_path = os.path.join(matdir, matname+".pbasediffusetexture.png")
	diffuse = load_tex(tree, diffuse_path)

	roughness_path = os.path.join(matdir, matname+".pbasepackedtexture_01.png")
	roughness = load_tex(tree, roughness_path)
	roughness.image.colorspace_settings.name = "Non-Color"

	ao_path = os.path.join(matdir, matname+".pbasepackedtexture_03.png")
	ao = load_tex(tree, ao_path)
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
	return mat
	# #now finally set all the textures we have in the mesh
	# me = ob.data
	# me.materials.append(mat)
	
def get_data(p, d):
	dat = d()
	with open(p, "rb") as stream:
		dat.read(stream)
	return dat
	
def load_matcol(matcol_path):
	lib_dir = os.path.normpath(os.path.dirname(matcol_path))
	matcol_file = MatcolFile()
	matcol_file.load(matcol_path)
	slots = []
	rootname = "anky_ankylo_backplates"
	basecol = ".pbasecolourtexture"
	baseheight = ".pheighttexture"
	all_textures = [file for file in os.listdir(lib_dir) if file.lower().endswith(".png")]
	base_textures = [os.path.join(lib_dir, file) for file in all_textures if rootname in file and basecol in file]
	height_textures = [os.path.join(lib_dir, file) for file in all_textures if rootname in file and baseheight in file]
	# print(base_textures)
	# for layer in matcol_file.layered_wrapper:
		# print(layer)
	for layer in matcol_file.layered_wrapper.layers:
		print(layer.name)
		if layer.name == "Default":
			print("Skipping Default layer")
			htex = None
		else:
			fgm_path = os.path.join(lib_dir, layer.name+".fgm")
			# print(fgm_path)
			fgm_data = FgmFile()
			fgm_data.load(fgm_path)
			if fgm_data.textures[0].is_textured == 8:
				base_index = fgm_data.textures[0].indices[1]
				height_index = fgm_data.textures[1].indices[1]
			else:
				print("tell Developers not using indices")
			print("base_array_index", base_index)
			print("height_array_index", height_index)
			print("base", base_textures[base_index])
			print("height", height_textures[height_index])
			htex = height_textures[height_index]
		slots.append((layer.infos, htex))
	return slots
	
if __name__ == '__main__':
	matcol_path = "C:/Users/arnfi/Desktop/pp/herrerasaurus.materialcollection"
	load_matcol(matcol_path)
	# python tmc.py
