from generated.base_struct import BaseStruct
from generated.formats.base.basic import Float
from generated.formats.base.basic import Uint
from generated.formats.ms2.compound.Vector3 import Vector3


class Sphere(BaseStruct):

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# center of the sphere
		self.center = 0

		# radius around the center
		self.radius = 0

		# apparently unused
		self.zero = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		print(f'set_defaults {self.__class__.__name__}')
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
		super().read_fields(stream, instance)
		instance.center = Vector3.from_stream(stream, instance.context, 0, None)
		instance.radius = stream.read_float()
		instance.zero = stream.read_uint()

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Vector3.to_stream(stream, instance.center)
		stream.write_float(instance.radius)
		stream.write_uint(instance.zero)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		super()._get_filtered_attribute_list(instance)
		yield ('center', Vector3, (0, None))
		yield ('radius', Float, (0, None))
		yield ('zero', Uint, (0, None))

	def get_info_str(self, indent=0):
		return f'Sphere [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* center = {self.fmt_member(self.center, indent+1)}'
		s += f'\n	* radius = {self.fmt_member(self.radius, indent+1)}'
		s += f'\n	* zero = {self.fmt_member(self.zero, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
