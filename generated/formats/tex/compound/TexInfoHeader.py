import numpy
import typing
from generated.array import Array
from generated.formats.ovl_base.compound.GenericHeader import GenericHeader
from generated.formats.tex.compound.Frag00 import Frag00
from generated.formats.tex.compound.Header3Data0 import Header3Data0
from generated.formats.tex.compound.Header3Data1 import Header3Data1
from generated.formats.tex.compound.Header7Data1 import Header7Data1
from generated.formats.tex.compound.TexHeader import TexHeader


class TexInfoHeader(GenericHeader):

	def __init__(self, context, arg=None, template=None):
		self.name = ''
		super().__init__(context, arg, template)
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.tex_info = TexHeader(self.context, None, None)
		self.frag_00 = Frag00(self.context, None, None)
		self.frag_10 = Header3Data0(self.context, None, None)
		self.frag_01 = Array(self.context)
		self.frag_11 = Header7Data1(self.context, None, None)
		self.set_defaults()

	def set_defaults(self):
		self.tex_info = TexHeader(self.context, None, None)
		if not (self.context.version < 19):
			self.frag_00 = Frag00(self.context, None, None)
		self.frag_10 = Header3Data0(self.context, None, None)
		self.frag_01 = Array(self.context)
		self.frag_11 = Header7Data1(self.context, None, None)

	def read(self, stream):
		self.io_start = stream.tell()
		super().read(stream)
		self.tex_info = stream.read_type(TexHeader, (self.context, None, None))
		if not (self.context.version < 19):
			self.frag_00 = stream.read_type(Frag00, (self.context, None, None))
		self.frag_10 = stream.read_type(Header3Data0, (self.context, None, None))
		self.frag_01.read(stream, Header3Data1, self.frag_10.stream_count, None)
		self.frag_11 = stream.read_type(Header7Data1, (self.context, None, None))

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()
		super().write(stream)
		stream.write_type(self.tex_info)
		if not (self.context.version < 19):
			stream.write_type(self.frag_00)
		stream.write_type(self.frag_10)
		self.frag_01.write(stream, Header3Data1, self.frag_10.stream_count, None)
		stream.write_type(self.frag_11)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'TexInfoHeader [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* tex_info = {self.tex_info.__repr__()}'
		s += f'\n	* frag_00 = {self.frag_00.__repr__()}'
		s += f'\n	* frag_10 = {self.frag_10.__repr__()}'
		s += f'\n	* frag_01 = {self.frag_01.__repr__()}'
		s += f'\n	* frag_11 = {self.frag_11.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
