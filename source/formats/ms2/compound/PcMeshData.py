# START_GLOBALS
import math
import logging
import numpy as np
from generated.formats.ms2.compound.packing_utils import *
from plugin.utils.tristrip import triangulate
# END_GLOBALS


class PcMeshData:

	# START_CLASS

	def init_arrays(self, count):
		self.vertex_count = count
		self.vertices = np.empty((self.vertex_count, 3), np.float32)
		self.residues = np.empty(self.vertex_count, np.bool)
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

	def update_dtype(self):
		"""Update MeshData.dt (numpy dtype) according to MeshData.flag"""
		# basic shared stuff
		dt = [
			("pos", np.uint64),
			("normal", np.ubyte, (3,)),
			("winding", np.ubyte),
			("tangent", np.ubyte, (3,)),
			("bone index", np.ubyte),
		]
		dt_uv = [
			("uvs", np.ushort, (1, 2)),
		]
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

	def read_verts(self):
		# read a vertices of this mesh
		self.stream_info.stream.seek(self.vertex_offset * 16)
		logging.debug(f"VERTS at {self.stream_info.stream.tell()}")
		# get dtype according to which the vertices are packed
		self.update_dtype()
		# read the packed ms2_file
		self.verts_data = np.empty(dtype=self.dt, shape=self.vertex_count)
		self.stream_info.stream.readinto(self.verts_data)
		self.stream_info.stream.seek(self.uv_offset * 16)
		logging.debug(f"UV at {self.stream_info.stream.tell()}")
		self.uv_data = np.empty(dtype=self.dt_uv, shape=self.vertex_count)
		self.stream_info.stream.readinto(self.uv_data)
		self.stream_info.stream.seek(self.weights_offset * 16)
		logging.debug(f"WEIGHTS at {self.stream_info.stream.tell()}")
		# PC ostrich download has self.weights_offset = 0 for eyes and lashes, which consequently get wrong weights
		self.weights_data = np.empty(dtype=self.dt_w, shape=self.vertex_count)
		self.stream_info.stream.readinto(self.weights_data)
		# create arrays for the unpacked ms2_file
		self.init_arrays(self.vertex_count)
		# first cast to the float uvs array so unpacking doesn't use int division
		if self.uvs is not None:
			self.uvs[:] = self.uv_data["uvs"]
			self.uvs = unpack_ushort_vector(self.uvs)

		self.bone_weights = self.weights_data["bone weights"].astype(np.float32) / 255
		self.get_weights(self.weights_data["bone ids"], self.bone_weights)
		unpack_int64_vector(self.verts_data["pos"], self.vertices, self.residues)
		scale_unpack_vectorized(self.vertices, self.base)
		unpack_ubyte_vector(self.normals)
		unpack_ubyte_vector(self.tangents)
		unpack_swizzle_vectorized(self.vertices)
		unpack_swizzle_vectorized(self.normals)
		unpack_swizzle_vectorized(self.tangents)
		# print(self.vertices)
