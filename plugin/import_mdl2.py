import logging
import os
import time

import bpy
# import bmesh

from plugin.modules_import.armature import import_armature, append_armature_modifier, import_vertex_groups, \
	get_bone_names, get_weights
from plugin.helpers import create_ob
from plugin.modules_import.hair import add_psys
from plugin.modules_import.material import import_material
from plugin.utils import matrix_util
from generated.formats.ms2 import Mdl2File, is_old
from plugin.utils.shell import is_fin


def load(filepath="", use_custom_normals=False, mirror_mesh=False):
	start_time = time.time()
	in_dir, mdl2_name = os.path.split(filepath)
	bare_name = os.path.splitext(mdl2_name)[0]
	mdl2 = Mdl2File()
	mdl2.load(filepath, entry=True, read_editable=True, read_bytes=False)
	# print(mdl2)
	mdl2.update_lod_vertex_counts()
	messages = set()
	bone_names = get_bone_names(mdl2)
	b_armature_obj = import_armature(mdl2, bone_names)
	
	bpy.context.scene["render_flag"] = int(mdl2.model_info.render_flag)
	created_materials = {}
	mesh_dict = {}
	ob_dict = {}
	# print("mdl2.models",mdl2.models)
	for lod_i, m_lod in enumerate(mdl2.lods):
		print("lod_i", lod_i)
		for ob_i, m_ob in enumerate(m_lod.objects):
			model = mdl2.models[m_ob.model_index]
			# lod_i = model.lod_index
			print("flag", model.flag)
			if m_ob.model_index in mesh_dict:
				b_me = mesh_dict[m_ob.model_index]
			# create object and mesh from data
			else:
				model.weights_info = get_weights(model)
				b_me = bpy.data.meshes.new(f"{bare_name}_model{m_ob.model_index}")
				# cast array to prevent truth check in from_pydata
				b_me.from_pydata(model.vertices, [], tuple(model.tris))
				# store mesh unknowns
				# cast the bitfield to int
				b_me["flag"] = int(model.flag)
				if not is_old(mdl2):
					b_me["unk_f0"] = float(model.unk_floats[0])
					b_me["unk_f1"] = float(model.unk_floats[1])
				mesh_dict[m_ob.model_index] = b_me
				import_mesh_layers(b_me, model, use_custom_normals)

			# link material to mesh
			import_material(created_materials, in_dir, b_me, m_ob.material)

			if m_ob.model_index not in ob_dict:
				b_ob = create_ob(f"{bare_name}_lod{lod_i}_ob{ob_i}", b_me)

				# parenting
				b_ob.parent = b_armature_obj

				b_ob["bone_index"] = m_lod.bone_index

				import_vertex_groups(b_ob, model, bone_names)
				import_shapekeys(b_ob, model)
				# link to armature, only after mirror so the order is good and weights are mirrored
				append_armature_modifier(b_ob, b_armature_obj)
				if mirror_mesh:
					append_bisect_modifier(b_ob)
				ob_postpro(b_ob, mirror_mesh, use_custom_normals)
				if not is_old(mdl2) and model.flag.fur_shells:
					add_psys(b_ob, model)
				# only set the lod index here so that hiding it does not mess with any operators applied above
				matrix_util.to_lod(b_ob, lod_i)
				ob_dict[m_ob.model_index] = b_ob
			else:
				b_ob = ob_dict[m_ob.model_index]

			# from plugin.modules_import.tangents import visualize_tangents
			# ob2, me2 = visualize_tangents(b_ob.name, model.vertices, model.normals, model.tangents)
			# matrix_util.to_lod(ob2, lod_i)
	messages.add(f"Finished MDL2 import in {time.time() - start_time:.2f} seconds")
	return messages


def import_mesh_layers(b_me, model, use_custom_normals):
	# set uv data
	if model.uvs is not None:
		num_uv_layers = model.uvs.shape[1]
		for uv_i in range(num_uv_layers):
			uvs = model.uvs[:, uv_i]
			b_me.uv_layers.new(name=f"UV{uv_i}")
			b_me.uv_layers[-1].data.foreach_set("uv",
												[uv for pair in [uvs[l.vertex_index] for l in b_me.loops] for uv in
												 (pair[0], 1 - pair[1])])
	if model.colors is not None:
		num_vcol_layers = model.colors.shape[1]
		for col_i in range(num_vcol_layers):
			vcols = model.colors[:, col_i]
			b_me.vertex_colors.new(name=f"RGBA{col_i}")
			b_me.vertex_colors[-1].data.foreach_set("color",
													[c for col in [vcols[l.vertex_index] for l in b_me.loops] for c in
													 col])
	# b_me.vertex_colors.new(name="tangents")
	# b_me.vertex_colors[-1].data.foreach_set("color", [c for col in [model.tangents[l.vertex_index] for l in b_me.loops] for c in (*col, 1,)])
	#
	# b_me.vertex_colors.new(name="normals")
	# b_me.vertex_colors[-1].data.foreach_set("color", [c for col in [model.normals[l.vertex_index] for l in b_me.loops] for c in (*col,1,)])
	# set faces to smooth
	b_me.polygons.foreach_set('use_smooth', [True] * len(b_me.polygons))
	# set normals
	if use_custom_normals and model.flag not in (565,):
		b_me.use_auto_smooth = True
		b_me.normals_split_custom_set_from_vertices(model.normals)
	# else:
	# 	remove_doubles_bmesh(b_me)


def import_shapekeys(b_obj, model):
	if model.shapekeys is not None:
		b_mesh = b_obj.data
		# insert base key
		sk_basis = b_obj.shape_key_add(name="Basis")
		b_mesh.shape_keys.use_relative = True

		# base_verts = [v.co for v in b_mesh.vertices]
		# for morph_verts, key_name in morphs:
		# 	# convert tuples into vector here so we can simply add in morph_mesh()
		# 	for b_v_index, (bv, mv) in enumerate(zip(base_verts, morph_verts)):
		# 		b_mesh.vertices[b_v_index].co = bv + mathutils.Vector(mv)
		# 	# TODO [animation] unused variable is it required
		# 	shape_key = b_obj.shape_key_add(name=key_name, from_mix=False)
		for v_index, v in enumerate(model.shapekeys):
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


