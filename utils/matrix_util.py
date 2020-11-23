import mathutils
import math
import bpy
from bpy_extras.io_utils import axis_conversion

THETA_THRESHOLD_NEGY = 1.0e-9
THETA_THRESHOLD_NEGY_CLOSE = 1.0e-5

# a tuple of prefix, clipped prefix, suffix
naming_convention = (
	("def_r_", "def_", ".R"),
	("def_l_", "def_", ".L"),
)


def vec_roll_to_mat3(vec, roll):
	# port of the updated C function from armature.c
	# https://developer.blender.org/T39470
	# note that C accesses columns first, so all matrix indices are swapped compared to the C version

	nor = vec.normalized()

	# create a 3x3 matrix
	b_matrix = mathutils.Matrix().to_3x3()

	theta = 1.0 + nor[1]

	if (theta > THETA_THRESHOLD_NEGY_CLOSE) or ((nor[0] or nor[2]) and theta > THETA_THRESHOLD_NEGY):

		b_matrix[1][0] = -nor[0]
		b_matrix[0][1] = nor[0]
		b_matrix[1][1] = nor[1]
		b_matrix[2][1] = nor[2]
		b_matrix[1][2] = -nor[2]
		if theta > THETA_THRESHOLD_NEGY_CLOSE:
			# If nor is far enough from -Y, apply the general case.
			b_matrix[0][0] = 1 - nor[0] * nor[0] / theta
			b_matrix[2][2] = 1 - nor[2] * nor[2] / theta
			b_matrix[0][2] = b_matrix[2][0] = -nor[0] * nor[2] / theta

		else:
			# If nor is too close to -Y, apply the special case.
			theta = nor[0] * nor[0] + nor[2] * nor[2]
			b_matrix[0][0] = (nor[0] + nor[2]) * (nor[0] - nor[2]) / -theta
			b_matrix[2][2] = -b_matrix[0][0]
			b_matrix[0][2] = b_matrix[2][0] = 2.0 * nor[0] * nor[2] / theta

	else:
		# If nor is -Y, simple symmetry by Z axis.
		b_matrix = mathutils.Matrix().to_3x3()
		b_matrix[0][0] = b_matrix[1][1] = -1.0

	# Make Roll matrix
	r_matrix = mathutils.Matrix.Rotation(roll, 3, nor)

	# Combine and output result
	mat = r_matrix @ b_matrix
	return mat


def mat3_to_vec_roll(mat):
	# this hasn't changed
	vec = mat.col[1]
	vecmat = vec_roll_to_mat3(mat.col[1], 0)
	vecmatinv = vecmat.inverted()
	rollmat = vecmatinv @ mat
	roll = math.atan2(rollmat[0][2], rollmat[2][2])
	return vec, roll


def bone_name_for_blender(n):
	"""Appends a suffix to the end if relevant prefix was found"""
	for prefix, clipped_prefix, suffix in naming_convention:
		if prefix in n:
			n = n.replace(prefix, clipped_prefix)+suffix
	return n


def bone_name_for_ovl(n):
	"""Restores the proper prefix if relevant suffix was found"""
	for prefix, clipped_prefix, suffix in naming_convention:
		if n.endswith(suffix):
			n = n.replace(suffix, "").replace(clipped_prefix, prefix)
	return n


def nif_bind_to_blender_bind(nif_armature_space_matrix):
	# post multiplication: local space
	y = correction_glob @ nif_armature_space_matrix @ correction_inv
	return xflip @ y


def blender_bind_to_nif_bind(blender_armature_space_matrix):
	bind = blender_armature_space_matrix @ xflip
	y = xflip.inverted() @ bind
	b = correction_glob.inverted() @ y @ correction_inv.inverted()
	return b


correction_glob = axis_conversion("-Z", "Y").to_4x4()
correction_glob_inv = correction_glob.inverted()
correction = axis_conversion("-X", "Y").to_4x4()
correction_inv = correction.inverted()
# mirror about x axis too:
xflip = mathutils.Matrix().to_4x4()
xflip[0][0] = -1
xflip_inv = xflip.inverted()


def import_matrix(m):
	"""Retrieves a niBlock's transform matrix as a Mathutil.Matrix."""
	return mathutils.Matrix(m.as_list())


def get_lod(ob):
	for coll in bpy.data.collections:
		if "LOD" in coll.name and ob.name in coll.objects:
			return coll.name


def to_lod(ob, level=0, lod=None):
	# level is given, but not lod
	if not lod:
		lod = "LOD"+str(level)
	# lod is given, but no level
	else:
		level = int(lod[3:])
		print(level)
	if lod not in bpy.data.collections:
		coll = bpy.data.collections.new(lod)
		bpy.context.scene.collection.children.link(coll)
	else:
		coll = bpy.data.collections[lod]
	# Link active object to the new collection
	coll.objects.link(ob)
	# show lod 0, hide the others
	should_hide = level != 0
	# get view layer, hide collection there
	vlayer = bpy.context.view_layer
	vlayer.layer_collection.children[lod].hide_viewport = should_hide
	# hide object in view layer
	ob.hide_set(should_hide, view_layer=vlayer)
