# START_GLOBALS
import struct
import math
import numpy as np
from generated.formats.ms2.compound.packing_utils import *
from utils.tristrip import triangulate
# END_GLOBALS


class ZtModelData:

	# START_CLASS

	def populate(self, ms2_file, ms2_stream, start_buffer2, base=512, last_vert_offset=0):
		self.last_vert_offset = last_vert_offset
		self.new_vert_offset = 0
		self.streams = ms2_file.pc_buffer1.buffer_info_pc.streams
		self.stream_info = self.streams[self.stream_index]
		self.stream_offset = 0
		for s in self.streams[:self.stream_index]:
			self.stream_offset += s.vertex_buffer_length + s.tris_buffer_length + s.next_buffer_length
		self.start_buffer2 = start_buffer2
		print(f"Stream {self.stream_index}, Offset: {self.stream_offset}, Address: {self.start_buffer2+self.stream_offset}")
		print("Tri info address", self.start_buffer2+self.stream_offset+self.tri_info_offset)
		print("Vertex info address", self.start_buffer2+self.stream_offset+self.vert_info_offset)
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
		dt_colors = [
			("colors", np.ubyte, (1, 4)),
			("uvs", np.ushort, (1 + self.some_index, 2)),
		]
		self.dt = np.dtype(dt)
		self.dt_colors = np.dtype(dt_colors)
		self.update_shell_count()
		print("PC size of vertex:", self.dt.itemsize)
		print("PC size of vcol:", self.dt_colors.itemsize)

	def update_shell_count(self):
		if self.flag.repeat_tris:
			self.shell_count = 6
		else:
			self.shell_count = 1

	def read_tris(self, stream):
		# read all tri indices for this model
		stream.seek(self.start_buffer2 + self.stream_offset + self.stream_info.vertex_buffer_length + self.tri_offset)
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
			stream.seek(self.last_vert_offset - (self.vertex_count * self.dt.itemsize))
		else:
			stream.seek(self.start_buffer2 + self.stream_offset + self.vert_offset)
		print("VERTS", stream.tell(), self.vertex_count)
		self.verts_data = np.fromfile(stream, dtype=self.dt, count=self.vertex_count)
		self.new_vert_offset = stream.tell()
		print(self.verts_data.shape)
		stream.seek(self.start_buffer2 + self.stream_offset + self.stream_info.vertex_buffer_length + self.stream_info.tris_buffer_length + self.uv_offset)
		print("UV", stream.tell())
		self.colors_data = np.fromfile(stream, dtype=self.dt_colors, count=self.vertex_count)
		# first cast to the float uvs array so unpacking doesn't use int division
		if self.colors is not None:
			# first cast to the float colors array so unpacking doesn't use int division
			self.colors[:] = self.colors_data[:]["colors"]
			self.colors /= 255
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
