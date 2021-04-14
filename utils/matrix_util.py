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


def vec_roll_to_mat3_24(vec, roll):
	target = mathutils.Vector((0, 1, 0))
	nor = vec.normalized()
	axis = target.cross(nor)
	if axis.dot(axis) > 0.0000000000001:
		axis.normalize()
		theta = target.angle(nor)
		bMatrix = mathutils.Matrix.Rotation(theta, 3, axis)
	else:
		updown = 1 if target.dot(nor) > 0 else -1
		bMatrix = mathutils.Matrix().to_3x3()
		bMatrix[0][0] = bMatrix[1][1] = updown
	return bMatrix


def vec_roll_to_mat3d(nor, roll):
	nor = nor.normalized()
	print(nor)
	SAFE_THRESHOLD = 6.1e-3     # theta above this value has good enough precision. */
	CRITICAL_THRESHOLD = 2.5e-4 # true singularity if xz distance is below this. */
	THRESHOLD_SQUARED = CRITICAL_THRESHOLD * CRITICAL_THRESHOLD

	x = nor[0]
	y = nor[1]
	z = nor[2]

	theta = 1.0 + y                # remapping Y from [-1,+1] to [0,2]. */
	theta_alt = x * x + z * z # squared distance from origin in x,z plane. */
	b_matrix = mathutils.Matrix().to_3x3()

	# BLI_ASSERT_UNIT_V3(nor);
	#
	# # Determine if the input is far enough from the true singularity of this type of
	#  * transformation at (0,-1,0), where roll becomes 0/0 undefined without a limit.
	#  *
	#  * When theta is close to zero (nor is aligned close to negative Y Axis),
	#  * we have to check we do have non-null X/Z components as well.
	#  * Also, due to float precision errors, nor can be (0.0, -0.99999994, 0.0) which results
	#  * in theta being close to zero. This will cause problems when theta is used as divisor.

	if theta > SAFE_THRESHOLD or theta_alt > THRESHOLD_SQUARED:
		# nor is *not* aligned to negative Y-axis (0,-1,0).

		b_matrix[1][0] = -nor.x
		b_matrix[0][1] = nor.x
		b_matrix[1][1] = nor.y
		b_matrix[2][1] = nor.z
		b_matrix[1][2] = -nor.z

		if theta <= SAFE_THRESHOLD:
			# When nor is close to negative Y axis (0,-1,0) the theta precision is very bad,
			#  * so recompute it from x and z instead, using the series expansion for sqrt. */
			theta = theta_alt * 0.5 + theta_alt * theta_alt * 0.125
			print("Close to -1 y, new theta", theta)

		b_matrix[0][0] = 1 - nor.x * nor.x / theta
		b_matrix[2][2] = 1 - nor.z * nor.z / theta
		b_matrix[0][2] = b_matrix[2][0] = -nor.x * nor.z / theta
		
	else:
		target = mathutils.Vector((0, 1, 0))
		updown = 1 if target.dot(nor) > 0 else -1
		b_matrix = mathutils.Matrix.Scale(updown, 3)
		# print(target.dot(nor), updown)
		print(b_matrix)
		print(roll)
		# /* if nor is a multiple of target ... */
		# float updown;
		#
		# /* point same direction, or opposite? */
		# updown = ( Inpf (target,nor) > 0 ) ? 1.0 : -1.0;
		#
		# /* I think this should work ... */
		# b_matrix = mathutils.Matrix().to_3x3()
		# b_matrix[0][0] = b_matrix[1][1] = updown
		# print(b_matrix)
		# b_matrix = mathutils.Matrix.Scale(updown, 3)
		# b_matrix[0][0] = updown; bMatrix[1][0] = 0.0;    bMatrix[2][0] = 0.0;
		# b_matrix[0][1] = 0.0;    bMatrix[1][1] = updown; bMatrix[2][1] = 0.0;
		# b_matrix[0][2] = 0.0;    bMatrix[1][2] = 0.0;    bMatrix[2][2] = 1.0;
		# # nor is very close to negative Y axis (0,-1,0): use simple symmetry by Z axis.
		# b_matrix = mathutils.Matrix().to_3x3()
		# b_matrix[0][0] = b_matrix[1][1] = -1.0

	# Make Roll matrix
	r_matrix = mathutils.Matrix.Rotation(roll, 3, nor)
	
	# Combine and output result
	return r_matrix @ b_matrix


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


class Corrector:
	def __init__(self, is_zt):
		# axis_conversion(from_forward='Y', from_up='Z', to_forward='Y', to_up='Z')
		self.correction_glob = axis_conversion("-Z", "Y").to_4x4()
		self.correction_glob_inv = self.correction_glob.inverted()
		if is_zt:
			self.correction = axis_conversion("X", "Y").to_4x4()
		else:
			self.correction = axis_conversion("-X", "Y").to_4x4()
		self.correction_inv = self.correction.inverted()
		# mirror about x axis too:
		self.xflip = mathutils.Matrix().to_4x4()
		self.xflip[0][0] = -1

	# https://stackoverflow.com/questions/1263072/changing-a-matrix-from-right-handed-to-left-handed-coordinate-system
	def nif_bind_to_blender_bind(self, nif_armature_space_matrix):
		# post multiplication: local space
		# position of xflip does not matter
		return self.xflip @ self.correction_glob @ nif_armature_space_matrix @ self.correction_inv @ self.xflip

	def blender_bind_to_nif_bind(self, blender_armature_space_matrix):
		# xflip must be done before the conversions
		bind = self.xflip @ blender_armature_space_matrix @ self.xflip
		return self.correction_glob_inv @ bind @ self.correction


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


def eval_me(ob):
	dg = bpy.context.evaluated_depsgraph_get()
	# make a copy with all modifiers applied
	eval_obj = ob.evaluated_get(dg)
	me = eval_obj.to_mesh(preserve_all_data_layers=True, depsgraph=dg)
	return eval_obj, me
