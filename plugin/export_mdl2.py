import os
import time
import struct

import bpy
import mathutils
from utils import matrix_util
from generated.formats.ms2 import Mdl2File

MAX_USHORT = 65535


def get_armature():
	src_armatures = [ob for ob in bpy.data.objects if type(ob.data) == bpy.types.Armature]
	# do we have armatures?
	if src_armatures:
		# see if one of these is selected
		if len(src_armatures) > 1:
			sel_armatures = [ob for ob in src_armatures if ob.select_get()]
			if sel_armatures:
				return sel_armatures[0]
		return src_armatures[0]




def ensure_tri_modifier(ob):
	"""Makes sure that ob has a triangulation modifier in its stack."""
	for mod in ob.modifiers:
		if mod.type in ('TRIANGULATE',):
			break
	else:
		ob.modifiers.new('Triangulate', 'TRIANGULATE')


def handle_transforms(ob, me, errors, apply=True):
	"""Ensures that non-zero object transforms are either applied or reported"""
	identity = mathutils.Matrix()
	# the world space transform of every rigged mesh must be neutral
	if ob.matrix_world != identity:
		if apply:
			# we only transform the evaluated mesh and leave the actual scene alone
			me.transform(ob.matrix_world)
			errors.append(ob.name+" has had its object transforms applied on the fly to avoid ingame distortion!")
		else:
			# we simply ignore the transforms and export the mesh as is, but warn the user
			errors.append(f"Ignored object transforms for {ob.name} - orientation will not match what you see in blender!")


