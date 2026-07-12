import logging
import math
import mathutils
import random
import colorsys

import bpy
import numpy as np

from generated.formats.ms2.structs.packing_utils import has_nan
from generated.formats.ms2.enums.MeshFormat import MeshFormat
from plugin.utils.blender_util import set_auto_smooth_safe
from plugin.utils.shell import num_fur_as_weights, FUR_FIN


def per_loop(flattened_tris, per_vertex_input):
	return np.take(per_vertex_input, flattened_tris, axis=0)


def import_mesh_layers(b_me, mesh, use_custom_normals, mat_name, mesh_tris_flat, unique_indices):
	# set uv data
	# decide how to import the UVs according to mat_name
	num_uv_layers = mesh.uvs.shape[1]
	num_fur_weights = num_fur_as_weights(mat_name)
	if num_fur_weights:
		# fur is uv 1
		mesh.import_fur_as_weights(mesh.uvs[unique_indices, num_fur_weights])
		# so just use uv 0 as actual uv
		num_uv_layers = 1
	for uv_i in range(num_uv_layers):
		uvs = mesh.uvs[:, uv_i].copy()
		uvs[:, 1] = 1.0 - uvs[:, 1]
		b_me.uv_layers.new(name=f"UV{uv_i}")
		b_me.uv_layers[-1].data.foreach_set("uv", per_loop(mesh_tris_flat, uvs).flatten())
	if mesh.get_vcol_count():
		# num_vcol_layers = mesh.colors.shape[1]
		# for col_i in range(num_vcol_layers):
		cols = b_me.attributes.new(f"RGBA{0}", "BYTE_COLOR", "CORNER")
		cols.data.foreach_set("color", per_loop(mesh_tris_flat, mesh.colors).flatten())
		if num_fur_weights:
			mesh.import_vcol_a_as_weights(mesh.colors[unique_indices])

	if hasattr(mesh, "tangents"):
		tangents = b_me.attributes.new("ct_tangents", "FLOAT_VECTOR", "CORNER")
		tangents.data.foreach_set("vector", per_loop(mesh_tris_flat, mesh.tangents).flatten())

	if hasattr(mesh, "normals"):
		normals = b_me.attributes.new("ct_normals", "FLOAT_VECTOR", "CORNER")
		normals.data.foreach_set("vector", per_loop(mesh_tris_flat, mesh.normals).flatten())

	# set faces to smooth
	b_me.polygons.foreach_set('use_smooth', [True] * len(b_me.polygons))
	# set normals if desired and safe to do so; crash on fur fin geometry due to zero area faces
	if use_custom_normals and not mat_name.lower().endswith(FUR_FIN):
		set_auto_smooth_safe(b_me)
		normals = mesh.normals_custom if mesh.is_speedtree else mesh.normals
		b_me.normals_split_custom_set(per_loop(mesh_tris_flat, normals))


def import_shapekeys(b_ob, mesh, unique_indices):
	b_me = b_ob.data
	if (mesh.flag == 517 and mesh.expect_shapekeys) or mesh.mesh_format in (MeshFormat.SPEEDTREE_32, MeshFormat.FOLIAGE_24,):
		# insert base key
		b_ob.shape_key_add(name="Basis")
		b_me.shape_keys.use_relative = True

		for v_index, v in enumerate(mesh.lod_keys[unique_indices]):
			b_me.vertices[v_index].co = v
		b_ob.shape_key_add(name="LOD", from_mix=False)
		# optional dissolve shape key
		if not has_nan(mesh.center_keys[unique_indices]):
			for v_index, v in enumerate(mesh.center_keys[unique_indices]):
				b_me.vertices[v_index].co = v[:3]
			b_ob.shape_key_add(name="Center", from_mix=False)
		if hasattr(mesh, "whatever_range"):
			b_me["whatever_range"] = float(mesh.whatever_range)


