from source.formats.base.basic import fmt_member
from generated.formats.ovl_base.compound.MemStruct import MemStruct
from generated.formats.ovl_base.compound.Pointer import Pointer


class BaniRoot(MemStruct):

	"""
	24 bytes This varies per bani animation file and describes the bani's frames and duration
	"""

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		super().__init__(context, arg, template, set_default)
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.zero = 0

		# The frame in the banis where this bani starts reading
		self.read_start_frame = 0

		# Number of frames in this bani file
		self.num_frames = 0

		# length of the animation, can easily get keyframe spacing now
		self.animation_length = 0.0

		# if 1381323599 then looped
		self.loop_flag = 0
		self.banis = Pointer(self.context, 0, None)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.zero = 0
		self.read_start_frame = 0
		self.num_frames = 0
		self.animation_length = 0.0
		self.loop_flag = 0
		self.banis = Pointer(self.context, 0, None)

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
		instance.banis = Pointer.from_stream(stream, instance.context, 0, None)
		instance.zero = stream.read_uint64()
		instance.read_start_frame = stream.read_uint()
		instance.num_frames = stream.read_uint()
		instance.animation_length = stream.read_float()
		instance.loop_flag = stream.read_uint()
		instance.banis.arg = 0

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Pointer.to_stream(stream, instance.banis)
		stream.write_uint64(instance.zero)
		stream.write_uint(instance.read_start_frame)
		stream.write_uint(instance.num_frames)
		stream.write_float(instance.animation_length)
		stream.write_uint(instance.loop_flag)

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
		return f'BaniRoot [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* banis = {fmt_member(self.banis, indent+1)}'
		s += f'\n	* zero = {fmt_member(self.zero, indent+1)}'
		s += f'\n	* read_start_frame = {fmt_member(self.read_start_frame, indent+1)}'
		s += f'\n	* num_frames = {fmt_member(self.num_frames, indent+1)}'
		s += f'\n	* animation_length = {fmt_member(self.animation_length, indent+1)}'
		s += f'\n	* loop_flag = {fmt_member(self.loop_flag, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
