class Vector3:

	# START_CLASS

	def set(self, vec):
		if hasattr(vec, "x"):
			self.x = vec.x
			self.y = vec.y
			self.z = vec.z
		else:
			self.x, self.y, self.z = vec

	def __repr__(self):
		return "[ %6.3f %6.3f %6.3f ]" % (self.x, self.y, self.z)
