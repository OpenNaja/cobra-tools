class MimeEntry:

	"""
	Description of one mime type, which is sort of a container for
	Note that for JWE at least, inside the archive not the stored mime hash is used but the extension hash, has to be generated, eg. djb(".bani") == 2090104799
	"""

	def __init__(self, arg=None, template=None):
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# offset in the header's Names block
		self.offset = 0

		# usually zero
		self.unknown = 0

		# hash of this file extension; same across all files, but seemingly not used anywhere else in the archive
		self.mime_hash = 0
		self.unknown_1 = 0

		# usually zero
		self.unknown_2 = 0

		# offset into FileEntry list in number of files
		self.file_index_offset = 0

		# from 'file index offset', this many files belong to this file extension
		self.file_count = 0

	def read(self, stream):

		self.io_start = stream.tell()
		self.offset = stream.read_uint()
		self.unknown = stream.read_uint()
		self.mime_hash = stream.read_uint()
		self.unknown_1 = stream.read_ushort()
		self.unknown_2 = stream.read_ushort()
		self.file_index_offset = stream.read_uint()
		self.file_count = stream.read_uint()

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_uint(self.offset)
		stream.write_uint(self.unknown)
		stream.write_uint(self.mime_hash)
		stream.write_ushort(self.unknown_1)
		stream.write_ushort(self.unknown_2)
		stream.write_uint(self.file_index_offset)
		stream.write_uint(self.file_count)

		self.io_size = stream.tell() - self.io_start

	def __repr__(self):
		s = 'MimeEntry [Size: '+str(self.io_size)+', Address:'+str(self.io_start)+']'
		s += '\n	* offset = ' + self.offset.__repr__()
		s += '\n	* unknown = ' + self.unknown.__repr__()
		s += '\n	* mime_hash = ' + self.mime_hash.__repr__()
		s += '\n	* unknown_1 = ' + self.unknown_1.__repr__()
		s += '\n	* unknown_2 = ' + self.unknown_2.__repr__()
		s += '\n	* file_index_offset = ' + self.file_index_offset.__repr__()
		s += '\n	* file_count = ' + self.file_count.__repr__()
		s += '\n'
		return s
