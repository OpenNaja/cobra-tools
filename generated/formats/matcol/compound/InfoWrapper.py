from generated.formats.matcol.compound.Info import Info


class InfoWrapper:
	info: Info
	name: str

	def __init__(self, arg=None, template=None):
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.info = Info()
		self.name = 0

	def read(self, stream):

		io_start = stream.tell()
		self.info = stream.read_type(Info)
		self.name = stream.read_zstring()

		self.io_size = stream.tell() - io_start

	def write(self, stream):

		io_start = stream.tell()
		stream.write_type(self.info)
		stream.write_zstring(self.name)

		self.io_size = stream.tell() - io_start

	def __repr__(self):
		s = 'InfoWrapper [Size: '+str(self.io_size)+']'
		s += '\n	* info = ' + self.info.__repr__()
		s += '\n	* name = ' + self.name.__repr__()
		s += '\n'
		return s
