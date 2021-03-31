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
from generated.formats.ms2 import Mdl2File
from utils.shell import get_ob_from_lod_and_flags


def load(operator, context, filepath="", use_custom_normals=False, mirror_mesh=False):
	start_time = time.time()
	in_dir, mdl2_name = os.path.split(filepath)
	bare_name = os.path.splitext(mdl2_name)[0]
	data = Mdl2File()
	data.load(filepath)

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
		print("bits", bin(model.flag))

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
			# map normals so we can set them to the edge corners (stored per loop)
			no_array = [model.normals[vertex_index] for face in me.polygons for vertex_index in face.vertices]
			me.use_auto_smooth = True
			me.normals_split_custom_set(no_array)
		# else:
		# # no operator, but bmesh
		# 	bm = bmesh.new()
		# 	bm.from_mesh(me)
		# 	bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=0.001)
		# 	bm.to_mesh(me)
		# 	me.update()
		# 	bm.clear()
		# 	bm.free()

		bpy.ops.object.mode_set(mode='EDIT')
		if mirror_mesh:
			bpy.ops.mesh.bisect(plane_co=(0, 0, 0), plane_no=(1, 0, 0), clear_inner=True)
			bpy.ops.mesh.select_all(action='SELECT')
			mod = ob.modifiers.new('Mirror', 'MIRROR')
			mod.use_clip = True
			mod.use_mirror_merge = True
			mod.use_mirror_vertex_groups = True
			mod.use_x = True
			mod.merge_threshold = 0.001
		bpy.ops.mesh.tris_convert_to_quads()
		# shells are messed up by remove doubles, affected faces have their dupe faces removed
		# since we are now stripping shells, shell meshes can use remove doubles but fins still can not
		if not use_custom_normals and model.flag not in (565, ):
			bpy.ops.mesh.remove_doubles(threshold=0.000001, use_unselected=False)
		try:
			bpy.ops.uv.seams_from_islands()
		except:
			print(ob.name+" has no UV coordinates!")
		bpy.ops.object.mode_set(mode='OBJECT')

		# link to armature, only after mirror so the order is good and weights are mirrored
		if data.ms2_file.bone_info:
			append_armature_modifier(ob, b_armature_obj)
		if model.flag in (1013, 821, 853, 885):
			add_psys(ob, model)
		# only set the lod index here so that hiding it does not mess with any operators applied above
		matrix_util.to_lod(ob, lod_i)
		# ob2, me2 = visualize_tangents(ob.name, model.vertices, model.normals, model.tangents)
		# matrix_util.to_lod(ob2, lod_i)
	print(f"Finished MDL2 import in {time.time()-start_time:.2f} seconds!")
	return errors


def visualize_tangents(name, verts, normals, tangents):
	out_verts = []
	out_faces = []
	v_len = 0.01
	for i, (v, n, t) in enumerate(zip(verts, normals, tangents)):
		out_verts.append(v)
		out_verts.append(v+v_len*n)
		out_verts.append(v+v_len*t)
		out_faces.append((i * 3, i*3 + 1, i * 3 + 2))
	return mesh_from_data(f"{name}_Tangents", out_verts, out_faces, wireframe=False)


def eval_me(ob):
	dg = bpy.context.evaluated_depsgraph_get()
	# make a copy with all modifiers applied
	eval_obj = ob.evaluated_get(dg)
	me = eval_obj.to_mesh(preserve_all_data_layers=True, depsgraph=dg)
	return eval_obj, me

def create_tangents():

	for lod_i in range(6):
		lod_group_name = "LOD" + str(lod_i)
		src_ob = get_ob_from_lod_and_flags(lod_group_name, flags=[885, 821, 1013, ])
		trg_ob = get_ob_from_lod_and_flags(lod_group_name, flags=[565, ])

		eval_ob_src, me_src = eval_me(src_ob)
		eval_ob_trg, me_trg = eval_me(trg_ob)

		# tangents have to be pre-calculated
		# this will also calculate loop normal
		me_trg.calc_tangents()
		me_src.calc_tangents()
		# calc_tangents(me)

		kd = fill_kd_tree(me_src)
		# stores values retrieved from blender, will be packed into array by pyffi
		verts = []
		normals = []
		tangents = []

		uv = me_trg.uv_layers[0].data
		# loop faces and collect unique and repeated vertices
		for face in me_trg.polygons:
			# loop over face loop to get access to face corner data (normals, uvs, vcols, etc)
			for loop_index in face.loop_indices:
				b_loop = me_trg.loops[loop_index]
				b_vert = me_trg.vertices[b_loop.vertex_index]

				uv_co = uv[b_loop.index].uv.to_3d()
				co, index, dist = kd.find(uv_co)
				src_tangent = me_src.loops[index].tangent
				# get the vectors
				verts.append(b_vert.co)
				tangents.append(src_tangent)
				normals.append(b_loop.normal)
		ob2, me2 = visualize_tangents(trg_ob.name+"Gen", verts, normals, tangents)

