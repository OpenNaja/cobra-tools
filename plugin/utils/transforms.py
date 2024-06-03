from bpy_extras.io_utils import axis_conversion
import mathutils


class Corrector:
	def __init__(self, is_zt):
		# axis_conversion(from_forward='Y', from_up='Z', to_forward='Y', to_up='Z')
		self.correction_glob = axis_conversion("-Z", "Y").to_4x4()
		self.correction_glob_inv = self.correction_glob.inverted()
		if is_zt:
			# from_up=Z or -Z allows legs to be mirrored, but breaks the spine's mirroring
			self.correction = axis_conversion("X", "Y").to_4x4()
		else:
			self.correction = axis_conversion("-X", "Y").to_4x4()
		self.correction_inv = self.correction.inverted()
		# mirror about x axis too:
		self.xflip = mathutils.Matrix().to_4x4()
		self.xflip[0][0] = -1

	# https://stackoverflow.com/questions/1263072/changing-a-matrix-from-right-handed-to-left-handed-coordinate-system
	def to_blender(self, nif_armature_space_matrix):
		# post multiplication: local space
		# position of xflip does not matter
		return self.xflip @ self.correction_glob @ nif_armature_space_matrix @ self.correction_inv @ self.xflip

	def from_blender(self, blender_armature_space_matrix):
		# xflip must be done before the conversions
		bind = self.xflip @ blender_armature_space_matrix @ self.xflip
		return self.correction_glob_inv @ bind @ self.correction


class ManisCorrector(Corrector):
	def __init__(self, is_zt):
		super().__init__(is_zt)
		# affects loc and orientation of rotation
		if is_zt:
			self.correction_glob = axis_conversion("X", "Y").to_4x4()
		else:
			self.correction_glob = axis_conversion("-X", "Y").to_4x4()
		self.correction_glob_inv = self.correction_glob.inverted()
		# the local correction changes the respective axis of a rotation input


class CorrectorRagdoll(Corrector):
	def __init__(self, is_zt):
		super().__init__(is_zt)
		if is_zt:
			self.correction = axis_conversion("X", "Y").to_4x4()
		else:
			self.correction = axis_conversion("-X", "-Y").to_4x4()  # total inversion
		self.correction_inv = self.correction.inverted()
