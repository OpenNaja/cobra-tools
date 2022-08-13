import logging

import bpy
import mathutils

from generated.formats.ms2.compounds.packing_utils import unpack_swizzle
from generated.formats.ms2.enums.CollisionType import CollisionType
from plugin.utils import matrix_util
from plugin.utils.object import mesh_from_data, create_ob
from plugin.utils.quickhull import qhull3d


def import_collider(hitcheck, armature_ob, bone_name, corrector):
	logging.info(f"{hitcheck.name} type {hitcheck.type}")
	hitcheck_name = f"{bpy.context.scene.name}_{hitcheck.name}"
	coll = hitcheck.collider
	# print(hitcheck)
	if hitcheck.type == CollisionType.Sphere:
		ob = import_spherebv(coll, hitcheck_name)
	elif hitcheck.type == CollisionType.BoundingBox:
		ob = import_boxbv(coll, hitcheck_name, corrector)
	elif hitcheck.type == CollisionType.Capsule:
		ob = import_capsulebv(coll, hitcheck_name)
	elif hitcheck.type == CollisionType.Cylinder:
		ob = import_cylinderbv(coll, hitcheck_name)
	elif hitcheck.type == CollisionType.MeshCollision:
		ob = import_meshbv(coll, hitcheck_name, corrector)
	elif hitcheck.type == CollisionType.ConvexHull:
		ob = import_hullbv(coll, hitcheck_name, corrector)
	else:
		logging.warning(f"Unsupported collider type {hitcheck.type}")
		return
	parent_to(armature_ob, ob, bone_name)
	# h = HitCheckEntry()
	# print(export_hitcheck(ob, h))


def set_b_collider(b_obj, radius, bounds_type='BOX', display_type='BOX'):
	"""Helper function to set up b_obj so it becomes recognizable as a collision object"""
	# set bounds type
	if display_type == "MESH":
		b_obj.display_type = 'WIRE'
	else:
		b_obj.show_bounds = True
		b_obj.display_type = 'BOUNDS'
		b_obj.display_bounds_type = display_type

	override = bpy.context.copy()
	override['selected_objects'] = b_obj
	bpy.ops.rigidbody.object_add(override)
	# viable alternative:
	# bpy.context.view_layer.objects.active = b_col_obj
	# bpy.ops.rigidbody.object_add(type='PASSIVE')

	b_r_body = b_obj.rigid_body
	b_r_body.enabled = True
	b_r_body.use_margin = True
	b_r_body.collision_margin = radius
	b_r_body.collision_shape = bounds_type
	# if they are set to active they explode once you play back an anim
	b_r_body.type = "PASSIVE"


def box_from_extents(b_name, minx, maxx, miny, maxy, minz, maxz, coll_name="hitchecks", coll=None):
	verts = []
	for x in [minx, maxx]:
		for y in [miny, maxy]:
			for z in [minz, maxz]:
				verts.append((x, y, z))
	faces = [[0, 1, 3, 2], [6, 7, 5, 4], [0, 2, 6, 4], [3, 1, 5, 7], [4, 5, 1, 0], [7, 6, 2, 3]]
	scene = bpy.context.scene
	return mesh_from_data(scene, b_name, verts, faces, coll_name=coll_name, coll=coll)


def center_origin_to_matrix(n_center, n_dir):
	"""Helper for capsules to transform nif data into a local matrix """
	# get the rotation that makes (1,0,0) match m_dir
	n_dir = unpack_swizzle((n_dir.x, n_dir.y, n_dir.z))
	n_center = unpack_swizzle((n_center.x, n_center.y, n_center.z))
	m_dir = mathutils.Vector(n_dir).normalized()
	rot = m_dir.to_track_quat("Z", "Y").to_matrix().to_4x4()
	rot.translation = n_center
	return rot


def import_spherebv(sphere, hitcheck_name):
	r = sphere.radius
	b_obj, b_me = box_from_extents(hitcheck_name, -r, r, -r, r, -r, r)
	b_obj.location = unpack_swizzle((sphere.center.x, sphere.center.y, sphere.center.z))
	set_b_collider(b_obj, r, bounds_type="SPHERE", display_type="SPHERE")
	return b_obj


def import_collision_matrix(container, corrector):
	mat = mathutils.Matrix(container.data).to_4x4()
	mat.transpose()
	return corrector.nif_bind_to_blender_bind(mat)


def import_collision_quat(q, corrector):
	mat = mathutils.Quaternion((q.w, q.x, q.y, q.z)).to_matrix().to_4x4()
	# mat = mathutils.Euler((q.x, q.y, q.z)).to_matrix().to_4x4()
	# mat.transpose()
	return corrector.nif_bind_to_blender_bind(mat)


