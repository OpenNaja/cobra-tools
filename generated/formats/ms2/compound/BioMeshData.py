
import logging
import numpy as np
import struct

from generated.array import Array
from generated.formats.ms2.compound.OffsetChunk import OffsetChunk
from generated.formats.ms2.compound.PosChunk import PosChunk
from generated.formats.ms2.compound.packing_utils import *
from generated.formats.ms2.enum.MeshFormat import MeshFormat
from plugin.utils.tristrip import triangulate


from source.formats.base.basic import fmt_member
import numpy
from generated.formats.ms2.bitfield.BioModelFlag import BioModelFlag
from generated.formats.ms2.compound.MeshData import MeshData


class BioMeshData(MeshData):

	"""
	JWE2 - 48 bytes incl. inheritance
	"""

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		super().__init__(context, arg, template, set_default)
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# unk
		self.chunks_offset = 0

		# unk
		self.chunks_count = 0
		self.tris_count = 0

		# num verts in mesh
		self.vertex_count = 0

		# unk, may be used in other models
		self.zero_1 = 0

		# power of 2 increasing with lod index
		self.poweroftwo = 0

		# some floats, purpose unknown
		self.unk_floats = numpy.zeros((2,), dtype=numpy.dtype('float32'))

		# seen 1 or 13
		self.flag = BioModelFlag(self.context, 0, None)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
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
	def from_stream(cls, stream, context, arg=0, template=None):
		instance = cls(context, arg, template, set_default=False)
		instance.io_start = stream.tell()
		cls.read_fields(stream, instance)
		instance.io_size = stream.tell() - instance.io_start
		return instance

	@classmethod
	def to_stream(cls, stream, instance):
		instance.io_start = stream.tell()
		cls.write_fields(stream, instance)
		instance.io_size = stream.tell() - instance.io_start
		return instance

	def get_info_str(self, indent=0):
		return f'BioMeshData [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* chunks_offset = {fmt_member(self.chunks_offset, indent+1)}'
		s += f'\n	* chunks_count = {fmt_member(self.chunks_count, indent+1)}'
		s += f'\n	* tris_count = {fmt_member(self.tris_count, indent+1)}'
		s += f'\n	* vertex_count = {fmt_member(self.vertex_count, indent+1)}'
		s += f'\n	* zero_1 = {fmt_member(self.zero_1, indent+1)}'
		s += f'\n	* poweroftwo = {fmt_member(self.poweroftwo, indent+1)}'
		s += f'\n	* unk_floats = {fmt_member(self.unk_floats, indent+1)}'
		s += f'\n	* flag = {fmt_member(self.flag, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s

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

	def get_tri_counts(self):
		for i, pos in enumerate(self.pos_chunks[:-1]):
			next_pos = self.pos_chunks[i+1]
			pos.tri_indices_count = next_pos.tris_offset - pos.tris_offset
		last_pos = self.pos_chunks[-1]
		last_pos.tri_indices_count = (self.tris_count * 3) - last_pos.tris_offset + self.pos_chunks[0].tris_offset
		for i, pos in enumerate(self.pos_chunks):
			logging.info(f"pos {i} {last_pos.tri_indices_count} tris")

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
		self.get_tri_counts()
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
		# 48 bytes per vertex, with all data interleaved, totally different from older 48 bytes vert
		dt_interleaved48 = [
			("pos", np.float16, (3,)),
			("one", np.ubyte),  # not sure
			("zero", np.ubyte),  # may be bone index
			("normal_oct", np.ubyte, (2,)),
			("tangent_oct", np.ubyte, (2,)),
			("colors", np.ubyte, (1, 4)),  # zero, may be colors
			("uvs", np.ushort, (8, 2)),
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
		# colors_shape = self.dt["colors"].shape
		colors_shape = (1, 4)
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
		self.face_maps = {}
		self.bones_sets = []
		for i, (pos, off) in enumerate(zip(self.pos_chunks, self.offset_chunks)):
			abs_tris = self.tris_start_address + pos.tris_offset
			# bones_per_chunk = set()
			logging.debug(f"{i}, {pos}, {off}")
			# these sometimes correspond but not always
			logging.info(f"{i}, {pos.u_0}, {off.weights_flag.mesh_format}")
			# print(i, pos.u_1)
			logging.info(f"chunk {i} tris at {abs_tris}, weights_flag {off.weights_flag}")

			self.stream_info.stream.seek(off.vertex_offset)
			logging.info(f"verts {i} start {self.stream_info.stream.tell()}, count {off.vertex_count}")

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
					# 			bones_per_chunk.add(bone_index)
					# logging.info(f"Length set {len(bones_per_chunk)}")
				else:
					# use the chunk's bone index for each vertex in chunk
					for vertex_index in range(off.vertex_count):
						self.add_to_weights(off.weights_flag.bone_index, vertex_index + offs, 1.0)
					# bones_per_chunk.add(off.weights_flag.bone_index)

				for vertex_index in range(off.vertex_count):
					self.add_to_weights("u_0", vertex_index + offs, pos.u_0 / 255)
					self.add_to_weights("u_1", vertex_index + offs, pos.u_1 / 255)
				# uv, normals etc
				logging.info(f"meta {i} start {self.stream_info.stream.tell()}")
				off.raw_meta = np.empty(dtype=self.dt, shape=off.vertex_count)
				self.stream_info.stream.readinto(off.raw_meta)

				# store chunk's data
				unpack_int64_vector(off.raw_verts, self.vertices[offs:offs + off.vertex_count], self.use_blended_weights[offs:offs + off.vertex_count])
				scale_unpack_vectorized(self.vertices[offs:offs + off.vertex_count], off.pack_offset)
				self.uvs[offs:offs + off.vertex_count] = off.raw_meta["uvs"]
				self.colors[offs:offs + off.vertex_count] = off.raw_meta["colors"]
				self.normals[offs:offs + off.vertex_count, 0:2] = off.raw_meta["normal_oct"]
				self.tangents[offs:offs + off.vertex_count, 0:2] = off.raw_meta["tangent_oct"]

			elif off.weights_flag.mesh_format in (MeshFormat.Interleaved32, MeshFormat.Interleaved48):
				# read the interleaved vertex array, including all extra data
				off.raw_verts = np.empty(dtype=self.dt, shape=off.vertex_count)
				self.stream_info.stream.readinto(off.raw_verts)

				# store chunk's data
				self.vertices[offs:offs + off.vertex_count] = off.raw_verts["pos"]
				self.uvs[offs:offs + off.vertex_count] = off.raw_verts["uvs"]
				self.colors[offs:offs + off.vertex_count] = off.raw_verts["colors"]
				self.normals[offs:offs + off.vertex_count, 0:2] = off.raw_verts["normal_oct"]
				self.tangents[offs:offs + off.vertex_count, 0:2] = off.raw_verts["tangent_oct"]
			else:
				raise AttributeError(f"Unsupported weights_flag.mesh_format {off.weights_flag.mesh_format}")

			# self.bones_sets.append((off.vertex_count, bones_per_chunk))
			# same for all chunked meshes, regardless if flat or interleaved arrays
			flags.add(off.weights_flag)
			us.add(pos.u_1)
			tris_start = pos.tris_offset - first_tris_offs
			self.tri_indices[tris_start:] += v_off

			# prep face maps
			fmt_str = str(off.weights_flag.mesh_format).split(".")[1]
			_weights = f"_weights" if off.weights_flag.has_weights else ""
			id_str = f"{fmt_str}_{i:03}{_weights}"
			self.face_maps[id_str] = list(range(tris_start // 3, (tris_start+pos.tri_indices_count) // 3))

			v_off = off.vertex_count
			offs += off.vertex_count
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

	def read_chunk_infos(self):
		# logging.debug(f"Reading {self.vertex_count} verts at {self.stream_info.stream.tell()}")
		self.stream_info.stream.seek(self.pos_chunks_address)
		self.pos_chunks = Array.from_stream(self.stream_info.stream, (self.chunks_count,), PosChunk, self.context, 0,
											None)
		logging.debug(self)
		logging.debug(f"{self.chunks_count} pos_chunks at {self.pos_chunks_address}")
		self.stream_info.stream.seek(self.offset_chunks_address)
		self.offset_chunks = Array.from_stream(self.stream_info.stream, (self.chunks_count,), OffsetChunk, self.context,
											   0, None)
		logging.debug(f"{self.chunks_count} offset_chunks at {self.offset_chunks_address}")

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

