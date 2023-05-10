from plugin.utils.matrix_util import Corrector
from bpy_extras.io_utils import axis_conversion
import mathutils


class ManisCorrector(Corrector):
	def __init__(self, is_zt):
		# axis_conversion(from_forward='Y', from_up='Z', to_forward='Y', to_up='Z')
		self.correction_glob = axis_conversion("Z", "Y").to_4x4().to_4x4()
		self.correction_glob_inv = self.correction_glob.inverted()
		# if is_zt:
		# 	self.correction = axis_conversion("X", "Y").to_4x4()
		# else:
		# 	self.correction = axis_conversion("-X", "Y").to_4x4()
		self.correction = mathutils.Matrix()
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


class ManisCorrector2(Corrector):
	def __init__(self, is_zt):
		# axis_conversion(from_forward='Y', from_up='Z', to_forward='Y', to_up='Z')
		# self.correction_glob = axis_conversion("Z", "Y").to_4x4()
		# self.correction_glob = axis_conversion("-Y", "Z").to_4x4()
		# my last
		self.correction_glob = axis_conversion("-X", "Y").to_4x4()
		# NDP
		# self.correction_glob = axis_conversion("-Z", "Y").to_4x4()
		# self.correction_glob = mathutils.Matrix()
		self.correction_glob_inv = self.correction_glob.inverted()
		# if is_zt:
		# 	self.correction = axis_conversion("X", "Y").to_4x4()
		# else:
		# 	self.correction = axis_conversion("-X", "Y").to_4x4()
		# my last
		# self.correction = axis_conversion("-Z", "-X").to_4x4()
		# NDP
		# self.correction = axis_conversion("X", "-Y").to_4x4()
		self.correction = mathutils.Matrix()
		# this and no glob is pretty good, but fails the relative transforms
		# self.correction = axis_conversion("X", "Z").to_4x4()
		self.correction_inv = self.correction.inverted()
		# mirror about x axis too:
		self.xflip = mathutils.Matrix().to_4x4()
		self.xflip[0][0] = -1

	# https://stackoverflow.com/questions/1263072/changing-a-matrix-from-right-handed-to-left-handed-coordinate-system
	def nif_bind_to_blender_bind(self, nif_armature_space_matrix):
		# post multiplication: local space
		# position of xflip does not matter
		return self.xflip @ self.correction_glob @ nif_armature_space_matrix @ self.correction_inv @ self.xflip

	# https://github.com/niftools/blender_niftools_addon/blob/e8ede4488e2bb63c07deba06f5aac1a2a68e92e8/io_scene_niftools/utils/math.py#L83
	def blender_bind_to_nif_bind(self, blender_armature_space_matrix):
		# xflip must be done before the conversions
		bind = self.xflip @ blender_armature_space_matrix @ self.xflip
		return self.correction_glob_inv @ bind @ self.correction


class ManisCorrector3(Corrector):
	def __init__(self, is_zt):
		# axis_conversion(from_forward='Y', from_up='Z', to_forward='Y', to_up='Z')
		# self.correction_glob = axis_conversion("Z", "Y").to_4x4()
		# self.correction_glob = axis_conversion("-Y", "Z").to_4x4()
		# my last
		# self.correction_glob = axis_conversion("-X", "Y").to_4x4()
		# NDP
		# self.correction_glob = axis_conversion("-Z", "Y").to_4x4()
		self.correction_glob = mathutils.Matrix()
		self.correction_glob_inv = self.correction_glob.inverted()
		# if is_zt:
		# 	self.correction = axis_conversion("X", "Y").to_4x4()
		# else:
		# 	self.correction = axis_conversion("-X", "Y").to_4x4()
		# my last
		# self.correction = axis_conversion("-Z", "-X").to_4x4()
		# NDP
		# self.correction = axis_conversion("X", "-Y").to_4x4()
		self.correction = mathutils.Matrix()
		# this and no glob is pretty good, but fails the relative transforms
		self.correction = axis_conversion("-Y", "Z").to_4x4()
		# correction in blender to replicate ingame when no transform is active
		# <Quaternion (w=0.5000, x=0.5000, y=-0.5000, z=-0.5000)> <Matrix 3x3 (-0.0000,  0.0000, -1.0000)
		#             (-1.0000, -0.0000,  0.0000)
		#             ( 0.0000,  1.0000, -0.0000)>
		self.correction_inv = self.correction.inverted()
		# mirror about x axis too:
		self.xflip = mathutils.Matrix().to_4x4()
		# self.xflip[0][0] = -1

	# https://stackoverflow.com/questions/1263072/changing-a-matrix-from-right-handed-to-left-handed-coordinate-system
	def nif_bind_to_blender_bind(self, nif_armature_space_matrix):
		# post multiplication: local space
		# position of xflip does not matter
		return self.xflip @ self.correction_glob @ nif_armature_space_matrix @ self.correction_inv @ self.xflip

	# https://github.com/niftools/blender_niftools_addon/blob/e8ede4488e2bb63c07deba06f5aac1a2a68e92e8/io_scene_niftools/utils/math.py#L83
	def blender_bind_to_nif_bind(self, blender_armature_space_matrix):
		# xflip must be done before the conversions
		bind = self.xflip @ blender_armature_space_matrix @ self.xflip
		return self.correction_glob_inv @ bind @ self.correction
