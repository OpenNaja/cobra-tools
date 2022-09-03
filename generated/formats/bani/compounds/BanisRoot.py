import numpy
from generated.array import Array
from generated.formats.base.basic import Float
from generated.formats.base.basic import Uint
from generated.formats.base.basic import Uint64
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class BanisRoot(MemStruct):

	"""
	40 bytes
	"""

	__name__ = 'BanisRoot'

	_import_path = 'generated.formats.bani.compounds.BanisRoot'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.zeros = Array((0,), Uint64, self.context, 0, None)

		# bytes per bone * num bones
		self.bytes_per_frame = 0

		# how many bytes for each bone per frame
		self.bytes_per_bone = 0

		# Number of frames for all bani files in banis buffer
		self.num_frames = 0

		# matches number of bones parrot has
		self.num_bones = 0

		# translation range
		self.loc_scale = 0.0

		# translation range
		self.loc_offset = 0.0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.zeros = numpy.zeros((2,), dtype=numpy.dtype('uint64'))
		self.bytes_per_frame = 0
		self.bytes_per_bone = 0
		self.num_frames = 0
		self.num_bones = 0
		self.loc_scale = 0.0
		self.loc_offset = 0.0

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.zeros = Array.from_stream(stream, instance.context, 0, None, (2,), Uint64)
		instance.bytes_per_frame = Uint.from_stream(stream, instance.context, 0, None)
		instance.bytes_per_bone = Uint.from_stream(stream, instance.context, 0, None)
		instance.num_frames = Uint.from_stream(stream, instance.context, 0, None)
		instance.num_bones = Uint.from_stream(stream, instance.context, 0, None)
		instance.loc_scale = Float.from_stream(stream, instance.context, 0, None)
		instance.loc_offset = Float.from_stream(stream, instance.context, 0, None)

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Array.to_stream(stream, instance.zeros, (2,), Uint64, instance.context, 0, None)
		Uint.to_stream(stream, instance.bytes_per_frame)
		Uint.to_stream(stream, instance.bytes_per_bone)
		Uint.to_stream(stream, instance.num_frames)
		Uint.to_stream(stream, instance.num_bones)
		Float.to_stream(stream, instance.loc_scale)
		Float.to_stream(stream, instance.loc_offset)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'zeros', Array, ((2,), Uint64, 0, None), (False, None)
		yield 'bytes_per_frame', Uint, (0, None), (False, None)
		yield 'bytes_per_bone', Uint, (0, None), (False, None)
		yield 'num_frames', Uint, (0, None), (False, None)
		yield 'num_bones', Uint, (0, None), (False, None)
		yield 'loc_scale', Float, (0, None), (False, None)
		yield 'loc_offset', Float, (0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'BanisRoot [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* zeros = {self.fmt_member(self.zeros, indent+1)}'
		s += f'\n	* bytes_per_frame = {self.fmt_member(self.bytes_per_frame, indent+1)}'
		s += f'\n	* bytes_per_bone = {self.fmt_member(self.bytes_per_bone, indent+1)}'
		s += f'\n	* num_frames = {self.fmt_member(self.num_frames, indent+1)}'
		s += f'\n	* num_bones = {self.fmt_member(self.num_bones, indent+1)}'
		s += f'\n	* loc_scale = {self.fmt_member(self.loc_scale, indent+1)}'
		s += f'\n	* loc_offset = {self.fmt_member(self.loc_offset, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
