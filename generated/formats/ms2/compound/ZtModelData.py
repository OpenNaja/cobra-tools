
import struct
import math
import numpy as np
from generated.formats.ms2.compound.packing_utils import *
from utils.tristrip import triangulate
import typing
from generated.formats.ms2.bitfield.ModelFlagZT import ModelFlagZT


class ZtModelData:

	"""
	Defines one model's data. Both LODs and mdl2 files may contain several of these.
	This is a fragment from headers of type (0,0)
	If there is more than one of these, the fragments appear as a list according to
	"""

	def __init__(self, arg=None, template=None):
		self.name = ''
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# index into streamed buffers
		self.stream_index = 0

		# always zero
		self.zero_a = 0

		# increments somewhat in platypus
		self.some_index = 0

		# always zero
		self.zero_b = 0

		# repeat
		self.tri_index_count = 0

		# vertex count of model
		self.vertex_count = 0

		# stores count, -1 as ints
		self.tri_info_offset = 0

		# stores count, -1 as ints
		self.vert_info_offset = 0

		# x*16 = offset in buffer 2
		self.known_ff_0 = 0

		# relative to start of buffer[i]'s tris section start, blocks of 2 bytes (ushort), tri index count
		self.tri_offset = 0

		# relative to start of buffer[i], blocks of 8 bytes, count vertex_count
		self.uv_offset = 0

		# relative to start of buffer[i], blocks of 24 bytes, count vertex_count
		self.vert_offset = 0

		# x*16 = offset in buffer 2
		self.known_ff_1 = 0

		# x*16 = offset in buffer 2
		self.one_0 = 0

		# ?
		self.one_1 = 0

		# ?
		self.poweroftwo = 0

		# power of 2 increasing with lod index
		self.poweroftwo = 0

		# always zero
		self.zero = 0

		# some floats
		self.unknown_07 = 0

		# bitfield
		self.flag = ModelFlagZT()

		# always zero
		self.zero_uac = 0

	def read(self, stream):

		self.io_start = stream.tell()
		self.stream_index = stream.read_uint()
		self.zero_a = stream.read_uint()
		self.some_index = stream.read_uint()
		self.zero_b = stream.read_uint()
		self.tri_index_count = stream.read_uint()
		self.vertex_count = stream.read_uint()
		self.tri_info_offset = stream.read_uint()
		self.vert_info_offset = stream.read_uint()
		self.known_ff_0 = stream.read_int()
		self.tri_offset = stream.read_uint()
		self.uv_offset = stream.read_uint()
		self.vert_offset = stream.read_uint()
		self.known_ff_1 = stream.read_short()
		self.one_0 = stream.read_ushort()
		self.one_1 = stream.read_ushort()
		if stream.version == 17:
			self.poweroftwo = stream.read_ushort()
		if stream.version == 18:
			self.poweroftwo = stream.read_uint()
			self.zero = stream.read_uint()
			self.unknown_07 = stream.read_float()
		self.flag = stream.read_type(ModelFlagZT)
		if stream.version == 17:
			self.zero_uac = stream.read_uint()

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_uint(self.stream_index)
		stream.write_uint(self.zero_a)
		stream.write_uint(self.some_index)
		stream.write_uint(self.zero_b)
		stream.write_uint(self.tri_index_count)
		stream.write_uint(self.vertex_count)
		stream.write_uint(self.tri_info_offset)
		stream.write_uint(self.vert_info_offset)
		stream.write_int(self.known_ff_0)
		stream.write_uint(self.tri_offset)
		stream.write_uint(self.uv_offset)
		stream.write_uint(self.vert_offset)
		stream.write_short(self.known_ff_1)
		stream.write_ushort(self.one_0)
		stream.write_ushort(self.one_1)
		if stream.version == 17:
			stream.write_ushort(self.poweroftwo)
		if stream.version == 18:
			stream.write_uint(self.poweroftwo)
			stream.write_uint(self.zero)
			stream.write_float(self.unknown_07)
		stream.write_type(self.flag)
		if stream.version == 17:
			stream.write_uint(self.zero_uac)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'ZtModelData [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* stream_index = {self.stream_index.__repr__()}'
		s += f'\n	* zero_a = {self.zero_a.__repr__()}'
		s += f'\n	* some_index = {self.some_index.__repr__()}'
		s += f'\n	* zero_b = {self.zero_b.__repr__()}'
		s += f'\n	* tri_index_count = {self.tri_index_count.__repr__()}'
		s += f'\n	* vertex_count = {self.vertex_count.__repr__()}'
		s += f'\n	* tri_info_offset = {self.tri_info_offset.__repr__()}'
		s += f'\n	* vert_info_offset = {self.vert_info_offset.__repr__()}'
		s += f'\n	* known_ff_0 = {self.known_ff_0.__repr__()}'
		s += f'\n	* tri_offset = {self.tri_offset.__repr__()}'
		s += f'\n	* uv_offset = {self.uv_offset.__repr__()}'
		s += f'\n	* vert_offset = {self.vert_offset.__repr__()}'
		s += f'\n	* known_ff_1 = {self.known_ff_1.__repr__()}'
		s += f'\n	* one_0 = {self.one_0.__repr__()}'
		s += f'\n	* one_1 = {self.one_1.__repr__()}'
		s += f'\n	* poweroftwo = {self.poweroftwo.__repr__()}'
		s += f'\n	* zero = {self.zero.__repr__()}'
		s += f'\n	* unknown_07 = {self.unknown_07.__repr__()}'
		s += f'\n	* flag = {self.flag.__repr__()}'
		s += f'\n	* zero_uac = {self.zero_uac.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s

	def populate(self, ms2_file, ms2_stream, buffer_2_offset, base=512, last_vert_offset=0, sum_uv_dict={}):
		self.sum_uv_dict = sum_uv_dict
		self.last_vert_offset = last_vert_offset
		self.new_vert_offset = 0
		self.streams = ms2_file.pc_buffer1.buffer_info_pc.streams
		self.stream_info = self.streams[self.stream_index]
		self.stream_offset = 0
		for s in self.streams[:self.stream_index]:
			self.stream_offset += s.vertex_buffer_length + s.tris_buffer_length + s.uv_buffer_length
		self.buffer_2_offset = buffer_2_offset
		print(f"Stream {self.stream_index}, Offset: {self.stream_offset}, Address: {self.buffer_2_offset+self.stream_offset}")
		print("Tri info address", self.buffer_2_offset+self.stream_offset+self.tri_info_offset)
		print("Vertex info address", self.buffer_2_offset+self.stream_offset+self.vert_info_offset)
		print(self)
		self.ms2_file = ms2_file
		self.base = base
		self.read_verts(ms2_stream)
		self.read_tris(ms2_stream)
		return self.new_vert_offset

	def init_arrays(self):
		self.vertices = np.empty((self.vertex_count, 3), np.float32)
		self.normals = np.empty((self.vertex_count, 3), np.float32)
		self.tangents = np.empty((self.vertex_count, 3), np.float32)
		try:
			uv_shape = self.dt_colors["uvs"].shape
			self.uvs = np.empty((self.vertex_count, *uv_shape), np.float32)
		except:
			self.uvs = None
		try:
			colors_shape = self.dt_colors["colors"].shape
			self.colors = np.empty((self.vertex_count, *colors_shape), np.float32)
		except:
			self.colors = None
		self.weights = []

	def update_dtype(self):
		"""Update ModelData.dt (numpy dtype) according to ModelData.flag"""
		# basic shared stuff
		dt = [
			("bone ids", np.ubyte, (4,)),
			("bone weights", np.ubyte, (4,)),
			("pos", np.float16, (3,)),
			("one", np.float16),
			("normal", np.ubyte, (3,)),
			("a", np.ubyte, ),
			("tangent", np.ubyte, (3,)),
			("b", np.ubyte, ),
		]
		vert_count_in_stream = self.sum_uv_dict[self.stream_index]
		stream_info = self.streams[self.stream_index]
		# hack for zt monitor
		if stream_info.uv_buffer_length // vert_count_in_stream == 4:
			dt_colors = [
				("uvs", np.ushort, (1, 2)),
			]
		else:
			dt_colors = [
				("colors", np.ubyte, (1, 4)),
				("uvs", np.ushort, (1 + self.some_index, 2)),
			]
		self.dt = np.dtype(dt)
		self.dt_colors = np.dtype(dt_colors)
		self.update_shell_count()
		print("PC size of vertex:", self.dt.itemsize)
		print("PC size of vcol+uv:", self.dt_colors.itemsize)

	def update_shell_count(self):
		if self.flag.repeat_tris:
			self.shell_count = 6
		else:
			self.shell_count = 1

	def read_tris(self, stream):
		# read all tri indices for this model
		stream.seek(self.buffer_2_offset + self.stream_offset + self.stream_info.vertex_buffer_length + self.tri_offset)
		print("tris offset", stream.tell())
		# read all tri indices for this model segment
		self.tri_indices = np.fromfile(stream, dtype=np.uint16, count=self.tri_index_count // self.shell_count)

	@property
	def tris(self, ):
		# tri strip
		if self.flag.stripify:
			return triangulate((self.tri_indices,))
		else:
			return list([(self.tri_indices[i], self.tri_indices[i+1], self.tri_indices[i+2]) for i in range(0, len(self.tri_indices), 3)])

	def read_verts(self, stream):
		# get dtype according to which the vertices are packed
		self.update_dtype()
		# create arrays for the unpacked ms2_file
		self.init_arrays()
		# read a vertices of this model
		if 4294967295 == self.vert_offset:
			# self.vert_offset = 0
			print(f"Warning, vert_offset is -1, seeking to last vert offset {self.last_vert_offset}")
			# stream.seek(self.last_vert_offset - (self.vertex_count * self.dt.itemsize))
			stream.seek(self.last_vert_offset)
		else:
			stream.seek(self.buffer_2_offset + self.stream_offset + self.vert_offset)
		print("VERTS", stream.tell(), self.vertex_count)
		self.new_vert_offset = stream.tell()
		self.verts_data = np.fromfile(stream, dtype=self.dt, count=self.vertex_count)
		print(self.verts_data.shape)
		stream.seek(self.buffer_2_offset + self.stream_offset + self.stream_info.vertex_buffer_length + self.stream_info.tris_buffer_length + self.uv_offset)
		print("UV", stream.tell())
		self.colors_data = np.fromfile(stream, dtype=self.dt_colors, count=self.vertex_count)
		# first cast to the float uvs array so unpacking doesn't use int division
		if self.colors is not None:
			# first cast to the float colors array so unpacking doesn't use int division
			self.colors[:] = self.colors_data[:]["colors"]
			self.colors /= 255
		if self.uvs is not None:
			self.uvs[:] = self.colors_data[:]["uvs"]
			self.uvs /= 2048
		print(self.normals.shape)
		self.normals[:] = self.verts_data[:]["normal"]
		# self.tangents[:] = self.verts_data[:]["tangent"]
		self.vertices[:] = self.verts_data[:]["pos"]
		self.normals = (self.normals - 128) / 128
		# self.tangents = (self.tangents - 128) / 128
		for i in range(self.vertex_count):
			self.vertices[i] = unpack_swizzle(self.vertices[i])
			# self.normals[i] = unpack_swizzle(self.normals[i])
			# different swizzle!
			self.normals[i] = (-self.normals[i][2], -self.normals[i][0], self.normals[i][1])
		# 	self.tangents[i] = unpack_swizzle(self.tangents[i])
			self.weights.append(unpack_weights(self, i, 0, extra=False))
			# print(math.sqrt(sum(x**2 for x in self.normals[i])))
		# print(self.normals)
		# print(self.verts_data)
		# print(self.vertices)
		# print(self.weights)

	@staticmethod
	def get_weights(bone_ids, bone_weights):
		return [(i, w / 255) for i, w in zip(bone_ids, bone_weights) if w > 0]

	@property
	def lod_index(self, ):
		try:
			lod_i = int(math.log2(self.poweroftwo))
		except:
			lod_i = 0
			print("EXCEPTION: math domain for lod", self.poweroftwo)
		return lod_i

	@lod_index.setter
	def lod_index(self, lod_i):
		self.poweroftwo = int(math.pow(2, lod_i))

