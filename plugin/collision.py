import mathutils
import bpy

from generated.formats.ms2.compound.packing_utils import unpack_swizzle
from plugin.helpers import mesh_from_data, create_ob


def set_b_collider(b_obj, radius, bounds_type='BOX', display_type='BOX'):
	"""Helper function to set up b_obj so it becomes recognizable as a collision object"""
	# set bounds type
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


def box_from_extents(b_name, minx, maxx, miny, maxy, minz, maxz):
	verts = []
	for x in [minx, maxx]:
		for y in [miny, maxy]:
			for z in [minz, maxz]:
				verts.append((x, y, z))
	faces = [[0, 1, 3, 2], [6, 7, 5, 4], [0, 2, 6, 4], [3, 1, 5, 7], [4, 5, 1, 0], [7, 6, 2, 3]]
	return mesh_from_data(b_name, verts, faces)


def center_origin_to_matrix(n_center, n_dir):
	"""Helper for capsules to transform nif data into a local matrix """
	# get the rotation that makes (1,0,0) match m_dir
	n_dir = unpack_swizzle((n_dir.x, n_dir.y, n_dir.z))
	n_center = unpack_swizzle((n_center.x, n_center.y, n_center.z))
	m_dir = mathutils.Vector(n_dir).normalized()
	rot = m_dir.to_track_quat("Z", "Y").to_matrix().to_4x4()
	rot.translation = n_center
	return rot


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
	set_b_collider(b_obj, bounds_type="CAPSULE", display_type="CAPSULE", radius=capsule.radius)
