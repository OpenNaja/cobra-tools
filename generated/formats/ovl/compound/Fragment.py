from source.formats.base.basic import fmt_member
from generated.context import ContextReference
from generated.formats.ovl.compound.HeaderPointer import HeaderPointer


class Fragment:

	"""
	These are to be thought of as instructions for loading. Their order is irrelevant.
	"""

	context = ContextReference()

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# determines where to write a pointer address
		self.link_ptr = 0

		# the struct that is pointed to can be found here
		self.struct_ptr = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.link_ptr = HeaderPointer(self.context, 0, None)
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
		instance.link_ptr = HeaderPointer.from_stream(stream, instance.context, 0, None)
		instance.struct_ptr = HeaderPointer.from_stream(stream, instance.context, 0, None)

	@classmethod
	def write_fields(cls, stream, instance):
		HeaderPointer.to_stream(stream, instance.link_ptr)
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
		return f'Fragment [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += f'\n	* link_ptr = {fmt_member(self.link_ptr, indent+1)}'
		s += f'\n	* struct_ptr = {fmt_member(self.struct_ptr, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
