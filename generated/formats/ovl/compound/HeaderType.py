class HeaderType:

# Located at start of deflated archive stream

	# Type of the headers that follow
	type: int

	# Amount of the headers of that type that follow the headers block
	num_headers: int

	def __init__(self, arg=None, template=None):
		self.arg = arg
		self.template = template

	def read(self, stream):
		self.type = stream.read_ushort()
		self.num_headers = stream.read_ushort()

	def write(self, stream):
		stream.write_ushort(self.type)
		stream.write_ushort(self.num_headers)

	def __repr__(self):
		s = 'HeaderType'
		s += '\ntype ' + self.type.__repr__()
		s += '\nnum_headers ' + self.num_headers.__repr__()
		s += '\n'
		return s