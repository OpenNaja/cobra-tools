from source.formats.base.basic import fmt_member
from generated.context import ContextReference
from generated.formats.ovl.compound.HeaderPointer import HeaderPointer


class DependencyEntry:

	"""
	Description of dependency; links it to an entry from this archive
	"""

	context = ContextReference()

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# Hash of this dependency, for lookup in hash dict. Can be either external or internal.
		self.file_hash = 0

		# offset for extension into string name table
		self.offset = 0

		# index into ovl file table, points to the file entry where this dependency is used
		self.file_index = 0

		# pointer into flattened list of all archives' pools
		self.link_ptr = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.file_hash = 0
		self.offset = 0
		self.file_index = 0
		self.link_ptr = HeaderPointer(self.context, 0, None)

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
		instance.file_hash = stream.read_uint()
		instance.offset = stream.read_uint()
		instance.file_index = stream.read_uint()
		instance.link_ptr = HeaderPointer.from_stream(stream, instance.context, 0, None)

	@classmethod
	def write_fields(cls, stream, instance):
		stream.write_uint(instance.file_hash)
		stream.write_uint(instance.offset)
		stream.write_uint(instance.file_index)
		HeaderPointer.to_stream(stream, instance.link_ptr)

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

	def get_info_str(self, indent=0):
		return f'DependencyEntry [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += f'\n	* file_hash = {fmt_member(self.file_hash, indent+1)}'
		s += f'\n	* offset = {fmt_member(self.offset, indent+1)}'
		s += f'\n	* file_index = {fmt_member(self.file_index, indent+1)}'
		s += f'\n	* link_ptr = {fmt_member(self.link_ptr, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
