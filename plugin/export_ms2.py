import logging
import math
import os
import time
import struct

import bpy
import mathutils

from generated.formats.ms2.compounds.LodInfo import LodInfo
from generated.formats.ms2.compounds.MaterialName import MaterialName
from generated.formats.ms2.compounds.MeshDataWrap import MeshDataWrap
from generated.formats.ms2.compounds.Object import Object
from generated.formats.ms2 import Ms2File
from generated.formats.ms2.compounds.packing_utils import remap, USHORT_MAX
from generated.formats.ms2.enums.MeshFormat import MeshFormat
from plugin.import_ms2 import num_fur_as_weights
from plugin.modules_export.armature import get_armature, handle_transforms, export_bones_custom
from plugin.modules_export.collision import export_bounds
from plugin.modules_import.armature import get_bone_names
from plugin.utils.matrix_util import evaluate_mesh
from plugin.utils.object import NedryError
from plugin.utils.shell import get_collection, is_shell, is_fin
from root_path import root_dir

mesh_mode = os.path.isdir(os.path.join(root_dir, ".git"))
DISCARD_STATIC_TRIS = 16
DYNAMIC_ID = -1
NO_BONES_ID = -2
SOFT_MAX_VERTS = 200
SOFT_MAX_TRIS = 200


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
	mesh.stream_info.offset = get_property(b_me, "stream")

	# register this format for all vert chunks that will be created later
	if mesh.context.biosyn:
		mesh.mesh_format = MeshFormat[b_me.cobra.mesh_format]
		# if not mesh_mode:
		# 	if mesh.mesh_format == MeshFormat.SEPARATE:
		# 		raise NedryError()
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
			(len(b_me.uv_layers) + num_fur_weights, num_uvs, "UV"),
			(len(b_me.vertex_colors), num_vcols, "Vertex Color")):
		logging.debug(f"{name_type} count: {num_type}")
		if len_type != num_type:
			raise AttributeError(f"Mesh {b_ob.name} has {len_type} {name_type} layers, but {num_type} were expected!")

	# make sure the mesh has a triangulation modifier
	ensure_tri_modifier(b_ob)
	eval_obj, eval_me = evaluate_mesh(b_ob)
	handle_transforms(eval_obj, eval_me, apply=apply_transforms)
	bounds.append(eval_obj.bound_box)

	hair_length = get_hair_length(b_ob)
	mesh.fur_length = hair_length

	# tangents have to be pre-calculated; this will also calculate loop normal
	eval_me.calc_tangents()

	# these were stored on import per loop
	if use_stock_normals_tangents:
		ct_tangents = eval_me.attributes["ct_tangents"]
		ct_normals = eval_me.attributes["ct_normals"]
	if "RGBA0" in eval_me.attributes:
		rgba0_layer = eval_me.attributes["RGBA0"]
	else:
		rgba0_layer = None

	unweighted_vertices = []

	shell_ob = None
	shapekey = (0, 0, 0)
	vcols = (0, 0, 0, 0)

	validate_vertex_groups(b_ob, bones_table)
	# calculate bone weights per vertex first to reuse data
	# vertex_bone_id, weights, fur_length, fur_width
	weights_data = [export_weights(b_ob, b_vert, bones_table, hair_length, unweighted_vertices) for b_vert in
					eval_me.vertices]

	# report unweighted vertices
	should_have_no_weights = (hasattr(mesh.flag, "weights") and not mesh.flag.weights)
	if unweighted_vertices and bones_table:
		if should_have_no_weights:
			logging.info(f"Should have no weights and has none.")
		else:
			raise AttributeError(f"{b_ob.name} has {len(unweighted_vertices)} unweighted vertices!")

	# fin meshes have to grab tangents from shell
	if is_fin(b_ob):
		shell_obs = [ob for ob in b_lod_coll.objects if is_shell(ob) and ob is not b_ob]
		if shell_obs:
			shell_ob = shell_obs[0]
			logging.debug(f"Copying data for {b_ob.name} from base mesh {shell_ob.name}...")
			shell_eval_ob, shell_eval_me = evaluate_mesh(shell_ob)
			shell_eval_me.calc_tangents()
			shell_kd = fill_kd_tree(shell_eval_me)
			fin_uv_layer = eval_me.uv_layers[0].data

	if mesh.context.biosyn:
		t_map = {}
		# check which bones are used per face
		for face in eval_me.polygons:
			r = list(set(weights_data[v_index][0] for v_index in face.vertices))
			# are there weights at all?
			if not bones_table:
				face_vertex_bone_id = NO_BONES_ID
			# do all verts of this face use the same bone id?
			elif len(r) == 1:
				face_vertex_bone_id = r[0]
			else:
				face_vertex_bone_id = DYNAMIC_ID
			# append face for this bone id
			if face_vertex_bone_id not in t_map:
				t_map[face_vertex_bone_id] = list()
			t_map[face_vertex_bone_id].append(face)
		# deleting small static chunks only on dynamic meshes, static meshes will not have -1 in
		if DYNAMIC_ID in t_map:
			for face_vertex_bone_id, bone_tris in tuple(t_map.items()):
				# delete small static chunk
				if face_vertex_bone_id != DYNAMIC_ID and len(bone_tris) < DISCARD_STATIC_TRIS:
					logging.info(f"Moving {len(bone_tris)} tris for bone {face_vertex_bone_id} to dynamic chunk")
					v_list = t_map.pop(face_vertex_bone_id)
					t_map[DYNAMIC_ID].extend(v_list)
		# now try to sort the tris so that vertices are re-used as often as possible
		sort_tri_map(t_map)
		# for face_vertex_bone_id, bone_tris in tuple(t_map.items()):
		# 	t_map[face_vertex_bone_id] = list(sorted(bone_tris, key=lambda x: tuple(x.vertices)))
	else:
		# no chunking by weights, just take all faces
		t_map = {-1: eval_me.polygons}

	# stores values retrieved from blender, will be packed into array later
	verts = []
	# list of tri lists to support chunks
	# always add to last entry
	tris_chunks = []
	for b_chunk_bone_id, b_chunk_faces in t_map.items():
		logging.info(f"Exporting {len(b_chunk_faces)} tris for bone index {b_chunk_bone_id}")
		# create new chunk
		tris_chunks.append((b_chunk_bone_id, []))
		# use a dict mapping dummy vertices to their index for fast lookup
		# this is used to convert blender vertices (several UVs, normals per face corner) to ms2 vertices
		dummy_vertices = {}
		count_unique = 0
		count_reused = 0
		# loop faces and collect unique and repeated vertices
		for face in b_chunk_faces:
			if len(face.loop_indices) != 3:
				# this is a bug - we are applying the triangulation modifier above
				raise AttributeError(f"Mesh {b_ob.name} is not triangulated!")

			if mesh.context.biosyn:
				# tris are apparently not allowed to exceed 64 in stock
				# seen chunks with more than 100 verts
				if len(dummy_vertices) >= SOFT_MAX_VERTS or len(tris_chunks[-1][1]) >= SOFT_MAX_TRIS:
					logging.debug(f"Starting new chunk")
					tris_chunks.append((b_chunk_bone_id, []))
					dummy_vertices = {}
					count_unique = 0
					count_reused = 0

			# build indices into vertex buffer for the current face and chunk
			tri = []
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
					normal = shell_loop.normal
					tangent = shell_loop.tangent
					negate_bitangent = False
				else:
					normal = b_loop.normal
					tangent = b_loop.tangent
					negate_bitangent = b_loop.bitangent_sign < 0.0
				# reindeer is a special case: has edited beard normals pointing straight down for shell & fins
				# if the custom normal is used, the tangent generated by blender does not appear to be correct
				# override with custom data if asked
				if use_stock_normals_tangents:
					normal = ct_normals.data[loop_index].vector
					tangent = ct_tangents.data[loop_index].vector

				# shape key morphing
				b_key = b_me.shape_keys
				if b_key and len(b_key.key_blocks) > 1:
					lod_key = b_key.key_blocks[1]
					# yes, there is a key object attached
					if lod_key.name.startswith("LOD"):
						shapekey = lod_key.data[b_loop.vertex_index].co

				uvs = [(layer.data[loop_index].uv.x, 1 - layer.data[loop_index].uv.y) for layer in eval_me.uv_layers]
				# create a dummy bytes str for indexing
				float_items = [c for uv in uvs[:2] for c in uv] + [*normal]
				dummy = struct.pack(f'<HB{len(float_items)}f', b_loop.vertex_index, negate_bitangent, *float_items)

				# see if this dummy key exists
				try:
					# if it does - reuse it by grabbing its index from the dict
					v_index = dummy_vertices[dummy]
					count_reused += 1
				except KeyError:
					# it doesn't, so we have to fill in additional data
					v_index = count_unique
					if v_index > USHORT_MAX:
						raise OverflowError(
							f"{b_ob.name} has too many ms2 verts. The limit is {USHORT_MAX}. "
							f"\nBlender vertices have to be duplicated on every UV seam, hence the increase.")
					dummy_vertices[dummy] = v_index
					count_unique += 1

					# now collect any missing vert data that was not needed for the splitting of blender verts
					# use attribute api, ensure fallback so array setting does not choke
					if rgba0_layer:
						vcols = rgba0_layer.data[loop_index].color
					vertex_bone_id, weights, fur_length, fur_width = weights_data[b_loop.vertex_index]
					if num_fur_weights:
						# append to uv
						uvs.append((fur_length, remap(fur_width, 0, 1, -16, 16)))
					# store all raw blender data
					verts.append((position, vertex_bone_id == DYNAMIC_ID, normal, negate_bitangent, tangent, uvs, vcols,
								  weights, shapekey))
				tri.append(v_index)
			# add it to the latest chunk
			tris_chunks[-1][1].append(tri)

		logging.debug(f"count_unique {count_unique}")
		logging.debug(f"count_reused {count_reused}")
	logging.debug(f"count_chunks {len(tris_chunks)}")

	# update vert & tri array
	mesh.pack_base = model_info.pack_base
	# transfer raw verts into mesh data packed array
	mesh.tris = tris_chunks
	try:
		mesh.set_verts(verts)
	except ValueError as err:
		raise AttributeError(f"Could not export {b_ob.name}!")
	return wrapper


