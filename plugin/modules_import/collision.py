import logging

import bpy
import mathutils
import numpy as np

import plugin.utils.transforms
from generated.formats.ms2.structs.packing_utils import unpack_swizzle, unpack_swizzle_collision
from generated.formats.ms2.enums.CollisionType import CollisionType
from plugin.utils import blender_util
from plugin.utils.object import mesh_from_data, create_ob
from plugin.utils.quickhull import qhull3d


def import_collider(hitcheck, b_joint, corrector, collection):
	# logging.debug(f"{hitcheck.name} type {hitcheck.dtype}")
	hitcheck_name = f"{collection.name}_{hitcheck.name}"
	coll = hitcheck.collider
	# print(hitcheck)
	if hitcheck.dtype == CollisionType.SPHERE:
		ob = import_spherebv(coll, hitcheck_name, collection)
	elif hitcheck.dtype == CollisionType.BOUNDING_BOX:
		ob = import_boxbv(coll, hitcheck_name, corrector, collection)
	elif hitcheck.dtype == CollisionType.CAPSULE:
		ob = import_capsulebv(coll, hitcheck_name, collection)
	elif hitcheck.dtype == CollisionType.CYLINDER:
		ob = import_cylinderbv(coll, hitcheck_name, collection)
	elif hitcheck.dtype == CollisionType.MESH_COLLISION:
		ob = import_meshbv(coll, hitcheck_name, corrector, collection)
	elif hitcheck.dtype in (CollisionType.CONVEX_HULL, CollisionType.CONVEX_HULL_P_C):
		ob = import_hullbv(coll, hitcheck_name, corrector, collection)
	else:
		logging.warning(f"Unsupported collider type {hitcheck.dtype}")
		return
	parent_to(b_joint, ob)
	# store the strings on the right enum property
	ob.cobra_coll.set_value(bpy.context, "surface", hitcheck.surface_name)
	ob.cobra_coll.set_value(bpy.context, "classification", hitcheck.classification_name)
	return ob


def set_b_collider(b_obj, bounds_type='BOX', display_type='BOX'):
	"""Helper function to set up b_obj so it becomes recognizable as a collision object"""
	# set bounds type
	if display_type == "MESH":
		b_obj.display_type = 'WIRE'
	else:
		b_obj.show_bounds = True
		b_obj.display_type = 'BOUNDS'
		b_obj.display_bounds_type = display_type

	# alternative
	bpy.context.view_layer.objects.active = b_obj
	with bpy.context.temp_override(selected_objects=[b_obj], object=b_obj, active_object=b_obj):
		logging.debug(f"Operating on obj '{b_obj.name}'")
		bpy.ops.rigidbody.object_add()

	#bpy.context.view_layer.objects.active = b_obj
	#bpy.ops.rigidbody.object_add()

	b_r_body = b_obj.rigid_body
	b_r_body.enabled = True
	# b_r_body.use_margin = True
	# b_r_body.collision_margin = radius
	b_r_body.collision_shape = bounds_type
	# if they are set to active they explode once you play back an anim
	b_r_body.type = "PASSIVE"
	

def box_from_dimensions(b_name, dim, coll=None):
	x, y, z = dim
	return box_from_extents(b_name, -x/2, x/2, -y/2, y/2, -z/2, z/2, coll)


def box_from_extents(b_name, minx, maxx, miny, maxy, minz, maxz, coll=None):
	verts = []
	for x in [minx, maxx]:
		for y in [miny, maxy]:
			for z in [minz, maxz]:
				verts.append((x, y, z))
	faces = [[0, 1, 3, 2], [6, 7, 5, 4], [0, 2, 6, 4], [3, 1, 5, 7], [4, 5, 1, 0], [7, 6, 2, 3]]
	scene = bpy.context.scene
	return mesh_from_data(scene, b_name, verts, faces, coll_name=None, coll=coll)


