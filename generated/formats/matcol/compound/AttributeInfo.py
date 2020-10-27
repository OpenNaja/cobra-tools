class AttributeInfo:

	"""
	part of fgm fragment, repeated per attribute
	"""

	def __init__(self, arg=None, template=None):
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# byte offset to name in fgm buffer
		self.offset = 0

		# 6=bool 5=integer 0=float
		self.dtype = 0

		# byte offset to first value in the 4th fragment entry
		self.first_value_offset = 0
		self.zero = 0

	def read(self, stream):

		self.io_start = stream.tell()
		self.offset = stream.read_uint()
		self.dtype = stream.read_uint()
		self.first_value_offset = stream.read_uint()
		self.zero = stream.read_uint()

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_uint(self.offset)
		stream.write_uint(self.dtype)
		stream.write_uint(self.first_value_offset)
		stream.write_uint(self.zero)

		self.io_size = stream.tell() - self.io_start

	def __repr__(self):
		s = 'AttributeInfo [Size: '+str(self.io_size)+', Address:'+str(self.io_start)+']'
		s += '\n	* offset = ' + self.offset.__repr__()
		s += '\n	* dtype = ' + self.dtype.__repr__()
		s += '\n	* first_value_offset = ' + self.first_value_offset.__repr__()
		s += '\n	* zero = ' + self.zero.__repr__()
		s += '\n'
		return s
