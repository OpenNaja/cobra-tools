import os
import time

import bpy
# import bmesh

from plugin.modules_import.armature import import_armature, append_armature_modifier, import_vertex_groups, \
	get_bone_names
from plugin.helpers import mesh_from_data
from plugin.modules_import.hair import add_psys
from plugin.modules_import.material import import_material
from utils import matrix_util
from generated.formats.ms2 import Mdl2File, is_old
from utils.shell import is_fin


def load(operator, context, filepath="", use_custom_normals=False, mirror_mesh=False):
	start_time = time.time()
	in_dir, mdl2_name = os.path.split(filepath)
	bare_name = os.path.splitext(mdl2_name)[0]
	data = Mdl2File()
	data.load(filepath, entry=True, read_editable=True)

	errors = []
	bone_names = get_bone_names(data)
	b_armature_obj = import_armature(data, bone_names)
	# b_armature_obj2 = import_armature_new(data)
	created_materials = {}
	# print("data.models",data.models)
	for model_i, model in enumerate(data.models):
		lod_i = model.lod_index
		print("\nmodel_i", model_i)
		print("lod_i", lod_i)
		print("flag", model.flag)

		# create object and mesh from data
		ob, me = mesh_from_data(f"{bare_name}_model{model_i}", model.vertices, model.tris, wireframe=False)
		# cast the bitfield to int
		ob["flag"] = int(model.flag)

		# link material to mesh
		me = ob.data
		import_material(created_materials, in_dir, me, model)

		# set uv data
		if model.uvs is not None:
			num_uv_layers = model.uvs.shape[1]
			for uv_i in range(num_uv_layers):
				uvs = model.uvs[:, uv_i]
				me.uv_layers.new(name=f"UV{uv_i}")
				me.uv_layers[-1].data.foreach_set("uv", [uv for pair in [uvs[l.vertex_index] for l in me.loops] for uv in (pair[0], 1-pair[1])])

		if model.colors is not None:
			num_vcol_layers = model.colors.shape[1]
			for col_i in range(num_vcol_layers):
				vcols = model.colors[:, col_i]
				me.vertex_colors.new(name=f"RGBA{col_i}")
				me.vertex_colors[-1].data.foreach_set("color", [c for col in [vcols[l.vertex_index] for l in me.loops] for c in col])

		# me.vertex_colors.new(name="tangents")
		# me.vertex_colors[-1].data.foreach_set("color", [c for col in [model.tangents[l.vertex_index] for l in me.loops] for c in (*col, 1,)])
		#
		# me.vertex_colors.new(name="normals")
		# me.vertex_colors[-1].data.foreach_set("color", [c for col in [model.normals[l.vertex_index] for l in me.loops] for c in (*col,1,)])

		mesh_start_time = time.time()

		import_vertex_groups(ob, model, bone_names)
		print(f"mesh cleanup took {time.time() - mesh_start_time:.2f} seconds")

		# set faces to smooth
		me.polygons.foreach_set('use_smooth', [True] * len(me.polygons))
		# set normals
		if use_custom_normals and model.flag not in (565, ):
			me.use_auto_smooth = True
			me.normals_split_custom_set_from_vertices(model.normals)
		# else:
		# 	remove_doubles_bmesh(me)

		bpy.ops.object.mode_set(mode='EDIT')
		if mirror_mesh:
			bisect_mesh(ob)
		bpy.ops.mesh.tris_convert_to_quads()
		# shells are messed up by remove doubles, affected faces have their dupe faces removed
		# since we are now stripping shells, shell meshes can use remove doubles but fins still can not
		if not use_custom_normals and not is_fin(ob):
			bpy.ops.mesh.remove_doubles(threshold=0.000001, use_unselected=False)
		bpy.ops.uv.select_all(action='SELECT')
		bpy.ops.uv.seams_from_islands()
		bpy.ops.object.mode_set(mode='OBJECT')

		# link to armature, only after mirror so the order is good and weights are mirrored
		append_armature_modifier(ob, b_armature_obj)
		if not is_old(data) and model.flag.fur_shells:
			add_psys(ob, model)
		# only set the lod index here so that hiding it does not mess with any operators applied above
		matrix_util.to_lod(ob, lod_i)
		# ob2, me2 = visualize_tangents(ob.name, model.vertices, model.normals, model.tangents)
		# matrix_util.to_lod(ob2, lod_i)
	print(f"Finished MDL2 import in {time.time()-start_time:.2f} seconds!")
	return errors


# def remove_doubles_bmesh(me):
# 	# no operator, but bmesh
# 	bm = bmesh.new()
# 	bm.from_mesh(me)
# 	bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=0.001)
# 	bm.to_mesh(me)
# 	me.update()
# 	bm.clear()
# 	bm.free()


def bisect_mesh(ob):
	bpy.ops.mesh.bisect(plane_co=(0, 0, 0), plane_no=(1, 0, 0), clear_inner=True)
	bpy.ops.mesh.select_all(action='SELECT')
	mod = ob.modifiers.new('Mirror', 'MIRROR')
	mod.use_clip = True
	mod.use_mirror_merge = True
	mod.use_mirror_vertex_groups = True
	mod.use_x = True
	mod.merge_threshold = 0.001


