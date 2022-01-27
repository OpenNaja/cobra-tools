# START_GLOBALS
import logging
import math
import numpy as np
from generated.formats.ms2.compound.packing_utils import *
from plugin.utils.tristrip import triangulate
# END_GLOBALS


class ZtMeshData:

	# START_CLASS

	def populate(self, ms2_file, ms2_stream, buffer_2_offset, base=512, last_vertex_offset=0, sum_uv_dict={}):
		self.sum_uv_dict = sum_uv_dict
		self.last_vertex_offset = last_vertex_offset
		self.new_vertex_offset = 0
		self.streams = ms2_file.buffer_info.streams
		self.stream_info = self.streams[self.stream_index]
		self.stream_offset = 0
		for s in self.streams[:self.stream_index]:
			s.size = s.vertex_buffer_length + s.tris_buffer_length + s.uv_buffer_length
			self.stream_offset += s.size
			logging.debug(f"Stream {s.size}")
		self.buffer_2_offset = buffer_2_offset
		# determine end of vertex stream to seek back from
		self.vert_stream_end = self.buffer_2_offset + self.stream_offset + self.stream_info.vertex_buffer_length
		logging.debug(f"Stream {self.stream_index}, Offset: {self.stream_offset}, Address: {self.buffer_2_offset+self.stream_offset}")
		logging.debug(f"Vertex Stream end {self.vert_stream_end}")
		logging.debug(f"Tri info address {self.buffer_2_offset+self.stream_offset+self.tri_info_offset}")
		logging.debug(f"Vertex info address {self.buffer_2_offset+self.stream_offset+self.vert_info_offset}")
		# print(self)
		self.ms2_file = ms2_file
		self.base = base
		self.shapekeys = None
		self.read_verts(ms2_stream)
		self.read_tris(ms2_stream)
		return self.new_vertex_offset

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
		"""Update MeshData.dt (numpy dtype) according to MeshData.flag"""
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
		logging.debug(f"PC size of vertex: {self.dt.itemsize}")
		logging.debug(f"PC size of vcol+uv: {self.dt_colors.itemsize}")

	def update_shell_count(self):
		if self.flag.repeat_tris:
			self.shell_count = 6
		else:
			self.shell_count = 1

	def read_tris(self, stream):
		# read all tri indices for this mesh
		stream.seek(self.buffer_2_offset + self.stream_offset + self.stream_info.vertex_buffer_length + self.tri_offset)
		logging.debug(f"tris offset {stream.tell()}")
		# read all tri indices for this mesh segment
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
		# read a vertices of this mesh
		if 4294967295 == self.vertex_offset:
			logging.warning(f"vertex_offset is -1, seeking to last vertex offset {self.last_vertex_offset}")
			if self.last_vertex_offset == 0:
				self.last_vertex_offset = self.buffer_2_offset + self.stream_offset
				# stream.seek(self.vert_stream_end - (self.vertex_count * self.dt.itemsize))
				logging.warning(f"Zero, starting at buffer start {stream.tell()}")
			else:
				stream.seek(self.last_vertex_offset)
		else:
			stream.seek(self.buffer_2_offset + self.stream_offset + self.vertex_offset)
		logging.debug(f"{self.vertex_count} VERTS at {stream.tell()}")
		self.verts_data = np.fromfile(stream, dtype=self.dt, count=self.vertex_count)
		self.new_vertex_offset = stream.tell()
		# print(self.verts_data.shape)
		stream.seek(self.buffer_2_offset + self.stream_offset + self.stream_info.vertex_buffer_length + self.stream_info.tris_buffer_length + self.uv_offset)
		logging.debug(f"UV at {stream.tell()}")
		self.colors_data = np.fromfile(stream, dtype=self.dt_colors, count=self.vertex_count)
		# first cast to the float uvs array so unpacking doesn't use int division
		if self.colors is not None:
			# first cast to the float colors array so unpacking doesn't use int division
			self.colors[:] = self.colors_data[:]["colors"]
			self.colors /= 255
		if self.uvs is not None:
			self.uvs[:] = self.colors_data[:]["uvs"]
			self.uvs /= 2048
		logging.debug(self.normals.shape)
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
			logging.warning(f"math domain for lod {self.poweroftwo}")
		return lod_i

	@lod_index.setter
	def lod_index(self, lod_i):
		self.poweroftwo = int(math.pow(2, lod_i))