def import_boxbv(box, hitcheck_name, corrector):
	mat = import_collision_matrix(box.rotation, corrector)
	y, x, z = unpack_swizzle((box.extent.x / 2, box.extent.y / 2, box.extent.z / 2))
	b_obj, b_me = box_from_extents(hitcheck_name, -x, x, -y, y, -z, z)
	mat.translation = unpack_swizzle((box.center.x, box.center.y, box.center.z))
	b_obj.matrix_local = mat
	set_b_collider(b_obj, (x+y+z)/3)
	return b_obj


def import_capsulebv(capsule, hitcheck_name):
	# positions of the box verts
	minx = miny = -capsule.radius
	maxx = maxy = +capsule.radius
	minz = -(capsule.extent + 2 * capsule.radius) / 2
	maxz = +(capsule.extent + 2 * capsule.radius) / 2

	# create blender object
	b_obj, b_me = box_from_extents(hitcheck_name, minx, maxx, miny, maxy, minz, maxz)
	# apply transform in local space
	b_obj.matrix_local = center_origin_to_matrix(capsule.offset, capsule.direction)
	set_b_collider(b_obj, capsule.radius, bounds_type="CAPSULE", display_type="CAPSULE")
	return b_obj


def import_cylinderbv(cylinder, hitcheck_name):
	# positions of the box verts
	minx = miny = -cylinder.radius
	maxx = maxy = +cylinder.radius
	minz = -cylinder.extent / 2
	maxz = cylinder.extent / 2

	# create blender object
	b_obj, b_me = box_from_extents(hitcheck_name, minx, maxx, miny, maxy, minz, maxz)
	# apply transform in local space
	b_obj.matrix_local = center_origin_to_matrix(cylinder.offset, cylinder.direction)
	set_b_collider(b_obj, cylinder.radius, bounds_type="CYLINDER", display_type="CYLINDER")
	return b_obj


def import_meshbv(coll, hitcheck_name, corrector):
	# print(coll)
	scene = bpy.context.scene
	b_obj, b_me = mesh_from_data(scene, hitcheck_name, [unpack_swizzle(v) for v in coll.vertices], list(coll.triangles), coll_name="hitchecks")
	mat = import_collision_matrix(coll.rotation, corrector)
	mat.translation = unpack_swizzle((coll.offset.x, coll.offset.y, coll.offset.z))
	b_obj.matrix_local = mat
	set_b_collider(b_obj, 1, bounds_type="MESH", display_type="MESH")
	return b_obj


def unpack_swizzle2(vec):
	# swizzle to avoid a matrix multiplication for global axis correction
	# Z, -X, Y
	return vec[2], -vec[0], vec[1]


def import_hullbv(coll, hitcheck_name, corrector):
	# print(coll)
	scene = bpy.context.scene
	b_obj, b_me = mesh_from_data(scene, hitcheck_name, *qhull3d([unpack_swizzle2(v) for v in coll.vertices]), coll_name="hitchecks")
	mat = import_collision_matrix(coll.rotation, corrector)
	# mat.translation = unpack_swizzle((coll.offset.x, coll.offset.y, coll.offset.z))
	b_obj.matrix_local = mat
	set_b_collider(b_obj, 1, bounds_type="CONVEX_HULL", display_type="MESH")
	return b_obj


def parent_to(armature_ob, ob, bone_name):
	ob.parent = armature_ob
	ob.parent_type = 'BONE'
	ob.parent_bone = bone_name
	b_bone = armature_ob.data.bones[bone_name]
	# re-set matrix to update the binding
	ob.matrix_local = ob.matrix_local


def import_chunk_bounds(b_full_me, mesh, lod_coll):
	corrector = matrix_util.Corrector(False)
	if hasattr(mesh, "tri_chunks"):
		for i, pos in enumerate(mesh.tri_chunks):
			name = f"{b_full_me.name}_bbox_{i:03}"
			v0 = unpack_swizzle([pos.bounds_min.x, pos.bounds_min.y, pos.bounds_min.z])
			v1 = unpack_swizzle([pos.bounds_max.x, pos.bounds_max.y, pos.bounds_max.z])
			# print(v0, v1)
			b_obj, b_me = box_from_extents(name, v1[0], v0[0], v1[1], v0[1], v0[2], v1[2], coll_name=None, coll=lod_coll)
			set_b_collider(b_obj, 1, bounds_type="CONVEX_HULL", display_type="MESH")
			# print(name, v1[0], v0[0], v1[1], v0[1], v0[2], v1[2], pos.loc, pos.rot)
			empty = create_ob(bpy.context.scene, name+"_empty", None, coll=lod_coll)
			empty.matrix_local = import_collision_quat(pos.rot, corrector)
			empty.location = unpack_swizzle((pos.loc.x, pos.loc.y, pos.loc.z))
			empty.empty_display_type = "ARROWS"
			empty.empty_display_size = 0.05
			if i == 3:
				break
