import logging

import bpy
import time


def mesh_from_data(scene, name, verts, faces, wireframe=False):
	me = bpy.data.meshes.new(name)
	start_time = time.time()
	me.from_pydata(verts, [], faces)
	# print(f"from_pydata() took {time.time()-start_time:.2f} seconds for {len(verts)} verts")
	# me.update()
	ob = create_ob(scene, name, me)
	if wireframe:
		ob.draw_type = 'WIRE'
	return ob, me


def create_ob(scene, ob_name, ob_data):
	logging.debug(f"Adding {ob_name} to scene {scene.name}")
	ob = bpy.data.objects.new(ob_name, ob_data)
	scene.collection.objects.link(ob)
	bpy.context.view_layer.objects.active = ob
	return ob


def get_lod(ob):
	for coll in bpy.data.collections:
		if "LOD" in coll.name and ob.name in coll.objects:
			return coll.name


def to_lod(scene, ob, level=0, lod=None):
	# level is given, but not lod
	if not lod:
		lod = f"LOD{level}"
	# lod group name is given, but no level
	else:
		scene_name, lod = lod.rsplit("_", 1)
		level = int(lod[3:])
		# print(level)
	coll_name = link_to_collection(scene, ob, lod)
	# show lod 0, hide the others
	should_hide = level != 0
	# get view layer, hide collection there
	vlayer = bpy.context.view_layer
	vlayer.layer_collection.children[coll_name].hide_viewport = should_hide
	# hide object in view layer
	ob.hide_set(should_hide, view_layer=vlayer)


def link_to_collection(scene, ob, coll_name):
	coll_name = f"{scene.name}_{coll_name}"
	if coll_name not in bpy.data.collections:
		coll = bpy.data.collections.new(coll_name)
		scene.collection.children.link(coll)
	else:
		coll = bpy.data.collections[coll_name]
	# Link active object to the new collection
	coll.objects.link(ob)
	return coll_name