def center_origin_to_matrix(n_center, n_dir):
	"""Helper for capsules to transform nif data into a local matrix """
	# get the rotation that makes (1,0,0) match m_dir
	n_dir = unpack_swizzle((n_dir.x, n_dir.y, n_dir.z))
	n_center = unpack_swizzle((n_center.x, n_center.y, n_center.z))
	m_dir = mathutils.Vector(n_dir).normalized()
	rot = m_dir.to_track_quat("Z", "Y").to_matrix().to_4x4()
	rot.translation = n_center
	return rot


def import_spherebv(sphere, hitcheck_name, collection):
	r = sphere.radius
	b_obj, b_me = box_from_extents(hitcheck_name, -r, r, -r, r, -r, r, collection)
	b_obj.location = unpack_swizzle((sphere.center.x, sphere.center.y, sphere.center.z))
	set_b_collider(b_obj, bounds_type="SPHERE", display_type="SPHERE")
	return b_obj


def import_collision_matrix(container, corrector):
	mat = mathutils.Matrix(container.data).to_4x4()
	mat.transpose()
	return corrector.to_blender(mat)


def import_collision_quat(q, corrector):
	mat = mathutils.Matrix.Rotation(q.a, 4, get_vec(q))
	# mat = mathutils.Matrix.Rotation(q.a, 4, (q.x, q.y, q.z))
	# mat = mathutils.Quaternion((q.w, q.x, q.y, q.z)).to_matrix().to_4x4()
	# mat = mathutils.Euler((q.x, q.y, q.z)).to_matrix().to_4x4()
	# mat.transpose()
	return mat
	# not sure if a correction is right here
	# return corrector.to_blender(mat)


def import_boxbv(box, hitcheck_name, corrector, collection):
	mat = import_collision_matrix(box.rotation, corrector)
	y, x, z = unpack_swizzle((box.extent.x / 2, box.extent.y / 2, box.extent.z / 2))
	b_obj, b_me = box_from_extents(hitcheck_name, -x, x, -y, y, -z, z, collection)
	mat.translation = unpack_swizzle((box.center.x, box.center.y, box.center.z))
	b_obj.matrix_local = mat
	set_b_collider(b_obj)
	return b_obj


def import_capsulebv(capsule, hitcheck_name, collection):
	# positions of the box verts
	minx = miny = -capsule.radius
	maxx = maxy = +capsule.radius
	minz = -(capsule.extent + 2 * capsule.radius) / 2
	maxz = +(capsule.extent + 2 * capsule.radius) / 2

	# create blender object
	b_obj, b_me = box_from_extents(hitcheck_name, minx, maxx, miny, maxy, minz, maxz, collection)
	# apply transform in local space
	b_obj.matrix_local = center_origin_to_matrix(capsule.offset, capsule.direction)
	set_b_collider(b_obj, bounds_type="CAPSULE", display_type="CAPSULE")
	return b_obj


def import_cylinderbv(cylinder, hitcheck_name, collection):
	# positions of the box verts
	minx = miny = -cylinder.radius
	maxx = maxy = +cylinder.radius
	minz = -cylinder.extent / 2
	maxz = cylinder.extent / 2

	# create blender object
	b_obj, b_me = box_from_extents(hitcheck_name, minx, maxx, miny, maxy, minz, maxz, collection)
	# apply transform in local space
	b_obj.matrix_local = center_origin_to_matrix(cylinder.offset, cylinder.direction)
	set_b_collider(b_obj, bounds_type="CYLINDER", display_type="CYLINDER")
	return b_obj


