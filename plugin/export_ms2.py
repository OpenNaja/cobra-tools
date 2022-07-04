import logging
import math
import os
import time
import struct
import traceback

import bpy
import mathutils

from generated.formats.ms2.compound.LodInfo import LodInfo
from generated.formats.ms2.compound.MaterialName import MaterialName
from generated.formats.ms2.compound.MeshDataWrap import MeshDataWrap
from generated.formats.ms2.compound.Object import Object
from generated.formats.ms2 import Ms2File
from generated.formats.ms2.compound.packing_utils import remap
from plugin.import_ms2 import num_fur_as_weights
from plugin.modules_export.armature import get_armature, handle_transforms, export_bones_custom
from plugin.modules_export.collision import export_bounds
from plugin.modules_import.armature import get_bone_names
from plugin.modules_import.hair import comb_common, get_hair_keys, find_modifier_for_particle_system
from plugin.utils.matrix_util import evaluate_mesh
from plugin.utils.shell import get_collection, is_shell, is_fin, is_flipped

MAX_USHORT = 65535


def ensure_tri_modifier(ob):
	"""Makes sure that ob has a triangulation modifier in its stack."""
	for mod in ob.modifiers:
		if mod.type in ('TRIANGULATE',):
			break
	else:
		ob.modifiers.new('Triangulate', 'TRIANGULATE')


def has_objects_in_scene(scene):
	if scene.objects:
		# operator needs an active object, set one if missing (eg. user had deleted the active object)
		if not bpy.context.view_layer.objects.active:
			bpy.context.view_layer.objects.active = scene.objects[0]
		# now enter object mode on the active object, if we aren't already in it
		bpy.ops.object.mode_set(mode="OBJECT")
		return True


def export_material(ms2, b_mat):
	mat = MaterialName(ms2.context)
	mat.some_index = get_property(b_mat, "some_index")
	mat.name = b_mat.name
	ms2.model.materials.append(mat)