def fill_kd_tree(me):
	size = len(me.loops)
	kd = mathutils.kdtree.KDTree(size)
	uv_layer = me.uv_layers[0].data
	for i, loop in enumerate(me.loops):
		kd.insert(uv_layer[loop.index].uv.to_3d(), i)
	kd.balance()
	return kd

def calc_tangents(me):
	# See "Tangent Space Calculation" at http://www.terathon.com/code/tangent.html
	# for v in me.vertices:
	# 	v.tangent = mathutils.Vector((0.0, 0.0, 0.0))
	# 	v.bitangent = mathutils.Vector((0.0, 0.0, 0.0))
	# for (v0, v1, v2) in me.tris:
	# 	dco1 = v1.coord - v0.coord
	# 	dco2 = v2.coord - v0.coord
	# 	duv1 = v1.uv - v0.uv
	# 	duv2 = v2.uv - v0.uv
	# 	tangent = dco2 * duv1.y - dco1 * duv2.y
	# 	bitangent = dco2 * duv1.x - dco1 * duv2.x
	# 	if dco2.cross(dco1).dot(bitangent.cross(tangent)) < 0:
	# 		tangent.negate()
	# 		bitangent.negate()
	# 	v0.tangent += tangent
	# 	v1.tangent += tangent
	# 	v2.tangent += tangent
	# 	v0.bitangent += bitangent
	# 	v1.bitangent += bitangent
	# 	v2.bitangent += bitangent
	# for v in self.verts:
	# 	v.tangent = v.tangent - v.normal * v.tangent.dot(v.normal)
	# 	v.tangent.normalize()
	# 	if v.normal.cross(v.tangent).dot(v.bitangent) < 0:
	# 		v.bitangent = -1.0
	# 	else:
	# 		v.bitangent = 1.0

	tangents = [mathutils.Vector((0.0, 0.0, 0.0)) for _ in range(len(me.loops))]
	bitangents = [mathutils.Vector((0.0, 0.0, 0.0)) for _ in range(len(me.loops))]
	# loop faces and collect unique and repeated vertices
	for face in me.polygons:
		assert len(face.loop_indices) == 3
		# loop over face loop to get access to face corner data (normals, uvs, vcols, etc)
		l0, l1, l2 = [me.loops[loop_index] for loop_index in face.loop_indices]
		# get vert coords
		v0 = me.vertices[l0.vertex_index]
		v1 = me.vertices[l1.vertex_index]
		v2 = me.vertices[l2.vertex_index]
		dco1 = v1.co - v0.co
		dco2 = v2.co - v0.co

		uv = me.uv_layers[0].data
		duv1 = uv[l1.index].uv - uv[l0.index].uv
		duv2 = uv[l2.index].uv - uv[l0.index].uv
		tangent = dco2 * duv1.y - dco1 * duv2.y
		bitangent = dco2 * duv1.x - dco1 * duv2.x
		if dco2.cross(dco1).dot(bitangent.cross(tangent)) < 0:
			tangent.negate()
			bitangent.negate()
		for loop_index in face.loop_indices:
			tangents[loop_index] += tangent
			bitangents[loop_index] += bitangent
	for tangent in tangents:
		tangent.normalize()
		# v.tangent = v.tangent - v.normal * v.tangent.dot(v.normal)
		# for loop_index in face.loop_indices:
		# 	b_loop = me.loops[loop_index]
		# 	b_vert = me.vertices[b_loop.vertex_index]
		#
		# 	b_loop.tangent = mathutils.Vector((0.0, 0.0, 0.0))
		# 	b_loop.bitangent = mathutils.Vector((0.0, 0.0, 0.0))
		# 	# # get the vectors
		# 	# position = b_vert.co
		# 	# tangent = b_loop.tangent
		# 	# normal = b_loop.normal
		# 	# uvs = [(layer.data[loop_index].uv.x, 1 - layer.data[loop_index].uv.y) for layer in me.uv_layers]


