class DependencyEntry:

	"""
	Description of dependency; links it to an entry (usually fgm) from this archive
	"""

	def __init__(self, arg=None, template=None):
		self.name = ''
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# Hash of this dependency, for lookup in hash dict. Can be either external or internal.
		self.file_hash = 0

		# offset for extension into string name table
		self.offset = 0

		# index into file table, points to the file entry where this dependency is used
		self.file_index = 0

		# usually 0, 1 (dino common), 4 (aardvark), 5 (dilo) or 7 (detailobjects); definitely NOT file type
		self.ovsblock_id = 0

		# probably an address??
		self.pool_offset = 0

	def read(self, stream):

		self.io_start = stream.tell()
		self.file_hash = stream.read_uint()
		self.offset = stream.read_uint()
		self.file_index = stream.read_uint()
		self.ovsblock_id = stream.read_uint()
		self.pool_offset = stream.read_uint()

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_uint(self.file_hash)
		stream.write_uint(self.offset)
		stream.write_uint(self.file_index)
		stream.write_uint(self.ovsblock_id)
		stream.write_uint(self.pool_offset)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'DependencyEntry [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* file_hash = {self.file_hash.__repr__()}'
		s += f'\n	* offset = {self.offset.__repr__()}'
		s += f'\n	* file_index = {self.file_index.__repr__()}'
		s += f'\n	* ovsblock_id = {self.ovsblock_id.__repr__()}'
		s += f'\n	* pool_offset = {self.pool_offset.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
