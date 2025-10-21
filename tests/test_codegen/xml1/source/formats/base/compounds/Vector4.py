class Vector4:

	# START_CLASS

	def __setitem__(self, k, v):
		self.x, self.y, self.z, self.w = v

	def set(self, vec):
		if hasattr(vec, "x"):
			self.x = vec.x
			self.y = vec.y
			self.z = vec.z
			self.w = vec.w
		else:
			self.x, self.y, self.z, self.w = vec

	@staticmethod
	def format_indented(self, indent=0):
		return f"[ {self.w:6.3f} {self.x:6.3f} {self.y:6.3f} {self.z:6.3f} ]"

	def __eq__(self, other):
		if hasattr(other, "x"):
			return self.x == other.x and self.y == other.y and self.z == other.z and self.w == other.w