def save(operator, context, filepath='', apply_transforms=False):
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
		return ("No objects in scene, nothing to export!", )

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

	bone_names = data.ms2_file.bone_names
	# used to get index from bone name for faster weights
	bones_table = dict((matrix_util.bone_name_for_blender(bone_name), bone_i) for bone_i, bone_name in enumerate(bone_names))
	bone_parents = data.ms2_file.bone_info.bone_parents
	old_bone_names = [matrix_util.bone_name_for_blender(n) for n in data.ms2_file.bone_names]
	boness = b_armature_ob.data.bones
	bpy.ops.object.mode_set(mode='EDIT', toggle=False)
	mats = {}
	bones = data.ms2_file.bone_info.bones
	idx = 0
	for bone_name, bb, o_parent_ind in zip(old_bone_names, bones, bone_parents):
		if idx in (0,1):
			print(idx)
		else:
			bbb = boness.get(bone_name)
			#ebb = edit_bones(bone_name)
			print(bone_name)
			print(data.ms2_file.bone_info.inverse_bind_matrices[idx])
			print("old: ",bb)
			#print(matrix_util.nif_bind_to_blender_bind(matrix_util.import_matrix(data.bone_info.inverse_bind_matrices[idx]).inverted_safe()))
			if bbb.parent is None:
				mat_local_to_parent = bbb.matrix_local
			else:
				parent_name = old_bone_names[o_parent_ind]
				mat_local_to_parent = bbb.parent.matrix_local.inverted() @ bbb.matrix_local
			data.ms2_file.bone_info.inverse_bind_matrices[idx].set_rows(*matrix_util.blender_bind_to_nif_bind(bbb.matrix_local).inverted())
			print(data.ms2_file.bone_info.inverse_bind_matrices[idx])
			bb.set_bone(mat_local_to_parent)

			print(" ")
			print("new: ",bb)
		idx+=1
	bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
	# ensure that these are initialized
	for model in data.models:
		model.tri_indices = []
		model.verts = []

	for ob in bpy.data.objects:
		if type(ob.data) == bpy.types.Mesh:
			print("\nNext mesh...")

			# make sure the model has a triangulation modifier
			ensure_tri_modifier(ob)

			# make a copy with all modifiers applied
			dg = bpy.context.evaluated_depsgraph_get()
			eval_obj = ob.evaluated_get(dg)
			me = eval_obj.to_mesh(preserve_all_data_layers=True, depsgraph=dg)
			handle_transforms(eval_obj, me, errors, apply=apply_transforms)

			# get the index of this model in the mdl2 model buffer
			try:
				ind = int(ob.name.rsplit("_model", 1)[1])
			except:
				print("Bad name, skipping",ob.name)
				continue
			print("Model slot",ind)

			# we get the corresponding mdl2 model
			model = data.models[ind]
			# perhaps we want to update model.flag from ob["flag"]
			model.update_dtype()
			num_uvs = model.get_uv_count()
			num_vcols = model.get_vcol_count()
			print("num_uvs",num_uvs)
			print("num_vcols",num_vcols)

			if not len(me.vertices):
				errors.append(f"Model {ob.name} has no vertices!")
				return errors

			if not len(me.polygons):
				errors.append(f"Model {ob.name} has no polygons!")
				return errors

			if len(me.uv_layers) != num_uvs:
				errors.append(f"Model {ob.name} has {len(me.uv_layers)} UV layers, but {num_uvs} were expected!")
				return errors

			if len(me.vertex_colors) != num_vcols:
				errors.append(f"Model {ob.name} has {len(me.vertex_colors)} Vertex Color layers, but {num_vcols} were expected!")
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
					tangent = b_loop.tangent
					normal = b_loop.normal
					uvs = [(layer.data[loop_index].uv.x, 1-layer.data[loop_index].uv.y) for layer in me.uv_layers]
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
								residue = int(vertex_group.weight)
							elif vgroup_name == "fur_length":
								# only store this hack for shells, never for fins
								if model.flag in (885,1013,821):
									fur_length = vertex_group.weight
							else:
								# avoid check for dummy vertex groups without corresponding bones
								try:
									w.append([bones_table[vgroup_name], vertex_group.weight])
								except:
									try:
										w.append([int(vgroup_name), vertex_group.weight])
									except:
										errors.append(f"Ignored extraneous vertex group {vgroup_name} on mesh {ob.name}!")
						# get the 4 strongest influences on this vert
						w_s = sorted(w, key=lambda x: x[1], reverse=True)[0:4]
						# pad the weight list to 4 bones, ie. add empty bones if missing
						for i in range(0, 4-len(w_s)): w_s.append([0, 0])
						# summed weights
						sw = sum(w[1] for w in w_s)
						# print(sw)
						if sw > 0.0:
							# normalize
							for x in range(4):
								w_s[x][1] /= sw
						elif b_loop.vertex_index not in unweighted_vertices:
							# print("Sum of weights",sw)
							unweighted_vertices.append(b_loop.vertex_index)
						if v_index > MAX_USHORT:
							errors.append(f"{ob.name} has too many MDL2 verts. The limit is {MAX_USHORT}. \nBlender vertices have to be duplicated on every UV seam, hence the increase.")
							return errors

						# ensure that we have 4 weights at this point
						assert (len(w_s) == 4)
						# split the list of tuples into two separate lists
						bone_ids, bone_weights = zip(*w_s)
						# get the index for the skin partition - the bone with the highest weight
						bone_index = w_s[0][0]
						# store all raw blender data for pyffi
						verts.append((position, residue, normal, unk_0, tangent, bone_index, uvs, vcols, bone_ids, bone_weights, fur_length))
					tri.append(v_index)
				tris.append(tri)

			print("count_unique",count_unique)
			print("count_reused",count_reused)

			# report unweighted vertices
			if model.flag not in (513,):
				if unweighted_vertices:
					errors.append(f"{ob.name} has {len(unweighted_vertices)} unweighted vertices!")
					return errors

			# set shell count if not present
			if "add_shells" in ob:
				shell_count = ob["add_shells"]
			else:
				shell_count = 0
				ob["add_shells"] = 0
			# extend tri array according to shell count
			print("Got to add shells",shell_count)
			out_tris = list(tris)
			for shell in range(shell_count):
				print("Shell",shell)
				out_tris.extend(tris)

			# update vert & tri array
			model.base = data.model_info.pack_offset
			# transfer raw verts into model data packed array
			model.set_verts(verts)
			model.tris = out_tris

	# check if any modeldata is empty
	for i, model in enumerate(data.models):
		if not model.tri_indices or not model.verts:
			errors.append(f"MDL2 Modeldata #{i} has not been populated. \nEnsure that the name of the blender model for that number follows the naming convention.")
			return errors

	# write modified data
	data.save(filepath)

	print(f"\nFinished Mdl2 Export in {time.time()-start_time:.2f} seconds")
	# only return unique errors
	return set(errors)
