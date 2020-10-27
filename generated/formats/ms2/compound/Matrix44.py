class Matrix44:

	"""
	A 4x4 transformation matrix.
	"""

	def __init__(self, arg=None, template=None):
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# The (1,1) element.
		self.m_11 = 1.0

		# The (2,1) element.
		self.m_21 = 0.0

		# The (3,1) element.
		self.m_31 = 0.0

		# The (4,1) element.
		self.m_41 = 0.0

		# The (1,2) element.
		self.m_12 = 0.0

		# The (2,2) element.
		self.m_22 = 1.0

		# The (3,2) element.
		self.m_32 = 0.0

		# The (4,2) element.
		self.m_42 = 0.0

		# The (1,3) element.
		self.m_13 = 0.0

		# The (2,3) element.
		self.m_23 = 0.0

		# The (3,3) element.
		self.m_33 = 1.0

		# The (4,3) element.
		self.m_43 = 0.0

		# The (1,4) element.
		self.m_14 = 0.0

		# The (2,4) element.
		self.m_24 = 0.0

		# The (3,4) element.
		self.m_34 = 0.0

		# The (4,4) element.
		self.m_44 = 1.0

	def read(self, stream):

		self.io_start = stream.tell()
		self.m_11 = stream.read_float()
		self.m_21 = stream.read_float()
		self.m_31 = stream.read_float()
		self.m_41 = stream.read_float()
		self.m_12 = stream.read_float()
		self.m_22 = stream.read_float()
		self.m_32 = stream.read_float()
		self.m_42 = stream.read_float()
		self.m_13 = stream.read_float()
		self.m_23 = stream.read_float()
		self.m_33 = stream.read_float()
		self.m_43 = stream.read_float()
		self.m_14 = stream.read_float()
		self.m_24 = stream.read_float()
		self.m_34 = stream.read_float()
		self.m_44 = stream.read_float()

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_float(self.m_11)
		stream.write_float(self.m_21)
		stream.write_float(self.m_31)
		stream.write_float(self.m_41)
		stream.write_float(self.m_12)
		stream.write_float(self.m_22)
		stream.write_float(self.m_32)
		stream.write_float(self.m_42)
		stream.write_float(self.m_13)
		stream.write_float(self.m_23)
		stream.write_float(self.m_33)
		stream.write_float(self.m_43)
		stream.write_float(self.m_14)
		stream.write_float(self.m_24)
		stream.write_float(self.m_34)
		stream.write_float(self.m_44)

		self.io_size = stream.tell() - self.io_start

	def __repr__(self):
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

