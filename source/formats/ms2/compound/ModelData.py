# START_GLOBALS
import struct
import math
import numpy as np
from generated.formats.ms2.compound.packing_utils import *


FUR_OVERHEAD = 2
# END_GLOBALS


class ModelData:

	# START_CLASS

	def read_bytes(self, start_buffer2, vertex_data_size, stream):
		"""Used to store raw binary vertex and tri data on the model, for merging"""
		# print("reading binary model data")
		# read a vertices of this model
		stream.seek(start_buffer2 + self.vertex_offset)
		self.verts_bytes = stream.read(self.size_of_vertex * self.vertex_count)
		stream.seek(start_buffer2 + vertex_data_size + self.tri_offset)
		self.tris_bytes = stream.read(2 * self.tri_index_count)
		# print(len(self.verts_bytes), len(self.tris_bytes))

	def read_bytes_map(self, start_buffer2, stream):
		"""Used to document byte usage of different vertex formats"""
		# read a vertices of this model
		stream.seek(start_buffer2 + self.vertex_offset)
		# read the packed ms2_file
		ms2_file = np.fromfile(stream, dtype=np.ubyte, count=self.size_of_vertex * self.vertex_count)
		ms2_file = ms2_file.reshape((self.vertex_count, self.size_of_vertex))
		self.bytes_map = np.max(ms2_file, axis=0)
		if self.size_of_vertex != 48:
			raise AttributeError(f"size_of_vertex != 48: size_of_vertex {self.size_of_vertex}, flag {self.flag}", )

	# print(self.size_of_vertex, self.flag, self.bytes_map)

	def init_arrays(self, count):
		self.vertex_count = count
		self.vertices = np.empty((self.vertex_count, 3), np.float32)
		self.normals = np.empty((self.vertex_count, 3), np.float32)
		self.tangents = np.empty((self.vertex_count, 3), np.float32)
		try:
			uv_shape = self.dt["uvs"].shape
			self.uvs = np.empty((self.vertex_count, *uv_shape), np.float32)
		except:
			self.uvs = None
		try:
			fur_shape = self.dt["fur_length"].shape
			self.fur = np.empty((self.vertex_count, *fur_shape), np.float32)
		except:
			self.fur = None
		try:
			colors_shape = self.dt["colors"].shape
			self.colors = np.empty((self.vertex_count, *colors_shape), np.float32)
		except:
			self.colors = None
		self.weights = []

	def get_vcol_count(self, ):
		if "colors" in self.dt.fields:
			return self.dt["colors"].shape[0]
		return 0

	def get_uv_count(self, ):
		if "uvs" in self.dt.fields:
			return self.dt["uvs"].shape[0]
		return 0

	def update_dtype(self):
		"""Update ModelData.dt (numpy dtype) according to ModelData.flag"""
		# basic shared stuff
		dt = [
			("pos", np.uint64),
			("normal", np.ubyte, (3,)),
			("unk", np.ubyte),
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
		elif self.flag in (565,):
			dt.extend([
				("uvs", np.ushort, (2, 2)),
				("colors", np.ubyte, (1, 4)), # these appear to be directional vectors
				("zeros0", np.int32, (1,))
			])
		elif self.flag in (821, 853, 885, 1013):
			dt.extend([
				("uvs", np.ushort, (1, 2)),
				("fur_length", np.ushort, (2,)),
				("colors", np.ubyte, (1, 4)), # these appear to be directional vectors
				("zeros0", np.int32, (1,))
			])
		elif self.flag == 533:
			dt.extend([
				# see walls_gate.mdl2, two uv layers
				("uvs", np.ushort, (2, 2)),
				("colors", np.ubyte, (1, 4)),
				("zeros2", np.int32, (1,))
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
				# trees seem to have two uvs, then something like normals
				("uvs", np.ushort, (2, 2)),
				("colors", np.ubyte, (6, 4)),
			])
		elif self.flag == 545:
			dt.extend([
				# cz_glasspanel_4m_02.mdl2
				("uvs", np.ushort, (1, 2)),
				("zeros2", np.uint32, (7,)),
			])

		# bone weights
		if self.flag in (528, 529, 533, 565, 821, 853, 885, 1013):
			dt.extend([
				("bone ids", np.ubyte, (4,)),
				("bone weights", np.ubyte, (4,)),
				("zeros1", np.uint64)
			])
		self.dt = np.dtype(dt)
		if self.dt.itemsize != self.size_of_vertex:
			raise AttributeError(
				f"Vertex size for flag {self.flag} is wrong! Collected {self.dt.itemsize}, got {self.size_of_vertex}")

	def read_verts(self, stream):
		# read a vertices of this model
		stream.seek(self.start_buffer2 + self.vertex_offset)
		# get dtype according to which the vertices are packed
		self.update_dtype()
		# read the packed ms2_file
		self.verts_data = np.fromfile(stream, dtype=self.dt, count=self.vertex_count)
		# create arrays for the unpacked ms2_file
		self.init_arrays(self.vertex_count)
		# first cast to the float uvs array so unpacking doesn't use int division
		# print(self.verts_data[:]["uvs"][1])
		if self.uvs is not None:
			self.uvs[:] = self.verts_data[:]["uvs"]
			# unpack uvs
			self.uvs = (self.uvs - 32768) / 2048
		self.fur_length = 0.0
		if self.fur is not None:
			self.fur[:] = self.verts_data[:]["fur_length"]
			# unpack fur
			self.fur = (self.fur - 32768) / 2048
			# print("self.fur[0]",self.fur[0])
			# normalize with some overhead
			self.fur_length = np.max(self.fur) * FUR_OVERHEAD
			# print("self.fur_length", self.fur_length)
			self.fur /= self.fur_length
		if self.colors is not None:
			# first cast to the float colors array so unpacking doesn't use int division
			self.colors[:] = self.verts_data[:]["colors"]
			self.colors /= 255
		self.normals[:] = self.verts_data[:]["normal"]
		self.tangents[:] = self.verts_data[:]["tangent"]
		self.normals = (self.normals - 128) / 128
		# normalize
		self.normals /= np.linalg.norm(self.normals, axis=1, keepdims=True)
		self.tangents = (self.tangents - 128) / 128
		for i in range(self.vertex_count):
			in_pos_packed = self.verts_data[i]["pos"]
			vert, residue = unpack_longint_vec(in_pos_packed, self.base)
			self.vertices[i] = unpack_swizzle(vert)
			self.normals[i] = unpack_swizzle(self.normals[i])
			self.tangents[i] = unpack_swizzle(self.tangents[i])
			self.weights.append(unpack_weights(self, i, residue))

	def write_verts(self, stream):
		stream.write(self.verts_data.tobytes())

	def read_tris(self, stream):
		# read all tri indices for this model
		stream.seek(self.start_buffer2 + self.ms2_file.buffer_info.vertexdatasize + self.tri_offset)
		# read all tri indices for this model segment
		self.tri_indices = np.fromfile(stream, dtype=np.uint16, count=self.tri_index_count)

	def write_tris(self, stream):
		tri_bytes = struct.pack(f"{len(self.tri_indices)}H", *self.tri_indices)
		stream.write(tri_bytes)
		# extend tri array according to shell count
		print(f"Adding {self.shell_count} shells")
		for shell in range(self.shell_count):
			stream.write(tri_bytes)

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

	def set_verts(self, verts):
		"""Update self.verts_data from list of new verts"""
		self.verts = verts
		self.verts_data = np.zeros(len(verts), dtype=self.dt)
		for i, (
		position, residue, normal, unk_0, tangent, bone_index, uvs, vcols, bone_ids, bone_weights, fur) in enumerate(
				verts):
			self.verts_data[i]["pos"] = pack_longint_vec(pack_swizzle(position), residue, self.base)
			self.verts_data[i]["normal"] = pack_ubyte_vector(pack_swizzle(normal))
			self.verts_data[i]["tangent"] = pack_ubyte_vector(pack_swizzle(tangent))
			self.verts_data[i]["unk"] = unk_0 * 255
			self.verts_data[i]["bone index"] = bone_index
			if "bone ids" in self.dt.fields:
				self.verts_data[i]["bone ids"] = bone_ids
				# round is essential so the float is not truncated
				self.verts_data[i]["bone weights"] = list(round(w * 255) for w in bone_weights)
				# print(self.verts_data[i]["bone weights"], np.sum(self.verts_data[i]["bone weights"]))
				# additional double check
				d = np.sum(self.verts_data[i]["bone weights"]) - 255
				self.verts_data[i]["bone weights"][0] -= d
				assert np.sum(self.verts_data[i]["bone weights"]) == 255
			if "uvs" in self.dt.fields:
				self.verts_data[i]["uvs"] = list(pack_ushort_vector(uv) for uv in uvs)
			if "fur_length" in self.dt.fields and fur is not None:
				self.verts_data[i]["fur_length"] = pack_ushort_vector((fur, -1.1))
			if "colors" in self.dt.fields:
				self.verts_data[i]["colors"] = list(list(c * 255 for c in vcol) for vcol in vcols)

	@property
	def tris(self, ):
		# create non-overlapping tris
		# reverse to account for the flipped normals from mirroring in blender
		return [(self.tri_indices[i + 2], self.tri_indices[i + 1], self.tri_indices[i]) for i in
				range(0, len(self.tri_indices), 3)]

	@tris.setter
	def tris(self, b_tris):
		# clear tri array
		self.tri_indices = []
		for tri in b_tris:
			# reverse to account for the flipped normals from mirroring in blender
			self.tri_indices.extend(reversed(tri))

	def populate(self, ms2_file, ms2_stream, start_buffer2, base=512):
		self.start_buffer2 = start_buffer2
		self.ms2_file = ms2_file
		self.base = base
		self.read_verts(ms2_stream)
		self.read_tris(ms2_stream)
