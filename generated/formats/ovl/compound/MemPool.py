class MemPool:

	"""
	Description of one archive header entry
	"""

	def __init__(self, arg=None, template=None):
		self.name = ''
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# always 0
		self.zero_1 = 0

		# the number of bytes representing the text files data
		self.size = 0

		# starting point to read text file data
		self.offset = 0

		# always 0
		self.zero_2 = 0

		# DJB hash of the first file in the txt data block
		self.file_hash = 0

		# unknown count (number of .txt files)
		self.num_files = 0

		# JWE: DJB hash for extension, 0 for PZ
		self.ext_hash = 0

		# always 0
		self.zero_3 = 0

	def read(self, stream):

		self.io_start = stream.tell()
		if not (stream.version == 15):
			self.zero_1 = stream.read_uint64()
		self.size = stream.read_uint()
		self.offset = stream.read_uint()
		if stream.version == 15:
			self.zero_2 = stream.read_uint64()
		self.file_hash = stream.read_uint()
		self.num_files = stream.read_uint()
		if stream.version >= 19:
			self.ext_hash = stream.read_uint()
			self.zero_3 = stream.read_uint()

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		if not (stream.version == 15):
			stream.write_uint64(self.zero_1)
		stream.write_uint(self.size)
		stream.write_uint(self.offset)
		if stream.version == 15:
			stream.write_uint64(self.zero_2)
		stream.write_uint(self.file_hash)
		stream.write_uint(self.num_files)
		if stream.version >= 19:
			stream.write_uint(self.ext_hash)
			stream.write_uint(self.zero_3)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'MemPool [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* zero_1 = {self.zero_1.__repr__()}'
		s += f'\n	* size = {self.size.__repr__()}'
		s += f'\n	* offset = {self.offset.__repr__()}'
		s += f'\n	* zero_2 = {self.zero_2.__repr__()}'
		s += f'\n	* file_hash = {self.file_hash.__repr__()}'
		s += f'\n	* num_files = {self.num_files.__repr__()}'
		s += f'\n	* ext_hash = {self.ext_hash.__repr__()}'
		s += f'\n	* zero_3 = {self.zero_3.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
