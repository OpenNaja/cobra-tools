from source.formats.base.basic import fmt_member
from generated.context import ContextReference
from generated.formats.ovl.compound.HeaderPointer import HeaderPointer


class RootEntry:

	"""
	Main file entry in the ovs, one per FileEntry
	"""

	context = ContextReference()

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# id (index or djb) of the file
		self.file_hash = 0

		# djb of extension
		self.ext_hash = 0

		# points to the main struct of this file OR -1 pointer for assets
		self.struct_ptr = HeaderPointer(self.context, 0, None)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.file_hash = 0
		if self.context.version >= 19:
			self.ext_hash = 0
		self.struct_ptr = HeaderPointer(self.context, 0, None)

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
		if instance.context.version >= 19:
			instance.ext_hash = stream.read_uint()
		instance.struct_ptr = HeaderPointer.from_stream(stream, instance.context, 0, None)

	@classmethod
	def write_fields(cls, stream, instance):
		stream.write_uint(instance.file_hash)
		if instance.context.version >= 19:
			stream.write_uint(instance.ext_hash)
		HeaderPointer.to_stream(stream, instance.struct_ptr)

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
		return f'RootEntry [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += f'\n	* file_hash = {fmt_member(self.file_hash, indent+1)}'
		s += f'\n	* ext_hash = {fmt_member(self.ext_hash, indent+1)}'
		s += f'\n	* struct_ptr = {fmt_member(self.struct_ptr, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
