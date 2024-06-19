import logging
import os
import time

import bpy

from plugin.modules_import.armature import import_armature, append_armature_modifier, import_vertex_groups, \
	get_bone_names
from plugin.modules_import.geometry import import_mesh_layers, import_shapekeys, ob_postpro, append_mirror_modifier, \
	get_valid_lod_objects, import_mesh_properties
from plugin.modules_import.material import import_material
from plugin.utils.hair import add_psys
from plugin.utils.shell import is_shell, gauge_uv_scale_wrapper
from plugin.utils.object import create_ob, create_scene, create_collection, set_collection_visibility
from generated.formats.ms2 import Ms2File


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
			for ob_i, m_ob in enumerate(get_valid_lod_objects(m_lod)):
				mesh = m_ob.mesh
				# print(mesh)
				# logging.debug(f"flag {mesh.flag}")
				if m_ob.mesh_index in mesh_dict:
					b_me = mesh_dict[m_ob.mesh_index]
				# create object and mesh from data
				else:
					b_me = bpy.data.meshes.new(f"{model_info.name}_model{m_ob.mesh_index}")
					b_me.from_pydata(mesh.vertices, [], mesh.tris)
					mesh_dict[m_ob.mesh_index] = b_me
					import_mesh_properties(b_me, mesh)
					try:
						import_mesh_layers(b_me, mesh, use_custom_normals, m_ob.material.name)
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
						import_vertex_groups(b_ob, mesh, bone_names)
						import_shapekeys(b_ob, mesh)
						# link to armature, only after mirror so the order is good and weights are mirrored
						append_armature_modifier(b_ob, b_armature_obj)
						if mirror_mesh:
							append_mirror_modifier(b_ob)
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
