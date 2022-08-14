import logging

import mathutils
import numpy as np

from generated.formats.ms2.compounds.BoundingBox import BoundingBox
from generated.formats.ms2.compounds.Capsule import Capsule
from generated.formats.ms2.compounds.ConvexHull import ConvexHull
from generated.formats.ms2.compounds.Cylinder import Cylinder
from generated.formats.ms2.compounds.MeshCollision import MeshCollision
from generated.formats.ms2.compounds.Sphere import Sphere
from generated.formats.ms2.compounds.packing_utils import pack_swizzle
from generated.formats.ms2.enums.CollisionType import CollisionType

v = 9999


def export_bounds(bounds, model_info):
	logging.info("Exporting bounds")
	bounds_max, bounds_min = get_bounds(bounds)
	center = (bounds_min+bounds_max)/2
	model_info = model_info
	assign_bounds(model_info, bounds_max, bounds_min)
	model_info.center.set(center)
	model_info.radius = (center-bounds_max).length*0.77


def assign_bounds(model_info, bounds_max, bounds_min):
	model_info.bounds_max.set(bounds_max)
	model_info.bounds_min.set(bounds_min)
	model_info.bounds_max_repeat.set(bounds_max)
	model_info.bounds_min_repeat.set(bounds_min)


def get_bounds(bounds):
	bounds_max = mathutils.Vector((-v, -v, -v))
	bounds_min = mathutils.Vector((v, v, v))
	for bound in bounds:
		for co in bound:
			for i in range(3):
				vec = pack_swizzle(co)
				bounds_min[i] = min(bounds_min[i], vec[i])
				bounds_max[i] = max(bounds_max[i], vec[i])
	return bounds_max, bounds_min


# print(model_info)


def export_hitcheck(b_obj, hitcheck, corrector):
	hitcheck.name = b_obj.name
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


def get_collider_matrix(ob):
	"""Return the matrix relative to the armature for an object parented to a bone"""
	b_bone = ob.parent.data.bones[ob.parent_bone]
	m = mathutils.Matrix(ob.matrix_local)
	m.translation.y += b_bone.length
	return b_bone.matrix_local @ m


def export_spherebv(b_obj, hitcheck):
	hitcheck.type = CollisionType.Sphere
	hitcheck.collider = Sphere(hitcheck.context)

	matrix = get_collider_matrix(b_obj)
	hitcheck.collider.radius = b_obj.dimensions.x / 2
	c = hitcheck.collider.center
	c.x, c.y, c.z = pack_swizzle(matrix.translation)


def export_boxbv(b_obj, hitcheck, corrector):
	hitcheck.type = CollisionType.BoundingBox
	hitcheck.collider = BoundingBox(hitcheck.context)

	matrix = get_collider_matrix(b_obj)
	c = hitcheck.collider.center
	c.x, c.y, c.z = pack_swizzle(matrix.translation)
	e = hitcheck.collider.extent
	dim = b_obj.dimensions
	e.x, e.y, e.z = np.abs(pack_swizzle((dim.y, dim.x, dim.z)))
	set_rot_matrix(matrix, hitcheck.collider.rotation, corrector)


def set_rot_matrix(b_matrix_4x4, m_rot_3x3, corrector):
	rot = corrector.blender_bind_to_nif_bind(b_matrix_4x4).to_3x3()
	m_rot_3x3.data[:] = rot.transposed()


def export_capsulebv(b_obj, hitcheck):
	hitcheck.type = CollisionType.Capsule
	hitcheck.collider = Capsule(hitcheck.context)
	_capsule_transform(b_obj, hitcheck)


def export_cylinderbv(b_obj, hitcheck):
	hitcheck.type = CollisionType.Cylinder
	hitcheck.collider = Cylinder(hitcheck.context)
	_capsule_transform(b_obj, hitcheck)
	# sole difference
	hitcheck.collider.extent = b_obj.dimensions.z


def export_meshbv(b_obj, hitcheck, corrector):
	me = b_obj.data
	matrix = get_collider_matrix(b_obj)

	hitcheck.type = CollisionType.MeshCollision
	hitcheck.collider = MeshCollision(hitcheck.context)
	coll = hitcheck.collider

	bounds_max, bounds_min = get_bounds((b_obj.bound_box, ))
	assign_bounds(coll, bounds_max, bounds_min)

	# export rotation
	set_rot_matrix(matrix, hitcheck.collider.rotation, corrector)
	# export translation
	c = coll.offset
	c.x, c.y, c.z = pack_swizzle(matrix.translation)
	# export vertices
	coll.vertex_count = len(me.vertices)
	coll.vertices.resize((coll.vertex_count, 3))
	for vert_i, vert in enumerate(me.vertices):
		coll.vertices[vert_i, :] = pack_swizzle(vert.co)
	# export triangles
	coll.tri_count = len(me.polygons)
	coll.triangles.resize((coll.tri_count, 3))
	for face_i, face in enumerate(me.polygons):
		coll.triangles[face_i, :] = face.vertices
		assert len(face.vertices) == 3


def pack_swizzle2(vec):
	# swizzle to avoid a matrix multiplication for global axis correction
	return -vec[1], vec[2], vec[0]


def export_hullbv(b_obj, hitcheck, corrector):
	me = b_obj.data
	matrix = get_collider_matrix(b_obj)

	hitcheck.type = CollisionType.ConvexHull
	hitcheck.collider = ConvexHull(hitcheck.context)
	coll = hitcheck.collider

	# export rotation
	set_rot_matrix(matrix, hitcheck.collider.rotation, corrector)
	# export translation
	c = coll.offset
	c.x, c.y, c.z = pack_swizzle(matrix.translation)
	# export vertices
	coll.vertex_count = len(me.vertices)
	coll.vertices = np.empty((coll.vertex_count, 3), dtype="float")
	# coll.vertices.resize((coll.vertex_count, 3))
	for vert_i, vert in enumerate(me.vertices):
		coll.vertices[vert_i, :] = pack_swizzle2(vert.co)


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
