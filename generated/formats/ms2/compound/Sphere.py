from source.formats.base.basic import fmt_member
from generated.context import ContextReference
from generated.formats.ms2.compound.Vector3 import Vector3


class Sphere:

	context = ContextReference()

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# center of the sphere
		self.center = Vector3(self.context, 0, None)

		# radius around the center
		self.radius = 0.0

		# apparently unused
		self.zero = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.center = Vector3(self.context, 0, None)
		self.radius = 0.0
		self.zero = 0

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
		instance.center = Vector3.from_stream(stream, instance.context, 0, None)
		instance.radius = stream.read_float()
		instance.zero = stream.read_uint()

	@classmethod
	def write_fields(cls, stream, instance):
		Vector3.to_stream(stream, instance.center)
		stream.write_float(instance.radius)
		stream.write_uint(instance.zero)

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
		return f'Sphere [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += f'\n	* center = {fmt_member(self.center, indent+1)}'
		s += f'\n	* radius = {fmt_member(self.radius, indent+1)}'
		s += f'\n	* zero = {fmt_member(self.zero, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
