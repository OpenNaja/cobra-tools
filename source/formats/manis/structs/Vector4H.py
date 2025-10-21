class Vector4H:

	# START_CLASS

	@classmethod
	def format_indented(cls, self, indent=0):
		return f"[ W {self.w:6.3f} X {self.x:6.3f} Y {self.y:6.3f} Z {self.z:6.3f} ]"
