from source.formats.base.basic import fmt_member
from generated.context import ContextReference


class AuxEntry:

	"""
	describes an external AUX resource
	"""

	context = ContextReference()

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# index into files list
		self.file_index = 0

		# maybe index into extension list
		self.extension_index = 0

		# byte count of the complete external resource file
		self.size = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.file_index = 0
		self.extension_index = 0
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
		instance.file_index = stream.read_uint()
		instance.extension_index = stream.read_uint()
		instance.size = stream.read_uint()

	@classmethod
	def write_fields(cls, stream, instance):
		stream.write_uint(instance.file_index)
		stream.write_uint(instance.extension_index)
		stream.write_uint(instance.size)

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
		return f'AuxEntry [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += f'\n	* file_index = {fmt_member(self.file_index, indent+1)}'
		s += f'\n	* extension_index = {fmt_member(self.extension_index, indent+1)}'
		s += f'\n	* size = {fmt_member(self.size, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
