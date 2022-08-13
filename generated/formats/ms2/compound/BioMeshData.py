
import logging
from generated.array import Array
from generated.formats.ms2.compound.VertChunk import VertChunk
from generated.formats.ms2.compound.TriChunk import TriChunk
from generated.formats.ms2.compound.packing_utils import *
from generated.formats.ms2.enum.MeshFormat import MeshFormat
from plugin.utils.tristrip import triangulate


import numpy
from generated.array import Array
from generated.formats.base.basic import Float
from generated.formats.base.basic import Uint
from generated.formats.base.basic import Uint64
from generated.formats.ms2.bitfield.BioModelFlag import BioModelFlag
from generated.formats.ms2.compound.MeshData import MeshData


class BioMeshData(MeshData):

	"""
	JWE2 after Biosyn update - 48 bytes incl. inheritance
	"""

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# start index into list of verts / tris chunks
		self.chunks_offset = 0

		# count of verts / tris chunks
		self.chunks_count = 0
		self.tris_count = 0

		# num verts in mesh
		self.vertex_count = 0

		# unk, may be used in other models
		self.zero_1 = 0

		# power of 2 increasing with lod index
		self.poweroftwo = 0

		# some floats, purpose unknown
		self.unk_floats = 0

		# seen 1 or 13
		self.flag = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		print(f'set_defaults {self.__class__.__name__}')
		self.chunks_offset = 0
		self.chunks_count = 0
		self.tris_count = 0
		self.vertex_count = 0
		self.zero_1 = 0
		self.poweroftwo = 0
		self.unk_floats = numpy.zeros((2,), dtype=numpy.dtype('float32'))
		self.flag = BioModelFlag(self.context, 0, None)

	def read(self, stream):
		self.io_start = stream.tell()
		self.read_fields(stream, self)
		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()
		self.write_fields(stream, self)
		self.io_size = stream.tell() - self.io_start

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.chunks_offset = stream.read_uint()
		instance.chunks_count = stream.read_uint()
		instance.tris_count = stream.read_uint()
		instance.vertex_count = stream.read_uint()
		instance.zero_1 = stream.read_uint64()
		instance.poweroftwo = stream.read_uint()
		instance.unk_floats = stream.read_floats((2,))
		instance.flag = BioModelFlag.from_stream(stream, instance.context, 0, None)

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		stream.write_uint(instance.chunks_offset)
		stream.write_uint(instance.chunks_count)
		stream.write_uint(instance.tris_count)
		stream.write_uint(instance.vertex_count)
		stream.write_uint64(instance.zero_1)
		stream.write_uint(instance.poweroftwo)
		stream.write_floats(instance.unk_floats)
		BioModelFlag.to_stream(stream, instance.flag)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		super()._get_filtered_attribute_list(instance)
		yield ('chunks_offset', Uint, (0, None))
		yield ('chunks_count', Uint, (0, None))
		yield ('tris_count', Uint, (0, None))
		yield ('vertex_count', Uint, (0, None))
		yield ('zero_1', Uint64, (0, None))
		yield ('poweroftwo', Uint, (0, None))
		yield ('unk_floats', Array, ((2,), Float, 0, None))
		yield ('flag', BioModelFlag, (0, None))

	def get_info_str(self, indent=0):
		return f'BioMeshData [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* chunks_offset = {self.fmt_member(self.chunks_offset, indent+1)}'
		s += f'\n	* chunks_count = {self.fmt_member(self.chunks_count, indent+1)}'
		s += f'\n	* tris_count = {self.fmt_member(self.tris_count, indent+1)}'
		s += f'\n	* vertex_count = {self.fmt_member(self.vertex_count, indent+1)}'
		s += f'\n	* zero_1 = {self.fmt_member(self.zero_1, indent+1)}'
		s += f'\n	* poweroftwo = {self.fmt_member(self.poweroftwo, indent+1)}'
		s += f'\n	* unk_floats = {self.fmt_member(self.unk_floats, indent+1)}'
		s += f'\n	* flag = {self.fmt_member(self.flag, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s

	# @property
	def get_stream_index(self):
		# logging.debug(f"Using stream {self.stream_info.offset}")
		return self.stream_info.offset

	@property
	def tris_address(self):
		# this assumes that chunks are sorted by tris_offset, not guaranteed to be always true
		return self.tri_chunks[0].tris_offset

	def read_tris(self):
		pass

	def read_tris_bio(self):
		# read all tri indices for this mesh
		self.buffer_info.tris.seek(self.tris_address)
		index_count = self.tris_count * 3  # // self.shell_count
		# logging.info(f"Reading {index_count} indices at {self.buffer_info.tris.tell()}")
		_tri_indices = np.empty(dtype=np.uint8, shape=index_count)
		self.buffer_info.tris.readinto(_tri_indices)
		self.tri_indices = _tri_indices.astype(np.uint32)

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
		logging.debug(self)
		self.read_chunk_infos()
		# check first vert_chunk
		vert_chunk = self.vert_chunks[0]
		self.mesh_format = vert_chunk.weights_flag.mesh_format
		self.update_dtype()
		self.init_arrays()

		first_tris_offs = self.tri_chunks[0].tris_offset
		offs = 0

		self.read_tris_bio()
		self.weights_info = {}
		self.face_maps = {}
		self.bones_sets = []
		mesh_formats = set()
		for i, (tri_chunk, vert_chunk) in enumerate(zip(self.tri_chunks, self.vert_chunks)):
			# bones_per_chunk = set()
			logging.debug(f"{i}, {tri_chunk}, {vert_chunk}")
			# these sometimes correspond but not always
			# logging.info(f"chunk {i} tris at {tri_chunk.tris_offset}, weights_flag {vert_chunk.weights_flag}")

			self.buffer_info.verts.seek(vert_chunk.vertex_offset)
			logging.info(f"tri_chunk {i} {tri_chunk.tris_offset} {tri_chunk.tris_count} tris")
			logging.info(f"packed_verts {i} start {self.buffer_info.verts.tell()}, count {vert_chunk.vertex_count}")

			v_slice = np.s_[offs: offs + vert_chunk.vertex_count]
			self.init_vert_chunk_arrays(v_slice, vert_chunk)
			tris_start = tri_chunk.tris_offset - first_tris_offs
			tri_chunk.tri_indices = self.tri_indices[tris_start: tris_start+tri_chunk.tris_count * 3]
			mesh_formats.add(vert_chunk.weights_flag.mesh_format)
			if vert_chunk.weights_flag.mesh_format == MeshFormat.Separate:
				self.buffer_info.verts.readinto(vert_chunk.packed_verts)
				# decode and store position
				unpack_int64_vector(vert_chunk.packed_verts, vert_chunk.vertices, vert_chunk.negate_bitangents)
				scale_unpack_vectorized(vert_chunk.vertices, vert_chunk.pack_base)

				self.read_weights(vert_chunk, offs)
				# read uv, normals etc
				# logging.info(f"meta {i} start {self.buffer_info.verts.tell()}")
				self.buffer_info.verts.readinto(vert_chunk.meta)

			elif vert_chunk.weights_flag.mesh_format in (MeshFormat.Interleaved32, MeshFormat.Interleaved48):
				# interleaved vertex array, meta includes all extra data
				self.buffer_info.verts.readinto(vert_chunk.meta)
				# store position
				vert_chunk.vertices[:] = vert_chunk.meta["pos"]
				self.read_weights(vert_chunk, offs)
			else:
				raise AttributeError(f"Unsupported weights_flag.mesh_format {vert_chunk.weights_flag.mesh_format}")
			# store chunk's meta data in mesh's array
			vert_chunk.uvs[:] = vert_chunk.meta["uvs"]
			vert_chunk.colors[:] = vert_chunk.meta["colors"]
			vert_chunk.normals[:, :2] = vert_chunk.meta["normal_oct"]
			vert_chunk.tangents[:, :2] = vert_chunk.meta["tangent_oct"]

			if vert_chunk.weights_flag.mesh_format in (MeshFormat.Interleaved32,):
				vert_chunk.shapekeys[:] = vert_chunk.meta["shapekey"]
				vert_chunk.floats[:] = vert_chunk.meta["floats"]
			# create absolute vertex indices for the total mesh
			tri_chunk.tri_indices += offs
			offs += vert_chunk.vertex_count

			# ##### temporary debugging stuff
			# self.bones_sets.append((vert_chunk.vertex_count, bones_per_chunk))
			# prep face maps
			fmt_str = str(vert_chunk.weights_flag.mesh_format).split(".")[1]
			_weights = f"_weights" if vert_chunk.weights_flag.has_weights else ""
			id_str = f"{fmt_str}_{i:03}{_weights}"
			self.face_maps[id_str] = list(range(tris_start // 3, tris_start // 3 + tri_chunk.tris_count))
		assert len(mesh_formats) == 1
		# print(self.face_maps)
		# logging.info(self.bones_sets)
		max_verts = max(vert_chunk.vertex_count for vert_chunk in self.vert_chunks)
		logging.info(f"max_verts {max_verts}")

		for vertex_index, use_blended in enumerate(self.negate_bitangents):
			self.add_to_weights("negate_bitangents", vertex_index, use_blended)
		# slower
		# decode_oct(vert_chunk.tangents, vert_chunk.meta["tangent_oct"])
		# decode_oct(vert_chunk.normals, vert_chunk.meta["normal_oct"])
		oct_to_vec3(self.normals)
		oct_to_vec3(self.tangents)
		unpack_swizzle_vectorized(self.vertices)
		unpack_swizzle_vectorized(self.shapekeys)
		unpack_swizzle_vectorized(self.normals)
		unpack_swizzle_vectorized(self.tangents)
		unpack_ubyte_color(self.colors)
		# currently, known uses of Interleaved48 use impostor uv atlas
		if vert_chunk.weights_flag.mesh_format == MeshFormat.Interleaved48:
			unpack_ushort_vector_impostor(self.uvs)
		else:
			unpack_ushort_vector(self.uvs)
		self.fur_length = 0.0
		# just a sanity check
		assert self.vertex_count == sum(o.vertex_count for o in self.vert_chunks)

	def init_vert_chunk_arrays(self, v_slice, vert_chunk):
		vert_chunk.packed_verts = None
		vert_chunk.weights = None
		vert_chunk.meta = None
		# views into main array
		vert_chunk.vertices = self.vertices[v_slice]
		vert_chunk.shapekeys = self.shapekeys[v_slice]
		vert_chunk.negate_bitangents = self.negate_bitangents[v_slice]
		vert_chunk.colors = self.colors[v_slice]
		vert_chunk.uvs = self.uvs[v_slice]
		vert_chunk.normals = self.normals[v_slice]
		vert_chunk.tangents = self.tangents[v_slice]
		vert_chunk.floats = self.floats[v_slice]
		if vert_chunk.weights_flag.mesh_format == MeshFormat.Separate:
			# todo - once stable, change back to empty
			vert_chunk.packed_verts = np.zeros(dtype=np.int64, shape=vert_chunk.vertex_count)
			vert_chunk.weights = np.zeros(dtype=self.dt_weights, shape=vert_chunk.vertex_count)
			vert_chunk.meta = np.zeros(dtype=self.dt, shape=vert_chunk.vertex_count)
		elif vert_chunk.weights_flag.mesh_format in (MeshFormat.Interleaved32, MeshFormat.Interleaved48):
			# interleaved vertex array, meta includes all extra data
			vert_chunk.meta = np.zeros(dtype=self.dt, shape=vert_chunk.vertex_count)

	def read_weights(self, vert_chunk, offs):
		# check if weights chunk is present
		if vert_chunk.weights_flag.has_weights:
			# read for each vertex
			self.buffer_info.verts.readinto(vert_chunk.weights)
			for vertex_index, (bone_indices, bone_weights) in enumerate(
					zip(vert_chunk.weights["bone ids"], vert_chunk.weights["bone weights"] / 255)):
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
		dt_interleaved32 = [
			("pos", np.float16, (3,)),
			("shapekey", np.float16, (3,)),  # used for lod fading
			("floats", np.float16, 4),
			*_normal_tangent_oct,
			("uvs", np.ushort, (1, 2)),
			("colors", np.ubyte, 4)
		]
		# 48 bytes per vertex, with all data interleaved, totally different from older 48 bytes vert
		dt_interleaved48 = [
			("pos", np.float16, (3,)),
			("one", np.ubyte),  # not sure
			("zero", np.ubyte),  # may be bone index
			*_normal_tangent_oct,
			("colors", np.ubyte, 4),  # zero, may be colors
			("uvs", np.ushort, (8, 2)),
		]
		if self.mesh_format == MeshFormat.Separate:
			self.dt = np.dtype(dt_separate)
		elif self.mesh_format == MeshFormat.Interleaved32:
			self.dt = np.dtype(dt_interleaved32)
		elif self.mesh_format == MeshFormat.Interleaved48:
			self.dt = np.dtype(dt_interleaved48)
		else:
			raise AttributeError(f"Unsupported mesh_format {self.mesh_format}")
		self.dt_weights = np.dtype(dt_weights)

	def read_chunk_infos(self):
		self.buffer_info.tri_chunks.seek(self.tri_chunks_address)
		self.tri_chunks = Array.from_stream(self.buffer_info.tri_chunks, (self.chunks_count,), TriChunk, self.context)
		# logging.debug(f"{self.chunks_count} tri_chunks at {self.tri_chunks_address}")
		self.buffer_info.vert_chunks.seek(self.vert_chunks_address)
		self.vert_chunks = Array.from_stream(self.buffer_info.vert_chunks, (self.chunks_count,), VertChunk, self.context)
		# logging.debug(f"{self.chunks_count} vert_chunks at {self.vert_chunks_address}")

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

	@tris.setter
	def tris(self, list_of_b_tris):
		# create chunks for each segment in tris
		self.tris_count = sum(len(b_tris) for b_tris in list_of_b_tris)
		self.vert_chunks = Array((len(list_of_b_tris),), VertChunk, self.context)
		self.tri_chunks = Array((len(list_of_b_tris),), TriChunk, self.context)
		for vert_chunk, tri_chunk, b_tris in zip(self.vert_chunks, self.tri_chunks, list_of_b_tris):
			# logging.info(b_tris)
			# cast to uint16
			raw_tris = np.array(b_tris, dtype=np.uint8)
			# reverse tris
			raw_tris = np.flip(raw_tris, axis=-1)
			# flatten array
			tri_chunk.tri_indices = np.reshape(raw_tris, len(raw_tris) * 3)
			tri_chunk.tris_count = len(b_tris)
			# get the vertex count from the tri indices
			vert_chunk.vertex_count = np.max(tri_chunk.tri_indices) + 1
			vert_chunk.weights_flag.mesh_format = self.mesh_format
			vert_chunk.pack_base = self.pack_base
			vert_chunk.flags = (2, 16, 0, 58)
			# logging.info(f"vert_chunk.vertex_count {vert_chunk.vertex_count}")

	def pack_verts(self):
		"""Repack flat lists into verts_data"""
		# prepare data in whole mesh array for assignment
		pack_swizzle_vectorized(self.vertices)
		pack_swizzle_vectorized(self.shapekeys)
		pack_swizzle_vectorized(self.normals)
		pack_swizzle_vectorized(self.tangents)
		vec3_to_oct(self.normals)
		vec3_to_oct(self.tangents)
		pack_ubyte_color(self.colors)
		offs = 0
		for vert_chunk, tri_chunk in zip(self.vert_chunks, self.tri_chunks):
			# (re)generate views into mesh vertex arrays for vert_chunk according to tri_chunk
			v_slice = np.s_[offs: offs + vert_chunk.vertex_count]
			self.init_vert_chunk_arrays(v_slice, vert_chunk)
			offs += vert_chunk.vertex_count
			# we have the views, so set bounds for the chunk (after swizzling)
			tri_chunk.bounds_min.set(np.min(vert_chunk.vertices, axis=0))
			tri_chunk.bounds_max.set(np.max(vert_chunk.vertices, axis=0))
			# pack the verts
			if vert_chunk.weights_flag.mesh_format == MeshFormat.Separate:
				scale_pack_vectorized(vert_chunk.vertices, vert_chunk.pack_base)
				pack_int64_vector(vert_chunk.packed_verts, vert_chunk.vertices.astype(np.int64), vert_chunk.negate_bitangents)
				# just force weights for now?
				vert_chunk.weights_flag.has_weights = True
				for vert, weight in zip(vert_chunk.weights, self.weights[v_slice]):
					vert["bone ids"], vert["bone weights"] = self.unpack_weights_list(weight)
				# vert_chunk.weights_flag.has_weights = False
				# # vert_chunk.weights = self.weights[v_slice]
				# vert_chunk.weights_flag.bone_index = self.weights[v_slice][0][0][0]
			elif vert_chunk.weights_flag.mesh_format in (MeshFormat.Interleaved32, MeshFormat.Interleaved48):
				vert_chunk.meta["pos"] = vert_chunk.vertices
				vert_chunk.weights_flag.has_weights = False
			else:
				raise AttributeError(f"Unsupported mesh_format {self.mesh_format}")
			# store chunk's meta data
			if vert_chunk.weights_flag.mesh_format == MeshFormat.Interleaved32:
				vert_chunk.meta["shapekey"] = vert_chunk.shapekeys
				vert_chunk.meta["floats"] = vert_chunk.floats
			# currently, known uses of Interleaved48 use impostor uv atlas
			if vert_chunk.weights_flag.mesh_format == MeshFormat.Interleaved48:
				pack_ushort_vector_impostor(vert_chunk.uvs)
			else:
				pack_ushort_vector(vert_chunk.uvs)
			# assign the right views from the main arrays back to the chunks
			# print("bef", vert_chunk.meta)
			vert_chunk.meta["uvs"] = vert_chunk.uvs
			vert_chunk.meta["colors"] = vert_chunk.colors
			vert_chunk.meta["normal_oct"] = vert_chunk.normals[:, :2]
			vert_chunk.meta["tangent_oct"] = vert_chunk.tangents[:, :2]
			# print("after", vert_chunk.meta)

	def write_data(self):
		# save tris and verts per chunk, and update the offsets each time
		# write to the buffer_info that has been assigned to mesh
		self.vertex_count = len(self.vertices)
		# this may not be needed, but for now is used in update_buffer_2_bytes
		self.tri_index_count = len(self.tri_indices)
		for vert_chunk, tri_chunk in zip(self.vert_chunks, self.tri_chunks):
			# write vertices
			vert_chunk.vertex_offset = self.buffer_info.verts.tell()
			vert_chunk.vertex_count = len(vert_chunk.meta)
			# write the arrays if they exist, in this order
			if vert_chunk.weights_flag.mesh_format == MeshFormat.Separate:
				self.buffer_info.verts.write(vert_chunk.packed_verts.tobytes())
				if vert_chunk.weights_flag.has_weights:
					self.buffer_info.verts.write(vert_chunk.weights.tobytes())
			self.buffer_info.verts.write(vert_chunk.meta.tobytes())

			tri_chunk.tris_offset = self.buffer_info.tris.tell()
			# get tri indices of this chunk
			_tri_chunk_tri_indices = np.copy(tri_chunk.tri_indices)
			_tri_chunk_tri_indices -= np.min(_tri_chunk_tri_indices)
			tri_bytes = _tri_chunk_tri_indices.astype(np.uint8).tobytes()
			# extend tri array according to shell count
			# logging.debug(f"Writing {self.shell_count} shells of {len(self.tri_indices)} triangles")
			# for shell in range(self.shell_count):
			self.buffer_info.tris.write(tri_bytes)

		# write the chunks
		self.chunks_offset = self.buffer_info.tri_chunks.tell() // 64
		self.chunks_count = len(self.tri_chunks)
		Array.to_stream(self.buffer_info.tri_chunks, self.tri_chunks, (self.chunks_count,), TriChunk, self.context, 0, None)
		Array.to_stream(self.buffer_info.vert_chunks, self.vert_chunks, (self.chunks_count,), VertChunk, self.context, 0, None)

