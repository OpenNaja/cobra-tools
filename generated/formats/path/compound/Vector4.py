from source.formats.base.basic import fmt_member
from generated.formats.ovl_base.compound.MemStruct import MemStruct


class Vector4(MemStruct):

	"""
	A vector in 3D space (x,y,z).
	"""

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		super().__init__(context, arg, template, set_default)
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# First coordinate.
		self.x = 0

		# Second coordinate.
		self.y = 0

		# Third coordinate.
		self.z = 0

		# Fourth coordinate.
		self.w = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.x = 0.0
		self.y = 0.0
		self.z = 0.0
		self.w = 0.0

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
		instance.x = stream.read_float()
		instance.y = stream.read_float()
		instance.z = stream.read_float()
		instance.w = stream.read_float()

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		stream.write_float(instance.x)
		stream.write_float(instance.y)
		stream.write_float(instance.z)
		stream.write_float(instance.w)

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
		return f'Vector4 [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* x = {fmt_member(self.x, indent+1)}'
		s += f'\n	* y = {fmt_member(self.y, indent+1)}'
		s += f'\n	* z = {fmt_member(self.z, indent+1)}'
		s += f'\n	* w = {fmt_member(self.w, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