def export_model(model_info, b_lod_coll, b_ob, b_me, bones_table, bounds, apply_transforms, use_stock_normals_tangents):
	logging.info(f"Exporting mesh {b_me.name}")
	# we create a ms2 mesh
	wrapper = MeshDataWrap(model_info.context)
	mesh = wrapper.mesh
	# set data
	mesh.size_of_vertex = 48
	mesh.flag._value = get_property(b_me, "flag")
	mesh.unk_floats[:] = (get_property(b_me, "unk_f0"), get_property(b_me, "unk_f1"))

	mesh.update_dtype()
	num_uvs = mesh.get_uv_count()
	num_vcols = mesh.get_vcol_count()
	# ensure that these are initialized
	mesh.tri_indices = []
	mesh.verts = []
	model_info.model.meshes.append(wrapper)

	num_fur_weights = num_fur_as_weights(b_me.materials[0].name)

	if not len(b_me.vertices):
		raise AttributeError(f"Mesh {b_ob.name} has no vertices!")

	if not len(b_me.polygons):
		raise AttributeError(f"Mesh {b_ob.name} has no polygons!")

	for len_type, num_type, name_type in (
			(len(b_me.uv_layers)+num_fur_weights, num_uvs, "UV"),
			(len(b_me.vertex_colors), num_vcols, "Vertex Color")):
		logging.debug(f"{name_type} count: {num_type}")
		if len_type != num_type:
			raise AttributeError(f"Mesh {b_ob.name} has {len_type} {name_type} layers, but {num_type} were expected!")
	
	# make sure the mesh has a triangulation modifier
	ensure_tri_modifier(b_ob)
	eval_obj, eval_me = evaluate_mesh(b_ob)
	handle_transforms(eval_obj, eval_me, apply=apply_transforms)
	# print("Mesh slot", ind)
	bounds.append(eval_obj.bound_box)

	hair_length = get_hair_length(b_ob)
	mesh.fur_length = hair_length

	unweighted_vertices = []
	tris = []
	# tangents have to be pre-calculated
	# this will also calculate loop normal
	eval_me.calc_tangents()

	tangents = eval_me.attributes["ct_tangents"]
	normals = eval_me.attributes["ct_normals"]

	# stores values retrieved from blender, will be packed into array later
	verts = []
	# use a dict mapping dummy vertices to their index for fast lookup
	# this is used to convert blender vertices (several UVs, normals per face corner) to ms2 vertices
	dummy_vertices = {}
	count_unique = 0
	count_reused = 0
	shell_ob = None
	shapekey = None
	# fin meshes have to grab tangents from shell
	if is_fin(b_ob):
		shell_obs = [ob for ob in b_lod_coll.objects if is_shell(ob) and ob is not b_ob]
		if shell_obs:
			shell_ob = shell_obs[0]
			logging.debug(f"Copying data for {b_ob.name} from base mesh {shell_ob.name}...")

			# bpy.context.view_layer.objects.active = shell_ob
			# if not shell_ob:
			# 	raise AttributeError("No object in context")
			# # particle edit mode has to be entered so that hair strands are generated
			# # otherwise the non-eval ob's particle count is 0
			# if not shell_ob.particle_systems:
			# 	raise AttributeError(f"No particle system on {shell_ob.name}")
			# logging.debug(f"comb_common on object '{shell_ob.name}'")
			# bpy.ops.object.mode_set(mode='PARTICLE_EDIT')
			# bpy.ops.object.mode_set(mode='OBJECT')

			shell_eval_ob, shell_eval_me = evaluate_mesh(shell_ob)
			shell_eval_me.calc_tangents()
			shell_kd = fill_kd_tree(shell_eval_me)
			fin_uv_layer = eval_me.uv_layers[0].data

			# particle_system = shell_ob.particle_systems[0]
			# particle_modifier = find_modifier_for_particle_system(shell_ob, particle_system)
			# particle_modifier_eval = shell_eval_ob.modifiers[particle_modifier.name]
			# particle_system_eval = shell_eval_ob.particle_systems[0]
	# loop faces and collect unique and repeated vertices
	for face in eval_me.polygons:
		if len(face.loop_indices) != 3:
			# this is a bug - we are applying the triangulation modifier above
			raise AttributeError(f"Mesh {b_ob.name} is not triangulated!")
		# build indices into vertex buffer for the current face
		tri = []
		if is_fin(b_ob):
			winding = 0
		else:
			winding = is_flipped(eval_me.uv_layers[0].data, face)
		# loop over face loop to get access to face corner data (normals, uvs, vcols, etc)
		for loop_index in face.loop_indices:
			b_loop = eval_me.loops[loop_index]
			b_vert = eval_me.vertices[b_loop.vertex_index]

			# get the vectors
			position = b_vert.co
			if shell_ob:
				lookup = fin_uv_layer[b_loop.index].uv.to_3d()
				lookup.z = b_vert.co.x
				co, index, dist = shell_kd.find(lookup)
				shell_loop = shell_eval_me.loops[index]

				# reindeer is a special case: has beard normals pointing straight down for shell & fins
				# that is not the fur combing
				# from this test with reindeer normal on fins is confirmed to be the base shell normal
				# not with fur direction applied - that messes with the shading
				# # print(tangent)
				# ind = shell_loop.vertex_index
				# # vert = me.loops[loop_index]
				# particle = particle_system.particles[ind]
				# particle_eval = particle_system_eval.particles[ind]
				# root, tip = get_hair_keys(particle, particle_eval, shell_eval_ob, particle_modifier_eval)
				# hair_direction = (tip - root).normalized()
				# normal = hair_direction
				normal = shell_loop.normal
				tangent = shell_loop.tangent
			else:
				normal = b_loop.normal
				tangent = b_loop.tangent
			# override with custom data if asked
			if use_stock_normals_tangents:
				normal = normals.data[loop_index].vector
				tangent = tangents.data[loop_index].vector

			# shape key morphing
			b_key = b_me.shape_keys
			if b_key and len(b_key.key_blocks) > 1:
				lod_key = b_key.key_blocks[1]
				# yes, there is a key object attached
				if lod_key.name.startswith("LOD"):
					shapekey = lod_key.data[b_loop.vertex_index].co

			uvs = [(layer.data[loop_index].uv.x, 1 - layer.data[loop_index].uv.y) for layer in eval_me.uv_layers]
			# create a dummy bytes str for indexing
			float_items = [*position, *[c for uv in uvs[:2] for c in uv], *tangent]
			dummy = struct.pack(f'<{len(float_items)}f', *float_items)
			# see if this dummy key exists
			try:
				# if it does - reuse it by grabbing its index from the dict
				v_index = dummy_vertices[dummy]
				count_reused += 1
			except KeyError:
				# it doesn't, so we have to fill in additional data
				v_index = count_unique
				if v_index > MAX_USHORT:
					raise OverflowError(
						f"{b_ob.name} has too many ms2 verts. The limit is {MAX_USHORT}. "
						f"\nBlender vertices have to be duplicated on every UV seam, hence the increase.")
				dummy_vertices[dummy] = v_index
				count_unique += 1

				# now collect any missing vert data that was not needed for the splitting of blender verts

				# collect vertex colors
				vcols = [tuple(x for x in layer.data[loop_index].color) for layer in eval_me.vertex_colors]
				weights, fur_length, fur_width, residue = export_weights(
					b_ob, b_vert, bones_table, hair_length, unweighted_vertices)
				if num_fur_weights:
					# append to uv
					uvs.append((fur_length, remap(fur_width, 0, 1, -16, 16)))
				# store all raw blender data
				verts.append((position, residue, normal, winding, tangent, uvs, vcols, weights, shapekey))
			tri.append(v_index)
		tris.append(tri)

	logging.debug(f"count_unique {count_unique}")
	logging.debug(f"count_reused {count_reused}")

	# report unweighted vertices
	if mesh.flag.weights:
		if unweighted_vertices:
			raise AttributeError(f"{b_ob.name} has {len(unweighted_vertices)} unweighted vertices!")

	# update vert & tri array
	mesh.base = model_info.pack_offset
	# transfer raw verts into mesh data packed array
	try:
		mesh.set_verts(verts)
	except ValueError as err:
		raise AttributeError(f"Could not export {b_ob.name}!")

	mesh.tris = tris
	return wrapper


