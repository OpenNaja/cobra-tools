class Matrix44:

	# START_CLASS

	def __str__(self):
		return f"{self.__class__} instance at {id(self):02x}\n" \
			   f"\t[{self.m_11:7.3f} {self.m_12:7.3f} {self.m_13:7.3f} {self.m_14:7.3f}]\n" \
			   f"\t[{self.m_21:7.3f} {self.m_22:7.3f} {self.m_23:7.3f} {self.m_24:7.3f}]\n" \
			   f"\t[{self.m_31:7.3f} {self.m_32:7.3f} {self.m_33:7.3f} {self.m_34:7.3f}]\n" \
			   f"\t[{self.m_41:7.3f} {self.m_42:7.3f} {self.m_43:7.3f} {self.m_44:7.3f}]"

	def as_list(self):
		"""Return matrix as 4x4 list."""
		return [
			[self.m_11, self.m_12, self.m_13, self.m_14],
			[self.m_21, self.m_22, self.m_23, self.m_24],
			[self.m_31, self.m_32, self.m_33, self.m_34],
			[self.m_41, self.m_42, self.m_43, self.m_44]
		]

	def as_tuple(self):
		"""Return matrix as 4x4 tuple."""
		return (
			(self.m_11, self.m_12, self.m_13, self.m_14),
			(self.m_21, self.m_22, self.m_23, self.m_24),
			(self.m_31, self.m_32, self.m_33, self.m_34),
			(self.m_41, self.m_42, self.m_43, self.m_44)
		)

	def set_rows(self, row0, row1, row2, row3):
		"""Set matrix from rows."""
		self.m_11, self.m_12, self.m_13, self.m_14 = row0
		self.m_21, self.m_22, self.m_23, self.m_24 = row1
		self.m_31, self.m_32, self.m_33, self.m_34 = row2
		self.m_41, self.m_42, self.m_43, self.m_44 = row3
