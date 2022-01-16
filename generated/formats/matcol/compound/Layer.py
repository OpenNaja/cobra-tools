import numpy
import typing
from generated.array import Array
from generated.context import ContextReference
from generated.formats.matcol.compound.Attrib import Attrib
from generated.formats.matcol.compound.Info import Info
from generated.formats.matcol.compound.LayerFrag import LayerFrag


class Layer:

	context = ContextReference()

	def __init__(self, context, arg=None, template=None):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.info = LayerFrag(self.context, None, None)
		self.name = 0
		self.infos = Array(self.context)
		self.info_names = Array(self.context)
		self.attribs = Array(self.context)
		self.attrib_names = Array(self.context)
		self.set_defaults()

	def set_defaults(self):
		self.info = LayerFrag(self.context, None, None)
		self.name = 0
		self.infos = Array(self.context)
		self.info_names = Array(self.context)
		self.attribs = Array(self.context)
		self.attrib_names = Array(self.context)

	def read(self, stream):
		self.io_start = stream.tell()
		self.info = stream.read_type(LayerFrag, (self.context, None, None))
		self.name = stream.read_zstring()
		self.infos.read(stream, Info, self.info.info_count, None)
		self.info_names = stream.read_zstrings((self.info.info_count))
		self.attribs.read(stream, Attrib, self.info.attrib_count, None)
		self.attrib_names = stream.read_zstrings((self.info.attrib_count))

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()
		stream.write_type(self.info)
		stream.write_zstring(self.name)
		self.infos.write(stream, Info, self.info.info_count, None)
		stream.write_zstrings(self.info_names)
		self.attribs.write(stream, Attrib, self.info.attrib_count, None)
		stream.write_zstrings(self.attrib_names)

		self.io_size = stream.tell() - self.io_start

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
