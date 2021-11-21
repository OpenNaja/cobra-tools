from generated.context import ContextReference


class Matrix33:

	"""
	A 3x3 rotation matrix; M^T M=identity, det(M)=1.    Stored in OpenGL column-major format.
	"""

	context = ContextReference()

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# Member 1,1 (top left)
		self.m_11 = 1.0

		# Member 2,1
		self.m_21 = 0.0

		# Member 3,1 (bottom left)
		self.m_31 = 0.0

		# Member 1,2
		self.m_12 = 0.0

		# Member 2,2
		self.m_22 = 1.0

		# Member 3,2
		self.m_32 = 0.0

		# Member 1,3 (top right)
		self.m_13 = 0.0

		# Member 2,3
		self.m_23 = 0.0

		# Member 3,3 (bottom left)
		self.m_33 = 1.0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.m_11 = 1.0
		self.m_21 = 0.0
		self.m_31 = 0.0
		self.m_12 = 0.0
		self.m_22 = 1.0
		self.m_32 = 0.0
		self.m_13 = 0.0
		self.m_23 = 0.0
		self.m_33 = 1.0

	def read(self, stream):
		self.io_start = stream.tell()
		self.read_fields(stream, self)
		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()
		self.write_fields(stream, self)
		self.io_size = stream.tell() - self.io_start

	@classmethod
	def read_fields(cls, stream, instance):
		instance.m_11 = stream.read_float()
		instance.m_21 = stream.read_float()
		instance.m_31 = stream.read_float()
		instance.m_12 = stream.read_float()
		instance.m_22 = stream.read_float()
		instance.m_32 = stream.read_float()
		instance.m_13 = stream.read_float()
		instance.m_23 = stream.read_float()
		instance.m_33 = stream.read_float()

	@classmethod
	def write_fields(cls, stream, instance):
		stream.write_float(instance.m_11)
		stream.write_float(instance.m_21)
		stream.write_float(instance.m_31)
		stream.write_float(instance.m_12)
		stream.write_float(instance.m_22)
		stream.write_float(instance.m_32)
		stream.write_float(instance.m_13)
		stream.write_float(instance.m_23)
		stream.write_float(instance.m_33)

	@classmethod
	def from_stream(cls, stream, context, arg=0, template=None):
		instance = cls(context, arg, template, set_default=False)
		instance.io_start = stream.tell()
		cls.read_fields(stream, instance)
		instance.io_size = stream.tell() - instance.io_start
		return instance

	@classmethod
	def to_stream(cls, stream, instance):
		instance.io_start = stream.tell()
		cls.write_fields(stream, instance)
		instance.io_size = stream.tell() - instance.io_start
		return instance

	def get_info_str(self):
		return f'Matrix33 [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* m_11 = {self.m_11.__repr__()}'
		s += f'\n	* m_21 = {self.m_21.__repr__()}'
		s += f'\n	* m_31 = {self.m_31.__repr__()}'
		s += f'\n	* m_12 = {self.m_12.__repr__()}'
		s += f'\n	* m_22 = {self.m_22.__repr__()}'
		s += f'\n	* m_32 = {self.m_32.__repr__()}'
		s += f'\n	* m_13 = {self.m_13.__repr__()}'
		s += f'\n	* m_23 = {self.m_23.__repr__()}'
		s += f'\n	* m_33 = {self.m_33.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
