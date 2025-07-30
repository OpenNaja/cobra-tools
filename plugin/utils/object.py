from contextlib import contextmanager
import logging
import bpy

from generated.formats.ms2 import get_game, Ms2Context


@contextmanager
def ensure_visible():
	"""Make all collections visible in view_layer [tick box] to ensure applying modifiers works"""
	all_collections = get_view_collections()
	states_exclude = {coll.name: bool(coll.exclude) for coll in all_collections}
	states_hide_viewport = {coll.name: bool(coll.hide_viewport) for coll in all_collections}
	for coll in all_collections:
		coll.exclude = False
	yield
	# get them again to avoid crashing blender if some have been deleted during yield
	all_collections = get_view_collections()
	# reset to original state, or defaults for newly added LODs
	for coll in all_collections:
		# default to included
		coll.exclude = states_exclude.get(coll.name, False)
		# default to hidden unless collection is L0 (newly created lods)
		hide_fallback = "_L0" not in coll.name
		coll.hide_viewport = states_hide_viewport.get(coll.name, hide_fallback)


def get_view_collections():
	view_collections = bpy.context.view_layer.layer_collection.children
	all_collections = set(view_collections)
	# account for nesting inside the mdl2 collection
	for coll in view_collections:
		all_collections.update(coll.children)
	return all_collections


def mesh_from_data(scene, name, verts, faces, wireframe=False, coll_name=None, coll=None):
	me = bpy.data.meshes.new(name)
	me.from_pydata(verts, [], faces)
	# me.update()
	ob = create_ob(scene, name, me, coll_name=coll_name, coll=coll)
	if wireframe:
		ob.display_type = 'WIRE'
	return ob, me


def create_ob(scene, ob_name, ob_data, coll_name=None, coll=None):
	logging.debug(f"Adding {ob_name} to scene {scene.name}")
	ob = bpy.data.objects.new(ob_name, ob_data)
	if coll_name is not None:
		link_to_collection(scene, ob, coll_name)
	elif coll is not None:
		coll.objects.link(ob)
	else:
		# link to scene root collection
		scene.collection.objects.link(ob)
	bpy.context.view_layer.objects.active = ob
	return ob


def get_lod(ob):
	for coll in bpy.data.collections:
		if "LOD" in coll.name and ob.name in coll.objects:
			return coll.name


# @TODO: Create appropriate defaults
def create_scene(name, num_streams=0, version=0):
	logging.debug(f"Adding scene {name} to blender")
	if name not in bpy.data.scenes:
		scene = bpy.data.scenes.new(name)
		# store scene properties
		scene.cobra.num_streams = num_streams
		context = Ms2Context()
		context.version = version
		game_item = get_game(context)[0]
		scene.cobra.game = game_item.value
	return bpy.data.scenes[name]


def create_collection(coll_name, parent_coll):
	if coll_name not in bpy.data.collections:
		coll = bpy.data.collections.new(coll_name)
		parent_coll.children.link(coll)
		return coll
	return bpy.data.collections[coll_name]


def link_to_collection(scene, ob, coll_name):
	# turn any relative collection names to include the scene prefix
	if not coll_name.startswith(f"{scene.name}_"):
		coll_name = f"{scene.name}_{coll_name}"
	if coll_name not in bpy.data.collections:
		coll = bpy.data.collections.new(coll_name)
		scene.collection.children.link(coll)
	else:
		coll = bpy.data.collections[coll_name]
	# Link active object to the new collection
	coll.objects.link(ob)
	return coll_name


def has_data_in_coll(coll):
	if coll.objects:
		# operator needs an active object, set one if missing (eg. user had deleted the active object)
		if not bpy.context.view_layer.objects.active:
			bpy.context.view_layer.objects.active = coll.objects[0]
		# now enter object mode on the active object, if we aren't already in it
		bpy.ops.object.mode_set(mode="OBJECT")
		return True
	if coll.children:
		return True


def get_property(ob, prop_name, default=None):
	"""Ensure that custom property is set or raise an intellegible error"""
	if prop_name in ob:
		return ob[prop_name]
	else:
		if default is not None:
			return default
		raise KeyError(f"Custom property '{prop_name}' missing from {ob.name} (data: {type(ob).__name__}). Add it!")


def find_collection(layer_collection, collection):
	# adapted from https://devtalk.blender.org/t/unique-identifier-for-layer-collections/23966
	if layer_collection.collection == collection:
		yield layer_collection
	for child_collection in layer_collection.children:
		yield from find_collection(child_collection, collection)


def set_collection_visibility(scene, coll_name, hide):
	if coll_name in bpy.data.collections:
		coll = bpy.data.collections[coll_name]
		coll.hide_render = hide
		# get view layer collection if it exists
		view_colls = list(find_collection(bpy.context.view_layer.layer_collection, coll))
		if view_colls:
			view_colls[0].hide_viewport = hide


def get_bones_table(b_armature_ob):
	p_bones = sorted(b_armature_ob.pose.bones, key=lambda pbone: pbone["index"])
	bones_table = [(bone["index"], bone.name) for bone in p_bones]
	return bones_table, p_bones


def get_p_index(pbone):
	if pbone:
		return pbone["index"]
	else:
		return None


def get_parent_map(p_bones):
	parent_index_map = [get_p_index(pbone.parent) for pbone in p_bones]
	return parent_index_map
