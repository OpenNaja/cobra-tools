class ZlibInfo:

	"""
	Description of one zlib archive
	"""

	# seemingly unused in JWE
	zlib_thing_1: int

	# seemingly unused in JWE, subtracting this from ovs uncompressed size to get length of the uncompressed ovs header
	zlib_thing_2: int

	def __init__(self, arg=None, template=None):
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
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

	def __repr__(self):
		s = 'ZlibInfo [Size: '+str(self.io_size)+', Address:'+str(self.io_start)+']'
		s += '\n	* zlib_thing_1 = ' + self.zlib_thing_1.__repr__()
		s += '\n	* zlib_thing_2 = ' + self.zlib_thing_2.__repr__()
		s += '\n'
		return s
