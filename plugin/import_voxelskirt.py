import logging
import math
import os
import time
import bpy

from generated.formats.ms2.structs.packing_utils import unpack_swizzle
from generated.formats.ovl_base import OvlContext
from generated.formats.voxelskirt.structs.VoxelskirtRoot import VoxelskirtRoot
from plugin.utils.node_util import load_img
from plugin.utils.object import mesh_from_data, create_ob, create_collection


def append_subsurf_modifiers(b_obj, num):
	added = 0
	while added < num:
		can_add = min(6, num-added)
		append_subsurf_modifier(b_obj, can_add)
		added += can_add


def append_subsurf_modifier(b_obj, levels):
	# max = 6
	if b_obj:
		b_mod = b_obj.modifiers.new("Subsurf", 'SUBSURF')
		b_mod.subdivision_type = 'SIMPLE'
		b_mod.levels = levels
		b_mod.render_levels = levels


def append_displacement_modifier(b_obj, b_tex):
	if b_obj and b_tex:
		b_mod = b_obj.modifiers.new(b_tex.name, 'DISPLACE')
		b_mod.texture_coords = 'UV'
		b_mod.direction = 'Z'
		b_mod.texture = b_tex


def generate_mesh(x, y, scale):
	w = x * scale / 2
	h = y * scale / 2
	verts = [(a, b, 0) for a in (-w, w) for b in (-h, h)]
	uvs = [(a, b) for a in (1, 0) for b in (0, 1)]
	quads = [(1, 0, 2, 3)]
	return verts, quads, uvs


def create_tex(fp):
	b_img = load_img(fp)
	# set linear colorspace
	b_img.colorspace_settings.name = 'Linear'
	b_tex = bpy.data.textures.new(os.path.splitext(os.path.basename(fp))[0], type="IMAGE")
	b_tex.image = b_img
	# disable clamp
	b_tex.use_clamp = False
	return b_tex


def load(reporter, filepath=""):
	in_dir = os.path.dirname(filepath)
	path_no_ext, ext = os.path.splitext(filepath)
	starttime = time.time()

	for area in bpy.context.screen.areas:  # iterate through areas in current screen
		if area.type == 'VIEW_3D':
			for space in area.spaces:  # iterate through spaces in current VIEW_3D area
				if space.type == 'VIEW_3D':  # check if space is a 3D view
					space.clip_start = 0.1
					space.clip_end = 100000

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
	verts, quads, uvs = generate_mesh(vox.x, vox.y, vox.scale)
	map_ob, b_me = mesh_from_data(scene, "map", verts, quads, False)
	b_me.polygons[0].use_smooth = True
	b_me.uv_layers.new(name=f"UV0")
	b_me.uv_layers[-1].data.foreach_set(
		"uv", [uv for pair in [uvs[l.vertex_index] for l in b_me.loops] for uv in pair])

	num_subdivisions = int(math.log2(vox.x))
	# add subsurf & displacement modifiers
	append_subsurf_modifiers(map_ob, num_subdivisions)
	# import textures
	if "COASTER" in vox.game:
		b_tex = create_tex(f"{path_no_ext}_height.tiff")
		append_displacement_modifier(map_ob, b_tex)
	else:
		for layer in vox.layers.data:
			if layer.dtype == 0:
				b_tex = create_tex(f"{path_no_ext}_{layer.name}.png")
			else:
				b_tex = create_tex(f"{path_no_ext}_{layer.name}.tiff")
				append_displacement_modifier(map_ob, b_tex)

	for entity_group in vox.entity_groups.data:
		coll = create_collection(f"{entity_group.name}", scene.collection)
		if entity_group.entity_instances:
			for i, entity_instance in enumerate(entity_group.entity_instances.data):
				ob = create_ob(bpy.context.scene, f"{entity_group.name}_{i}", None, coll=coll)
				loc = entity_instance.loc
				ob.location = unpack_swizzle((loc.x, loc.y, loc.z))
				ob.rotation_euler.z = entity_instance.z_rot

	reporter.show_info(f'Imported {path_no_ext} in {time.time() - starttime: .2f} seconds')
