class ZlibInfo:

# Description of one zlib archive

	# seemingly unused in JWE
	zlib_thing_1: int

	# seemingly unused in JWE, subtracting this from ovs uncompressed size to get length of the uncompressed ovs header
	zlib_thing_2: int

	def __init__(self, arg=None, template=None):
		self.arg = arg
		self.template = template

	def read(self, stream):
		self.zlib_thing_1 = stream.read_uint()
		self.zlib_thing_2 = stream.read_uint()

	def write(self, stream):
		stream.write_uint(self.zlib_thing_1)
		stream.write_uint(self.zlib_thing_2)

	def __repr__(self):
		s = 'ZlibInfo'
		s += '\nzlib_thing_1 ' + self.zlib_thing_1.__repr__()
		s += '\nzlib_thing_2 ' + self.zlib_thing_2.__repr__()
		s += '\n'
		return s