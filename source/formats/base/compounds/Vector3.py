class Vector3:

	# START_CLASS

	def __setitem__(self, k, v):
		self.x, self.y, self.z = v

	def set(self, vec):
		if hasattr(vec, "x"):
			self.x = vec.x
			self.y = vec.y
			self.z = vec.z
		else:
			self.x, self.y, self.z = vec

	@staticmethod
	def format_indented(self, indent=0):
		return f"[ {self.x:6.3f} {self.y:6.3f} {self.z:6.3f} ]"

	def __eq__(self, other):
		if hasattr(other, "x"):
			return self.x == other.x and self.y == other.y and self.z == other.z

	def __mul__(self, other):
		if isinstance(other, float):
			self.x *= other
			self.y *= other
			self.z *= other
			return self
		else:
			raise NotImplementedError(f"can't mul Vector3 * {type(other)}")

	def __imul__(self, other):
		return self * other
