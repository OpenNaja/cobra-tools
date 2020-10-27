import typing
from generated.array import Array
from generated.formats.matcol.compound.AttribWrapper import AttribWrapper
from generated.formats.matcol.compound.InfoWrapper import InfoWrapper
from generated.formats.matcol.compound.LayeredAttrib import LayeredAttrib
from generated.formats.matcol.compound.LayeredInfo import LayeredInfo


class Layer:

	def __init__(self, arg=None, template=None):
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.name = 0
		self.info_info = LayeredInfo()
		self.infos = Array()
		self.attrib_info = LayeredAttrib()
		self.attribs = Array()

	def read(self, stream):

		self.io_start = stream.tell()
		self.name = stream.read_zstring()
		self.info_info = stream.read_type(LayeredInfo)
		self.infos.read(stream, InfoWrapper, self.info_info.info_count, None)
		self.attrib_info = stream.read_type(LayeredAttrib)
		self.attribs.read(stream, AttribWrapper, self.attrib_info.attrib_count, None)

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_zstring(self.name)
		stream.write_type(self.info_info)
		self.infos.write(stream, InfoWrapper, self.info_info.info_count, None)
		stream.write_type(self.attrib_info)
		self.attribs.write(stream, AttribWrapper, self.attrib_info.attrib_count, None)

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
