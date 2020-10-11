class Texture:

	"""
	each texture = three fragments of format: data0 = 8 bytes zeros | data1 = null terminating string (scale texture name)
	"""
	fgm_name: str
	texture_suffix: str
	texture_type: str

	def __init__(self, arg=None, template=None):
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.fgm_name = 0
		self.texture_suffix = 0
		self.texture_type = 0

	def read(self, stream):

		self.io_start = stream.tell()
		self.fgm_name = stream.read_zstring()
		self.texture_suffix = stream.read_zstring()
		self.texture_type = stream.read_zstring()

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_zstring(self.fgm_name)
		stream.write_zstring(self.texture_suffix)
		stream.write_zstring(self.texture_type)

		self.io_size = stream.tell() - self.io_start

	def __repr__(self):
		s = 'Texture [Size: '+str(self.io_size)+', Address:'+str(self.io_start)+']'
		s += '\n	* fgm_name = ' + self.fgm_name.__repr__()
		s += '\n	* texture_suffix = ' + self.texture_suffix.__repr__()
		s += '\n	* texture_type = ' + self.texture_type.__repr__()
		s += '\n'
		return s
