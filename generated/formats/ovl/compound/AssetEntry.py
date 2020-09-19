class AssetEntry:

# refers to sized string entries so they can be grouped into set entries.
# It seems to point exclusively to SizedStringEntry's whose Ext Hash is FF FF FF FF aka max uint32

	# sometimes matches an archive header's first File Hash
	file_hash: int
	zero_0: int

	# always (?) matches an archive header's hash
	ext_hash: int
	zero_1: int

	# index into sized string entries array; hash of targeted file matches this assetentry's hash.
	file_index: int
	zero_2: int

	def __init__(self, arg=None, template=None):
		self.arg = arg
		self.template = template

	def read(self, stream):
		self.file_hash = stream.read_uint()
		self.zero_0 = stream.read_uint()
		self.ext_hash = stream.read_uint()
		self.zero_1 = stream.read_uint()
		self.file_index = stream.read_uint()
		self.zero_2 = stream.read_uint()

	def write(self, stream):
		stream.write_uint(self.file_hash)
		stream.write_uint(self.zero_0)
		stream.write_uint(self.ext_hash)
		stream.write_uint(self.zero_1)
		stream.write_uint(self.file_index)
		stream.write_uint(self.zero_2)

	def __repr__(self):
		s = 'AssetEntry'
		s += '\nfile_hash ' + self.file_hash.__repr__()
		s += '\nzero_0 ' + self.zero_0.__repr__()
		s += '\next_hash ' + self.ext_hash.__repr__()
		s += '\nzero_1 ' + self.zero_1.__repr__()
		s += '\nfile_index ' + self.file_index.__repr__()
		s += '\nzero_2 ' + self.zero_2.__repr__()
		s += '\n'
		return s