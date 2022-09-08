import logging
import os
import time
import bpy

from generated.formats.ms2.compounds.packing_utils import unpack_swizzle
from generated.formats.ovl_base import OvlContext
from generated.formats.voxelskirt.compounds.VoxelskirtRoot import VoxelskirtRoot
from plugin.utils.object import mesh_from_data, create_ob, get_collection


def generate_mesh(x, y, scale):
	w = x * scale / 2
	h = y * scale / 2
	verts = [(a, b, 0) for a in (-w, w) for b in (-h, h)]
	quads = [(1, 0, 2, 3)]
	return verts, quads


def load(filepath=""):
	starttime = time.time()
	errors = []

	scene = bpy.context.scene
	sculpt_settings = scene.tool_settings.sculpt
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

	verts, quads = generate_mesh(vox.x, vox.y, vox.scale)
	map_ob, me = mesh_from_data(scene, "map", verts, quads, False)
	me.polygons[0].use_smooth = True

	# add subsurf & displacement modifiers

	# add displacement texture
	# set linear colorspace, disable clamp

	for entity_group in vox.entity_groups.data:
		coll = get_collection(scene, f"{entity_group.name}")
		if entity_group.entity_instances:
			for i, entity_instance in enumerate(entity_group.entity_instances.data):
				ob = create_ob(bpy.context.scene, f"{entity_group.name}_{i}", None, coll=coll)
				loc = entity_instance.loc
				ob.location = unpack_swizzle((loc.x, loc.y, loc.z))
				ob.rotation_euler.z = entity_instance.z_rot

	logging.info(f'Finished Import in {time.time() - starttime: .2f} seconds')
	return errors
