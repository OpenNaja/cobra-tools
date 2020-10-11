class FileEntry:

	"""
	Description of one file in the archive
	"""

	# offset in the header's Names block; start offset of zero terminated string
	offset: int

	# this hash is used to retrieve the file name from inside the archive
	file_hash: int

	# could be the number of fragments this file is split into; Or the amount of entries that refer to this file
	unkn_0: int
	unkn_1: int

	# index into 'Extensions' array
	extension: int

	def __init__(self, arg=None, template=None):
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.offset = 0
		self.file_hash = 0
		self.unkn_0 = 0
		self.unkn_1 = 0
		self.extension = 0

	def read(self, stream):

		self.io_start = stream.tell()
		self.offset = stream.read_uint()
		self.file_hash = stream.read_uint()
		self.unkn_0 = stream.read_byte()
		self.unkn_1 = stream.read_byte()
		self.extension = stream.read_ushort()

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_uint(self.offset)
		stream.write_uint(self.file_hash)
		stream.write_byte(self.unkn_0)
		stream.write_byte(self.unkn_1)
		stream.write_ushort(self.extension)

		self.io_size = stream.tell() - self.io_start

	def __repr__(self):
		s = 'FileEntry [Size: '+str(self.io_size)+', Address:'+str(self.io_start)+']'
		s += '\n	* offset = ' + self.offset.__repr__()
		s += '\n	* file_hash = ' + self.file_hash.__repr__()
		s += '\n	* unkn_0 = ' + self.unkn_0.__repr__()
		s += '\n	* unkn_1 = ' + self.unkn_1.__repr__()
		s += '\n	* extension = ' + self.extension.__repr__()
		s += '\n'
		return s
