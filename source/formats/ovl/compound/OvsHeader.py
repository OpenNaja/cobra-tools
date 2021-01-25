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

	# START_CLASS

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

