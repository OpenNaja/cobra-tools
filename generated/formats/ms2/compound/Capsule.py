from generated.formats.base.basic import fmt_member
from generated.formats.base.basic import Float
from generated.formats.base.basic import Uint
from generated.formats.ms2.compound.Vector3 import Vector3
from generated.struct import StructBase


class Capsule(StructBase):

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		super().__init__(context, arg, template, set_default)
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# relative to the armature, ie. not in bone space
		self.offset = 0

		# normalized
		self.direction = 0

		# radius of the caps
		self.radius = 0

		# distance between the center points of the capsule caps, total extent is 2 * radius + extent
		self.extent = 0

		# apparently unused
		self.zero = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.offset = Vector3(self.context, 0, None)
		self.direction = Vector3(self.context, 0, None)
		self.radius = 0.0
		self.extent = 0.0
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
		instance.offset = Vector3.from_stream(stream, instance.context, 0, None)
		instance.direction = Vector3.from_stream(stream, instance.context, 0, None)
		instance.radius = stream.read_float()
		instance.extent = stream.read_float()
		instance.zero = stream.read_uint()

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Vector3.to_stream(stream, instance.offset)
		Vector3.to_stream(stream, instance.direction)
		stream.write_float(instance.radius)
		stream.write_float(instance.extent)
		stream.write_uint(instance.zero)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		super()._get_filtered_attribute_list(instance)
		yield ('offset', Vector3, (0, None))
		yield ('direction', Vector3, (0, None))
		yield ('radius', Float, (0, None))
		yield ('extent', Float, (0, None))
		yield ('zero', Uint, (0, None))

	def get_info_str(self, indent=0):
		return f'Capsule [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* offset = {fmt_member(self.offset, indent+1)}'
		s += f'\n	* direction = {fmt_member(self.direction, indent+1)}'
		s += f'\n	* radius = {fmt_member(self.radius, indent+1)}'
		s += f'\n	* extent = {fmt_member(self.extent, indent+1)}'
		s += f'\n	* zero = {fmt_member(self.zero, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
