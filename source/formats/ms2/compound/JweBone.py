class JweBone:

	# START_CLASS

	def set_bone(self, matrix):
		pos, quat, sca = matrix.decompose()
		self.loc.x, self.loc.y, self.loc.z = -1 * pos.y, pos.z, pos.x
		self.rot.x, self.rot.y, self.rot.z, self.rot.w = quat.y, -1 * quat.z, -1 * quat.x, quat.w
		self.scale = sca.x
