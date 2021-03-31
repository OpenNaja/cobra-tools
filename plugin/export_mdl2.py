import os
import time
import struct

import bpy
import mathutils

from plugin.modules_export.armature import get_armature, handle_transforms, export_bones
from plugin.modules_export.collision import export_bounds
from plugin.modules_import.armature import get_bone_names
from generated.formats.ms2 import Mdl2File
from utils.shell import get_ob_from_lod_and_flags

MAX_USHORT = 65535


def ensure_tri_modifier(ob):
	"""Makes sure that ob has a triangulation modifier in its stack."""
	for mod in ob.modifiers:
		if mod.type in ('TRIANGULATE',):
			break
	else:
		ob.modifiers.new('Triangulate', 'TRIANGULATE')


def save(operator, context, filepath='', apply_transforms=False, edit_bones=False):
	errors = []
	start_time = time.time()

	# ensure that we have objects in the scene
	if bpy.context.scene.objects:
		# operator needs an active object, set one if missing (eg. user had deleted the active object)
		if not bpy.context.view_layer.objects.active:
			bpy.context.view_layer.objects.active = bpy.context.scene.objects[0]
		# now enter object mode on the active object, if we aren't already in it
		bpy.ops.object.mode_set(mode="OBJECT")
	else:
		return "No objects in scene, nothing to export!",

	print(f"\nExporting {filepath} into export subfolder...")
	if not os.path.isfile(filepath):
		errors.append(f"{filepath} does not exist. You must open an existing MDL2 file for exporting.")
		return errors

	data = Mdl2File()
	# open file for binary reading
	data.load(filepath, quick=True)

	b_armature_ob = get_armature()
	if not b_armature_ob:
		errors.append(f"No armature was found - did you delete it?")
		return errors
	# clear pose
	for pbone in b_armature_ob.pose.bones:
		pbone.matrix_basis = mathutils.Matrix()

	# used to get index from bone name for faster weights
	bones_table = dict(((b, i) for i, b in enumerate(get_bone_names(data))))
	if edit_bones:
		export_bones(b_armature_ob, data)
	# ensure that these are initialized
	for model in data.models:
		model.tri_indices = []
		model.verts = []

	bounds = []
	mesh_objects = [ob for ob in bpy.data.objects if type(ob.data) == bpy.types.Mesh and ob.display_type != 'BOUNDS']
	for ob in mesh_objects:
		print("\nNext mesh...")

		# make sure the model has a triangulation modifier
		ensure_tri_modifier(ob)

		dg = bpy.context.evaluated_depsgraph_get()
		# make a copy with all modifiers applied
		eval_obj = ob.evaluated_get(dg)
		me = eval_obj.to_mesh(preserve_all_data_layers=True, depsgraph=dg)
		handle_transforms(eval_obj, me, errors, apply=apply_transforms)
		# get the index of this model in the mdl2 model buffer
		try:
			ind = int(ob.name.rsplit("_model", 1)[1])
		except:
			print("Bad name, skipping", ob.name)
			continue
		print("Model slot", ind)
		bounds.append(eval_obj.bound_box)

		# we get the corresponding mdl2 model
		model = data.models[ind]
		# perhaps we want to update model.flag from ob["flag"]
		model.update_dtype()

		hair_length = get_hair_length(ob)
		model.fur_length = hair_length

		num_uvs = model.get_uv_count()
		num_vcols = model.get_vcol_count()

		if not len(me.vertices):
			errors.append(f"Model {ob.name} has no vertices!")
			return errors

		if not len(me.polygons):
			errors.append(f"Model {ob.name} has no polygons!")
			return errors

		for len_type, num_type, name_type in (
				(len(me.uv_layers), num_uvs, "UV"),
				(len(me.vertex_colors), num_vcols, "Vertex Color")):
			print(f"{name_type} count:", num_type)
			if len_type != num_type:
				errors.append(f"Model {ob.name} has {len_type} {name_type} layers, but {num_type} were expected!")
				return errors

		unweighted_vertices = []
		tris = []
		# tangents have to be pre-calculated
		# this will also calculate loop normal
		me.calc_tangents()
		# stores values retrieved from blender, will be packed into array by pyffi
		verts = []
		# use a dict mapping dummy vertices to their index for fast lookup
		# this is used to convert blender vertices (several UVs, normals per face corner) to mdl2 vertices
		dummy_vertices = {}
		count_unique = 0
		count_reused = 0
		# defaults that may or may not be set later on
		unk_0 = 0
		residue = 1
		fur_length = None

		# fin models have to grab tangents from shell
		if model.flag == 565:
			lod_coll = ob.users_collection[0]
			print(lod_coll)
			shell_ob = get_ob_from_lod_and_flags(lod_coll, flags=[885, 821, 1013, ])
			print(shell_ob)
			if shell_ob:
				shell_eval_ob, shell_eval_me = eval_me(shell_ob)
				shell_eval_me.calc_tangents()
				shell_kd = fill_kd_tree(shell_eval_me)

				fin_uv_layer = me.uv_layers[0].data

		# loop faces and collect unique and repeated vertices
		for face in me.polygons:
			if len(face.loop_indices) != 3:
				# this is a bug - we are applying the triangulation modifier above
				errors.append(f"Model {ob.name} is not triangulated!")
				return errors
			# build indices into vertex buffer for the current face
			tri = []
			# loop over face loop to get access to face corner data (normals, uvs, vcols, etc)
			for loop_index in face.loop_indices:
				b_loop = me.loops[loop_index]
				b_vert = me.vertices[b_loop.vertex_index]

				# get the vectors
				position = b_vert.co
				if model.flag == 565 and shell_ob:
					uv_co = fin_uv_layer[b_loop.index].uv.to_3d()
					co, index, dist = shell_kd.find(uv_co)
					shell_loop = shell_eval_me.loops[index]
					# print(tangent)
					tangent = shell_loop.tangent
					normal = shell_loop.normal
				else:
					tangent = b_loop.tangent
					normal = b_loop.normal
				uvs = [(layer.data[loop_index].uv.x, 1 - layer.data[loop_index].uv.y) for layer in me.uv_layers]
				# create a dummy bytes str for indexing
				float_items = [*position, *[c for uv in uvs[:2] for c in uv], *tangent]
				dummy = struct.pack(f'<{len(float_items)}f', *float_items)
				# see if this dummy key exists
				try:
					# if it does - reuse it by grabbing its index from the dict
					v_index = dummy_vertices[dummy]
					count_reused += 1
				except:
					# it doesn't, so we have to fill in additional data
					v_index = count_unique
					if v_index > MAX_USHORT:
						errors.append(
							f"{ob.name} has too many MDL2 verts. The limit is {MAX_USHORT}. \nBlender vertices have to be duplicated on every UV seam, hence the increase.")
						return errors
					dummy_vertices[dummy] = v_index
					count_unique += 1

					# now collect any missing vert data that was not needed for the splitting of blender verts

					# collect vertex colors
					vcols = [(x for x in layer.data[loop_index].color) for layer in me.vertex_colors]

					# get the weights
					w = []
					for vertex_group in b_vert.groups:
						vgroup_name = ob.vertex_groups[vertex_group.group].name
						# get the unk0
						if vgroup_name == "unk0":
							unk_0 = vertex_group.weight
						elif vgroup_name == "residue":
							# if this is not rounded, somehow it affects the weights
							# might be a bug, but can't figure out where the rest is affected
							residue = int(round(vertex_group.weight))
						elif vgroup_name == "fur_length":
							# only store this hack for shells, never for fins
							if model.flag in (885, 1013, 821):
								fur_length = vertex_group.weight * hair_length
						else:
							# avoid dummy vertex groups without corresponding bones
							try:
								w.append([bones_table[vgroup_name], vertex_group.weight])
							except:
								print(f"Could not find bone name '{vgroup_name}' in bone table")
								errors.append(
									f"Ignored extraneous vertex group {vgroup_name} on mesh {ob.name}!")
					# print(residue, unk_0)
					# get the 4 strongest influences on this vert
					w_s = sorted(w, key=lambda x: x[1], reverse=True)[0:4]
					# print(w_s)
					# pad the weight list to 4 bones, ie. add empty bones if missing
					for i in range(0, 4 - len(w_s)):
						w_s.append([0, 0])
					# ensure that we have 4 weights at this point
					assert (len(w_s) == 4)
					# split the list of tuples into two separate lists
					bone_ids, bone_weights = zip(*w_s)
					# summed weights
					sw = sum(bone_weights)
					# print(sw)
					if sw > 0.0:
						# normalize
						bone_weights = [x / sw for x in bone_weights]
					elif b_loop.vertex_index not in unweighted_vertices:
						# print("Sum of weights",sw)
						unweighted_vertices.append(b_loop.vertex_index)
					# get the index for the skin partition - the bone with the highest weight
					bone_index = w_s[0][0]
					# store all raw blender data for pyffi
					verts.append((position, residue, normal, unk_0, tangent, bone_index, uvs, vcols, bone_ids,
								  bone_weights, fur_length))
				tri.append(v_index)
			tris.append(tri)

		print("count_unique", count_unique)
		print("count_reused", count_reused)

		# report unweighted vertices
		if model.flag not in (513,):
			if unweighted_vertices:
				errors.append(f"{ob.name} has {len(unweighted_vertices)} unweighted vertices!")
				return errors

		# update vert & tri array
		model.base = data.model_info.pack_offset
		# transfer raw verts into model data packed array
		model.set_verts(verts)
		model.tris = tris

	export_bounds(bounds, data)
	# check if any modeldata is empty
	for i, model in enumerate(data.models):
		if not model.tri_indices or not model.verts:
			errors.append(
				f"MDL2 Modeldata #{i} has not been populated. \n"
				f"Ensure that the name of the blender model for that number follows the naming convention.")
			return errors

	# write modified data
	data.save(filepath)

	print(f"\nFinished Mdl2 Export in {time.time() - start_time:.2f} seconds")
	# only return unique errors
	return set(errors)


def get_hair_length(ob):
	if ob.particle_systems:
		psys = ob.particle_systems[0]
		return psys.settings.hair_length
	return 0


def eval_me(ob):
	dg = bpy.context.evaluated_depsgraph_get()
	# make a copy with all modifiers applied
	eval_obj = ob.evaluated_get(dg)
	me = eval_obj.to_mesh(preserve_all_data_layers=True, depsgraph=dg)
	return eval_obj, me


def fill_kd_tree(me):
	size = len(me.loops)
	kd = mathutils.kdtree.KDTree(size)
	uv_layer = me.uv_layers[0].data
	for i, loop in enumerate(me.loops):
		kd.insert(uv_layer[loop.index].uv.to_3d(), i)
	kd.balance()
	return kd