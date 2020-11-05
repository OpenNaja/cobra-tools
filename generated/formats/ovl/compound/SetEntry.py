class SetEntry:

	"""
	the asset indices of two consecutive SetEntries define a set of AssetEntries
	"""

	def __init__(self, arg=None, template=None):
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# sometimes matches an archive header's first File Hash
		self.file_hash = 0

		# always (?) matches an archive header's hash
		self.ext_hash = 0

		# add from last set's entry up to this index to this set
		self.start = 0

	def read(self, stream):

		self.io_start = stream.tell()
		self.file_hash = stream.read_uint()
		if (((stream.user_version == 24724) or (stream.user_version == 25108)) and (stream.version == 19)) or ((stream.user_version == 8340) and (stream.version == 19)):
			self.ext_hash = stream.read_uint()
		self.start = stream.read_uint()

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_uint(self.file_hash)
		if (((stream.user_version == 24724) or (stream.user_version == 25108)) and (stream.version == 19)) or ((stream.user_version == 8340) and (stream.version == 19)):
			stream.write_uint(self.ext_hash)
		stream.write_uint(self.start)

		self.io_size = stream.tell() - self.io_start

	def __repr__(self):
		s = 'SetEntry [Size: '+str(self.io_size)+', Address:'+str(self.io_start)+']'
		s += '\n	* file_hash = ' + self.file_hash.__repr__()
		s += '\n	* ext_hash = ' + self.ext_hash.__repr__()
		s += '\n	* start = ' + self.start.__repr__()
		s += '\n'
		return s
