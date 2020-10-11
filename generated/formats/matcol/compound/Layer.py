import typing
from generated.formats.matcol.compound.AttribWrapper import AttribWrapper
from generated.formats.matcol.compound.InfoWrapper import InfoWrapper
from generated.formats.matcol.compound.LayeredAttrib import LayeredAttrib
from generated.formats.matcol.compound.LayeredInfo import LayeredInfo


class Layer:
	name: str
	info_info: LayeredInfo
	infos: typing.List[InfoWrapper]
	attrib_info: LayeredAttrib
	attribs: typing.List[AttribWrapper]

	def __init__(self, arg=None, template=None):
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.name = 0
		self.info_info = LayeredInfo()
		self.infos = []
		self.attrib_info = LayeredAttrib()
		self.attribs = []

	def read(self, stream):

		self.io_start = stream.tell()
		self.name = stream.read_zstring()
		self.info_info = stream.read_type(LayeredInfo)
		self.infos = [stream.read_type(InfoWrapper) for _ in range(self.info_info.info_count)]
		self.attrib_info = stream.read_type(LayeredAttrib)
		self.attribs = [stream.read_type(AttribWrapper) for _ in range(self.attrib_info.attrib_count)]

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_zstring(self.name)
		stream.write_type(self.info_info)
		for item in self.infos: stream.write_type(item)
		stream.write_type(self.attrib_info)
		for item in self.attribs: stream.write_type(item)

		self.io_size = stream.tell() - self.io_start

	def __repr__(self):
		s = 'Layer [Size: '+str(self.io_size)+', Address:'+str(self.io_start)+']'
		s += '\n	* name = ' + self.name.__repr__()
		s += '\n	* info_info = ' + self.info_info.__repr__()
		s += '\n	* infos = ' + self.infos.__repr__()
		s += '\n	* attrib_info = ' + self.attrib_info.__repr__()
		s += '\n	* attribs = ' + self.attribs.__repr__()
		s += '\n'
		return s
