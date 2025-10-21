import logging

import bpy
import numpy as np

from generated.formats.ms2.structs.packing_utils import has_nan
from generated.formats.ms2.enums.MeshFormat import MeshFormat
from plugin.utils.blender_util import set_auto_smooth_safe
from plugin.utils.shell import num_fur_as_weights


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
	# set normals
	if use_custom_normals and mesh.flag not in (565,):
		set_auto_smooth_safe(b_me)
		normals = mesh.normals_custom if mesh.is_speedtree else mesh.normals
		b_me.normals_split_custom_set(per_loop(mesh_tris_flat, normals))


def import_shapekeys(b_ob, mesh, unique_indices):
	b_me = b_ob.data
	if (mesh.flag == 517 and mesh.expect_shapekeys) or mesh.mesh_format == MeshFormat.SPEEDTREE_32:
		# insert base key
		b_ob.shape_key_add(name="Basis")
		b_me.shape_keys.use_relative = True

		for v_index, v in enumerate(mesh.lod_keys[unique_indices]):
			b_me.vertices[v_index].co = v
		b_ob.shape_key_add(name="LOD", from_mix=False)
		# optional dissolve shape key
		if not has_nan(mesh.center_keys[unique_indices]):
			for v_index, v in enumerate(mesh.center_keys):
				b_me.vertices[v_index].co = v[:3]
			b_ob.shape_key_add(name="Center", from_mix=False)
		b_me["whatever_range"] = float(mesh.whatever_range)


def ob_postpro(use_mirror_mesh):
	logging.debug("Postprocessing geometry")
	bpy.ops.object.mode_set(mode='EDIT')
	if use_mirror_mesh:
		bpy.ops.mesh.bisect(plane_co=(0, 0, 0), plane_no=(1, 0, 0), clear_inner=True)
		bpy.ops.mesh.select_all(action='SELECT')
	bpy.ops.uv.select_all(action='SELECT')
	bpy.ops.uv.seams_from_islands()
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