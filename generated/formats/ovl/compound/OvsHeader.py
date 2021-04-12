import numpy
import typing
from generated.array import Array
from generated.formats.ovl.compound.BufferEntry import BufferEntry
from generated.formats.ovl.compound.DataEntry import DataEntry
from generated.formats.ovl.compound.Fragment import Fragment
from generated.formats.ovl.compound.HeaderEntry import HeaderEntry
from generated.formats.ovl.compound.HeaderType import HeaderType
from generated.formats.ovl.compound.SetHeader import SetHeader
from generated.formats.ovl.compound.SizedStringEntry import SizedStringEntry


class OvsHeader:

	"""
	Description of one archive's content
	"""

	def __init__(self, arg=None, template=None):
		self.name = ''
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.header_types = Array()
		self.header_entries = Array()
		self.data_entries = Array()
		self.buffer_entries = Array()
		self.sized_str_entries = Array()
		self.fragments = Array()
		self.set_header = SetHeader()

	def get_info_str(self):
		return f'OvsHeader [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* header_types = {self.header_types.__repr__()}'
		s += f'\n	* header_entries = {self.header_entries.__repr__()}'
		s += f'\n	* data_entries = {self.data_entries.__repr__()}'
		s += f'\n	* buffer_entries = {self.buffer_entries.__repr__()}'
		s += f'\n	* sized_str_entries = {self.sized_str_entries.__repr__()}'
		s += f'\n	* fragments = {self.fragments.__repr__()}'
		s += f'\n	* set_header = {self.set_header.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s

	def read(self, stream):

		self.io_start = stream.tell()
		self.header_types.read(stream, HeaderType, self.arg.num_header_types, None)
		num_headers = sum(header_type.num_headers for header_type in self.header_types)
		self.header_entries.read(stream, HeaderEntry, num_headers, None)
		self.data_entries.read(stream, DataEntry, self.arg.num_datas, None)
		self.buffer_entries.read(stream, BufferEntry, self.arg.num_buffers, None)
		self.sized_str_entries.read(stream, SizedStringEntry, self.arg.num_files, None)
		self.fragments.read(stream, Fragment, self.arg.num_fragments, None)
		self.set_header = stream.read_type(SetHeader)

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		self.header_types.write(stream, HeaderType, self.arg.num_header_types, None)
		num_headers = sum(header_type.num_headers for header_type in self.header_types)
		self.header_entries.write(stream, HeaderEntry, num_headers, None)
		self.data_entries.write(stream, DataEntry, self.arg.num_datas, None)
		self.buffer_entries.write(stream, BufferEntry, self.arg.num_buffers, None)
		self.sized_str_entries.write(stream, SizedStringEntry, self.arg.num_files, None)
		self.fragments.write(stream, Fragment, self.arg.num_fragments, None)
		stream.write_type(self.set_header)

		self.io_size = stream.tell() - self.io_start


