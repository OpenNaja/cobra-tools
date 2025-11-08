import logging
import os
import time

import bpy
import numpy as np

from plugin.modules_import.armature import import_armature, append_armature_modifier, import_vertex_groups, \
	get_bone_names
from plugin.modules_import.collision import import_chunk_bounds
from plugin.modules_import.geometry import import_mesh_layers, import_shapekeys, ob_postpro, append_mirror_modifier, \
	get_valid_lod_objects, import_mesh_properties
from plugin.modules_import.material import import_material
from plugin.utils.fast_mesh import FastMesh
from plugin.utils.hair import add_psys
from plugin.utils.shell import is_shell, gauge_uv_scale_wrapper, is_fin_mat
from plugin.utils.object import create_ob, create_scene, create_collection, set_collection_visibility
from generated.formats.ms2 import Ms2File


def load(reporter, filepath: str = "", use_custom_normals: bool = False, mirror_mesh: bool = False, quadrify = True):
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
			for ob_i, m_ob in enumerate(get_valid_lod_objects(m_lod)):
				mesh = m_ob.mesh
				# print(mesh)
				if m_ob.mesh_index in mesh_dict:
					b_me = mesh_dict[m_ob.mesh_index]
				# create object and mesh from data
				else:
					b_me = FastMesh.new(f"{model_info.name}_model{m_ob.mesh_index}")
					mesh_dict[m_ob.mesh_index] = b_me
					original_tris = mesh.tris

					if is_fin_mat(m_ob.material):
						b_me.from_pydata(mesh.vertices, [], mesh.tris)
						sorted_indices = np.arange(len(mesh.vertices))
					else:
						# todo split on weights, fins, double sided faces sharing verts
						verts_unique, unique_indices, unique_inverse = np.unique(mesh.vertices, return_index=True, return_inverse=True, axis=0)
						sorted_indices = np.sort(unique_indices)
						verts_unique = mesh.vertices[sorted_indices]
						transsort = np.argsort(unique_indices)
						i_rev = transsort.copy()
						i_rev[transsort] = np.arange(len(i_rev))
						unique_inverse = i_rev[unique_inverse]
						tris = np.take(unique_inverse, mesh.tris)

						keep = []
						for i, (tri_orig, tri_deci) in enumerate(zip(original_tris, tris)):
							if len(set(tri_deci)) < 3:
								logging.warning(f"Discarding degenerate tri {i} as it would break custom normals")
							else:
								keep.append(i)
						original_tris = original_tris[keep]
						tris = tris[keep]
						# find duped tris
						# sorted_tris = np.sort(tris, axis=1)
						# # tris_unique, tris_unique_indices = np.unique(sorted_tris, return_index=True, axis=0)
						# tri_sets = set()
						# num_verts = len(verts_unique)
						# for decimated_tri, tri in zip(sorted_tris, mesh.tris):
						# 	print(decimated_tri, tri)
						# 	set_tri = tuple(decimated_tri)
						# 	if set_tri in tri_sets:
						# 		print("duped tri")
						# 	if len(set(set_tri)) < 3:
						# 		print("degenerate tri")
						# 	tri_sets.add(set_tri)
							# decimated_tri[:] = tri
						# rebuild vertices from de-duplicated tris
						# sorted_indices = np.unique(tris)
						# verts_unique = mesh.vertices[sorted_indices]
						# print(sorted_indices)

						b_me.from_pydata(verts_unique, [], tris)
					import_mesh_properties(b_me, mesh)
					try:
						import_mesh_layers(b_me, mesh, use_custom_normals, m_ob.material.name, original_tris.flatten(), sorted_indices)
					except:
						logging.exception("import_mesh_layers failed")
				# import_chunk_bounds(b_me, mesh, lod_coll)
				# link material to mesh
				import_material(reporter, created_materials, in_dir, b_me, m_ob.material)

				if m_ob.mesh_index in ob_dict:
					b_ob = ob_dict[m_ob.mesh_index]
				else:
					b_ob = create_ob(scene, f"{model_info.name}_ob{ob_i}_L{lod_i}", b_me, coll=lod_coll)
					b_ob.parent = b_armature_obj
					ob_dict[m_ob.mesh_index] = b_ob
					try:
						import_vertex_groups(b_ob, mesh, bone_names, sorted_indices)
						import_shapekeys(b_ob, mesh, sorted_indices)
						# link to armature, only after mirror so the order is good and weights are mirrored
						append_armature_modifier(b_ob, b_armature_obj)
						if mirror_mesh:
							append_mirror_modifier(b_ob)
						ob_postpro(mirror_mesh, quadrify)
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
