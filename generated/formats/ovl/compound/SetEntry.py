class SetEntry:

	"""
	the asset indices of two consecutive SetEntries define a set of AssetEntries
	"""

	# sometimes matches an archive header's first File Hash
	file_hash: int

	# always (?) matches an archive header's hash
	ext_hash: int

	# add from last set's entry up to this index to this set
	start: int

	def __init__(self, arg=None, template=None):
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.file_hash = 0
		self.ext_hash = 0
		self.start = 0

	def read(self, stream):

		io_start = stream.tell()
		self.file_hash = stream.read_uint()
		if ((stream.user_version == 24724) and (stream.version == 19)) or ((stream.user_version == 8340) and (stream.version == 19)):
			self.ext_hash = stream.read_uint()
		self.start = stream.read_uint()

		self.io_size = stream.tell() - io_start

	def write(self, stream):

		io_start = stream.tell()
		stream.write_uint(self.file_hash)
		if ((stream.user_version == 24724) and (stream.version == 19)) or ((stream.user_version == 8340) and (stream.version == 19)):
			stream.write_uint(self.ext_hash)
		stream.write_uint(self.start)

		self.io_size = stream.tell() - io_start

	def __repr__(self):
		s = 'SetEntry [Size: '+str(self.io_size)+']'
		s += '\n	* file_hash = ' + self.file_hash.__repr__()
		s += '\n	* ext_hash = ' + self.ext_hash.__repr__()
		s += '\n	* start = ' + self.start.__repr__()
		s += '\n'
		return s
