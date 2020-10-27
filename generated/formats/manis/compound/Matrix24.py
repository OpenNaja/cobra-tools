class Matrix24:

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

		self.io_size = stream.tell() - self.io_start

	def __repr__(self):
		s = 'Matrix24 [Size: '+str(self.io_size)+', Address:'+str(self.io_start)+']'
		s += '\n	* m_11 = ' + self.m_11.__repr__()
		s += '\n	* m_21 = ' + self.m_21.__repr__()
		s += '\n	* m_31 = ' + self.m_31.__repr__()
		s += '\n	* m_41 = ' + self.m_41.__repr__()
		s += '\n	* m_12 = ' + self.m_12.__repr__()
		s += '\n	* m_22 = ' + self.m_22.__repr__()
		s += '\n	* m_32 = ' + self.m_32.__repr__()
		s += '\n	* m_42 = ' + self.m_42.__repr__()
		s += '\n'
		return s
