class DirEntry:

	"""
	Description of one directory in the archive
	"""

	# offset in the header's Names block
	offset: int

	def __init__(self, arg=None, template=None):
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.offset = 0

	def read(self, stream):

		io_start = stream.tell()
		self.offset = stream.read_uint()

		self.io_size = stream.tell() - io_start

	def write(self, stream):

		io_start = stream.tell()
		stream.write_uint(self.offset)

		self.io_size = stream.tell() - io_start

	def __repr__(self):
		s = 'DirEntry [Size: '+str(self.io_size)+']'
		s += '\n	* offset = ' + self.offset.__repr__()
		s += '\n'
		return s
