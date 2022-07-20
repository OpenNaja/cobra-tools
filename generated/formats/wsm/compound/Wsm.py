from source.formats.base.basic import fmt_member
import numpy
from generated.formats.ovl_base.compound.GenericHeader import GenericHeader
from generated.formats.wsm.compound.WsmHeader import WsmHeader


class Wsm(GenericHeader):

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		super().__init__(context, arg, template, set_default)
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.header = 0

		# xyz
		self.locs = 0

		# xyzw
		self.quats = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.header = WsmHeader(self.context, 0, None)
		self.locs = numpy.zeros((self.header.frame_count, 3,), dtype=numpy.dtype('float32'))
		self.quats = numpy.zeros((self.header.frame_count, 4,), dtype=numpy.dtype('float32'))

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
		instance.header = WsmHeader.from_stream(stream, instance.context, 0, None)
		instance.locs = stream.read_floats((instance.header.frame_count, 3,))
		instance.quats = stream.read_floats((instance.header.frame_count, 4,))

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		WsmHeader.to_stream(stream, instance.header)
		stream.write_floats(instance.locs)
		stream.write_floats(instance.quats)

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
		return f'Wsm [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* header = {fmt_member(self.header, indent+1)}'
		s += f'\n	* locs = {fmt_member(self.locs, indent+1)}'
		s += f'\n	* quats = {fmt_member(self.quats, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