def sort_tri_map(t_map):
	for face_vertex_bone_id, bone_tris in tuple(t_map.items()):
		tris_per_v_index = {}
		added_tris = set()
		for f in bone_tris:
			for v_index in f.vertices:
				if v_index not in tris_per_v_index:
					tris_per_v_index[v_index] = set()
				if f not in added_tris:
					added_tris.add(f)
					tris_per_v_index[v_index].add(f)
		current_tri = bone_tris[0]
		sorted_tris = []
		while current_tri:
			all_neighbors = set()
			for v_index in current_tri.vertices:
				neighbor_tris = tris_per_v_index.pop(v_index, [])
				all_neighbors.update(neighbor_tris)
				if neighbor_tris:
					for tri in neighbor_tris:
						if tri not in sorted_tris:
							sorted_tris.append(tri)
							added_tris.remove(tri)
				else:
					# neighbors are used up, continue, with a new tri
					if added_tris:
						current_tri = next(iter(added_tris))
					else:
						current_tri = None
			if all_neighbors:
				for neighbor in all_neighbors:
					for v_index in neighbor.vertices:
						if v_index in tris_per_v_index:
							current_tri = neighbor
							break
		assert len(sorted_tris) == len(bone_tris)
		t_map[face_vertex_bone_id] = sorted_tris


