from generated.formats.bani.imports import name_type_map
from generated.formats.ovl_base.structs.MemStruct import MemStruct


class BaniRoot(MemStruct):

	"""
	This varies per bani animation file and describes the bani's frames and duration
	older: 24 bytes
	PC2: 32 bytes
	"""

	__name__ = 'BaniRoot'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# Maps this CPU-side struct to the struct in the GPU buffer
		self.gpu_header_index = name_type_map['Uint'](self.context, 0, None)

		# Offset into the engine GPU buffer. gpu_header_index * [compute shader thread count or 16-byte rounded bones count] for wavefront/warp alignment.
		self.gpu_header_offset = name_type_map['Uint'](self.context, 0, None)

		# The frame in the banis where this bani starts reading
		self.read_start_frame = name_type_map['Uint'](self.context, 0, None)

		# Number of frames in this bani file
		self.num_frames = name_type_map['Uint'](self.context, 0, None)

		# length of the animation, can easily get keyframe spacing now
		self.animation_length = name_type_map['Float'](self.context, 0, None)

		# unknown - seen 0 or 1381323599
		self.flags = name_type_map['Uint'](self.context, 0, None)
		self.num_bones = name_type_map['Ushort'](self.context, 0, None)

		# Mode 1 Absolute, Mode 2 Relative, Mode 3 Additive
		self.mode = name_type_map['Ushort'](self.context, 0, None)

		# points to the banis file used
		self.banis = name_type_map['Pointer'](self.context, 0, None)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'banis', name_type_map['Pointer'], (0, None), (False, None), (None, None)
		yield 'gpu_header_index', name_type_map['Uint'], (0, None), (False, None), (lambda context: context.version >= 7, None)
		yield 'gpu_header_offset', name_type_map['Uint'], (0, None), (False, None), (lambda context: context.version >= 7, None)
		yield 'read_start_frame', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'num_frames', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'animation_length', name_type_map['Float'], (0, None), (False, None), (None, None)
		yield 'flags', name_type_map['Uint'], (0, None), (False, None), (lambda context: context.version <= 5, None)
		yield 'num_bones', name_type_map['Ushort'], (0, None), (False, None), (lambda context: context.version >= 7, None)
		yield 'mode', name_type_map['Ushort'], (0, None), (False, None), (lambda context: context.version >= 7, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'banis', name_type_map['Pointer'], (0, None), (False, None)
		if instance.context.version >= 7:
			yield 'gpu_header_index', name_type_map['Uint'], (0, None), (False, None)
			yield 'gpu_header_offset', name_type_map['Uint'], (0, None), (False, None)
		yield 'read_start_frame', name_type_map['Uint'], (0, None), (False, None)
		yield 'num_frames', name_type_map['Uint'], (0, None), (False, None)
		yield 'animation_length', name_type_map['Float'], (0, None), (False, None)
		if instance.context.version <= 5:
			yield 'flags', name_type_map['Uint'], (0, None), (False, None)
		if instance.context.version >= 7:
			yield 'num_bones', name_type_map['Ushort'], (0, None), (False, None)
			yield 'mode', name_type_map['Ushort'], (0, None), (False, None)
