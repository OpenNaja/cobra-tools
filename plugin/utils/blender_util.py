import collections
import logging
import re

import mathutils
import bpy

THETA_THRESHOLD_NEGY = 1.0e-9
THETA_THRESHOLD_NEGY_CLOSE = 1.0e-5

# a tuple of prefix, clipped prefix, suffix
naming_convention = (
	("def_r_", "def_", ".R"),
	("def_l_", "def_", ".L"),
)


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


def import_matrix(m):
	"""Retrieves a niBlock's transform matrix as a Mathutil.Matrix."""
	return mathutils.Matrix(m.as_list())


def evaluate_mesh(ob):
	dg = bpy.context.evaluated_depsgraph_get()
	# make a copy with all modifiers applied
	eval_obj = ob.evaluated_get(dg)
	me = eval_obj.to_mesh(preserve_all_data_layers=True, depsgraph=dg)
	return eval_obj, me


def ensure_tri_modifier(ob):
	"""Makes sure that ob has a triangulation modifier in its stack."""
	for mod in ob.modifiers:
		if mod.type in ('TRIANGULATE',):
			break
	else:
		ob.modifiers.new('Triangulate', 'TRIANGULATE')


# match a .001 style suffix
blender_name_suffix_re = re.compile(r'\.\d+$')


def strip_duplicate_suffix(name, dtype="", reporter=None):
	without_copy_suffixes = blender_name_suffix_re.sub('', name)
	if without_copy_suffixes != name:
		msg = f"{dtype} '{name}' seems to be an unwanted duplicate of '{without_copy_suffixes}'"
		if reporter is not None:
			reporter.show_warning(msg)
		logging.warning(msg)
	return without_copy_suffixes


def get_joint_name(b_armature_basename, b_ob):
	joints_prefix = f"{b_armature_basename}_joints"
	ob_name = b_ob.name[len(joints_prefix)+1:]
	long_name = b_ob.get("long_name", None)
	if not long_name:
		# logging.warning(f"Custom property 'long_name' is not set for {b_ob.name}")
		return ob_name
	if len(long_name) > len(ob_name):
		# assert long_name[:len(ob_name)] == ob_name, f"ob name does not match"
		return long_name
	# check for .001 suffixes incase user dupes rig by copy pasting some mesh
	without_copy_suffixes = strip_duplicate_suffix(ob_name, "Joint")
	if without_copy_suffixes != long_name:
		logging.warning(f"Stored long name and blender name don't match for '{ob_name}'")
	return long_name


def get_scale_mat(scale_vec):
	scale_matrix_x2 = mathutils.Matrix.Scale(scale_vec.x, 4, (1.0, 0.0, 0.0))
	scale_matrix_y2 = mathutils.Matrix.Scale(scale_vec.y, 4, (0.0, 1.0, 0.0))
	scale_matrix_z2 = mathutils.Matrix.Scale(scale_vec.z, 4, (0.0, 0.0, 1.0))
	return scale_matrix_x2 @ scale_matrix_y2 @ scale_matrix_z2


class OperatorWrap:
	def __init__(self, op):
		self.op = op
		self.infos = []
		self.warnings = []

	def show_info(self, msg: str):
		self.infos.append(msg)
		logging.info(msg)

	def show_warning(self, msg: str):
		self.warnings.append(msg)
		logging.warning(msg)

	def show_error(self, exception: Exception):
		self.op.report({"ERROR"}, str(exception))
		logging.exception('Got exception on main handler')

	@staticmethod
	def count(msgs):
		for msg, count in collections.Counter(msgs).items():
			if count > 1:
				msg = f"{msg} (x{count})"
			yield msg

	def report(self):
		for msg in self.count(self.warnings):
			self.op.report({"WARNING"}, msg)
		for msg in self.count(self.infos):
			self.op.report({"INFO"}, msg)


def vectorisclose(vector1, vector2, tolerance=0.0001):
	# Determine if the inputs are correctly utilized.
	if not isinstance(vector1, mathutils.Vector) or not isinstance(vector2, mathutils.Vector) or not isinstance(tolerance, float):
		raise TypeError("Input 1 must be a vector. Input 2 must be a vector. Input 3 must be a float.")
	# Compare the components of the vectors.
	if len(vector1) != len(vector2):
		raise TypeError("Both vectors must have the same amount of components")
	# Compare components
	for component in range(0, len(vector1)):
		if not abs(vector1[component] - vector2[component]) < abs(tolerance):
			return False
	return True


def set_auto_smooth_safe(b_me):
	"""Blender 4.1 removes the property and uses custom normals automatically if they are present"""
	if hasattr(b_me, "use_auto_smooth"):
		b_me.use_auto_smooth = True
