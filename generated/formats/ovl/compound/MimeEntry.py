class MimeEntry:

	"""
	Description of one mime type, which is sort of a container for
	Note that for JWE at least, inside the archive not the stored mime hash is used but the extension hash, has to be generated, eg. djb("bani") == 2090104799
	"""

	def __init__(self, arg=None, template=None):
		self.name = ''
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# offset in the header's Names block
		self.offset = 0

		# usually zero
		self.unknown = 0

		# changes with game version; hash of this file extension; same across all files, but seemingly not used anywhere else in the archive
		self.mime_hash = 0

		# usually increments with game
		self.version = 0

		# Id of this class type. Later in the file there is a reference to this Id; offset into FileEntry list in number of files
		self.file_index_offset = 0

		# Number of entries of this class in the file.; from 'file index offset', this many files belong to this file extension
		self.file_count = 0

	def read(self, stream):

		self.io_start = stream.tell()
		self.offset = stream.read_uint()
		self.unknown = stream.read_uint()
		self.mime_hash = stream.read_uint()
		self.version = stream.read_uint()
		stream.version = self.version
		self.file_index_offset = stream.read_uint()
		self.file_count = stream.read_uint()

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_uint(self.offset)
		stream.write_uint(self.unknown)
		stream.write_uint(self.mime_hash)
		stream.write_uint(self.version)
		stream.version = self.version
		stream.write_uint(self.file_index_offset)
		stream.write_uint(self.file_count)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'MimeEntry [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* offset = {self.offset.__repr__()}'
		s += f'\n	* unknown = {self.unknown.__repr__()}'
		s += f'\n	* mime_hash = {self.mime_hash.__repr__()}'
		s += f'\n	* version = {self.version.__repr__()}'
		s += f'\n	* file_index_offset = {self.file_index_offset.__repr__()}'
		s += f'\n	* file_count = {self.file_count.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
