from generated.array import Array
from generated.context import ContextReference
from generated.formats.matcol.compound.AttribWrapper import AttribWrapper
from generated.formats.matcol.compound.InfoWrapper import InfoWrapper
from generated.formats.matcol.compound.LayeredAttrib import LayeredAttrib
from generated.formats.matcol.compound.LayeredInfo import LayeredInfo


class Layer:

	context = ContextReference()

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.name = ''
		self.info_info = LayeredInfo(self.context, 0, None)
		self.infos = Array((self.info_info.info_count,), InfoWrapper, self.context, 0, None)
		self.attrib_info = LayeredAttrib(self.context, 0, None)
		self.attribs = Array((self.attrib_info.attrib_count,), AttribWrapper, self.context, 0, None)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.name = ''
		self.info_info = LayeredInfo(self.context, 0, None)
		self.infos = Array((self.info_info.info_count,), InfoWrapper, self.context, 0, None)
		self.attrib_info = LayeredAttrib(self.context, 0, None)
		self.attribs = Array((self.attrib_info.attrib_count,), AttribWrapper, self.context, 0, None)

	def read(self, stream):
		self.io_start = stream.tell()
		self.read_fields(stream, self)
		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()
		self.write_fields(stream, self)
		self.io_size = stream.tell() - self.io_start

	@classmethod
	def read_fields(cls, stream, instance):
		instance.name = stream.read_zstring()
		instance.info_info = LayeredInfo.from_stream(stream, instance.context, 0, None)
		instance.infos = Array.from_stream(stream, (instance.info_info.info_count,), InfoWrapper, instance.context, 0, None)
		instance.attrib_info = LayeredAttrib.from_stream(stream, instance.context, 0, None)
		instance.attribs = Array.from_stream(stream, (instance.attrib_info.attrib_count,), AttribWrapper, instance.context, 0, None)

	@classmethod
	def write_fields(cls, stream, instance):
		stream.write_zstring(instance.name)
		LayeredInfo.to_stream(stream, instance.info_info)
		Array.to_stream(stream, instance.infos, (instance.info_info.info_count,), InfoWrapper, instance.context, 0, None)
		LayeredAttrib.to_stream(stream, instance.attrib_info)
		Array.to_stream(stream, instance.attribs, (instance.attrib_info.attrib_count,), AttribWrapper, instance.context, 0, None)

	@classmethod
	def from_stream(cls, stream, context, arg=0, template=None):
		instance = cls(context, arg, template, set_default=False)
		instance.io_start = stream.tell()
		cls.read_fields(stream, instance)
		instance.io_size = stream.tell() - instance.io_start
		return instance

	@classmethod
	def to_stream(cls, stream, instance):
		instance.io_start = stream.tell()
		cls.write_fields(stream, instance)
		instance.io_size = stream.tell() - instance.io_start
		return instance

	def get_info_str(self):
		return f'Layer [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* name = {self.name.__repr__()}'
		s += f'\n	* info_info = {self.info_info.__repr__()}'
		s += f'\n	* infos = {self.infos.__repr__()}'
		s += f'\n	* attrib_info = {self.attrib_info.__repr__()}'
		s += f'\n	* attribs = {self.attribs.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
