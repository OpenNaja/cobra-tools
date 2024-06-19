# import bmesh
import logging

import bpy

from generated.formats.ms2.compounds.packing_utils import has_nan
from generated.formats.ms2.enums.MeshFormat import MeshFormat
from plugin.utils.shell import num_fur_as_weights, is_fin


def per_loop(b_me, per_vertex_input):
	return [c for col in [per_vertex_input[l.vertex_index] for l in b_me.loops] for c in col]


def import_mesh_layers(b_me, mesh, use_custom_normals, mat_name):
	# set uv data
	# decide how to import the UVs according to mat_name
	num_uv_layers = mesh.uvs.shape[1]
	num_fur_weights = num_fur_as_weights(mat_name)
	if num_fur_weights:
		# fur is uv 1
		mesh.import_fur_as_weights(mesh.uvs[:, num_fur_weights])
		# so just use uv 0 as actual uv
		num_uv_layers = 1
	for uv_i in range(num_uv_layers):
		uvs = mesh.uvs[:, uv_i]
		b_me.uv_layers.new(name=f"UV{uv_i}")
		b_me.uv_layers[-1].data.foreach_set(
			"uv", [uv for pair in [uvs[l.vertex_index] for l in b_me.loops] for uv in (pair[0], 1 - pair[1])])
	if mesh.get_vcol_count():
		# num_vcol_layers = mesh.colors.shape[1]
		# for col_i in range(num_vcol_layers):
		cols = b_me.attributes.new(f"RGBA{0}", "BYTE_COLOR", "CORNER")
		cols.data.foreach_set("color", per_loop(b_me, mesh.colors))
		if num_fur_weights:
			mesh.import_vcol_a_as_weights(mesh.colors)

	if hasattr(mesh, "tangents"):
		tangents = b_me.attributes.new("ct_tangents", "FLOAT_VECTOR", "CORNER")
		tangents.data.foreach_set("vector", per_loop(b_me, mesh.tangents))

	if hasattr(mesh, "normals"):
		normals = b_me.attributes.new("ct_normals", "FLOAT_VECTOR", "CORNER")
		normals.data.foreach_set("vector", per_loop(b_me, mesh.normals))

	# set faces to smooth
	b_me.polygons.foreach_set('use_smooth', [True] * len(b_me.polygons))
	# set normals
	if use_custom_normals and mesh.flag not in (565,):
		b_me.use_auto_smooth = True
		normals = mesh.normals_custom if mesh.is_speedtree else mesh.normals
		b_me.normals_split_custom_set_from_vertices(normals)


# def remove_doubles_bmesh(b_me):
# 	# no operator, but bmesh
# 	bm = bmesh.new()
# 	bm.from_mesh(b_me)
# 	bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=0.0)
# 	bm.to_mesh(b_me)
# 	b_me.update()
# 	bm.clear()
# 	bm.free()

def import_shapekeys(b_ob, mesh):
	b_me = b_ob.data
	if (mesh.flag == 517 and mesh.expect_shapekeys) or mesh.mesh_format == MeshFormat.SPEEDTREE_32:
		# insert base key
		b_ob.shape_key_add(name="Basis")
		b_me.shape_keys.use_relative = True

		for v_index, v in enumerate(mesh.lod_keys):
			b_me.vertices[v_index].co = v
		b_ob.shape_key_add(name="LOD", from_mix=False)
		# optional dissolve shape key
		if not has_nan(mesh.center_keys):
			for v_index, v in enumerate(mesh.center_keys):
				b_me.vertices[v_index].co = v[:3]
			b_ob.shape_key_add(name="Center", from_mix=False)
		b_me["whatever_range"] = float(mesh.whatever_range)


def ob_postpro(b_ob, use_mirror_mesh, use_custom_normals):
	logging.debug("Postprocessing geometry")
	bpy.ops.object.mode_set(mode='EDIT')
	if use_mirror_mesh:
		bpy.ops.mesh.bisect(plane_co=(0, 0, 0), plane_no=(1, 0, 0), clear_inner=True)
		bpy.ops.mesh.select_all(action='SELECT')
	bpy.ops.mesh.tris_convert_to_quads()
	bpy.ops.uv.select_all(action='SELECT')
	bpy.ops.uv.seams_from_islands()
	# shells are messed up by remove doubles, affected faces have their dupe faces removed
	# since we are now stripping shells, shell meshes can use remove doubles but fins still can not
	if not use_custom_normals and not is_fin(b_ob):
		bpy.ops.mesh.remove_doubles(threshold=0.0, use_unselected=False)
		# remove_doubles_bmesh(b_me)
	bpy.ops.object.mode_set(mode='OBJECT')


def append_mirror_modifier(b_ob):
	mod = b_ob.modifiers.new('Mirror', 'MIRROR')
	mod.use_clip = True
	mod.use_mirror_merge = True
	mod.use_mirror_vertex_groups = True
	# mod.use_x = True
	mod.use_axis = (True, False, False)
	mod.merge_threshold = 0.001
