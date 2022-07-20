from source.formats.base.basic import fmt_member
from generated.formats.ms2.compound.Descriptor import Descriptor
from generated.formats.ms2.compound.Vector3 import Vector3


class ListShort(Descriptor):

	"""
	used in JWE dinos
	"""

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		super().__init__(context, arg, template, set_default)
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# location of the joint
		self.loc = 0

		# normalized
		self.direction = 0

		# min, le 0
		self.min = 0

		# max, ge 0
		self.max = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.loc = Vector3(self.context, 0, None)
		self.direction = Vector3(self.context, 0, None)
		self.min = 0.0
		self.max = 0.0

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
		instance.loc = Vector3.from_stream(stream, instance.context, 0, None)
		instance.direction = Vector3.from_stream(stream, instance.context, 0, None)
		instance.min = stream.read_float()
		instance.max = stream.read_float()

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Vector3.to_stream(stream, instance.loc)
		Vector3.to_stream(stream, instance.direction)
		stream.write_float(instance.min)
		stream.write_float(instance.max)

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
		return f'ListShort [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* loc = {fmt_member(self.loc, indent+1)}'
		s += f'\n	* direction = {fmt_member(self.direction, indent+1)}'
		s += f'\n	* min = {fmt_member(self.min, indent+1)}'
		s += f'\n	* max = {fmt_member(self.max, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
