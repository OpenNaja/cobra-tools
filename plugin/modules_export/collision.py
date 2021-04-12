import mathutils
import bpy

from generated.formats.ms2.compound.BoundingBox import BoundingBox
from generated.formats.ms2.compound.Capsule import Capsule
from generated.formats.ms2.compound.Cylinder import Cylinder
from generated.formats.ms2.compound.HitCheckEntry import HitCheckEntry
from generated.formats.ms2.compound.MeshCollision import MeshCollision
from generated.formats.ms2.compound.Sphere import Sphere
from generated.formats.ms2.compound.packing_utils import pack_swizzle
from generated.formats.ms2.enum.CollisionType import CollisionType

v = 9999


def export_bounds(bounds, mdl2):
	print("Exporting bounds")
	bounds_max = mathutils.Vector((-v, -v, -v))
	bounds_min = mathutils.Vector((v, v, v))
	for bound in bounds:
		for co in bound:
			for i in range(3):
				vec = pack_swizzle(co)
				bounds_min[i] = min(bounds_min[i], vec[i])
				bounds_max[i] = max(bounds_max[i], vec[i])
	center = (bounds_min+bounds_max)/2
	model_info = mdl2.model_info
	model_info.bounds_max.set(bounds_max)
	model_info.bounds_min.set(bounds_min)
	model_info.bounds_max_repeat.set(bounds_max)
	model_info.bounds_min_repeat.set(bounds_min)
	model_info.center.set(center)
	model_info.radius = (center-bounds_max).length*0.77
	# print(model_info)


def export_hitcheck(b_obj, hitcheck, corrector):
	hitcheck.name = b_obj.name
	if b_obj.display_type == 'WIRE':
		export_meshbv(b_obj, hitcheck)
	elif b_obj.display_type == 'BOUNDS':
		if b_obj.display_bounds_type == 'SPHERE':
			export_spherebv(b_obj, hitcheck)
		elif b_obj.display_bounds_type == 'BOX':
			export_boxbv(b_obj, hitcheck, corrector)
		elif b_obj.display_bounds_type == 'CAPSULE':
			export_capsulebv(b_obj, hitcheck)
		elif b_obj.display_bounds_type == 'CYLINDER':
			export_cylinderbv(b_obj, hitcheck)
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
	hitcheck.collider = Sphere()

	matrix = get_collider_matrix(b_obj)
	hitcheck.collider.radius = b_obj.dimensions.x / 2
	c = hitcheck.collider.center
	c.x, c.y, c.z = pack_swizzle(matrix.translation)


def export_boxbv(b_obj, hitcheck, corrector):
	hitcheck.type = CollisionType.BoundingBox
	hitcheck.collider = BoundingBox()

	matrix = get_collider_matrix(b_obj)
	c = hitcheck.collider.center
	c.x, c.y, c.z = pack_swizzle(matrix.translation)
	e = hitcheck.collider.extent
	dim = b_obj.dimensions
	e.x, e.y, e.z = pack_swizzle((dim.y, dim.x, dim.z))
	rot = corrector.blender_bind_to_nif_bind(matrix).to_3x3()
	hitcheck.collider.rotation.data[:] = rot.transposed()


def export_capsulebv(b_obj, hitcheck):
	hitcheck.type = CollisionType.Capsule
	hitcheck.collider = Capsule()
	_capsule_transform(b_obj, hitcheck)


def export_cylinderbv(b_obj, hitcheck):
	hitcheck.type = CollisionType.Cylinder
	hitcheck.collider = Cylinder()
	_capsule_transform(b_obj, hitcheck)
	# sole difference
	hitcheck.collider.extent = b_obj.dimensions.z


def export_meshbv(b_obj, hitcheck):
	me = b_obj.data

	hitcheck.type = CollisionType.MeshCollision
	hitcheck.collider = MeshCollision()
	coll = hitcheck.collider
	coll.vertex_count = len(me.vertices)
	coll.vertices.resize((coll.vertex_count, 3))
	for vert_i, vert in enumerate(me.vertices):
		coll.vertices[vert_i, :] = pack_swizzle(vert.co)
	coll.tri_count = len(me.polygons)
	coll.triangles.resize((coll.tri_count, 3))
	for face_i, face in enumerate(me.polygons):
		coll.triangles[face_i, :] = face.vertices
		assert len(face.vertices) == 3
	print("Mesh collision export is not supported!")
	print(coll)


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
