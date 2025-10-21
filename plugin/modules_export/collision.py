import logging

import mathutils
import numpy as np

from generated.formats.ms2.structs.MeshCollisionData import MeshCollisionData
from generated.formats.ms2.structs.packing_utils import pack_swizzle, pack_swizzle_collision
from generated.formats.ms2.enums.CollisionType import CollisionType
from plugin.utils.blender_util import evaluate_mesh, ensure_tri_modifier, get_joint_name

v = 9999


def export_bounds(bounds, model_info):
	logging.debug("Exporting bounds")
	bounds_max, bounds_min = get_bounds(bounds)
	assign_bounds(model_info, bounds_max, bounds_min)
	center = (bounds_min+bounds_max)/2
	model_info.center.set(center)
	model_info.radius = (center-bounds_max).length*0.77


def assign_bounds(target, bounds_max, bounds_min):
	target.bounds_max.set(bounds_max)
	target.bounds_min.set(bounds_min)
	if hasattr(target, "bounds_max_repeat"):
		target.bounds_max_repeat.set(bounds_max)
		target.bounds_min_repeat.set(bounds_min)


def get_bounds(bounds, swizzle_func=pack_swizzle):
	bounds_max = mathutils.Vector((-v, -v, -v))
	bounds_min = mathutils.Vector((v, v, v))
	if not bounds:
		zero_vec = mathutils.Vector((0, 0, 0))
		return zero_vec, zero_vec
	for bound in bounds:
		for co in bound:
			for i in range(3):
				vec = swizzle_func(co)
				bounds_min[i] = min(bounds_min[i], vec[i])
				bounds_max[i] = max(bounds_max[i], vec[i])
	return bounds_max, bounds_min


def export_hitcheck(b_obj, hitcheck, corrector, b_armature_basename):
	hitcheck.name = get_joint_name(b_armature_basename, b_obj)
	b_rb = b_obj.rigid_body
	if not b_rb:
		raise AttributeError(f"No rigid body on {b_obj.name} - can't identify collision type.")
	b_type = b_rb.collision_shape
	if b_type == 'MESH':
		export_meshbv(b_obj, hitcheck, corrector)
	elif b_type == 'SPHERE':
		export_spherebv(b_obj, hitcheck)
	elif b_type == 'BOX':
		export_boxbv(b_obj, hitcheck, corrector)
	elif b_type == 'CAPSULE':
		export_capsulebv(b_obj, hitcheck)
	elif b_type == 'CYLINDER':
		export_cylinderbv(b_obj, hitcheck)
	elif b_type == 'CONVEX_HULL':
		export_hullbv(b_obj, hitcheck, corrector)
	else:
		raise AttributeError(f"Unsupported display type for {b_obj.name} - can't identify collision type.")
	return hitcheck


def get_collider_matrix(b_hitcheck):
	"""Return the matrix relative to the armature for an object parented to a bone"""
	# reflect the parenting: bone > joint > hitchecks
	b_joint = b_hitcheck.parent
	b_bone = b_joint.parent.data.bones[b_joint.parent_bone]
	m = mathutils.Matrix(b_joint.matrix_local)
	m.translation.y += b_bone.length
	return b_bone.matrix_local @ m @ b_hitcheck.matrix_local


def export_spherebv(b_obj, hitcheck):
	hitcheck.dtype = CollisionType.SPHERE
	hitcheck.reset_field("collider")

	matrix = get_collider_matrix(b_obj)
	hitcheck.collider.radius = b_obj.dimensions.x / 2
	c = hitcheck.collider.center
	c.x, c.y, c.z = pack_swizzle(matrix.translation)


def export_boxbv(b_obj, hitcheck, corrector):
	hitcheck.dtype = CollisionType.BOUNDING_BOX
	hitcheck.reset_field("collider")

	matrix = get_collider_matrix(b_obj)
	c = hitcheck.collider.center
	c.x, c.y, c.z = pack_swizzle(matrix.translation)
	e = hitcheck.collider.extent
	dim = b_obj.dimensions
	e.x, e.y, e.z = np.abs(pack_swizzle((dim.y, dim.x, dim.z)))
	set_rot_matrix(matrix, hitcheck.collider.rotation, corrector)


