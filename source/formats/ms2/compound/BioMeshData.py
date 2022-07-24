# START_GLOBALS
import logging
import numpy as np
import struct

from generated.array import Array
from generated.formats.ms2.compound.OffsetChunk import OffsetChunk
from generated.formats.ms2.compound.PosChunk import PosChunk
from generated.formats.ms2.compound.packing_utils import *
from generated.formats.ms2.enum.MeshFormat import MeshFormat
from plugin.utils.tristrip import triangulate


# END_GLOBALS


class BioMeshData:

	# START_CLASS

	# @property
	def get_stream_index(self):
		# logging.debug(f"Using stream {self.buffer_info.offset}")
		return self.buffer_info.offset

	def get_vcol_count(self, ):
		if "colors" in self.dt.fields:
			return self.dt["colors"].shape[0]
		return 0

	def get_uv_count(self, ):
		if "uvs" in self.dt.fields:
			return self.dt["uvs"].shape[0]
		return 0

	@property
	def tris_start_address(self):
		return self.stream_info.vertex_buffer_size

	@property
	def tris_address(self):
		# just a guess here, not guaranteed to be the right starting offset
		return self.tris_start_address + self.pos_chunks[0].tris_offset

	def read_tris(self):
		pass

	def read_tris_bio(self):
		# read all tri indices for this mesh, but only as many as needed if there are shells
		self.stream_info.stream.seek(self.tris_address)
		index_count = self.tris_count * 3  # // self.shell_count
		logging.info(f"Reading {index_count} indices at {self.stream_info.stream.tell()}")
		_tri_indices = np.empty(dtype=np.uint8, shape=index_count)
		self.stream_info.stream.readinto(_tri_indices)
		self.tri_indices = _tri_indices.astype(np.uint32)

	@property
	def pos_chunks_address(self):
		size_of_chunk = 64
		rel_chunks_offset = self.chunks_offset * size_of_chunk
		return self.stream_info.vertex_buffer_size + self.stream_info.tris_buffer_size + rel_chunks_offset

	@staticmethod
	def pr_indices(input_list, indices, msg):
		print(f"\n{msg}")
		for i, inp in enumerate(input_list):
			if i in indices:
				print(f"{i} = {inp}")

	@property
	def offset_chunks_address(self):
		size_of_chunk = 16
		rel_chunks_offset = self.chunks_offset * size_of_chunk
		return self.stream_info.vertex_buffer_size + self.stream_info.tris_buffer_size + self.stream_info.chunk_pos_size + rel_chunks_offset

	def read_verts(self):
		self.read_chunk_infos()
		# the format differs if its flat or interleaved
		# per-vertex weights may or may not be used in a given chunk
		dt_weights = [
			("bone ids", np.ubyte, (4,)),
			("bone weights", np.ubyte, (4,)),
		]
		# 16 bytes of metadata that follows the vertices array
		dt_separate = [
			("normal_oct", np.ubyte, (2,)),
			("tangent_oct", np.ubyte, (2,)),
			("uvs", np.ushort, (2, 2)),
			("colors", np.ubyte, (1, 4))
		]
		# 32 bytes per vertex, with all data interleaved
		dt_interleaved32 = [
			("pos", np.float16, (3,)),
			("shapekey", np.float16, (3,)),  # used for lod fading
			("floats", np.float16, (4,)),
			("normal_oct", np.ubyte, (2,)),
			("tangent_oct", np.ubyte, (2,)),
			("uvs", np.ushort, (1, 2)),
			("colors", np.ubyte, (1, 4))
		]
		# 48 bytes per vertex, with all data interleaved, old style??
		dt_interleaved48 = [
			("pos", np.float16, (3,)),
			("uvs", np.ushort, (1, 2)),
			("colors", np.ubyte, (1, 4))
			# todo
		]
		# create arrays for this mesh
		self.vertices = np.empty(dtype=np.float, shape=(self.vertex_count, 3))
		self.normals = np.zeros(dtype=np.float, shape=(self.vertex_count, 3))
		self.tangents = np.zeros(dtype=np.float, shape=(self.vertex_count, 3))
		self.use_blended_weights = np.empty(self.vertex_count, np.bool)

		# check first off
		off = self.offset_chunks[0]
		if off.weights_flag.mesh_format == MeshFormat.Separate:
			self.dt = np.dtype(dt_separate)
		elif off.weights_flag.mesh_format == MeshFormat.Interleaved32:
			self.dt = np.dtype(dt_interleaved32)
		elif off.weights_flag.mesh_format == MeshFormat.Interleaved48:
			self.dt = np.dtype(dt_interleaved48)

		uv_shape = self.dt["uvs"].shape
		self.uvs = np.empty((self.vertex_count, *uv_shape), np.float32)
		colors_shape = self.dt["colors"].shape
		self.colors = np.empty((self.vertex_count, *colors_shape), np.float32)

		self.dt_weights = np.dtype(dt_weights)

		first_tris_offs = self.pos_chunks[0].tris_offset
		v_off = 0
		offs = 0
		flags = set()
		us = set()

		self.read_tris_bio()
		self.weights = []
		self.weights_info = {}

		for i, (pos, off) in enumerate(zip(self.pos_chunks, self.offset_chunks)):
			abs_tris = self.tris_start_address + pos.tris_offset
			print("\n", i, pos, off)
			print("\n", i, pos.u_1)
			print(f"chunk {i} tris at {abs_tris}, weights_flag {off.weights_flag}")

			self.stream_info.stream.seek(off.vertex_offset)
			print(f"verts {i} start {self.stream_info.stream.tell()}, count {off.vertex_count}")

			if off.weights_flag.mesh_format == MeshFormat.Separate:
				# verts packed into uint64
				off.raw_verts = np.empty(dtype=np.int64, shape=off.vertex_count)
				self.stream_info.stream.readinto(off.raw_verts)

				# check if weights chunk is present
				if off.weights_flag.has_weights:
					# read for each vertex
					off.weights = np.empty(dtype=self.dt_weights, shape=off.vertex_count)
					self.stream_info.stream.readinto(off.weights)
					for vertex_index, (bone_indices, bone_weights) in enumerate(zip(off.weights["bone ids"], off.weights["bone weights"] / 255)):
						for bone_index, weight in zip(bone_indices, bone_weights):
							if weight > 0.0:
								self.add_to_weights(bone_index, vertex_index + offs, weight)
				else:
					# use the chunk's bone index for each vertex in chunk
					for vertex_index in range(off.vertex_count):
						self.add_to_weights(off.weights_flag.bone_index, vertex_index + offs, 1.0)

				for vertex_index in range(off.vertex_count):
					self.add_to_weights("u_0", vertex_index + offs, pos.u_0 / 255)
					self.add_to_weights("u_1", vertex_index + offs, pos.u_1 / 255)
				# uv, normals etc
				print(f"meta {i} start {self.stream_info.stream.tell()}")
				off.raw_meta = np.empty(dtype=self.dt, shape=off.vertex_count)
				self.stream_info.stream.readinto(off.raw_meta)

				# store chunk's data
				unpack_int64_vector(off.raw_verts, self.vertices[offs:offs + off.vertex_count], self.use_blended_weights[offs:offs + off.vertex_count])
				scale_unpack_vectorized(self.vertices[offs:offs + off.vertex_count], off.pack_offset)
				self.uvs[offs:offs + off.vertex_count] = off.raw_meta["uvs"]
				self.colors[offs:offs + off.vertex_count] = off.raw_meta["colors"]
				self.normals[offs:offs + off.vertex_count, 0:2] = off.raw_meta["normal_oct"]
				self.tangents[offs:offs + off.vertex_count, 0:2] = off.raw_meta["tangent_oct"]

			elif off.weights_flag.mesh_format == MeshFormat.Interleaved32:
				# read the interleaved vertex array, including all extra data
				off.raw_verts = np.empty(dtype=self.dt, shape=off.vertex_count)
				self.stream_info.stream.readinto(off.raw_verts)

				# store chunk's data
				self.vertices[offs:offs + off.vertex_count] = off.raw_verts["pos"]
				self.uvs[offs:offs + off.vertex_count] = off.raw_verts["uvs"]
				self.colors[offs:offs + off.vertex_count] = off.raw_verts["colors"]
				self.normals[offs:offs + off.vertex_count, 0:2] = off.raw_verts["normal_oct"]
				self.tangents[offs:offs + off.vertex_count, 0:2] = off.raw_verts["tangent_oct"]

			elif off.weights_flag.mesh_format == MeshFormat.Interleaved48:
				logging.warning(f"Interleaved48 not supported")
				continue
			# same for all chunked meshes, regardless if flat or interleaved arrays
			flags.add(off.weights_flag)
			us.add(pos.u_1)
			self.tri_indices[pos.tris_offset - first_tris_offs:] += v_off
			v_off = off.vertex_count
			offs += off.vertex_count

		# print("weights_flags", flags, "u1s", us)
		self.oct_to_vec3(self.normals)
		self.oct_to_vec3(self.tangents)
		unpack_swizzle_vectorized(self.vertices)
		unpack_swizzle_vectorized(self.normals)
		unpack_swizzle_vectorized(self.tangents)

		unpack_ushort_vector(self.uvs)
		self.fur_length = 0.0
		# just a sanity check
		assert self.vertex_count == sum(o.vertex_count for o in self.offset_chunks)

	def oct_to_vec3(self, arr):
		# vec3 oct_to_float32x3(vec2 e) {
		# vec3 v = vec3(e.xy, 1.0 - abs(e.x) - abs(e.y));
		# if (v.z < 0) v.xy = (1.0 - abs(v.yx)) * signNotZero(v.xy);
		# return normalize(v);
		# }
		unpack_ubyte_vector(arr, normalize=False)
		arr[:, 2] = 1.0 - np.abs(arr[:, 0]) - np.abs(arr[:, 1])
		# note that advanced indexing like this creates a copy instead of a view, which makes this messy
		arr[arr[:, 2] < 0, 0:2] = ((1.0 - np.abs(arr[:, (1, 0)])) * np.sign(arr[:, :2]))[arr[:, 2] < 0]
		# normalize after conversion
		arr /= np.linalg.norm(arr, axis=1, keepdims=True)

	@staticmethod
	def ubytes_2_ushort(a, b):
		return struct.unpack("H", struct.pack("BB", int(a), int(b)))[0]

	def read_chunk_infos(self):
		# logging.debug(f"Reading {self.vertex_count} verts at {self.stream_info.stream.tell()}")
		self.stream_info.stream.seek(self.pos_chunks_address)
		self.pos_chunks = Array.from_stream(self.stream_info.stream, (self.chunks_count,), PosChunk, self.context, 0,
											None)
		print(self)
		print(f"{self.chunks_count} pos_chunks at {self.pos_chunks_address}")
		self.stream_info.stream.seek(self.offset_chunks_address)
		self.offset_chunks = Array.from_stream(self.stream_info.stream, (self.chunks_count,), OffsetChunk, self.context,
											   0, None)
		print(f"{self.chunks_count} offset_chunks at {self.offset_chunks_address}")

	@property
	def tris(self, ):
		# if self.flag.flat_arrays:
		# print(self.tri_indices)
		# create non-overlapping tris from flattened tri indices
		tris_raw = np.reshape(self.tri_indices, (len(self.tri_indices) // 3, 3))
		# reverse each tri to account for the flipped normals from mirroring in blender
		return np.flip(tris_raw, axis=-1)
		# else:
		# 	return triangulate((self.tri_indices,))
