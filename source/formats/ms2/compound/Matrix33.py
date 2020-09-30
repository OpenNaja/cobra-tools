class Matrix33:

	# START_CLASS

	def __str__(self):
		return (
				"[ %6.3f %6.3f %6.3f ]\n"
				"[ %6.3f %6.3f %6.3f ]\n"
				"[ %6.3f %6.3f %6.3f ]\n"
				% (self.m_11, self.m_12, self.m_13, self.m_21, self.m_22, self.m_23, self.m_31, self.m_32, self.m_33))
