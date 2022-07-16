# START_GLOBALS
import logging
import time

import numpy as np
import struct
from generated.formats.ms2.compound.packing_utils import *


# END_GLOBALS


class NewMeshData:

	# START_CLASS

	# @property
	def get_stream_index(self):
		# logging.debug(f"Using stream {self.buffer_info.offset}")
		return self.buffer_info.offset

	def init_arrays(self):
		self.vertices = np.empty((self.vertex_count, 3), np.float32)
		self.normals = np.empty((self.vertex_count, 3), np.float32)
		self.tangents = np.empty((self.vertex_count, 3), np.float32)
		try:
			uv_shape = self.dt["uvs"].shape
			self.uvs = np.empty((self.vertex_count, *uv_shape), np.float32)
		except:
			self.uvs = None
		try:
			colors_shape = self.dt["colors"].shape
			self.colors = np.empty((self.vertex_count, *colors_shape), np.float32)
		except:
			self.colors = None
		try:
			shapekeys_shape = self.dt["shapekeys0"].shape
			self.shapekeys = np.empty((self.vertex_count, 3), np.float32)
		except:
			self.shapekeys = None
		self.weights = []
		self.residues = []

	def get_vcol_count(self, ):
		if "colors" in self.dt.fields:
			return self.dt["colors"].shape[0]
		return 0

	def get_uv_count(self, ):
		if "uvs" in self.dt.fields:
			return self.dt["uvs"].shape[0]
		return 0

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
		# uv variations
		if self.flag == 528:
			dt.extend([
				("uvs", np.ushort, (1, 2)),
				("zeros0", np.int32, (3,))
			])
		elif self.flag == 529:
			dt.extend([
				("uvs", np.ushort, (2, 2)),
				("zeros0", np.int32, (2,))
			])
		elif self.flag in (533, 565, 821, 853, 885, 1013):
			dt.extend([
				("uvs", np.ushort, (2, 2)),  # second UV is either fins texcoords or fur length and shell tile scale
				("colors", np.ubyte, (1, 4)),  # these appear to be directional vectors
				("zeros0", np.int32)
			])
		elif self.flag == 513:
			dt.extend([
				("uvs", np.ushort, (2, 2)),
				# ("colors", np.ubyte, (1, 4)),
				("zeros2", np.uint64, (3,))
			])
		elif self.flag == 512:
			dt.extend([
				# tree_birch_white_03 - apparently 8 uvs
				("uvs", np.ushort, (8, 2)),
			])
		elif self.flag == 517:
			dt.extend([
				("uvs", np.ushort, (1, 2)),
				("shapekeys0", np.uint32),
				("colors", np.ubyte, (1, 4)),  # this appears to be normals, or something similar
				("shapekeys1", np.uint32),
				# sometimes, only the last is set, the rest being 00 00 C0 7F (NaN)
				("floats", np.float32, (4,)),
			])
		elif self.flag == 545:
			dt.extend([
				# cz_glasspanel_4m_02.mdl2
				("uvs", np.ushort, (1, 2)),
				("zeros2", np.uint32, (7,)),
			])
		# bone weights
		if self.flag.weights:
			dt.extend([
				("bone ids", np.ubyte, (4,)),
				("bone weights", np.ubyte, (4,)),
				("zeros1", np.uint64)
			])
		self.dt = np.dtype(dt)
		self.update_shell_count()
		if self.dt.itemsize != self.size_of_vertex:
			raise AttributeError(
				f"Vertex size for flag {self.flag} is wrong! Collected {self.dt.itemsize}, got {self.size_of_vertex}")

	def read_verts(self):
		# get dtype according to which the vertices are packed
		self.update_dtype()
		# read vertices of this mesh
		self.fur_length = 0.0
		self.stream_info.stream.seek(self.vertex_offset)
		logging.debug(f"Reading {self.vertex_count} verts at {self.stream_info.stream.tell()}")
		# read the packed ms2_file
		self.verts_data = np.empty(dtype=self.dt, shape=self.vertex_count)
		self.stream_info.stream.readinto(self.verts_data)
		# create arrays for the unpacked ms2_file
		self.init_arrays()
		# first cast to the float uvs array so unpacking doesn't use int division
		if self.uvs is not None:
			self.uvs[:] = self.verts_data[:]["uvs"]
			self.uvs = unpack_ushort_vector(self.uvs)
		if self.colors is not None:
			# first cast to the float colors array so unpacking doesn't use int division
			self.colors[:] = self.verts_data[:]["colors"]
			self.colors /= 255
		self.windings = self.verts_data[:]["winding"] // 128
		self.normals[:] = self.verts_data[:]["normal"]
		self.tangents[:] = self.verts_data[:]["tangent"]
		self.normals = (self.normals - 128) / 128
		# normalize
		self.normals /= np.linalg.norm(self.normals, axis=1, keepdims=True)
		self.tangents = (self.tangents - 128) / 128
		# unpack the shapekeys
		if self.shapekeys is not None:
			for i in range(self.vertex_count):
				first = self.verts_data[i]["shapekeys0"]
				second = self.verts_data[i]["shapekeys1"]
				packed = struct.pack("LL", first, second)
				unpacked = struct.unpack("Q", packed)[0]
				vert, residue = unpack_longint_vec(unpacked, self.base)
				self.shapekeys[i] = unpack_swizzle(vert)
			# print(self.shapekeys)
		# start_time = time.time()
		for i in range(self.vertex_count):
			in_pos_packed = self.verts_data[i]["pos"]
			vert, residue = unpack_longint_vec(in_pos_packed, self.base)
			self.vertices[i] = unpack_swizzle(vert)
			self.normals[i] = unpack_swizzle(self.normals[i])
			self.tangents[i] = unpack_swizzle(self.tangents[i])
			self.weights.append(unpack_weights(self, i))
			self.residues.append(residue)

			# packing bit
			self.weights[i].append(("residue", residue))
		# logging.info(f"Unpacked mesh in {time.time() - start_time:.2f} seconds")

	def set_verts(self, verts):
		"""Store verts as flat lists for each component"""
		# need to update the count here
		self.vertices, self.residues, self.normals, self.windings, self.tangents, self.uvs, \
		self.colors, self.weights, self.shapekeys = zip(*verts)
		# if packing isn't done right after set_verts the plugin chokes, but that is probably just due tris setter
		self.pack_verts()

	def pack_verts(self):
		"""Repack flat lists into verts_data"""
		logging.info("Packing vertices")
		# get dtype according to which the vertices are packed
		self.update_dtype()
		self.verts_data = np.zeros(len(self.vertices), dtype=self.dt)
		for i, vert in enumerate(self.verts_data):
			# residue = 1 -> 4 bones per vertex, no alpha blending
			# residue = 0 -> 1 bone per vertex, alpha blending (whiskers)
			residue = self.residues[i]
			vert["pos"] = pack_longint_vec(pack_swizzle(self.vertices[i]), residue, self.base)
			vert["normal"] = pack_ubyte_vector(pack_swizzle(self.normals[i]))
			vert["tangent"] = pack_ubyte_vector(pack_swizzle(self.tangents[i]))

			# winding seems to be a bitflag (flipped UV toggles the first bit of all its vertices to 1)
			# 0 = natural winding matching the geometry
			# 128 = UV's winding is flipped / inverted compared to geometry
			vert["winding"] = self.windings[i] * 128
			# bone index of the strongest weight
			if self.weights[i]:
				vert["bone index"] = self.weights[i][0][0]
			# else:
			# 	print(f"bad weight {i}, {self.weights[i]}")
			if "bone ids" in self.dt.fields:
				vert["bone ids"], vert["bone weights"] = self.unpack_weights_list(self.weights[i])
			if "uvs" in self.dt.fields:
				vert["uvs"] = list(pack_ushort_vector(uv) for uv in self.uvs[i])
			if "colors" in self.dt.fields:
				vert["colors"] = list(list(round(c * 255) for c in vcol) for vcol in self.colors[i])
			if "shapekeys0" in self.dt.fields:
				# first pack it as uint64
				raw_packed = pack_longint_vec(pack_swizzle(self.shapekeys[i]), residue, self.base)
				if raw_packed < 0:
					logging.error(f"Shapekey {raw_packed} could not be packed into uint64")
					raw_packed = 0
				raw_bytes = struct.pack("Q", raw_packed)
				# unpack to 2 uints again and assign data
				first, second = struct.unpack("LL", raw_bytes)
				vert["shapekeys0"] = first
				vert["shapekeys1"] = second

	def unpack_weights_list(self, weights_sorted):
		# pad the weight list to 4 bones, ie. add empty bones if missing
		for i in range(0, 4 - len(weights_sorted)):
			weights_sorted.append([0, 0])
		assert len(weights_sorted) == 4
		ids, weights = zip(*weights_sorted)
		return ids, self.quantize_bone_weights(weights)