def validate_vertex_groups(b_ob, bones_table):
	for v_group in b_ob.vertex_groups:
		if v_group.name in bones_table:
			continue
		elif v_group.name in ("fur_width", "fur_length"):
			continue
		else:
			logging.warning(f"Ignored extraneous vertex group {v_group.name} on mesh {b_ob.name}")


def export_weights(b_ob, b_vert, bones_table, hair_length, unweighted_vertices):
	# defaults that may or may not be set later on
	# True if used, bone index if it isn't
	vertex_bone_id = DYNAMIC_ID
	fur_length = 0
	fur_width = 0
	bone_index_cutoff = get_property(b_ob, "bone")
	# get the weights
	w = []
	for v_group in b_vert.groups:
		try:
			v_group_name = b_ob.vertex_groups[v_group.group].name
			if v_group_name == "fur_length":
				fur_length = v_group.weight * hair_length
			elif v_group_name == "fur_width":
				fur_width = v_group.weight
			elif v_group_name in bones_table:
				# avoid dummy vertex groups without corresponding bones
				bone_index = bones_table[v_group_name]
				if bone_index > bone_index_cutoff:
					logging.error(
						f"Mesh {b_ob.name} has weights for bone {v_group_name} [{bone_index}] over the LOD's cutoff at {bone_index_cutoff}!"
						f"\nThis will cause distortions ingame!")
				if v_group.weight > 0.0:
					w.append([bone_index, v_group.weight])
		except:
			logging.exception(
				f"Vert with {len(b_vert.groups)} groups, index {v_group.group} into {len(b_ob.vertex_groups)} groups failed in {b_ob.name}")
	# get the strongest influences on this vert, truncate to 4
	weights_sorted = sorted(w, key=lambda x: x[1], reverse=True)[:4]
	# are there any weights at all
	if not weights_sorted:
		unweighted_vertices.append(b_vert.index)
	# this should no longer happen
	# is the strongest one actually weighted
	elif not weights_sorted[0][1] > 0.0:
		unweighted_vertices.append(b_vert.index)
	# more than one valid bone weight for this vertex?
	elif len(weights_sorted) == 1:
		vertex_bone_id = weights_sorted[0][0]
	return vertex_bone_id, weights_sorted, fur_length, fur_width


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
		if not scene.cobra.pack_base:
			raise AttributeError(f"Set the pack base value for scene '{scene.name}'!")

		model_info = model_info_lut[scene.name]
		model_info.pack_base = scene.cobra.pack_base
		model_info.render_flag._value = get_property(scene, "render_flag")
		# ensure that we have objects in the scene
		if not has_objects_in_scene(scene):
			raise AttributeError(f"No objects in scene '{scene.name}', nothing to export!")

		b_armature_ob = get_armature(scene)
		if not b_armature_ob:
			logging.warning(f"No armature was found in scene '{scene.name}' - did you delete it?")
		else:
			# clear pose
			for pbone in b_armature_ob.pose.bones:
				pbone.matrix_basis = mathutils.Matrix()
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
			m_lod.distance = math.pow(30 + 15 * lod_i, 2)
			m_lod.first_object_index = len(model_info.model.objects)
			m_lod.meshes = []
			m_lod.objects = []
			model_info.model.lods.append(m_lod)
			for b_ob in lod_coll.objects:
				b_me = b_ob.data
				# store & set bone index for lod
				m_lod.bone_index = get_property(b_ob, "bone")
				m_lod.stream_index = get_property(b_me, "stream")
				if b_me not in b_models:
					b_models.append(b_me)
					wrapper = export_model(model_info, lod_coll, b_ob, b_me, bones_table, bounds, apply_transforms,
										   use_stock_normals_tangents)
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
					wrapper = model_info.model.meshes[m_ob.mesh_index]
					m_lod.meshes.append(wrapper)
					if wrapper.context.biosyn:
						logging.info(f"Setting chunk material indices")
						for tri_chunk in wrapper.mesh.tri_chunks:
							tri_chunk.material_index = m_ob.material_index
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