def ob_postpro(use_mirror_mesh, quadrify):
	logging.debug("Postprocessing geometry")
	bpy.ops.object.mode_set(mode='EDIT')
	if use_mirror_mesh:
		bpy.ops.mesh.bisect(plane_co=(0, 0, 0), plane_no=(1, 0, 0), clear_inner=True)
		bpy.ops.mesh.select_all(action='SELECT')
	bpy.ops.uv.select_all(action='SELECT')
	bpy.ops.uv.seams_from_islands()
	if quadrify:
		bpy.ops.mesh.tris_convert_to_quads(uvs=True, vcols=True, seam=True, sharp=True)
	bpy.ops.object.mode_set(mode='OBJECT')


def append_mirror_modifier(b_ob):
	mod = b_ob.modifiers.new('Mirror', 'MIRROR')
	mod.use_clip = True
	mod.use_mirror_merge = True
	mod.use_mirror_vertex_groups = True
	# mod.use_x = True
	mod.use_axis = (True, False, False)
	mod.merge_threshold = 0.001


def get_valid_lod_objects(m_lod):
	"""Get objects, but skip later shells for JWE2"""
	for m_ob in m_lod.objects:
		mesh = m_ob.mesh
		if hasattr(mesh, "vert_chunks"):
			tri_chunk = mesh.tri_chunks[0]
			if tri_chunk.shell_index:
				logging.debug(f"Skipping import of shell duplicate {tri_chunk.shell_index}")
				continue
		yield m_ob


def import_mesh_properties(b_me, mesh):
	try:
		# store mesh unknowns
		# cast the bitfield to int
		b_me["flag"] = int(mesh.flag)
		if mesh.context.version > 13:
			b_me["unk_f0"] = float(mesh.unk_float_0)
		if mesh.context.version > 32:
			b_me["unk_f1"] = float(mesh.unk_float_1)
		if hasattr(mesh, "vert_chunks"):
			tri_chunk = mesh.tri_chunks[0]
			b_me["shell_count"] = tri_chunk.shell_count
		if mesh.context.version > 53:
			vert_chunk = mesh.vert_chunks[0]
			b_me["material_effects"] = vert_chunk.weights_flag.material_effects
	except:
		logging.exception("Setting unks failed")


# ==========================================================
# VISUALIZATION UTILS
# ==========================================================

def create_random_material(name):
	"""Creates a Principled BSDF material with a random bright color."""
	mat = bpy.data.materials.new(name=name)
	mat.use_nodes = True
	bsdf = mat.node_tree.nodes.get("Principled BSDF")
	if bsdf:
		h = random.random()
		s = 0.8 + random.random() * 0.2
		v = 0.8 + random.random() * 0.2
		r, g, b = colorsys.hsv_to_rgb(h, s, v)
		bsdf.inputs['Base Color'].default_value = (r, g, b, 1.0)
	return mat

def build_aabb_mesh(name, game_min, game_max, coll):
	"""Builds a wireframe bounding box from Game-space Min/Max coordinates."""
	
	# ==========================================
	# Game -> Blender AABB Swizzling
	# Blender(X, Y, Z) = Game(-X, -Z, Y)
	# Negated axes swap the Min and Max references
	# ==========================================
	
	b_min = (
		-game_max[0], # bMinX = -gMaxX
		-game_max[2], # bMinY = -gMaxZ
		 game_min[1]  # bMinZ =  gMinY
	)
	
	b_max = (
		-game_min[0], # bMaxX = -gMinX
		-game_min[2], # bMaxY = -gMinZ
		 game_max[1]  # bMaxZ =  gMaxY
	)

	# The 8 corners of the AABB
	verts = [
		(b_min[0], b_min[1], b_min[2]), # 0: Bottom-Left-Front
		(b_max[0], b_min[1], b_min[2]), # 1: Bottom-Right-Front
		(b_max[0], b_max[1], b_min[2]), # 2: Bottom-Right-Back
		(b_min[0], b_max[1], b_min[2]), # 3: Bottom-Left-Back
		(b_min[0], b_min[1], b_max[2]), # 4: Top-Left-Front
		(b_max[0], b_min[1], b_max[2]), # 5: Top-Right-Front
		(b_max[0], b_max[1], b_max[2]), # 6: Top-Right-Back
		(b_min[0], b_max[1], b_max[2]), # 7: Top-Left-Back
	]

	# The 6 faces of the cube
	faces = [
		(0, 1, 2, 3), # Bottom
		(4, 7, 6, 5), # Top
		(0, 4, 5, 1), # Front
		(1, 5, 6, 2), # Right
		(2, 6, 7, 3), # Back
		(3, 7, 4, 0)  # Left
	]

	mesh = bpy.data.meshes.new(name)
	mesh.from_pydata(verts, [], faces)
	mesh.update()

	obj = bpy.data.objects.new(name, mesh)
	obj.display_type = 'WIRE' # Set to wireframe so it acts like a bounds box visualizer
	
	coll.objects.link(obj)
	return obj

