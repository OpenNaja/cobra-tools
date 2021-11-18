import numpy
from generated.array import Array
from generated.context import ContextReference


class BanisHeader:

	"""
	Seems to be the same for all bani anims of one bani file
	"""

	context = ContextReference()

	def __init__(self, context, arg=None, template=None, set_default=True):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.zeros = numpy.zeros((2), dtype='uint64')

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
		self.zeros = numpy.zeros((2), dtype='uint64')
		self.bytes_per_frame = 0
		self.bytes_per_bone = 0
		self.num_frames = 0
		self.num_bones = 0
		self.loc_scale = 0
		self.loc_offset = 0

	def read(self, stream):
		self.io_start = stream.tell()
		self.zeros = stream.read_uint64s((2))
		self.bytes_per_frame = stream.read_uint()
		self.bytes_per_bone = stream.read_uint()
		self.num_frames = stream.read_uint()
		self.num_bones = stream.read_uint()
		self.loc_scale = stream.read_float()
		self.loc_offset = stream.read_float()

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()
		stream.write_uint64s(self.zeros)
		stream.write_uint(self.bytes_per_frame)
		stream.write_uint(self.bytes_per_bone)
		stream.write_uint(self.num_frames)
		stream.write_uint(self.num_bones)
		stream.write_float(self.loc_scale)
		stream.write_float(self.loc_offset)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'BanisHeader [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* zeros = {self.zeros.__repr__()}'
		s += f'\n	* bytes_per_frame = {self.bytes_per_frame.__repr__()}'
		s += f'\n	* bytes_per_bone = {self.bytes_per_bone.__repr__()}'
		s += f'\n	* num_frames = {self.num_frames.__repr__()}'
		s += f'\n	* num_bones = {self.num_bones.__repr__()}'
		s += f'\n	* loc_scale = {self.loc_scale.__repr__()}'
		s += f'\n	* loc_offset = {self.loc_offset.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
