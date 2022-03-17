from generated.context import ContextReference


class LayerFrag:

	"""
	name_ptr, u0, u1, info_ptr, info_count, u2, u3, attrib_ptr, attrib_count
	"""

	context = ContextReference()

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.name_ptr = 0
		self.u_0 = 0
		self.u_1 = 0
		self.info_ptr = 0
		self.info_count = 0
		self.u_2 = 0
		self.u_3 = 0
		self.attrib_ptr = 0
		self.attrib_count = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.name_ptr = 0
		self.u_0 = 0
		self.u_1 = 0
		self.info_ptr = 0
		self.info_count = 0
		self.u_2 = 0
		self.u_3 = 0
		self.attrib_ptr = 0
		self.attrib_count = 0

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
		instance.name_ptr = stream.read_uint64()
		instance.u_0 = stream.read_uint64()
		instance.u_1 = stream.read_uint64()
		instance.info_ptr = stream.read_uint64()
		instance.info_count = stream.read_uint64()
		instance.u_2 = stream.read_uint64()
		instance.u_3 = stream.read_uint64()
		instance.attrib_ptr = stream.read_uint64()
		instance.attrib_count = stream.read_uint64()

	@classmethod
	def write_fields(cls, stream, instance):
		stream.write_uint64(instance.name_ptr)
		stream.write_uint64(instance.u_0)
		stream.write_uint64(instance.u_1)
		stream.write_uint64(instance.info_ptr)
		stream.write_uint64(instance.info_count)
		stream.write_uint64(instance.u_2)
		stream.write_uint64(instance.u_3)
		stream.write_uint64(instance.attrib_ptr)
		stream.write_uint64(instance.attrib_count)

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
		return f'LayerFrag [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* name_ptr = {self.name_ptr.__repr__()}'
		s += f'\n	* u_0 = {self.u_0.__repr__()}'
		s += f'\n	* u_1 = {self.u_1.__repr__()}'
		s += f'\n	* info_ptr = {self.info_ptr.__repr__()}'
		s += f'\n	* info_count = {self.info_count.__repr__()}'
		s += f'\n	* u_2 = {self.u_2.__repr__()}'
		s += f'\n	* u_3 = {self.u_3.__repr__()}'
		s += f'\n	* attrib_ptr = {self.attrib_ptr.__repr__()}'
		s += f'\n	* attrib_count = {self.attrib_count.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