def build_cone_mesh(name, apex, axis, cutoff, length, coll):
	"""Builds a 4-sided pyramid wireframe to visualize the cone."""
	cutoff = max(-1.0, min(1.0, cutoff))
	angle_half = math.acos(cutoff)
	angle_half = min(angle_half, math.radians(89.9))
	
	R = length * math.tan(angle_half)
	L = length
	
	# Base points for the cone pointing down +Z locally
	verts = [(0, 0, 0), (R, 0, L), (0, R, L), (-R, 0, L), (0, -R, L)]
	faces = [(0, 1, 2), (0, 2, 3), (0, 3, 4), (0, 4, 1), (1, 4, 3, 2)]
	
	mesh = bpy.data.meshes.new(name)
	mesh.from_pydata(verts, [], faces)
	mesh.update()
	
	obj = bpy.data.objects.new(name, mesh)
	
	# ==========================================
	# Game -> Blender Coordinate Swizzling
	# Rule: Blender(X, Y, Z) = Game(-X, -Z, Y)
	# ==========================================
	
	# 1. Swizzle the Apex (Location)
	blender_apex = (-apex[0], -apex[2], apex[1])
	obj.location = blender_apex
	
	# 2. Swizzle the Axis (Direction)
	blender_axis = mathutils.Vector((-axis[0], -axis[2], axis[1]))
	
	if blender_axis.length > 0.0001:
		blender_axis.normalize()
		# Align the cone's local +Z axis to point in the direction of the swizzled axis
		z_axis = mathutils.Vector((0, 0, 1))
		obj.rotation_mode = 'QUATERNION'
		obj.rotation_quaternion = z_axis.rotation_difference(blender_axis)
	
	obj.display_type = 'WIRE'
	coll.objects.link(obj)
	return obj

