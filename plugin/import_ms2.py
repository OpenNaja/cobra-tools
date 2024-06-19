import logging
import os
import time

import bpy
# import bmesh

from plugin.modules_import.armature import import_armature, append_armature_modifier, import_vertex_groups, \
	get_bone_names
from plugin.modules_import.material import import_material
from plugin.utils.hair import add_psys
from plugin.utils.shell import is_fin, num_fur_as_weights, is_shell, gauge_uv_scale_wrapper
from plugin.utils.object import create_ob, create_scene, create_collection, set_collection_visibility
from generated.formats.ms2 import Ms2File
from generated.formats.ms2.enums.MeshFormat import MeshFormat
from generated.formats.ms2.compounds.packing_utils import has_nan


def load(reporter, filepath="", use_custom_normals=False, mirror_mesh=False):
	start_time = time.time()
	in_dir, ms2_name = os.path.split(filepath)
	ms2_basename = os.path.splitext(ms2_name)[0]
	ms2 = Ms2File()
	ms2.load(filepath, read_editable=True)
	scene = create_scene(ms2_basename, len(ms2.modelstream_names), ms2.context.version)
	bpy.context.window.scene = scene
	# print(ms2)
	created_materials = {}
	for model_info in ms2.model_infos:
		mdl2_coll = create_collection(model_info.name, scene.collection)
		mdl2_coll["render_flag"] = int(model_info.render_flag)
		bone_names = get_bone_names(model_info)
		b_armature_obj = import_armature(scene, model_info, bone_names, mdl2_coll)

		mesh_dict = {}
		ob_dict = {}
		# print(model_info)
		# print(model_info.model)
		for lod_i, m_lod in enumerate(model_info.model.lods):
			logging.info(f"Importing LOD{lod_i}")
			lod_coll = create_collection(f"{model_info.name}_L{lod_i}", mdl2_coll)
			# skip other shells for JWE2
			obs = []
			for m_ob in m_lod.objects:
				mesh = m_ob.mesh
				if hasattr(mesh, "vert_chunks"):
					tri_chunk = mesh.tri_chunks[0]
					if tri_chunk.shell_index:
						logging.debug(f"Skipping import of shell duplicate {tri_chunk.shell_index}")
						continue
				obs.append(m_ob)
			for ob_i, m_ob in enumerate(obs):
				mesh = m_ob.mesh
				# print(mesh)
				# logging.debug(f"flag {mesh.flag}")
				mesh_name = f"{model_info.name}_model{m_ob.mesh_index}"
				if m_ob.mesh_index in mesh_dict:
					b_me = mesh_dict[m_ob.mesh_index]
				# create object and mesh from data
				else:
					b_me = bpy.data.meshes.new(mesh_name)
					b_me.from_pydata(mesh.vertices, [], mesh.tris)
					try:
						# store mesh unknowns
						# cast the bitfield to int
						b_me["flag"] = int(mesh.flag)
						if ms2.context.version > 13:
							b_me["unk_f0"] = float(mesh.unk_float_0)
						if ms2.context.version > 32:
							b_me["unk_f1"] = float(mesh.unk_float_1)
					except:
						logging.exception("Setting unks failed")
					try:
						mesh_dict[m_ob.mesh_index] = b_me
						import_mesh_layers(b_me, mesh, use_custom_normals, m_ob.material.name)
					except:
						logging.exception("import_mesh_layers failed")
					# import_chunk_bounds(b_me, mesh, lod_coll)
				if hasattr(mesh, "vert_chunks"):
					tri_chunk = mesh.tri_chunks[0]
					b_me["shell_count"] = tri_chunk.shell_count
				# link material to mesh
				import_material(reporter, created_materials, in_dir, b_me, m_ob.material)

				if m_ob.mesh_index in ob_dict:
					b_ob = ob_dict[m_ob.mesh_index]
				else:
					b_ob = create_ob(scene, f"{model_info.name}_ob{ob_i}_L{lod_i}", b_me, coll=lod_coll)
					b_ob.parent = b_armature_obj
					ob_dict[m_ob.mesh_index] = b_ob
					try:
						import_vertex_groups(b_ob, mesh, bone_names)
						import_shapekeys(b_ob, mesh)
						# link to armature, only after mirror so the order is good and weights are mirrored
						append_armature_modifier(b_ob, b_armature_obj)
						if mirror_mesh:
							append_bisect_modifier(b_ob)
						ob_postpro(b_ob, mirror_mesh, use_custom_normals)
						# from plugin.modules_import.tangents import visualize_tangents
						# ob2, me2 = visualize_tangents(b_ob.name, mesh.vertices, mesh.normals, mesh.tangents)
					except:
						logging.exception("Some mesh data failed")
				# we can't assume that the first ob referencing this mesh has fur already
				if ms2.context.version > 32 and is_shell(b_ob):
					logging.debug(f"{b_ob.name} has shells, adding psys")
					add_psys(b_ob, mesh.fur_length)
			# show lod 0, hide the others
			set_collection_visibility(scene, lod_coll.name, lod_i != 0)
		gauge_uv_scale_wrapper(reporter)
	reporter.show_info(f"Imported {ms2_name} in {time.time() - start_time:.2f} seconds")


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
	# else:
	# 	remove_doubles_bmesh(b_me)


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
	bpy.ops.object.mode_set(mode='OBJECT')


# def remove_doubles_bmesh(b_me):
# 	# no operator, but bmesh
# 	bm = bmesh.new()
# 	bm.from_mesh(b_me)
# 	bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=0.0)
# 	bm.to_mesh(b_me)
# 	b_me.update()
# 	bm.clear()
# 	bm.free()


def append_bisect_modifier(b_ob):
	mod = b_ob.modifiers.new('Mirror', 'MIRROR')
	mod.use_clip = True
	mod.use_mirror_merge = True
	mod.use_mirror_vertex_groups = True
	# mod.use_x = True
	mod.use_axis = (True, False, False)
	mod.merge_threshold = 0.001
