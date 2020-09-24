class BufferEntry:

# 8 bytes

	# apparently index of buffer in file, at least that's how it looks in barbasol - 0, 1, 2, 3, 4...
	index: int

	# in bytes
	size: int

	def __init__(self, arg=None, template=None):
		self.arg = arg
		self.template = template

	def read(self, stream):
		self.index = stream.read_uint()
		self.size = stream.read_uint()

	def write(self, stream):
		stream.write_uint(self.index)
		stream.write_uint(self.size)

	def __repr__(self):
		s = 'BufferEntry'
		s += '\n	* index = ' + self.index.__repr__()
		s += '\n	* size = ' + self.size.__repr__()
		s += '\n'
		return s

	def read_data(self, stream):
		"""Load data from archive stream into self for modification and io"""
		self.data = stream.read(self.size)

	def update_data(self, data):
		"""Set data internal data so it can be written on save and update the size value"""
		self.data = data
		self.size = len(data)