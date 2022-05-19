# START_GLOBALS
import math
import logging
import numpy as np
from generated.formats.ms2.compound.packing_utils import *
from plugin.utils.tristrip import triangulate
# END_GLOBALS


class PcMeshData:

	# START_CLASS

	def populate(self, ms2_file, base=512, last_vertex_offset=0, sum_uv_dict={}):
		self.ms2_file = ms2_file
		self.base = base
		self.shapekeys = None
		stream = ms2_file.streams[self.stream_index]
		logging.debug(f"Using stream {self.stream_index}")
		self.stream_info = ms2_file.buffer_infos[self.stream_index]
		self.read_verts(stream)
		self.read_tris(stream)

	def init_arrays(self, count):
		self.vertex_count = count
		self.vertices = np.empty((self.vertex_count, 3), np.float32)
		self.normals = np.empty((self.vertex_count, 3), np.float32)
		self.tangents = np.empty((self.vertex_count, 3), np.float32)
		try:
			uv_shape = self.dt_uv["uvs"].shape
			self.uvs = np.empty((self.vertex_count, *uv_shape), np.float32)
		except:
			self.uvs = None
		try:
			colors_shape = self.dt["colors"].shape
			self.colors = np.empty((self.vertex_count, *colors_shape), np.float32)
		except:
			self.colors = None
		self.weights = []

	def update_dtype(self):
		"""Update MeshData.dt (numpy dtype) according to MeshData.flag"""
		# basic shared stuff
		dt = [
			("pos", np.uint64),
			("normal", np.ubyte, (3,)),
			("unk", np.ubyte),
			("tangent", np.ubyte, (3,)),
			("bone index", np.ubyte),
		]
		dt_uv = [
			("uvs", np.ushort, (1, 2)),
		]
		# bone weights
		# if self.flag in (529, 533, 885, 565, 1013, 528, 821):
		dt_w = [
			("bone ids", np.ubyte, (4,)),
			("bone weights", np.ubyte, (4,)),
		]
		self.dt = np.dtype(dt)
		self.dt_uv = np.dtype(dt_uv)
		self.dt_w = np.dtype(dt_w)
		self.update_shell_count()
		logging.debug(f"PC size of vertex: {self.dt.itemsize}")
		logging.debug(f"PC size of uv: {self.dt_uv.itemsize}")
		logging.debug(f"PC size of weights: {self.dt_w.itemsize}")

	@property
	def tris_address(self):
		logging.debug(f"count {self.tri_offset}")
		return self.tri_offset * 16

	def read_verts(self, stream):
		# read a vertices of this mesh
		stream.seek(self.vertex_offset * 16)
		logging.debug(f"VERTS at {stream.tell()}")
		# get dtype according to which the vertices are packed
		self.update_dtype()
		# read the packed ms2_file
		self.verts_data = np.empty(dtype=self.dt, shape=self.vertex_count)
		stream.readinto(self.verts_data)
		stream.seek(self.uv_offset * 16)
		logging.debug(f"UV at {stream.tell()}")
		self.uv_data = np.empty(dtype=self.dt_uv, shape=self.vertex_count)
		stream.readinto(self.uv_data)
		stream.seek(self.weights_offset * 16)
		logging.debug(f"WEIGHTS at {stream.tell()}")
		# print(self)
		# PC ostrich download has self.weights_offset = 0 for eyes and lashes, which consequently get wrong weights
		self.weights_data = np.empty(dtype=self.dt_w, shape=self.vertex_count)
		stream.readinto(self.weights_data)
		# print(self.verts_data)
		# create arrays for the unpacked ms2_file
		self.init_arrays(self.vertex_count)
		# first cast to the float uvs array so unpacking doesn't use int division
		if self.uvs is not None:
			self.uvs[:] = self.uv_data[:]["uvs"]
			# unpack uvs
			self.uvs = unpack_ushort_vector(self.uvs)
		# if self.colors is not None:
		# 	# first cast to the float colors array so unpacking doesn't use int division
		# 	self.colors[:] = self.verts_data[:]["colors"]
		# 	self.colors /= 255
		self.normals[:] = self.verts_data[:]["normal"]
		self.tangents[:] = self.verts_data[:]["tangent"]
		self.normals = (self.normals - 128) / 128
		self.tangents = (self.tangents - 128) / 128
		for i in range(self.vertex_count):
			in_pos_packed = self.verts_data[i]["pos"]
			vert, residue = unpack_longint_vec(in_pos_packed, self.base)
			self.vertices[i] = unpack_swizzle(vert)
			self.normals[i] = unpack_swizzle(self.normals[i])
			self.tangents[i] = unpack_swizzle(self.tangents[i])
			self.weights.append(unpack_weights(self, i, residue, extra=False))
		# print(self.vertices)
