# START_GLOBALS
import logging
import numpy as np
import struct

from generated.array import Array
from generated.formats.ms2.compound.VertChunk import VertChunk
from generated.formats.ms2.compound.TriChunk import TriChunk
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
		return self.stream_info.verts_size

	@property
	def tris_address(self):
		# just a guess here, not guaranteed to be the right starting offset
		return self.tris_start_address + self.tri_chunks[0].tris_offset

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

	def get_tri_counts(self):
		for i, tri_chunk in enumerate(self.tri_chunks[:-1]):
			next_pos = self.tri_chunks[i+1]
			tri_chunk.tri_indices_count = next_pos.tris_offset - tri_chunk.tris_offset
		last_pos = self.tri_chunks[-1]
		last_pos.tri_indices_count = (self.tris_count * 3) - last_pos.tris_offset + self.tri_chunks[0].tris_offset
		for i, tri_chunk in enumerate(self.tri_chunks):
			logging.info(f"tri_chunk {i} {last_pos.tri_indices_count} tris")

	@property
	def tri_chunks_address(self):
		size_of_chunk = 64
		rel_chunks_offset = self.chunks_offset * size_of_chunk
		return self.stream_info.verts_size + self.stream_info.tris_size + rel_chunks_offset

	@staticmethod
	def pr_indices(input_list, indices, msg):
		print(f"\n{msg}")
		for i, inp in enumerate(input_list):
			if i in indices:
				print(f"{i} = {inp}")

	@property
	def vert_chunks_address(self):
		size_of_chunk = 16
		rel_chunks_offset = self.chunks_offset * size_of_chunk
		return self.stream_info.verts_size + self.stream_info.tris_size + self.stream_info.tri_chunks_size + rel_chunks_offset

	def read_verts(self):
		self.read_chunk_infos()
		self.get_tri_counts()
		# check first vert_chunk
		vert_chunk = self.vert_chunks[0]
		self.get_dtypes(vert_chunk.weights_flag.mesh_format)

		# create arrays for this mesh
		self.vertices = np.empty(dtype=np.float, shape=(self.vertex_count, 3))
		self.normals = np.zeros(dtype=np.float, shape=(self.vertex_count, 3))
		self.tangents = np.zeros(dtype=np.float, shape=(self.vertex_count, 3))
		self.use_blended_weights = np.empty(self.vertex_count, np.bool)
		uv_shape = self.dt["uvs"].shape
		self.uvs = np.empty((self.vertex_count, *uv_shape), np.float32)
		# colors_shape = self.dt["colors"].shape
		colors_shape = (1, 4)
		self.colors = np.empty((self.vertex_count, *colors_shape), np.float32)

		first_tris_offs = self.tri_chunks[0].tris_offset
		v_off = 0
		offs = 0
		flags = set()
		us = set()

		self.read_tris_bio()
		self.weights_info = {}
		self.face_maps = {}
		self.bones_sets = []
		for i, (tri_chunk, vert_chunk) in enumerate(zip(self.tri_chunks, self.vert_chunks)):
			abs_tris = self.tris_start_address + tri_chunk.tris_offset
			# bones_per_chunk = set()
			logging.debug(f"{i}, {tri_chunk}, {vert_chunk}")
			# these sometimes correspond but not always
			logging.info(f"{i}, {tri_chunk.u_0}, {vert_chunk.weights_flag.mesh_format}")
			# print(i, tri_chunk.u_1)
			logging.info(f"chunk {i} tris at {abs_tris}, weights_flag {vert_chunk.weights_flag}")

			self.stream_info.stream.seek(vert_chunk.vertex_offset)
			logging.info(f"verts {i} start {self.stream_info.stream.tell()}, count {vert_chunk.vertex_count}")

			vert_chunk.verts = None
			vert_chunk.weights = None
			vert_chunk.meta = None
			if vert_chunk.weights_flag.mesh_format == MeshFormat.Separate:
				# verts packed into uint64
				vert_chunk.verts = np.empty(dtype=np.int64, shape=vert_chunk.vertex_count)
				self.stream_info.stream.readinto(vert_chunk.verts)

				# check if weights chunk is present
				if vert_chunk.weights_flag.has_weights:
					# read for each vertex
					vert_chunk.weights = np.empty(dtype=self.dt_weights, shape=vert_chunk.vertex_count)
					self.stream_info.stream.readinto(vert_chunk.weights)
					for vertex_index, (bone_indices, bone_weights) in enumerate(zip(vert_chunk.weights["bone ids"], vert_chunk.weights["bone weights"] / 255)):
						for bone_index, weight in zip(bone_indices, bone_weights):
							if weight > 0.0:
								self.add_to_weights(bone_index, vertex_index + offs, weight)
					# 			bones_per_chunk.add(bone_index)
					# logging.info(f"Length set {len(bones_per_chunk)}")
				else:
					# use the chunk's bone index for each vertex in chunk
					for vertex_index in range(vert_chunk.vertex_count):
						self.add_to_weights(vert_chunk.weights_flag.bone_index, vertex_index + offs, 1.0)
					# bones_per_chunk.add(vert_chunk.weights_flag.bone_index)

				for vertex_index in range(vert_chunk.vertex_count):
					self.add_to_weights("u_0", vertex_index + offs, tri_chunk.u_0 / 255)
					self.add_to_weights("u_1", vertex_index + offs, tri_chunk.u_1 / 255)
				# uv, normals etc
				logging.info(f"meta {i} start {self.stream_info.stream.tell()}")
				vert_chunk.meta = np.empty(dtype=self.dt, shape=vert_chunk.vertex_count)
				self.stream_info.stream.readinto(vert_chunk.meta)
				# store tri_chunk
				unpack_int64_vector(vert_chunk.verts, self.vertices[offs:offs + vert_chunk.vertex_count], self.use_blended_weights[offs:offs + vert_chunk.vertex_count])
				scale_unpack_vectorized(self.vertices[offs:offs + vert_chunk.vertex_count], vert_chunk.pack_offset)

			elif vert_chunk.weights_flag.mesh_format in (MeshFormat.Interleaved32, MeshFormat.Interleaved48):
				# interleaved vertex array, meta includes all extra data
				vert_chunk.meta = np.empty(dtype=self.dt, shape=vert_chunk.vertex_count)
				self.stream_info.stream.readinto(vert_chunk.meta)
				# store tri_chunk
				self.vertices[offs:offs + vert_chunk.vertex_count] = vert_chunk.meta["tri_chunk"]
			else:
				raise AttributeError(f"Unsupported weights_flag.mesh_format {vert_chunk.weights_flag.mesh_format}")
			# store chunk's meta data
			self.uvs[offs:offs + vert_chunk.vertex_count] = vert_chunk.meta["uvs"]
			self.colors[offs:offs + vert_chunk.vertex_count] = vert_chunk.meta["colors"]
			self.normals[offs:offs + vert_chunk.vertex_count, 0:2] = vert_chunk.meta["normal_oct"]
			self.tangents[offs:offs + vert_chunk.vertex_count, 0:2] = vert_chunk.meta["tangent_oct"]

			# self.bones_sets.append((vert_chunk.vertex_count, bones_per_chunk))
			# same for all chunked meshes, regardless if flat or interleaved arrays
			flags.add(vert_chunk.weights_flag)
			us.add(tri_chunk.u_1)
			tris_start = tri_chunk.tris_offset - first_tris_offs
			self.tri_indices[tris_start:] += v_off

			# prep face maps
			fmt_str = str(vert_chunk.weights_flag.mesh_format).split(".")[1]
			_weights = f"_weights" if vert_chunk.weights_flag.has_weights else ""
			id_str = f"{fmt_str}_{i:03}{_weights}"
			self.face_maps[id_str] = list(range(tris_start // 3, (tris_start+tri_chunk.tri_indices_count) // 3))

			v_off = vert_chunk.vertex_count
			offs += vert_chunk.vertex_count
		# print(self.face_maps)
		# logging.info(self.bones_sets)
		# print("weights_flags", flags, "u1s", us)
		self.oct_to_vec3(self.normals)
		self.oct_to_vec3(self.tangents)
		unpack_swizzle_vectorized(self.vertices)
		unpack_swizzle_vectorized(self.normals)
		unpack_swizzle_vectorized(self.tangents)
		# currently, known uses of Interleaved48 use the other unpacking
		unpack_ushort_vector(self.uvs)
		self.fur_length = 0.0
		# just a sanity check
		assert self.vertex_count == sum(o.vertex_count for o in self.vert_chunks)

	def get_dtypes(self, mesh_format):
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
			("tri_chunk", np.float16, (3,)),
			("shapekey", np.float16, (3,)),  # used for lod fading
			("floats", np.float16, (4,)),
			("normal_oct", np.ubyte, (2,)),
			("tangent_oct", np.ubyte, (2,)),
			("uvs", np.ushort, (1, 2)),
			("colors", np.ubyte, (1, 4))
		]
		# 48 bytes per vertex, with all data interleaved, totally different from older 48 bytes vert
		dt_interleaved48 = [
			("tri_chunk", np.float16, (3,)),
			("one", np.ubyte),  # not sure
			("zero", np.ubyte),  # may be bone index
			("normal_oct", np.ubyte, (2,)),
			("tangent_oct", np.ubyte, (2,)),
			("colors", np.ubyte, (1, 4)),  # zero, may be colors
			("uvs", np.ushort, (8, 2)),
		]
		if mesh_format == MeshFormat.Separate:
			self.dt = np.dtype(dt_separate)
		elif mesh_format == MeshFormat.Interleaved32:
			self.dt = np.dtype(dt_interleaved32)
		elif mesh_format == MeshFormat.Interleaved48:
			self.dt = np.dtype(dt_interleaved48)
		self.dt_weights = np.dtype(dt_weights)

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

	def read_chunk_infos(self):
		# logging.debug(f"Reading {self.vertex_count} verts at {self.stream_info.stream.tell()}")
		self.stream_info.stream.seek(self.tri_chunks_address)
		self.tri_chunks = Array.from_stream(self.stream_info.stream, (self.chunks_count,), TriChunk, self.context, 0,
											None)
		logging.debug(self)
		logging.debug(f"{self.chunks_count} tri_chunks at {self.tri_chunks_address}")
		self.stream_info.stream.seek(self.vert_chunks_address)
		self.vert_chunks = Array.from_stream(self.stream_info.stream, (self.chunks_count,), VertChunk, self.context,
											   0, None)
		logging.debug(f"{self.chunks_count} vert_chunks at {self.vert_chunks_address}")

	def set_chunks(self, verts):
		# correct bounds for the chunk, do after swizzling
		# tri_chunk.bounds_min.set(np.min(self.vertices[offs:offs + vert_chunk.vertex_count], axis=0))
		# tri_chunk.bounds_max.set(np.max(self.vertices[offs:offs + vert_chunk.vertex_count], axis=0))
		# logging.info(f"{bounds_min} {tri_chunk.bounds_min}")
		# logging.info(f"{bounds_max} {tri_chunk.bounds_max}")
		# logging.info(f"tri_chunk.loc {tri_chunk.loc} {np.mean((bounds_min, bounds_max), axis=0)} {np.mean(self.vertices[offs:offs + vert_chunk.vertex_count], axis=0)}")
		pass

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

	def write_data(self):
		# todo - rewrite to save tris and verts per chunk, and update the offsets each time
		# write vertices
		self.vertex_count = len(self.verts_data)
		for vert_chunk, tri_chunk in zip(self.vert_chunks, self.tri_chunks):
			vert_chunk.vertex_offset = self.stream_info.verts.tell()
			vert_chunk.vertex_count = len(vert_chunk.meta)
			if vert_chunk.verts is not None:
				self.stream_info.verts.write(vert_chunk.verts.tobytes())
			if vert_chunk.weights is not None:
				self.stream_info.verts.write(vert_chunk.weights.tobytes())
			if vert_chunk.meta is not None:
				self.stream_info.verts.write(vert_chunk.meta.tobytes())
		# write tris
		self.tris_count = (len(self.tri_indices) // 3)  # * self.shell_count
		for tri_chunk in self.tri_chunks:
			pass
			# write to the stream_info that has been assigned to mesh
			# tri_bytes = self.tri_indices.tobytes()
			# extend tri array according to shell count
			# logging.debug(f"Writing {self.shell_count} shells of {len(self.tri_indices)} triangles")
			# for shell in range(self.shell_count):
			# self.stream_info.tris.write(tri_bytes)

		# write the chunks
		self.chunks_offset = self.stream_info.tri_chunks.tell() // 64
		self.chunks_count = len(self.tri_chunks)
		Array.to_stream(self.stream_info.tri_chunks, self.tri_chunks, (self.chunks_count,), TriChunk, self.context, 0, None)
		Array.to_stream(self.stream_info.vert_chunks, self.vert_chunks, (self.chunks_count,), VertChunk, self.context, 0, None)
