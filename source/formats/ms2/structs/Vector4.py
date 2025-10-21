class Vector4:

	# START_CLASS

	@classmethod
	def format_indented(cls, self, indent=0):
		return f"[ {self.x:6.3f} {self.y:6.3f} {self.z:6.3f} {self.w:6.3f} ]"
