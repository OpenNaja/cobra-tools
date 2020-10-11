from generated.formats.matcol.compound.Attrib import Attrib


class AttribWrapper:
	attrib: Attrib
	name: str

	def __init__(self, arg=None, template=None):
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.attrib = Attrib()
		self.name = 0

	def read(self, stream):

		self.io_start = stream.tell()
		self.attrib = stream.read_type(Attrib)
		self.name = stream.read_zstring()

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_type(self.attrib)
		stream.write_zstring(self.name)

		self.io_size = stream.tell() - self.io_start

	def __repr__(self):
		s = 'AttribWrapper [Size: '+str(self.io_size)+', Address:'+str(self.io_start)+']'
		s += '\n	* attrib = ' + self.attrib.__repr__()
		s += '\n	* name = ' + self.name.__repr__()
		s += '\n'
		return s