def visualize_chunks(mesh, b_ob_name, coll):
	"""Generates meshes for chunks, applies random materials, and builds bounds cones grouped by AABB."""

	# Create the main parent collection for all chunks of this object
	viz_coll_name = f"Chunks_{b_ob_name}"
	if viz_coll_name in bpy.data.collections:
		main_viz_coll = bpy.data.collections[viz_coll_name]
	else:
		main_viz_coll = bpy.data.collections.new(viz_coll_name)
		coll.children.link(main_viz_coll)

	# Dictionary to store unique bounding box groups
	# Key: tuple of rounded bbox coordinates, Value: Blender Collection
	bbox_collections = {}
	bbox_group_counter = 0

	vert_offset = 0
	for chunk_index, (vert_chunk, tri_chunk) in enumerate(zip(mesh.vert_chunks, mesh.tri_chunks)):
		# Determine the group
		if hasattr(vert_chunk, '_foliage_bbox'):
			# Round to 4 decimals to avoid float16 precision drift making identical boxes appear unique
			bbox_key = tuple(round(float(x), 4) for x in vert_chunk._foliage_bbox[0:6])
			game_min = vert_chunk._foliage_bbox[0:3]
			game_max = vert_chunk._foliage_bbox[3:6]
		else:
			# Fallback if a chunk doesn't have a bounding box
			bbox_key = None
			game_min = None
			game_max = None

		# Create group per unique AABB
		if bbox_key not in bbox_collections:
			if bbox_key is None:
				sub_coll_name = f"No_BBox_{b_ob_name}"
			else:
				sub_coll_name = f"BBox_Group_{bbox_group_counter}_{b_ob_name}"
				bbox_group_counter += 1
			
			sub_coll = bpy.data.collections.new(sub_coll_name)
			main_viz_coll.children.link(sub_coll)
			bbox_collections[bbox_key] = sub_coll
			
			# Build the AABB mesh once
			if bbox_key is not None:
				build_aabb_mesh(
					f"AABB_{sub_coll_name}", 
					game_min, 
					game_max, 
					sub_coll
				)

		# Retrieve the target collection for this specific chunk
		chunk_coll = bbox_collections[bbox_key]

		# Build the chunk mesh
		# MS2 tri indices are flat sequential offsets on read, subtract the current offset 
		local_indices = tri_chunk.tri_indices - vert_offset
		local_indices = np.clip(local_indices, 0, vert_chunk.vertex_count - 1)
		
		# Re-shape to standard blender Nx3 triangles and reverse for orientation
		faces_2d = np.reshape(local_indices, (-1, 3))
		faces_2d = np.flip(faces_2d, axis=-1)
		
		chunk_mesh = bpy.data.meshes.new(f"Chunk_{chunk_index}_{b_ob_name}")
		chunk_mesh.from_pydata(vert_chunk.vertices.tolist(), [], faces_2d.tolist())
		chunk_mesh.update()
		
		chunk_obj = bpy.data.objects.new(f"Chunk_{chunk_index}_{b_ob_name}", chunk_mesh)
		# Link into the specific BBox group collection!
		chunk_coll.objects.link(chunk_obj)
		
		mat = create_random_material(f"Mat_Chunk_{chunk_index}")
		chunk_obj.data.materials.append(mat)
		
		# Calculate radius bound for the cone scale limit
		if len(vert_chunk.vertices) > 0:
			v_max = np.max(vert_chunk.vertices, axis=0)
			v_min = np.min(vert_chunk.vertices, axis=0)
			center = (v_max + v_min) / 2.0
			radius = np.max(np.linalg.norm(vert_chunk.vertices - center, axis=1))
		else:
			radius = 1.0
			
		if radius < 0.001: 
			radius = 1.0
		
		# Build the cone mesh
		if hasattr(tri_chunk, 'cone_apex'):
			apex = tri_chunk.cone_apex
		else:
			apex = [0.0, 0.0, 0.0]

		if hasattr(tri_chunk, 'cone_cutoff'):
			cutoff = tri_chunk.cone_cutoff
		else:
			cutoff = 1.0

		if hasattr(tri_chunk, 'cone_axis'):
			axis = tri_chunk.cone_axis
		else:
			axis = [0.0, 0.0, 0.0]
		
		# Check degenerate zeroes condition
		is_degenerate = (abs(axis[0]) < 1e-5 and abs(axis[1]) < 1e-5 and abs(axis[2]) < 1e-5)
		if not is_degenerate:
			cone_obj = build_cone_mesh(
				f"Cone_{chunk_index}_{b_ob_name}", 
				apex, 
				axis, 
				cutoff, 
				radius,
				chunk_coll # Link cone into the BBox group collection
			)
			cone_obj.parent = chunk_obj

		# Build the tri chunk bounds
		if hasattr(tri_chunk, 'bounds'):
			# tri_chunk.bounds[axis][min/max] (3x2 array)
			tri_bounds = tri_chunk.bounds
			
			# Extract Min [X, Y, Z] and Max [X, Y, Z]
			tri_min = [tri_bounds[0][0], tri_bounds[1][0], tri_bounds[2][0]]
			tri_max = [tri_bounds[0][1], tri_bounds[1][1], tri_bounds[2][1]]
			
			# Re-use our swizzling AABB builder!
			tri_aabb_obj = build_aabb_mesh(
				f"TriBounds_{chunk_index}_{b_ob_name}", 
				tri_min, 
				tri_max, 
				chunk_coll
			)
			tri_aabb_obj.parent = chunk_obj
			
		vert_offset += vert_chunk.vertex_count