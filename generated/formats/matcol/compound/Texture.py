from source.formats.base.basic import fmt_member
from generated.context import ContextReference


class Texture:

	"""
	each texture = three fragments of format: data0 = 8 bytes zeros | data1 = null terminating string (scale texture name)
	"""

	context = ContextReference()

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# first fgm slot
		self.fgm_name = ''
		self.texture_suffix = ''
		self.texture_type = ''
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.fgm_name = ''
		self.texture_suffix = ''
		self.texture_type = ''

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
		instance.fgm_name = stream.read_zstring()
		instance.texture_suffix = stream.read_zstring()
		instance.texture_type = stream.read_zstring()

	@classmethod
	def write_fields(cls, stream, instance):
		stream.write_zstring(instance.fgm_name)
		stream.write_zstring(instance.texture_suffix)
		stream.write_zstring(instance.texture_type)

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
		return f'Texture [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += f'\n	* fgm_name = {fmt_member(self.fgm_name, indent+1)}'
		s += f'\n	* texture_suffix = {fmt_member(self.texture_suffix, indent+1)}'
		s += f'\n	* texture_type = {fmt_member(self.texture_type, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
