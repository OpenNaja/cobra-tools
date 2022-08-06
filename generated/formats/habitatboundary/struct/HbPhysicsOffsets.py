from source.formats.base.basic import fmt_member
from generated.formats.habitatboundary.struct.HbPostSize import HbPostSize
from generated.formats.ovl_base.compound.MemStruct import MemStruct


class HbPhysicsOffsets(MemStruct):

	"""
	Physics values for barriers.
	"""

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		super().__init__(context, arg, template, set_default)
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# Wall thickness. Affects navcut, selection, and climb nav width. Must be under a certain value or it crashes.
		self.thickness = 0.0
		self.post_size = HbPostSize(self.context, 0, None)

		# Wall size above wall_height. Affects navcut, selection, and climb nav height.
		self.wall_pad_top = 0.0

		# Distance between post center and start of wall. Larger values create a visual and nav gap between the post and wall segment.
		self.wall_post_gap = 0.0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.thickness = 0.0
		self.post_size = HbPostSize(self.context, 0, None)
		self.wall_pad_top = 0.0
		self.wall_post_gap = 0.0

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
		instance.thickness = stream.read_float()
		instance.post_size = HbPostSize.from_stream(stream, instance.context, 0, None)
		instance.wall_pad_top = stream.read_float()
		instance.wall_post_gap = stream.read_float()

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		stream.write_float(instance.thickness)
		HbPostSize.to_stream(stream, instance.post_size)
		stream.write_float(instance.wall_pad_top)
		stream.write_float(instance.wall_post_gap)

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
		return f'HbPhysicsOffsets [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* thickness = {fmt_member(self.thickness, indent+1)}'
		s += f'\n	* post_size = {fmt_member(self.post_size, indent+1)}'
		s += f'\n	* wall_pad_top = {fmt_member(self.wall_pad_top, indent+1)}'
		s += f'\n	* wall_post_gap = {fmt_member(self.wall_post_gap, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
