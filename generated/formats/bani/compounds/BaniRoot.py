from generated.formats.base.basic import Float
from generated.formats.base.basic import Uint
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class BaniRoot(MemStruct):

	"""
	24 bytes This varies per bani animation file and describes the bani's frames and duration
	"""

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# The frame in the banis where this bani starts reading
		self.read_start_frame = 0

		# Number of frames in this bani file
		self.num_frames = 0

		# length of the animation, can easily get keyframe spacing now
		self.animation_length = 0.0

		# if 1381323599 then looped
		self.loop_flag = 0

		# points to the banis file used
		self.banis = Pointer(self.context, 0, None)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.read_start_frame = 0
		self.num_frames = 0
		self.animation_length = 0.0
		self.loop_flag = 0
		self.banis = Pointer(self.context, 0, None)

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.banis = Pointer.from_stream(stream, instance.context, 0, None)
		instance.read_start_frame = Uint.from_stream(stream, instance.context, 0, None)
		instance.num_frames = Uint.from_stream(stream, instance.context, 0, None)
		instance.animation_length = Float.from_stream(stream, instance.context, 0, None)
		instance.loop_flag = Uint.from_stream(stream, instance.context, 0, None)
		if not isinstance(instance.banis, int):
			instance.banis.arg = 0

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Pointer.to_stream(stream, instance.banis)
		stream.write_uint(instance.read_start_frame)
		stream.write_uint(instance.num_frames)
		stream.write_float(instance.animation_length)
		stream.write_uint(instance.loop_flag)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'banis', Pointer, (0, None)
		yield 'read_start_frame', Uint, (0, None)
		yield 'num_frames', Uint, (0, None)
		yield 'animation_length', Float, (0, None)
		yield 'loop_flag', Uint, (0, None)

	def get_info_str(self, indent=0):
		return f'BaniRoot [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* banis = {self.fmt_member(self.banis, indent+1)}'
		s += f'\n	* read_start_frame = {self.fmt_member(self.read_start_frame, indent+1)}'
		s += f'\n	* num_frames = {self.fmt_member(self.num_frames, indent+1)}'
		s += f'\n	* animation_length = {self.fmt_member(self.animation_length, indent+1)}'
		s += f'\n	* loop_flag = {self.fmt_member(self.loop_flag, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