def import_meshbv(coll, hitcheck_name, corrector, collection):
	# print(coll)
	# print(coll.data)
	scene = bpy.context.scene
	tris = np.flip(coll.data.triangles, axis=-1)
	if coll.is_optimized:
		good_tris = []
		optimizer = coll.data.optimizer
		# unsalt the tri indices per chunk
		for chunk in optimizer.chunks:
			for tri_index in chunk.tri_indices[:chunk.num_used_tri_slots]:
				salt = optimizer.tris_salt[chunk.salt_index]
				if tri_index > -1:
					raw_tris = tris[tri_index:tri_index+16]
					raw_tris -= salt
					good_tris.extend(raw_tris)
		# verify the output
		for i, tri in enumerate(good_tris):
			for v in tri:
				if v >= len(coll.data.vertices):
					logging.warning(f"{i} {tri} is bad")
	else:
		# cast array to list for blender
		good_tris = list(tris)
	b_obj, b_me = mesh_from_data(scene, hitcheck_name, [unpack_swizzle_collision(v) for v in coll.data.vertices], good_tris, coll=collection)
	mat = import_collision_matrix(coll.rotation, corrector)
	mat.translation = unpack_swizzle((coll.offset.x, coll.offset.y, coll.offset.z))
	b_obj.matrix_local = mat
	set_b_collider(b_obj, bounds_type="MESH", display_type="MESH")
	return b_obj


def import_hullbv(coll, hitcheck_name, corrector, collection):
	# print(coll)
	scene = bpy.context.scene
	b_obj, b_me = mesh_from_data(scene, hitcheck_name, *qhull3d([unpack_swizzle_collision(v) for v in coll.vertices]), coll=collection)
	mat = import_collision_matrix(coll.rotation, corrector)
	# this is certainly needed for JWE2 as of 2023-06-12
	mat.translation = unpack_swizzle((coll.offset.x, coll.offset.y, coll.offset.z))
	b_obj.matrix_local = mat
	set_b_collider(b_obj, bounds_type="CONVEX_HULL", display_type="MESH")
	return b_obj


def parent_to(armature_ob, ob, bone_name=None):
	ob.parent = armature_ob
	if bone_name is not None:
		ob.parent_type = 'BONE'
		ob.parent_bone = bone_name
	# this apparently forces an update of the local matrix and parent inverse
	ob.matrix_local = ob.matrix_local
	# doesnt't do the same
	# ob.matrix_parent_inverse = mathutils.Matrix().to_4x4()


def get_vec(v):
	return mathutils.Vector(unpack_swizzle([v.x, v.y, v.z]))


def import_chunk_bounds(mesh_name, mesh, lod_coll):
	scene = bpy.context.scene
	corrector = plugin.utils.transforms.Corrector(False)
	if hasattr(mesh, "tri_chunks"):
		for i, (tri_chunk, vert_chunk) in enumerate(zip(mesh.tri_chunks, mesh.vert_chunks)):

			chunk_name = f"{mesh_name}_{i:03}"
			b_me = bpy.data.meshes.new(chunk_name)
			b_me.from_pydata(vert_chunk.vertices, [], ())
			b_ob = create_ob(scene, chunk_name, b_me, coll=lod_coll)

			v0 = get_vec(tri_chunk.bounds_min)
			v1 = get_vec(tri_chunk.bounds_max)
			loc = get_vec(tri_chunk.loc)

			bbox_name = f"{chunk_name}_bbox"
			v0 -= loc
			v1 -= loc
			b_obj, b_me = box_from_extents(bbox_name, v1[0], v0[0], v1[1], v0[1], v0[2], v1[2], coll=lod_coll)
			set_b_collider(b_obj, bounds_type="CONVEX_HULL", display_type="MESH")
			# print(name, v1[0], v0[0], v1[1], v0[1], v0[2], v1[2], pos.loc, pos.rot)
			# empty = create_ob(bpy.context.scene, name+"_empty", None, coll=lod_coll)
			b_obj.matrix_local = import_collision_quat(tri_chunk.rot, corrector)
			# print(name, pos.rot)
			b_obj.location = loc
			# empty.empty_display_type = "ARROWS"
			# empty.empty_display_size = 0.05
			if i == 10:
				break
