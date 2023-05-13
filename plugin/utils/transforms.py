from plugin.utils.matrix_util import Corrector
from bpy_extras.io_utils import axis_conversion
import mathutils


class ManisCorrector(Corrector):
	def __init__(self, is_zt):
		super().__init__(is_zt)
		# affects loc and orientation of rotation
		self.correction_glob = axis_conversion("-X", "Y").to_4x4()
		self.correction_glob_inv = self.correction_glob.inverted()
		# the local correction changes the respective axis of a rotation input
		self.correction = axis_conversion("-X", "Y").to_4x4()
		self.correction_inv = self.correction.inverted()
		# mirror about x axis too:
		self.xflip = mathutils.Matrix().to_4x4()
		self.xflip[0][0] = -1
