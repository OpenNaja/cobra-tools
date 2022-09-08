from generated.formats.base.basic import Float
from generated.formats.base.basic import Uint
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class BaniRoot(MemStruct):

	"""
	24 bytes This varies per bani animation file and describes the bani's frames and duration
	"""

	__name__ = 'BaniRoot'

	_import_path = 'generated.formats.bani.compounds.BaniRoot'

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
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'banis', Pointer, (0, None), (False, None)
		yield 'read_start_frame', Uint, (0, None), (False, None)
		yield 'num_frames', Uint, (0, None), (False, None)
		yield 'animation_length', Float, (0, None), (False, None)
		yield 'loop_flag', Uint, (0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'BaniRoot [Size: {self.io_size}, Address: {self.io_start}] {self.name}'
