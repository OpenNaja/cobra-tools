# START_GLOBALS
import logging
import math
import numpy as np
from generated.formats.ms2.compound.packing_utils import *
from plugin.utils.tristrip import triangulate
# END_GLOBALS


class ZtMeshData:

	# START_CLASS

	def populate(self, ms2_file, base=512, last_vertex_offset=0, sum_uv_dict={}):
		self.sum_uv_dict = sum_uv_dict
		self.last_vertex_offset = last_vertex_offset
		self.new_vertex_offset = 0
		stream = ms2_file.streams[self.stream_index]
		logging.debug(f"Using stream {self.stream_index}")
		self.stream_info = ms2_file.buffer_infos[self.stream_index]
		logging.debug(f"Tri info address {self.tri_info_offset}")
		logging.debug(f"Vertex info address {self.vert_info_offset}")
		# print(self)
		self.ms2_file = ms2_file
		self.base = base
		self.shapekeys = None
		self.read_verts(stream)
		self.read_tris(stream)
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
		# hack for zt monitor
		if self.stream_info.uv_buffer_size // vert_count_in_stream == 4:
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

	@property
	def tris_address(self):
		return self.stream_info.vertex_buffer_size + self.tri_offset

	def read_verts(self, stream):
		# get dtype according to which the vertices are packed
		self.update_dtype()
		# create arrays for the unpacked ms2_file
		self.init_arrays()
		# read a vertices of this mesh
		if 4294967295 == self.vertex_offset:
			logging.warning(f"vertex_offset is -1, seeking to last vertex offset {self.last_vertex_offset}")
			if self.last_vertex_offset == 0:
				logging.warning(f"Zero, starting at buffer start {stream.tell()}")
			else:
				stream.seek(self.last_vertex_offset)
		else:
			stream.seek(self.vertex_offset)
		logging.debug(f"{self.vertex_count} VERTS at {stream.tell()}")
		self.verts_data = np.empty(dtype=self.dt, shape=self.vertex_count)
		stream.readinto(self.verts_data)
		self.new_vertex_offset = stream.tell()
		# print(self.verts_data.shape)
		stream.seek(self.stream_info.vertex_buffer_size + self.stream_info.tris_buffer_size + self.uv_offset)
		logging.debug(f"UV at {stream.tell()}")
		self.colors_data = np.empty(dtype=self.dt_colors, shape=self.vertex_count)
		stream.readinto(self.colors_data)
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

