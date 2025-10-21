# START_GLOBALS
import logging

from generated.array import Array
from generated.formats.ms2.structs.MeshData import MeshData
from generated.formats.ms2.structs.VertChunk import VertChunk
from generated.formats.ms2.structs.TriChunk import TriChunk
from generated.formats.ms2.structs.packing_utils import *
from generated.formats.ms2.enums.MeshFormat import MeshFormat


# END_GLOBALS


class ChunkedMesh(MeshData):

	# START_CLASS

	# @property
	def get_stream_index(self):
		# logging.debug(f"Using stream {self.stream_info.pool_index}")
		return self.stream_info.pool_index

	def read_tris(self):
		pass

	@staticmethod
	def pr_indices(input_list, indices, msg):
		print(f"\n{msg}")
		for i, inp in enumerate(input_list):
			if i in indices:
				print(f"{i} = {inp}")

	@property
	def tri_chunks_address(self):
		size_of_chunk = 64
		return self.chunks_offset * size_of_chunk

	@property
	def vert_chunks_address(self):
		size_of_chunk = 16
		return self.chunks_offset * size_of_chunk

	def read_verts(self):
		# logging.debug(self)
		self.read_chunk_infos()
		# check first vert_chunk
		vert_chunk = self.vert_chunks[0]
		self.mesh_format = vert_chunk.weights_flag.mesh_format
		if self.context.version > 53:
			self.material_effects = vert_chunk.weights_flag.material_effects
		self.update_dtype()
		self.init_arrays()

		first_tris_offs = self.tri_chunks[0].tris_offset
		offs = 0

		# tris reading has changed since v54
		self.buffer_info.tris.seek(self.tri_chunks[0].tris_offset)
		index_count = self.tris_count * 3  # // self.shell_count
		# logging.info(f"Reading {index_count} indices at {self.buffer_info.tris.tell()}")
		_tri_indices = np.empty(dtype=np.uint8, shape=index_count)
		self.buffer_info.tris.readinto(_tri_indices)
		self.tri_indices = _tri_indices.astype(np.uint32)

		self.weights_info = {}
		self.face_maps = {}
		self.bones_sets = []
		mesh_formats = set()
		# unks = set()
		for i, (tri_chunk, vert_chunk) in enumerate(zip(self.tri_chunks, self.vert_chunks)):
			# logging.debug(f"{i}, {tri_chunk}, {vert_chunk}")
			# logging.debug(vert_chunk.weights_flag)
			self.buffer_info.verts.seek(vert_chunk.vertex_offset)
			# logging.debug(f"tri_chunk {i} {tri_chunk.tris_offset} {tri_chunk.tris_index} {tri_chunk.tris_count} {tri_chunk.value_min} tris")
			# logging.debug(f"packed_verts {i} start {self.buffer_info.verts.tell()}, count {vert_chunk.vertex_count}")

			v_slice = np.s_[offs: offs + vert_chunk.vertex_count]
			self.init_vert_chunk_arrays(v_slice, vert_chunk)

			index_count = tri_chunk.tris_count * 3
			if self.context.version < 54:
				tris_start = tri_chunk.tris_offset - first_tris_offs
				tri_chunk.tri_indices = self.tri_indices[tris_start: tris_start+index_count]
				tri_chunk.tri_indices += offs
			else:
				tri_chunk.tri_indices = self.tri_indices[tri_chunk.tris_index*3: tri_chunk.tris_index*3+index_count]
				# logging.debug(tri_chunk.tri_indices)
				tri_chunk.tri_indices += tri_chunk.value_min

			mesh_formats.add(vert_chunk.weights_flag.mesh_format)
			try:
				if vert_chunk.weights_flag.mesh_format in (MeshFormat.SEPARATE,):
					self.buffer_info.verts.readinto(vert_chunk.packed_verts)
					# decode and store position
					unpack_int64_vector(vert_chunk.packed_verts, vert_chunk.vertices, vert_chunk.negate_bitangents)
					scale_unpack_vectorized(vert_chunk.vertices, vert_chunk.pack_base)

					self.read_weights(vert_chunk, offs)
					# read uv, normals etc
					# logging.info(f"meta {i} start {self.buffer_info.verts.tell()}")
					self.buffer_info.verts.readinto(vert_chunk.meta)

				elif vert_chunk.weights_flag.mesh_format in (MeshFormat.SPEEDTREE_32, MeshFormat.IMPOSTOR_48):
					# interleaved vertex array, meta includes all extra data
					self.buffer_info.verts.readinto(vert_chunk.meta)
					# store position
					vert_chunk.vertices[:] = vert_chunk.meta["pos"]
					self.read_weights(vert_chunk, offs)
				else:
					raise AttributeError(f"Unsupported weights_flag.mesh_format {vert_chunk.weights_flag.mesh_format}")
				# store chunk's meta data in mesh's array
				vert_chunk.uvs[:] = vert_chunk.meta["uvs"]
				if self.is_speedtree:
					vert_chunk.normals_custom[:] = vert_chunk.meta["normal_custom"]
					vert_chunk.wind[:] = vert_chunk.meta["wind"]
				else:
					vert_chunk.colors[:] = vert_chunk.meta["colors"]
				vert_chunk.normals[:, :2] = vert_chunk.meta["normal_oct"]
				vert_chunk.tangents[:, :2] = vert_chunk.meta["tangent_oct"]

				if vert_chunk.weights_flag.mesh_format in (MeshFormat.SPEEDTREE_32,):
					vert_chunk.lod_keys[:] = vert_chunk.meta["lod_key"]
					vert_chunk.center_keys[:] = vert_chunk.meta["center_key"]
					vert_chunk.whatever[:] = vert_chunk.meta["whatever"]
			except:
				logging.exception(f"Chunk {i} failed")
			# create absolute vertex indices for the total mesh
			offs += vert_chunk.vertex_count
			# logging.debug(vert_chunk.vertices)
			# logging.debug(vert_chunk.meta)

			# logging.info(f"Vert {i} rot {tri_chunk.rot}")
			# logging.info(f"Vert {i} loc {tri_chunk.loc}")
			# # logging.info(f"Vert {i} min {tri_chunk.bounds_min}")
			# logging.info(f"Vert {i} min {tri_chunk.bounds}")
			# logging.info(f"Vert {i} min {np.min(vert_chunk.vertices, axis=0)} max {np.max(vert_chunk.vertices, axis=0)} mean {np.mean(vert_chunk.vertices, axis=0)}")
		# logging.debug(self.tri_indices)
		# since malta dlc, one mesh can have several mesh formats
		# assert len(mesh_formats) == 1
		# logging.info(self.bones_sets)
		# max_verts = max(vert_chunk.vertex_count for vert_chunk in self.vert_chunks)
		# logging.debug(f"max_verts {max_verts}")

		oct_to_vec3(self.normals)
		oct_to_vec3(self.tangents)
		unpack_swizzle_vectorized(self.vertices)
		unpack_swizzle_vectorized(self.lod_keys)
		unpack_swizzle_vectorized(self.center_keys)
		unpack_swizzle_vectorized(self.normals)
		unpack_swizzle_vectorized(self.tangents)
		unpack_ubyte_color(self.colors)
		unpack_ubyte_color(self.wind)
		unpack_ubyte_vector(self.normals_custom)
		unpack_swizzle_vectorized(self.normals_custom)
		# currently, known uses of Impostor48 use impostor uv atlas
		if vert_chunk.weights_flag.mesh_format == MeshFormat.IMPOSTOR_48:
			unpack_ushort_vector_impostor(self.uvs)
		else:
			unpack_ushort_vector(self.uvs)
		self.fur_length = 0.0
		# just a sanity check
		assert self.vertex_count == sum(o.vertex_count for o in self.vert_chunks)
		if self.is_speedtree:
			for vertex_index, weight in enumerate(self.wind):
				self.add_to_weights("wind", vertex_index, weight)
			if vert_chunk.weights_flag.mesh_format == MeshFormat.SPEEDTREE_32:
				self.whatever_range = np.max(self.whatever)
				if self.whatever_range > 0.0:
					self.whatever /= self.whatever_range
				# print(self.whatever)
				for vertex_index, weight in enumerate(self.whatever):
					self.add_to_weights("whatever", vertex_index, weight)
		# for debugging
		# for vertex_index, res in enumerate(self.negate_bitangents):
		# 	self.add_to_weights(f"negate_bitangents", vertex_index, res)
		# print(unks)

	def init_vert_chunk_arrays(self, v_slice, vert_chunk):
		vert_chunk.packed_verts = None
		vert_chunk.weights = None
		vert_chunk.meta = None
		# views into main array
		vert_chunk.vertices = self.vertices[v_slice]
		vert_chunk.lod_keys = self.lod_keys[v_slice]
		vert_chunk.center_keys = self.center_keys[v_slice]
		vert_chunk.negate_bitangents = self.negate_bitangents[v_slice]
		vert_chunk.colors = self.colors[v_slice]
		vert_chunk.uvs = self.uvs[v_slice]
		vert_chunk.normals_custom = self.normals_custom[v_slice]
		vert_chunk.wind = self.wind[v_slice]
		vert_chunk.normals = self.normals[v_slice]
		vert_chunk.tangents = self.tangents[v_slice]
		vert_chunk.whatever = self.whatever[v_slice]
		vert_chunk.bone_indices = self.bone_indices[v_slice]
		vert_chunk.bone_weights = self.bone_weights[v_slice]
		chunk_fmt = vert_chunk.weights_flag.mesh_format
		if chunk_fmt in (MeshFormat.SEPARATE,):
			vert_chunk.packed_verts = np.zeros(dtype=np.int64, shape=vert_chunk.vertex_count)
			vert_chunk.weights = np.zeros(dtype=self.dt_weights, shape=vert_chunk.vertex_count)
			vert_chunk.meta = np.zeros(dtype=self.dts[chunk_fmt], shape=vert_chunk.vertex_count)
		elif chunk_fmt in (MeshFormat.SPEEDTREE_32, MeshFormat.IMPOSTOR_48):
			# interleaved vertex array, meta includes all extra data
			vert_chunk.meta = np.zeros(dtype=self.dts[chunk_fmt], shape=vert_chunk.vertex_count)

	@property
	def dt(self):
		return self.dts[self.mesh_format]

	def read_weights(self, vert_chunk, offs):
		# check if weights chunk is present
		if vert_chunk.weights_flag.has_weights:
			# read for each vertex
			if self.context.version >= 52:
				# not sure if uint or int, but seems to work!
				# vert_chunk.weights may have to be cast to uint16 because of the new 10 bit precision
				# however, there are no meshes that make use of the extra precision as of 2022-12
				vert_chunk.packed_weights = np.zeros(dtype=np.uint64, shape=vert_chunk.vertex_count)
				self.buffer_info.verts.readinto(vert_chunk.packed_weights)
				# logging.info(vert_chunk.packed_weights)
				unpack_int64_weights(vert_chunk.packed_weights, vert_chunk.weights)
				# logging.info(vert_chunk.weights)
			else:
				self.buffer_info.verts.readinto(vert_chunk.weights)
			vert_chunk.bone_indices[:] = vert_chunk.weights["bone ids"]
			vert_chunk.bone_weights[:] = vert_chunk.weights["bone weights"] / 255
		else:
			# use the chunk's bone index for each vertex in chunk
			vert_chunk.bone_indices[:] = (vert_chunk.weights_flag.bone_index, -1, -1, -1)
			vert_chunk.bone_weights[:] = (1.0, 0.0, 0.0, 0.0)
		# if vert_chunk.weights_flag.mesh_format == MeshFormat.SPEEDTREE_32:
		# 	for vertex_index in range(vert_chunk.vertex_count):
		# 		self.add_to_weights("weight", vertex_index + offs, vert_chunk.meta[vertex_index]["colors"][3] / 255)

	def update_dtype(self):
		# prepare descriptions of the dtypes
		_normal_tangent_oct = (("normal_oct", np.ubyte, (2,)), ("tangent_oct", np.ubyte, (2,)))
		# per-vertex weights may or may not be used in a given chunk
		dt_weights = [
			("bone ids", np.ubyte, (4,)),
			("bone weights", np.ubyte, (4,)),
		]
		# 16 bytes of metadata that follows the vertices array
		dt_separate = [
			*_normal_tangent_oct,
			("uvs", np.ushort, (2, 2)),
			("colors", np.ubyte, 4)
		]
		# 32 bytes per vertex, with all data interleaved
		dt_speedtree32 = [
			("pos", np.float16, (3,)),
			("lod_key", np.float16, (3,)),
			# nan (FF 7F) if unused, used on JWE2 mango, no apparent flag in tri or vert chunk or mesh
			("center_key", np.float16, 3),
			("whatever", np.ushort),  # 00 00 or 01 00 in calamites
			*_normal_tangent_oct,  # standard vertex / face normal
			("uvs", np.ushort, (1, 2)),
			("normal_custom", np.ubyte, 3),  # edited normal
			("wind", np.ubyte),
		]
		# 48 bytes per vertex, with all data interleaved, totally different from older 48 bytes vert
		dt_impostor48 = [
			("pos", np.float16, (3,)),
			("one", np.ubyte),  # not sure
			("zero", np.ubyte),  # may be bone index
			*_normal_tangent_oct,  # standard vertex / face normal
			("normal_custom", np.ubyte, 3),  # edited normal
			("wind", np.ubyte),
			("uvs", np.ushort, (8, 2)),
		]
		self.dts = {}
		self.dts[MeshFormat.SEPARATE] = np.dtype(dt_separate)
		self.dts[MeshFormat.SPEEDTREE_32] = np.dtype(dt_speedtree32)
		self.dts[MeshFormat.IMPOSTOR_48] = np.dtype(dt_impostor48)
		self.dt_weights = np.dtype(dt_weights)

	def read_chunk_infos(self):
		self.buffer_info.tri_chunks.seek(self.tri_chunks_address)
		self.tri_chunks = Array.from_stream(self.buffer_info.tri_chunks, self.context, 0, None, (self.chunks_count,), TriChunk)
		# logging.debug(f"{self.chunks_count} tri_chunks at {self.tri_chunks_address}")
		self.buffer_info.vert_chunks.seek(self.vert_chunks_address)
		self.vert_chunks = Array.from_stream(self.buffer_info.vert_chunks, self.context, 0, None, (self.chunks_count,), VertChunk)
		# logging.debug(f"{self.chunks_count} vert_chunks at {self.vert_chunks_address}")

	@property
	def tris(self, ):
		# create non-overlapping tris from flattened tri indices
		tris_raw = np.reshape(self.tri_indices, (len(self.tri_indices) // 3, 3))
		# reverse each tri to account for the flipped normals from mirroring in blender
		return np.flip(tris_raw, axis=-1)

	@tris.setter
	def tris(self, list_of_b_tris):
		# create chunks for each segment in tris
		self.tris_count = sum(len(tup[1]) for tup in list_of_b_tris)
		self.vert_chunks = Array(self.context, 0, None, (len(list_of_b_tris),), VertChunk,)
		self.tri_chunks = Array(self.context, 0, None, (len(list_of_b_tris),), TriChunk)
		for vert_chunk, tri_chunk, (b_bone_id, b_tris) in zip(self.vert_chunks, self.tri_chunks, list_of_b_tris):
			# logging.info(b_tris)
			# cast to uint16
			raw_tris = np.array(b_tris, dtype=np.uint8)
			# reverse tris
			raw_tris = np.flip(raw_tris, axis=-1)
			# flatten array
			tri_chunk.tri_indices = np.reshape(raw_tris, len(raw_tris) * 3)
			tri_chunk.tris_count = len(b_tris)
			tri_chunk.shell_index = self.shell_index
			tri_chunk.shell_count = self.shell_count
			# get the vertex count from the tri indices
			vert_chunk.vertex_count = np.max(tri_chunk.tri_indices) + 1
			vert_chunk.weights_flag.mesh_format = self.mesh_format
			if self.context.version > 53:
				vert_chunk.weights_flag.material_effects = self.material_effects
			if b_bone_id == -1:
				# dynamic weights, extra array
				vert_chunk.weights_flag.has_weights = True
			elif b_bone_id == -2:
				# no bone info, no weights
				vert_chunk.weights_flag.has_weights = False
				vert_chunk.weights_flag.bone_index = 0
			else:
				# static weights
				vert_chunk.weights_flag.has_weights = False
				vert_chunk.weights_flag.bone_index = b_bone_id
			vert_chunk.pack_base = self.pack_base
			vert_chunk.precision = self.precision

	@property
	def is_speedtree(self):
		return self.mesh_format in (MeshFormat.SPEEDTREE_32, MeshFormat.IMPOSTOR_48)

	def resize_vertices(self, model_info, fac):
		self.vertices *= fac
		pack_swizzle_vectorized(self.vertices)
		for vert_chunk, tri_chunk in zip(self.vert_chunks, self.tri_chunks):
			vert_chunk.pack_base = model_info.pack_base
			vert_chunk.precision = model_info.precision
			self.update_chunk_bounds(tri_chunk, vert_chunk)
			# pack the verts
			assert vert_chunk.weights_flag.mesh_format in (MeshFormat.SEPARATE,)
			scale_pack_vectorized(vert_chunk.vertices, vert_chunk.pack_base)
			pack_int64_vector(vert_chunk.packed_verts, vert_chunk.vertices.astype(np.int64),
							  vert_chunk.negate_bitangents)

	def pack_verts(self):
		"""Repack flat lists into verts_data"""
		# prepare data in whole mesh array for assignment
		pack_swizzle_vectorized(self.normals_custom)
		pack_ubyte_vector(self.normals_custom)
		pack_ubyte_color(self.colors)
		pack_ubyte_color(self.wind)
		pack_swizzle_vectorized(self.vertices)
		pack_swizzle_vectorized(self.lod_keys)
		pack_swizzle_vectorized(self.center_keys)
		pack_swizzle_vectorized(self.normals)
		pack_swizzle_vectorized(self.tangents)
		vec3_to_oct(self.normals)
		vec3_to_oct(self.tangents)
		offs = 0
		for vert_chunk, tri_chunk in zip(self.vert_chunks, self.tri_chunks):
			# (re)generate views into mesh vertex arrays for vert_chunk according to tri_chunk
			v_slice = np.s_[offs: offs + vert_chunk.vertex_count]
			self.init_vert_chunk_arrays(v_slice, vert_chunk)
			tri_chunk.value_min = offs
			offs += vert_chunk.vertex_count
			self.update_chunk_bounds(tri_chunk, vert_chunk)

			# pack the verts
			if vert_chunk.weights_flag.mesh_format in (MeshFormat.SEPARATE,):
				scale_pack_vectorized(vert_chunk.vertices, vert_chunk.pack_base)
				pack_int64_vector(vert_chunk.packed_verts, vert_chunk.vertices.astype(np.int64), vert_chunk.negate_bitangents)
				if vert_chunk.weights_flag.has_weights:
					for vert, weight in zip(vert_chunk.weights, self.weights[v_slice]):
						vert["bone ids"], vert["bone weights"] = self.unpack_weights_list(weight)
			elif vert_chunk.weights_flag.mesh_format in (MeshFormat.SPEEDTREE_32, MeshFormat.IMPOSTOR_48):
				vert_chunk.meta["pos"] = vert_chunk.vertices
				vert_chunk.weights_flag.has_weights = False
			else:
				raise AttributeError(f"Unsupported mesh_format {self.mesh_format}")
			# store chunk's meta data
			if vert_chunk.weights_flag.mesh_format == MeshFormat.SPEEDTREE_32:
				vert_chunk.meta["lod_key"] = vert_chunk.lod_keys
				vert_chunk.meta["center_key"] = vert_chunk.center_keys
				vert_chunk.meta["whatever"] = vert_chunk.whatever
			# currently, known uses of Impostor48 use impostor uv atlas
			if vert_chunk.weights_flag.mesh_format == MeshFormat.IMPOSTOR_48:
				pack_ushort_vector_impostor(vert_chunk.uvs)
			else:
				pack_ushort_vector(vert_chunk.uvs)
			# assign the right views from the main arrays back to the chunks
			if self.is_speedtree:
				vert_chunk.meta["normal_custom"] = vert_chunk.normals_custom
				vert_chunk.meta["wind"] = vert_chunk.wind
			else:
				vert_chunk.meta["colors"] = vert_chunk.colors
			vert_chunk.meta["uvs"] = vert_chunk.uvs
			vert_chunk.meta["normal_oct"] = vert_chunk.normals[:, :2]
			vert_chunk.meta["tangent_oct"] = vert_chunk.tangents[:, :2]
			# print("after", vert_chunk.meta)

	def update_chunk_bounds(self, tri_chunk, vert_chunk):
		"""Updates the bounding information on each tri chunk according to its associated vertices"""
		# we have the views, so set bounds for the chunk (after swizzling)
		if self.context.version < 54:
			tri_chunk.bounds_min.set(np.min(vert_chunk.vertices, axis=0))
			tri_chunk.bounds_max.set(np.max(vert_chunk.vertices, axis=0))
		else:
			tri_chunk.bounds[:, 1] = np.min(vert_chunk.vertices, axis=0)
			tri_chunk.bounds[:, 0] = np.max(vert_chunk.vertices, axis=0)
		# for alpha blended shells
		if self.flag == 13:
			# set the loc value as center of gravity, or center of bounds?
			tri_chunk.loc.set(np.mean(vert_chunk.vertices, axis=0))
		# rot is probably related to the normals of the chunk

	def write_data(self):
		# save tris and verts per chunk, and update the offsets each time
		# write to the buffer_info that has been assigned to mesh
		self.vertex_count = len(self.vertices)
		# this may not be needed, but for now is used in update_buffer_2_bytes
		self.tri_index_count = len(self.tri_indices)
		tris_index = 0
		for vert_chunk, tri_chunk in zip(self.vert_chunks, self.tri_chunks):
			# write vertices
			vert_chunk.vertex_offset = self.buffer_info.verts.tell()
			vert_chunk.vertex_count = len(vert_chunk.meta)
			# write the arrays if they exist, in this order
			if vert_chunk.weights_flag.mesh_format in (MeshFormat.SEPARATE,):
				self.buffer_info.verts.write(vert_chunk.packed_verts.tobytes())
				if vert_chunk.weights_flag.has_weights:
					if self.context.version >= 52:
						vert_chunk.packed_weights = np.zeros(dtype=np.uint64, shape=vert_chunk.vertex_count)
						pack_int64_weights(vert_chunk.packed_weights, vert_chunk.weights)
						self.buffer_info.verts.write(vert_chunk.packed_weights.tobytes())
					else:
						self.buffer_info.verts.write(vert_chunk.weights.tobytes())
			self.buffer_info.verts.write(vert_chunk.meta.tobytes())

			tri_chunk.tris_offset = self.buffer_info.tris.tell()
			tri_chunk.tris_index = tris_index
			tris_index += tri_chunk.tris_count
			# PC2 can re-use chunks, which can throw off the indexing and boost the vert indices in the tris
			# get tri indices of this chunk
			_tri_chunk_tri_indices = np.copy(tri_chunk.tri_indices)
			# chunking already produces the vert indices as 0-index-based per chunk, so don't do it again
			# tri_chunk.value_min = np.min(_tri_chunk_tri_indices)
			# tri_chunk.value_min is set during pack_verts
			# however when directly saving original chunks, reset back so that the tris offset from 0
			_tri_chunk_tri_indices -= np.min(_tri_chunk_tri_indices)
			tri_bytes = _tri_chunk_tri_indices.astype(np.uint8).tobytes()
			# extend tri array according to shell count
			# logging.debug(f"Writing {self.shell_count} shells of {len(self.tri_indices)} triangles")
			# for shell in range(self.shell_count):
			self.buffer_info.tris.write(tri_bytes)

		# write the chunks
		self.chunks_offset = self.buffer_info.tri_chunks.tell() // 64
		self.chunks_count = len(self.tri_chunks)
		Array.to_stream(self.tri_chunks, self.buffer_info.tri_chunks, self.context, dtype=TriChunk)
		Array.to_stream(self.vert_chunks, self.buffer_info.vert_chunks, self.context, dtype=VertChunk)
