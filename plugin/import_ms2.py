import logging
import os
import time
import traceback

import bpy
# import bmesh
from plugin.modules_import.armature import import_armature, append_armature_modifier, import_vertex_groups, \
	get_bone_names, get_weights
from plugin.modules_import.hair import add_psys
from plugin.modules_import.material import import_material
from plugin.utils.shell import is_fin
from plugin.utils.object import create_ob, get_collection
from generated.formats.ms2 import Ms2File, is_old


def load(filepath="", use_custom_normals=False, mirror_mesh=False):
	messages = set()
	start_time = time.time()
	in_dir, ms2_name = os.path.split(filepath)
	ms2 = Ms2File()
	ms2.load(filepath, read_editable=True)
	created_materials = {}
	for mdl2_name, model_info in zip(ms2.mdl_2_names, ms2.model_infos):
		scene = bpy.data.scenes.new(mdl2_name)
		bpy.context.window.scene = scene

		bone_names = get_bone_names(model_info)
		b_armature_obj = import_armature(scene, model_info, bone_names)

		# store scene properties
		scene["render_flag"] = int(model_info.render_flag)
		scene.cobra.pack_base = model_info.pack_offset

		mesh_dict = {}
		ob_dict = {}
		# print("mdl2.mesh.meshes",mdl2.mesh.meshes)
		for lod_i, m_lod in enumerate(model_info.model.lods):
			logging.debug(f"lod_i {lod_i}")
			lod_coll = get_collection(scene, f"LOD{lod_i}")
			for ob_i, m_ob in enumerate(m_lod.objects):
				mesh = model_info.model.meshes[m_ob.mesh_index]
				# print(model_info)
				# print(model_info.model)
				# print(mesh)
				# lod_i = mesh.lod_index
				logging.debug(f"flag {mesh.flag}")
				if m_ob.mesh_index in mesh_dict:
					b_me = mesh_dict[m_ob.mesh_index]
				# create object and mesh from data
				else:
					mesh.weights_info = get_weights(mesh)
					b_me = bpy.data.meshes.new(f"{mdl2_name}_model{m_ob.mesh_index}")
					# cast array to prevent truth check in from_pydata
					b_me.from_pydata(mesh.vertices, [], tuple(mesh.tris))
					# print(mesh.vertices, [], tuple(mesh.tris))
					# store mesh unknowns
					# cast the bitfield to int
					b_me["flag"] = int(mesh.flag)
					if not is_old(ms2.info):
						b_me["unk_f0"] = float(mesh.unk_floats[0])
						b_me["unk_f1"] = float(mesh.unk_floats[1])
					mesh_dict[m_ob.mesh_index] = b_me
					# try:
					import_mesh_layers(b_me, mesh, use_custom_normals)
					# except:
					# 	traceback.print_exc()
				# link material to mesh
				import_material(created_materials, in_dir, b_me, m_ob.material)

				if m_ob.mesh_index not in ob_dict:
					b_ob = create_ob(scene, f"{mdl2_name}_lod{lod_i}_ob{ob_i}", b_me, coll=lod_coll)
					b_ob.parent = b_armature_obj
					b_ob["bone_index"] = m_lod.bone_index

					import_vertex_groups(b_ob, mesh, bone_names)
					import_shapekeys(b_ob, mesh)
					# link to armature, only after mirror so the order is good and weights are mirrored
					append_armature_modifier(b_ob, b_armature_obj)
					if mirror_mesh:
						append_bisect_modifier(b_ob)
					ob_postpro(b_ob, mirror_mesh, use_custom_normals)
					if not is_old(ms2.info) and mesh.flag.fur_shells:
						add_psys(b_ob, mesh)
					ob_dict[m_ob.mesh_index] = b_ob
				# from plugin.modules_import.tangents import visualize_tangents
				# ob2, me2 = visualize_tangents(b_ob.name, mesh.vertices, mesh.normals, mesh.tangents)

			coll_name = f"{scene.name}_LOD{lod_i}"
			# get view layer if it exists, show lod 0, hide the others
			if coll_name in bpy.context.view_layer.layer_collection.children:
				bpy.context.view_layer.layer_collection.children[coll_name].hide_viewport = lod_i != 0

	messages.add(f"Finished MS2 import in {time.time() - start_time:.2f} seconds")
	return messages


def import_mesh_layers(b_me, mesh, use_custom_normals):
	# set uv data
	if mesh.uvs is not None:
		num_uv_layers = mesh.uvs.shape[1]
		for uv_i in range(num_uv_layers):
			uvs = mesh.uvs[:, uv_i]
			b_me.uv_layers.new(name=f"UV{uv_i}")
			b_me.uv_layers[-1].data.foreach_set("uv",
												[uv for pair in [uvs[l.vertex_index] for l in b_me.loops] for uv in
												 (pair[0], 1 - pair[1])])
	if mesh.colors is not None:
		num_vcol_layers = mesh.colors.shape[1]
		for col_i in range(num_vcol_layers):
			vcols = mesh.colors[:, col_i]
			b_me.vertex_colors.new(name=f"RGBA{col_i}")
			b_me.vertex_colors[-1].data.foreach_set("color",
													[c for col in [vcols[l.vertex_index] for l in b_me.loops] for c in
													 col])
	# b_me.vertex_colors.new(name="tangents")
	# b_me.vertex_colors[-1].data.foreach_set("color", [c for col in [mesh.tangents[l.vertex_index] for l in b_me.loops] for c in (*col, 1,)])
	#
	# b_me.vertex_colors.new(name="normals")
	# b_me.vertex_colors[-1].data.foreach_set("color", [c for col in [mesh.normals[l.vertex_index] for l in b_me.loops] for c in (*col,1,)])
	# set faces to smooth
	b_me.polygons.foreach_set('use_smooth', [True] * len(b_me.polygons))
	# set normals
	if use_custom_normals and mesh.flag not in (565,):
		b_me.use_auto_smooth = True
		b_me.normals_split_custom_set_from_vertices(mesh.normals)
	# else:
	# 	remove_doubles_bmesh(b_me)


def import_shapekeys(b_obj, mesh):
	if mesh.shapekeys is not None:
		b_mesh = b_obj.data
		# insert base key
		sk_basis = b_obj.shape_key_add(name="Basis")
		b_mesh.shape_keys.use_relative = True

		for v_index, v in enumerate(mesh.shapekeys):
			b_mesh.vertices[v_index].co = v
		shape_key = b_obj.shape_key_add(name="LOD", from_mix=False)


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
	# todo reimplement check against fins for mesh
	if not use_custom_normals and not is_fin(b_ob):
		bpy.ops.mesh.remove_doubles(threshold=0.000001, use_unselected=False)
	bpy.ops.object.mode_set(mode='OBJECT')


# def remove_doubles_bmesh(b_me):
# 	# no operator, but bmesh
# 	bm = bmesh.new()
# 	bm.from_mesh(b_me)
# 	bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=0.001)
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


