from source.formats.base.basic import fmt_member
from generated.formats.base.basic import Uint
from generated.struct import StructBase


class AuxEntry(StructBase):

	"""
	describes an external AUX resource
	"""

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		super().__init__(context, arg, template, set_default)
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# index into files list
		self.file_index = 0

		# offset for suffix into string name table
		self.offset = 0

		# byte count of the complete external resource file
		self.size = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.file_index = 0
		self.offset = 0
		self.size = 0

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
		super().read_fields(stream, instance)
		instance.file_index = stream.read_uint()
		instance.offset = stream.read_uint()
		instance.size = stream.read_uint()

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		stream.write_uint(instance.file_index)
		stream.write_uint(instance.offset)
		stream.write_uint(instance.size)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		super()._get_filtered_attribute_list(instance)
		yield ('file_index', Uint, (0, None))
		yield ('offset', Uint, (0, None))
		yield ('size', Uint, (0, None))

	def get_info_str(self, indent=0):
		return f'AuxEntry [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* file_index = {fmt_member(self.file_index, indent+1)}'
		s += f'\n	* offset = {fmt_member(self.offset, indent+1)}'
		s += f'\n	* size = {fmt_member(self.size, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
