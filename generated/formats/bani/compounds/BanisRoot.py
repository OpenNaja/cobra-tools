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

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.zeros = 0

		# bytes per bone * num bones
		self.bytes_per_frame = 0

		# how many bytes for each bone per frame
		self.bytes_per_bone = 0

		# Number of frames for all bani files in banis buffer
		self.num_frames = 0

		# matches number of bones parrot has
		self.num_bones = 0

		# translation range
		self.loc_scale = 0

		# translation range
		self.loc_offset = 0
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
		instance.zeros = stream.read_uint64s((2,))
		instance.bytes_per_frame = stream.read_uint()
		instance.bytes_per_bone = stream.read_uint()
		instance.num_frames = stream.read_uint()
		instance.num_bones = stream.read_uint()
		instance.loc_scale = stream.read_float()
		instance.loc_offset = stream.read_float()

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		stream.write_uint64s(instance.zeros)
		stream.write_uint(instance.bytes_per_frame)
		stream.write_uint(instance.bytes_per_bone)
		stream.write_uint(instance.num_frames)
		stream.write_uint(instance.num_bones)
		stream.write_float(instance.loc_scale)
		stream.write_float(instance.loc_offset)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		super()._get_filtered_attribute_list(instance)
		yield ('zeros', Array, ((2,), Uint64, 0, None))
		yield ('bytes_per_frame', Uint, (0, None))
		yield ('bytes_per_bone', Uint, (0, None))
		yield ('num_frames', Uint, (0, None))
		yield ('num_bones', Uint, (0, None))
		yield ('loc_scale', Float, (0, None))
		yield ('loc_offset', Float, (0, None))

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