def export_weights(b_ob, b_vert, bones_table, hair_length, unweighted_vertices):
	# defaults that may or may not be set later on
	residue = 1
	fur_length = 0
	fur_width = 0
	bone_index_cutoff = get_property(b_ob, "bone_index")
	# get the weights
	w = []
	for vertex_group in b_vert.groups:
		try:
			vgroup_name = b_ob.vertex_groups[vertex_group.group].name
			if vgroup_name == "residue":
				# if this is not rounded, somehow it affects the weights
				# might be a bug, but can't figure out where the rest is affected
				residue = int(round(vertex_group.weight))
			elif vgroup_name == "fur_length":
				fur_length = vertex_group.weight * hair_length
			elif vgroup_name == "fur_width":
				fur_width = vertex_group.weight
			elif vgroup_name in bones_table:
				# avoid dummy vertex groups without corresponding bones
				bone_index = bones_table[vgroup_name]
				if bone_index > bone_index_cutoff:
					logging.error(
						f"Mesh {b_ob.name} has weights for bone {vgroup_name} [{bone_index}] over the LOD's cutoff at {bone_index_cutoff}!"
						f"\nThis will cause distortions ingame!")
				w.append([bone_index, vertex_group.weight])
			else:
				logging.debug(f"Ignored extraneous vertex group {vgroup_name} on mesh {b_ob.name}!")
		except BaseException as err:
			logging.warning(f"Vert with {len(b_vert.groups)} groups, index {vertex_group.group} into {len(b_ob.vertex_groups)} groups failed in {b_ob.name}")
			traceback.print_exc()
	# print(residue)
	# get the 4 strongest influences on this vert
	weights_sorted = sorted(w, key=lambda x: x[1], reverse=True)[0:4]
	if not weights_sorted:
		# print("Sum of weights",sw)
		unweighted_vertices.append(b_vert.index)
	# print(weights_sorted)
	return weights_sorted, fur_length, fur_width, residue


def get_property(ob, prop_name):
	"""Ensure that custom property is set or raise an intellegible error"""
	if prop_name in ob:
		return ob[prop_name]
	else:
		raise KeyError(f"Custom property '{prop_name}' missing from {ob.name} (data: {type(ob).__name__}). Add it!")


