class AuxEntry:

	"""
	describes an external AUX resource
	"""

	def __init__(self, arg=None, template=None):
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# index into files list
		self.file_index = 0

		# maybe index into extension list
		self.extension_index = 0

		# byte count of the complete external resource file
		self.size = 0

	def read(self, stream):

		self.io_start = stream.tell()
		self.file_index = stream.read_uint()
		self.extension_index = stream.read_uint()
		self.size = stream.read_uint()

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_uint(self.file_index)
		stream.write_uint(self.extension_index)
		stream.write_uint(self.size)

		self.io_size = stream.tell() - self.io_start

	def __repr__(self):
		s = 'AuxEntry [Size: '+str(self.io_size)+', Address:'+str(self.io_start)+']'
		s += '\n	* file_index = ' + self.file_index.__repr__()
		s += '\n	* extension_index = ' + self.extension_index.__repr__()
		s += '\n	* size = ' + self.size.__repr__()
		s += '\n'
		return s
