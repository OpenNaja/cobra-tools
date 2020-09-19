class FileEntry:

# Description of one file in the archive

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

	def read(self, stream):
		self.offset = stream.read_uint()
		self.file_hash = stream.read_uint()
		self.unkn_0 = stream.read_byte()
		self.unkn_1 = stream.read_byte()
		self.extension = stream.read_ushort()

	def write(self, stream):
		stream.write_uint(self.offset)
		stream.write_uint(self.file_hash)
		stream.write_byte(self.unkn_0)
		stream.write_byte(self.unkn_1)
		stream.write_ushort(self.extension)

	def __repr__(self):
		s = 'FileEntry'
		s += '\noffset ' + self.offset.__repr__()
		s += '\nfile_hash ' + self.file_hash.__repr__()
		s += '\nunkn_0 ' + self.unkn_0.__repr__()
		s += '\nunkn_1 ' + self.unkn_1.__repr__()
		s += '\nextension ' + self.extension.__repr__()
		s += '\n'
		return s