def save(filepath='', apply_transforms=False, edit_bones=False, use_stock_normals_tangents=False):
	messages = set()
	start_time = time.time()

	logging.info(f"Exporting {filepath} into export subfolder...")
	if not os.path.isfile(filepath):
		raise FileNotFoundError(f"{filepath} does not exist. You must open an existing ms2 file for exporting.")

	old_dir, name = os.path.split(os.path.normpath(filepath))
	exp_dir = os.path.join(old_dir, "export")
	os.makedirs(exp_dir, exist_ok=True)
	export_path = os.path.join(exp_dir, name)
	ms2 = Ms2File()
	ms2.load(filepath)
	ms2.read_editable = True
	ms2.clear()

	model_info_lut = {mdl2_name: model_info for mdl2_name, model_info in zip(ms2.mdl_2_names, ms2.model_infos)}
	for scene in bpy.data.scenes:
		if scene.name not in model_info_lut:
			logging.warning(f"Scene '{scene.name}' was not found in the MS2 file, skipping")
			continue

		# make active scene
		bpy.context.window.scene = scene
		# ensure that we have objects in the scene
		if not has_objects_in_scene(scene):
			raise AttributeError(f"No objects in scene '{scene.name}', nothing to export!")
		b_armature_ob = get_armature(scene)
		if not b_armature_ob:
			raise AttributeError(f"No armature was found in scene '{scene.name}' - did you delete it?")
		# clear pose
		for pbone in b_armature_ob.pose.bones:
			pbone.matrix_basis = mathutils.Matrix()
	
		if not scene.cobra.pack_base:
			raise AttributeError(f"Set the pack base value for scene '{scene.name}'!")

		model_info = model_info_lut[scene.name]
		model_info.pack_offset = scene.cobra.pack_base
		model_info.render_flag._value = get_property(scene, "render_flag")
		if edit_bones:
			export_bones_custom(b_armature_ob, model_info)
		# used to get index from bone name for faster weights
		bones_table = dict(((b, i) for i, b in enumerate(get_bone_names(model_info))))
	
		b_models = []
		b_materials = []
		bounds = []
		# mesh_objects = [ob for ob in bpy.data.objects if type(ob.data) == bpy.types.Mesh and not ob.rigid_body]
		for lod_i in range(6):
			lod_group_name = f"{scene.name}_LOD{lod_i}"
			lod_coll = get_collection(lod_group_name)
			if not lod_coll:
				break
			m_lod = LodInfo(ms2.context)
			m_lod.distance = math.pow(30+15*lod_i, 2)
			m_lod.first_object_index = len(model_info.model.objects)
			m_lod.meshes = []
			m_lod.objects = []
			model_info.model.lods.append(m_lod)
			for b_ob in lod_coll.objects:
				# store & set bone index for lod
				m_lod.bone_index = get_property(b_ob, "bone_index")
	
				b_me = b_ob.data
				if b_me not in b_models:
					b_models.append(b_me)
					wrapper = export_model(model_info, lod_coll, b_ob, b_me, bones_table, bounds, apply_transforms, use_stock_normals_tangents)
					wrapper.mesh.lod_index = lod_i
				for b_mat in b_me.materials:
					if b_mat not in b_materials:
						b_materials.append(b_mat)
						export_material(model_info, b_mat)
						if "." in b_mat.name:
							messages.add(f"Material {b_mat.name} seems to be an unwanted duplication!")
					# create one unique mesh per material
					m_ob = Object(ms2.context)
					m_ob.mesh_index = b_models.index(b_me)
					m_ob.material_index = b_materials.index(b_mat)
					model_info.model.objects.append(m_ob)
					m_lod.meshes.append(model_info.model.meshes[m_ob.mesh_index])
					m_lod.objects.append(m_ob)
			m_lod.last_object_index = len(model_info.model.objects)
	
		export_bounds(bounds, model_info)

	# write modified ms2
	ms2.save(export_path)

	messages.add(f"Finished MS2 export in {time.time() - start_time:.2f} seconds")
	return messages


def get_hair_length(ob):
	if ob.particle_systems:
		psys = ob.particle_systems[0]
		return psys.settings.hair_length
	return 0


def fill_kd_tree(me):
	size = len(me.loops)
	kd = mathutils.kdtree.KDTree(size)
	uv_layer = me.uv_layers[0].data
	for i, loop in enumerate(me.loops):
		# include x coord in lookup to handle mirrored UVs
		lookup = uv_layer[loop.index].uv.to_3d()
		lookup.z = me.vertices[loop.vertex_index].co.x
		kd.insert(lookup, i)
	kd.balance()
	return kd
