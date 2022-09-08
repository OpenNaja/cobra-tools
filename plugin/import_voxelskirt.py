import logging
import os
import time
import bpy

from generated.formats.ms2.compounds.packing_utils import unpack_swizzle
from generated.formats.ovl_base import OvlContext
from generated.formats.voxelskirt import VoxelskirtFile
from generated.formats.voxelskirt.compounds.VoxelskirtRoot import VoxelskirtRoot
from plugin.utils.object import mesh_from_data, create_ob


def generate_mesh(x_verts, y_verts, scale, heights):
	verts = []
	i = 0
	for x in range(x_verts):
		for y in range(y_verts):
			verts.append((x * scale, y * scale, heights[x, y]), )
			i += 1
	quads = []
	i = 0
	for x in range(x_verts - 1):
		for y in range(y_verts - 1):
			quads.append((i + 1, i, i + y_verts, i + y_verts + 1))
			i += 1
		i += 1
	return verts, quads


def get_weights(weights):
	dic = {}
	for i, vert in enumerate(weights):
		for bone_index, weight in enumerate(vert):
			if bone_index not in dic:
				dic[bone_index] = {}
			if weight not in dic[bone_index]:
				dic[bone_index][weight] = []
			dic[bone_index][weight].append(i)
	return dic


def import_vertex_groups(ob, weights):
	# create vgroups and store weights
	for bone_index, weights_dic in get_weights(weights).items():
		bonename = str(bone_index)
		# todo lookup
		ob.vertex_groups.new(name=bonename)
		for weight, vert_indices in weights_dic.items():
			ob.vertex_groups[bonename].add(vert_indices, weight/255, 'REPLACE')


def load(filepath=""):
	starttime = time.time()
	errors = []

	sculpt_settings = bpy.context.scene.tool_settings.sculpt
	sculpt_settings.lock_x = True
	sculpt_settings.lock_y = True

	# when no object exists, or when we are in edit mode when script is run
	try:
		bpy.ops.object.mode_set(mode='OBJECT')
	except:
		pass
	file_name = os.path.basename(filepath)

	logging.info(f"Importing {file_name}")
	context = OvlContext()
	vox = VoxelskirtRoot.from_xml_file(filepath, context)

	# verts, quads = generate_mesh(vox.info.x, vox.info.y, 1.0, vox.heightmap / vox.info.height)
	# map_ob, me = mesh_from_data("map", verts, quads, False)
	for entity_group in vox.entity_groups.data:
		if entity_group.entity_instances:
			for i, entity_instance in enumerate(entity_group.entity_instances.data):
				ob = create_ob(bpy.context.scene, f"{entity_group.name}_{i}", None)
				loc = entity_instance.loc
				ob.location = unpack_swizzle((loc.x, loc.y, loc.z))
				ob.rotation_euler.z = entity_instance.z_rot
	# import_vertex_groups(map_ob, vox.weights)
	# verts, quads = generate_mesh(vox.info.x, vox.info.y, 1.0, vox.layer)
	# for face in me.polygons:
	# 	face.use_smooth = True

	logging.info(f'Finished Import in {time.time() - starttime: .2f} seconds')
	return errors
