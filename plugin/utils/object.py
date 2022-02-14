import logging

import bpy
import time


def mesh_from_data(scene, name, verts, faces, wireframe=False, coll_name=None):
	me = bpy.data.meshes.new(name)
	# start_time = time.time()
	me.from_pydata(verts, [], faces)
	# print(f"from_pydata() took {time.time()-start_time:.2f} seconds for {len(verts)} verts")
	# me.update()
	ob = create_ob(scene, name, me, coll_name=coll_name)
	if wireframe:
		ob.draw_type = 'WIRE'
	return ob, me


def create_ob(scene, ob_name, ob_data, coll_name=None):
	logging.debug(f"Adding {ob_name} to scene {scene.name}")
	ob = bpy.data.objects.new(ob_name, ob_data)
	if coll_name is None:
		# link to scene root collection
		scene.collection.objects.link(ob)
	else:
		link_to_collection(scene, ob, coll_name)
	bpy.context.view_layer.objects.active = ob
	return ob


def get_lod(ob):
	for coll in bpy.data.collections:
		if "LOD" in coll.name and ob.name in coll.objects:
			return coll.name


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
