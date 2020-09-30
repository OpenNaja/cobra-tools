class HeaderString:

	"""
	The string "DDS ".
	"""

	def __init__(self, arg=None, template=None):
		self.arg = arg
		self.template = template
		self.io_size = 0

	def read(self, stream):

		io_start = stream.tell()

		self.io_size = stream.tell() - io_start

	def write(self, stream):

		io_start = stream.tell()

		self.io_size = stream.tell() - io_start

	def __repr__(self):
		s = 'HeaderString [Size: '+str(self.io_size)+']'
		s += '\n'
		return s
