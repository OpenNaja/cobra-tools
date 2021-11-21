from generated.context import ContextReference


class BaniFragmentData0:

	"""
	This varies per bani animation file and describes the bani's frames and duration
	"""

	context = ContextReference()

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		self._context = context
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
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.zero = 0
		self.read_start_frame = 0
		self.num_frames = 0
		self.animation_length = 0.0
		self.loop_flag = 0

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
		instance.zero = stream.read_uint64()
		instance.read_start_frame = stream.read_uint()
		instance.num_frames = stream.read_uint()
		instance.animation_length = stream.read_float()
		instance.loop_flag = stream.read_uint()

	@classmethod
	def write_fields(cls, stream, instance):
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

	def get_info_str(self):
		return f'BaniFragmentData0 [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* zero = {self.zero.__repr__()}'
		s += f'\n	* read_start_frame = {self.read_start_frame.__repr__()}'
		s += f'\n	* num_frames = {self.num_frames.__repr__()}'
		s += f'\n	* animation_length = {self.animation_length.__repr__()}'
		s += f'\n	* loop_flag = {self.loop_flag.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
