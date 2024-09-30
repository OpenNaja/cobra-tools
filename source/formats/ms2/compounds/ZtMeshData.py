# START_GLOBALS
import logging
import math
import numpy as np

from generated.formats.ms2.compounds.ZtTriBlockInfo import ZtTriBlockInfo
from generated.formats.ms2.compounds.ZtVertBlockInfo import ZtVertBlockInfo
from generated.formats.ms2.compounds.packing_utils import *
from ovl_util.tristrip import triangulate
# END_GLOBALS


class ZtMeshData:

	# START_CLASS

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
		self.weights_info = {}

	def update_dtype(self):
		"""Update MeshData.dt (numpy dtype) according to MeshData.flag"""
		# basic shared stuff
		dt = [
			("bone ids", np.ubyte, (4,)),
			("bone weights", np.ubyte, (4,)),
			("pos", np.float16, (3,)),
			("one", np.float16),
			("normal", np.ubyte, (3,)),
			("winding", np.ubyte, ),  # not tested
			("tangent", np.ubyte, (3,)),
			("bone index", np.ubyte, ),  # not tested
		]
		size = self.guess_size(self.buffer_info.uvs_offsets, self.uv_offset, self.vertex_count)
		logging.info(f"Guessed size {size}")
		if 4294967295 == self.vertex_offset:
			if size == 24:
				# 24 bytes per vert, flag is unk
				dt_colors = [
					("pos", np.float16, (3,)),
					("one", np.float16),
					("normal", np.ubyte, (3,)),
					("winding", np.ubyte, ),  # not tested
					("tangent", np.ubyte, (3,)),
					("bone index", np.ubyte, ),  # not tested
					("colors", np.ubyte, (1, 4)),
					("uvs", np.ushort, (1, 2)),
				]
			else:
				# 20 bytes per vert
				dt_colors = [
					("pos", np.float16, (3,)),
					("one", np.float16),
					("normal", np.ubyte, (3,)),
					("winding", np.ubyte, ),  # not tested
					("tangent", np.ubyte, (3,)),
					("bone index", np.ubyte, ),  # not tested
					("uvs", np.ushort, (1, 2)),
				]
		else:
			# hack for zt monitor
			if size == 4:
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

	def read_verts(self):
		self.update_dtype()
		self.init_arrays()
		logging.info(self)
		# try:
		# 	self.buffer_info.verts.seek(self.tri_info_offset)
		# 	tri_info = ZtTriBlockInfo.from_stream(self.buffer_info.verts, self.context, 0, None)
		# 	logging.info(tri_info)
		# except:
		# 	logging.exception(f"tri_info failed @ {self.tri_info_offset} in {self.buffer_info.name}")
		# try:
		# 	self.buffer_info.verts.seek(self.vert_info_offset)
		# 	vert_info = ZtVertBlockInfo.from_stream(self.buffer_info.verts, self.context, 0, None)
		# 	logging.info(vert_info)
		# except:
		# 	logging.exception(f"vert_info failed @ {self.vert_info_offset} in {self.buffer_info.name}")
		# read vertices of this mesh
		self.verts_data = np.empty(dtype=self.dt, shape=self.vertex_count)
		self.colors_data = np.empty(dtype=self.dt_colors, shape=self.vertex_count)
		self.buffer_info.uvs.seek(self.uv_offset)
		# logging.debug(f"UV at {self.buffer_info.uvs.tell()}")
		self.buffer_info.uvs.readinto(self.colors_data)
		if 4294967295 != self.vertex_offset:
			self.buffer_info.verts.seek(self.vertex_offset)
			# logging.debug(f"{self.vertex_count} VERTS at {self.buffer_info.verts.tell()}")
			self.buffer_info.verts.readinto(self.verts_data)
			self.normals[:] = self.verts_data["normal"]
			self.tangents[:] = self.verts_data["tangent"]
			self.vertices[:] = self.verts_data["pos"]

			# if "bone weights" in self.dt.fields:
			bone_weights = self.verts_data["bone weights"].astype(np.float32) / 255
			self.get_blended_weights(self.verts_data["bone ids"], bone_weights)
		else:
			self.normals[:] = self.colors_data["normal"]
			self.tangents[:] = self.colors_data["tangent"]
			self.vertices[:] = self.colors_data["pos"]

		# first cast to the float uvs array so unpacking doesn't use int division
		if self.colors is not None:
			# first cast to the float colors array so unpacking doesn't use int division
			self.colors[:] = self.colors_data["colors"]
			unpack_ubyte_color(self.colors)
		if self.uvs is not None:
			self.uvs[:] = self.colors_data["uvs"]
			self.uvs /= 2048
		unpack_ubyte_vector(self.normals)
		unpack_ubyte_vector(self.tangents)
		unpack_swizzle_vectorized(self.vertices)
		unpack_swizzle_vectorized_b(self.normals)
		unpack_swizzle_vectorized(self.tangents)
		# print(self.vertices)
		# if np.nan in self.vertices:
		# 	logging.exception(f"Found NaN in verts")
		# self.get_static_weights(self.verts_data["bone index"], self.use_blended_weights)