def set_rot_matrix(b_matrix_4x4, m_rot_3x3, corrector):
	# get rid of object scale for rot
	rot = corrector.from_blender(b_matrix_4x4).to_3x3().normalized()
	m_rot_3x3.data[:] = rot.transposed()


def export_capsulebv(b_obj, hitcheck):
	hitcheck.dtype = CollisionType.CAPSULE
	hitcheck.reset_field("collider")
	_capsule_transform(b_obj, hitcheck)


def export_cylinderbv(b_obj, hitcheck):
	hitcheck.dtype = CollisionType.CYLINDER
	hitcheck.reset_field("collider")
	_capsule_transform(b_obj, hitcheck)
	# sole difference
	hitcheck.collider.extent = b_obj.dimensions.z


def export_meshbv(b_obj, hitcheck, corrector):
	ensure_tri_modifier(b_obj)
	eval_obj, eval_me = evaluate_mesh(b_obj)
	matrix = get_collider_matrix(b_obj)

	hitcheck.dtype = CollisionType.MESH_COLLISION
	hitcheck.reset_field("collider")
	coll = hitcheck.collider
	for i in range(3):
		coll.indices[i].index = i+1
	bounds_max, bounds_min = get_bounds((b_obj.bound_box, ), swizzle_func=pack_swizzle_collision)
	assign_bounds(coll, bounds_max, bounds_min)

	# export rotation
	set_rot_matrix(matrix, hitcheck.collider.rotation, corrector)
	# export translation
	coll.offset.set(pack_swizzle(matrix.translation))
	# export geometry
	coll.vertex_count = len(eval_me.vertices)
	coll.tri_count = len(eval_me.polygons)
	coll.data = MeshCollisionData(coll.context, coll)
	for vert_i, vert in enumerate(eval_me.vertices):
		coll.data.vertices[vert_i, :] = pack_swizzle_collision(vert.co)
	# export triangles
	for face_i, face in enumerate(eval_me.polygons):
		coll.data.triangles[face_i, :] = face.vertices
		assert len(face.vertices) == 3
	coll.data.triangles = np.flip(coll.data.triangles, axis=-1)
	# print(coll)
	# print(coll.data)


def export_hullbv(b_obj, hitcheck, corrector):
	me = b_obj.data
	matrix = get_collider_matrix(b_obj)

	hitcheck.dtype = CollisionType.CONVEX_HULL
	hitcheck.reset_field("collider")
	coll = hitcheck.collider

	# export rotation
	set_rot_matrix(matrix, hitcheck.collider.rotation, corrector)
	# export translation
	coll.offset.set(pack_swizzle(matrix.translation))
	# export vertices
	coll.vertex_count = len(me.vertices)
	coll.vertices = np.empty((coll.vertex_count, 3), dtype="float")
	# coll.vertices.resize((coll.vertex_count, 3))
	for vert_i, vert in enumerate(me.vertices):
		coll.vertices[vert_i, :] = pack_swizzle_collision(vert.co)


def _capsule_transform(b_obj, hitcheck):
	matrix = get_collider_matrix(b_obj)
	offset = matrix.translation
	# calculate the direction unit vector
	v_dir = (mathutils.Vector((0, 0, 1)) @ matrix.to_3x3().inverted()).normalized()

	c = hitcheck.collider.offset
	c.x, c.y, c.z = pack_swizzle(offset)

	d = hitcheck.collider.direction
	d.x, d.y, d.z = pack_swizzle(v_dir)

	hitcheck.collider.extent = b_obj.dimensions.z - b_obj.dimensions.x
	hitcheck.collider.radius = b_obj.dimensions.x / 2
