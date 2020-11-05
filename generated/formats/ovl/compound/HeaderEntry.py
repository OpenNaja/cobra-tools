class HeaderEntry:

	"""
	Description of one archive header entry
	"""

	def __init__(self, arg=None, template=None):
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# always 0
		self.zeros_1 = 0

		# always 0
		self.zeros_2 = 0

		# the number of bytes representing the text files data
		self.size = 0

		# starting point to read text file data
		self.offset = 0

		# DJB hash of the first file in the txt data block
		self.file_hash = 0

		# unknown count (number of .txt files)
		self.num_files = 0

		# JWE: DJB hash for extension, 0 for PZ
		self.ext_hash = 0

		# always 0
		self.zeros_3 = 0

	def read(self, stream):

		self.io_start = stream.tell()
		self.zeros_1 = stream.read_uint()
		self.zeros_2 = stream.read_uint()
		self.size = stream.read_uint()
		self.offset = stream.read_uint()
		self.file_hash = stream.read_uint()
		self.num_files = stream.read_uint()
		if (((stream.user_version == 24724) or (stream.user_version == 25108)) and (stream.version == 19)) or ((stream.user_version == 8340) and (stream.version == 19)):
			self.ext_hash = stream.read_uint()
			self.zeros_3 = stream.read_uint()

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_uint(self.zeros_1)
		stream.write_uint(self.zeros_2)
		stream.write_uint(self.size)
		stream.write_uint(self.offset)
		stream.write_uint(self.file_hash)
		stream.write_uint(self.num_files)
		if (((stream.user_version == 24724) or (stream.user_version == 25108)) and (stream.version == 19)) or ((stream.user_version == 8340) and (stream.version == 19)):
			stream.write_uint(self.ext_hash)
			stream.write_uint(self.zeros_3)

		self.io_size = stream.tell() - self.io_start

	def __repr__(self):
		s = 'HeaderEntry [Size: '+str(self.io_size)+', Address:'+str(self.io_start)+']'
		s += '\n	* zeros_1 = ' + self.zeros_1.__repr__()
		s += '\n	* zeros_2 = ' + self.zeros_2.__repr__()
		s += '\n	* size = ' + self.size.__repr__()
		s += '\n	* offset = ' + self.offset.__repr__()
		s += '\n	* file_hash = ' + self.file_hash.__repr__()
		s += '\n	* num_files = ' + self.num_files.__repr__()
		s += '\n	* ext_hash = ' + self.ext_hash.__repr__()
		s += '\n	* zeros_3 = ' + self.zeros_3.__repr__()
		s += '\n'
		return s
