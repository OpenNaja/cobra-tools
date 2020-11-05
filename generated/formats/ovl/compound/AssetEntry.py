class AssetEntry:

	"""
	refers to sized string entries so they can be grouped into set entries.
	It seems to point exclusively to SizedStringEntry's whose Ext Hash is FF FF FF FF aka max uint32
	"""

	def __init__(self, arg=None, template=None):
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# sometimes matches an archive header's first File Hash
		self.file_hash = 0
		self.zero_0 = 0

		# always (?) matches an archive header's hash
		self.ext_hash = 0
		self.zero_1 = 0

		# index into sized string entries array; hash of targeted file matches this assetentry's hash.
		self.file_index = 0
		self.zero_2 = 0

	def read(self, stream):

		self.io_start = stream.tell()
		self.file_hash = stream.read_uint()
		self.zero_0 = stream.read_uint()
		if (((stream.user_version == 24724) or (stream.user_version == 25108)) and (stream.version == 19)) or ((stream.user_version == 8340) and (stream.version == 19)):
			self.ext_hash = stream.read_uint()
			self.zero_1 = stream.read_uint()
		self.file_index = stream.read_uint()
		self.zero_2 = stream.read_uint()

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_uint(self.file_hash)
		stream.write_uint(self.zero_0)
		if (((stream.user_version == 24724) or (stream.user_version == 25108)) and (stream.version == 19)) or ((stream.user_version == 8340) and (stream.version == 19)):
			stream.write_uint(self.ext_hash)
			stream.write_uint(self.zero_1)
		stream.write_uint(self.file_index)
		stream.write_uint(self.zero_2)

		self.io_size = stream.tell() - self.io_start

	def __repr__(self):
		s = 'AssetEntry [Size: '+str(self.io_size)+', Address:'+str(self.io_start)+']'
		s += '\n	* file_hash = ' + self.file_hash.__repr__()
		s += '\n	* zero_0 = ' + self.zero_0.__repr__()
		s += '\n	* ext_hash = ' + self.ext_hash.__repr__()
		s += '\n	* zero_1 = ' + self.zero_1.__repr__()
		s += '\n	* file_index = ' + self.file_index.__repr__()
		s += '\n	* zero_2 = ' + self.zero_2.__repr__()
		s += '\n'
		return s
