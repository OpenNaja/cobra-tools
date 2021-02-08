import mathutils
import bpy

from generated.formats.ms2.compound.BoundingBox import BoundingBox
from generated.formats.ms2.compound.Capsule import Capsule
from generated.formats.ms2.compound.HitCheckEntry import HitCheckEntry
from generated.formats.ms2.compound.Sphere import Sphere
from generated.formats.ms2.compound.packing_utils import pack_swizzle
from generated.formats.ms2.enum.CollisionType import CollisionType


def export_hitcheck(b_obj, hitcheck):
	hitcheck.name = b_obj.name
	if b_obj.display_bounds_type == 'SPHERE':
		export_spherebv(b_obj, hitcheck)
	elif b_obj.display_bounds_type == 'BOX':
		export_boxbv(b_obj, hitcheck)
	elif b_obj.display_bounds_type == 'CAPSULE':
		export_capsulebv(b_obj, hitcheck)
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


def export_boxbv(b_obj, hitcheck):
	hitcheck.type = CollisionType.BoundingBox
	hitcheck.collider = BoundingBox()

	matrix = get_collider_matrix(b_obj)
	c = hitcheck.collider.center
	c.x, c.y, c.z = pack_swizzle(matrix.translation)
	e = hitcheck.collider.extent
	e.y, e.x, e.z = pack_swizzle(b_obj.dimensions)


def export_capsulebv(b_obj, hitcheck):
	hitcheck.type = CollisionType.Capsule
	hitcheck.collider = Capsule()

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
