from generated.context import ContextReference


class Matrix24:

	"""
	A 4x4 transformation matrix.
	"""

	context = ContextReference()

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		self._context = context
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
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.m_11 = 1.0
		self.m_21 = 0.0
		self.m_31 = 0.0
		self.m_41 = 0.0
		self.m_12 = 0.0
		self.m_22 = 1.0
		self.m_32 = 0.0
		self.m_42 = 0.0

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
		instance.m_41 = stream.read_float()
		instance.m_12 = stream.read_float()
		instance.m_22 = stream.read_float()
		instance.m_32 = stream.read_float()
		instance.m_42 = stream.read_float()

	@classmethod
	def write_fields(cls, stream, instance):
		stream.write_float(instance.m_11)
		stream.write_float(instance.m_21)
		stream.write_float(instance.m_31)
		stream.write_float(instance.m_41)
		stream.write_float(instance.m_12)
		stream.write_float(instance.m_22)
		stream.write_float(instance.m_32)
		stream.write_float(instance.m_42)

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
		return f'Matrix24 [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* m_11 = {self.m_11.__repr__()}'
		s += f'\n	* m_21 = {self.m_21.__repr__()}'
		s += f'\n	* m_31 = {self.m_31.__repr__()}'
		s += f'\n	* m_41 = {self.m_41.__repr__()}'
		s += f'\n	* m_12 = {self.m_12.__repr__()}'
		s += f'\n	* m_22 = {self.m_22.__repr__()}'
		s += f'\n	* m_32 = {self.m_32.__repr__()}'
		s += f'\n	* m_42 = {self.m_42.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
