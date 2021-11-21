from generated.context import ContextReference


class ZerosPadding:

	context = ContextReference()

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.hier_2_padding_0 = 0

		# 128 still has 16 bytes
		self.hier_2_padding_1 = 0

		# 129 is the first with 24 bytes
		self.hier_2_padding_2 = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.hier_2_padding_0 = 0
		if 64 < self.arg:
			self.hier_2_padding_1 = 0
		if 128 < self.arg:
			self.hier_2_padding_2 = 0

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
		instance.hier_2_padding_0 = stream.read_uint64()
		if 64 < instance.arg:
			instance.hier_2_padding_1 = stream.read_uint64()
		if 128 < instance.arg:
			instance.hier_2_padding_2 = stream.read_uint64()

	@classmethod
	def write_fields(cls, stream, instance):
		stream.write_uint64(instance.hier_2_padding_0)
		if 64 < instance.arg:
			stream.write_uint64(instance.hier_2_padding_1)
		if 128 < instance.arg:
			stream.write_uint64(instance.hier_2_padding_2)

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
		return f'ZerosPadding [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* hier_2_padding_0 = {self.hier_2_padding_0.__repr__()}'
		s += f'\n	* hier_2_padding_1 = {self.hier_2_padding_1.__repr__()}'
		s += f'\n	* hier_2_padding_2 = {self.hier_2_padding_2.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
