from generated.array import Array
from generated.context import ContextReference
from generated.formats.base.basic import ZString
from generated.formats.matcol.compound.Attrib import Attrib
from generated.formats.matcol.compound.Info import Info
from generated.formats.matcol.compound.LayerFrag import LayerFrag


class Layer:

	context = ContextReference()

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.info = LayerFrag(self.context, 0, None)
		self.name = ''
		self.infos = Array((self.info.info_count,), Info, self.context, 0, None)
		self.info_names = Array((self.info.info_count,), ZString, self.context, 0, None)
		self.attribs = Array((self.info.attrib_count,), Attrib, self.context, 0, None)
		self.attrib_names = Array((self.info.attrib_count,), ZString, self.context, 0, None)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.info = LayerFrag(self.context, 0, None)
		self.name = ''
		self.infos = Array((self.info.info_count,), Info, self.context, 0, None)
		self.info_names = Array((self.info.info_count,), ZString, self.context, 0, None)
		self.attribs = Array((self.info.attrib_count,), Attrib, self.context, 0, None)
		self.attrib_names = Array((self.info.attrib_count,), ZString, self.context, 0, None)

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
		instance.info = LayerFrag.from_stream(stream, instance.context, 0, None)
		instance.name = stream.read_zstring()
		instance.infos = Array.from_stream(stream, (instance.info.info_count,), Info, instance.context, 0, None)
		instance.info_names = stream.read_zstrings((instance.info.info_count,))
		instance.attribs = Array.from_stream(stream, (instance.info.attrib_count,), Attrib, instance.context, 0, None)
		instance.attrib_names = stream.read_zstrings((instance.info.attrib_count,))

	@classmethod
	def write_fields(cls, stream, instance):
		LayerFrag.to_stream(stream, instance.info)
		stream.write_zstring(instance.name)
		Array.to_stream(stream, instance.infos, (instance.info.info_count,), Info, instance.context, 0, None)
		stream.write_zstrings(instance.info_names)
		Array.to_stream(stream, instance.attribs, (instance.info.attrib_count,), Attrib, instance.context, 0, None)
		stream.write_zstrings(instance.attrib_names)

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
		s += f'\n	* info = {self.info.__repr__()}'
		s += f'\n	* name = {self.name.__repr__()}'
		s += f'\n	* infos = {self.infos.__repr__()}'
		s += f'\n	* info_names = {self.info_names.__repr__()}'
		s += f'\n	* attribs = {self.attribs.__repr__()}'
		s += f'\n	* attrib_names = {self.attrib_names.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
