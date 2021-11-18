from generated.context import ContextReference


class ZlibInfo:

	"""
	Description of one zlib archive
	"""

	context = ContextReference()

	def __init__(self, context, arg=None, template=None, set_default=True):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# seemingly unused in JWE
		self.zlib_thing_1 = 0

		# seemingly unused in JWE, subtracting this from ovs uncompressed_size to get length of the uncompressed ovs header
		self.zlib_thing_2 = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.zlib_thing_1 = 0
		self.zlib_thing_2 = 0

	def read(self, stream):
		self.io_start = stream.tell()
		self.zlib_thing_1 = stream.read_uint()
		self.zlib_thing_2 = stream.read_uint()

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()
		stream.write_uint(self.zlib_thing_1)
		stream.write_uint(self.zlib_thing_2)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'ZlibInfo [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* zlib_thing_1 = {self.zlib_thing_1.__repr__()}'
		s += f'\n	* zlib_thing_2 = {self.zlib_thing_2.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
