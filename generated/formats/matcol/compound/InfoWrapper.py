from generated.formats.matcol.compound.Info import Info


class InfoWrapper:

	def __init__(self, arg=None, template=None):
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.info = Info()
		self.name = 0

	def read(self, stream):

		self.io_start = stream.tell()
		self.info = stream.read_type(Info)
		self.name = stream.read_zstring()

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_type(self.info)
		stream.write_zstring(self.name)

		self.io_size = stream.tell() - self.io_start

	def __repr__(self):
		s = 'InfoWrapper [Size: '+str(self.io_size)+', Address:'+str(self.io_start)+']'
		s += '\n	* info = ' + self.info.__repr__()
		s += '\n	* name = ' + self.name.__repr__()
		s += '\n'
		return s
